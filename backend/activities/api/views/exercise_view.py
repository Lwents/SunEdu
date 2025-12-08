from typing import Any, Dict
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import JSONParser

# Import your serializers and services
from activities.serializers import (
    ExerciseModelSerializer,
    QuestionModelSerializer,
    ChoiceModelSerializer,
    StartAttemptSerializer,
    SubmitAnswerSerializer,
    FinalizeAttemptSerializer,
    ExerciseAttemptModelSerializer,
    ExerciseAnswerModelSerializer,
    exercise_domain_to_response,
    attempt_domain_to_response,
)
from activities.services import (
    get_exercise,
    list_exercises,
    save_exercise,
    delete_exercise,
    add_question,
    delete_question,
    add_choice,
    delete_choice,
    start_attempt,
    submit_answer,
    finalize_attempt,
    regrade_attempt,
    get_attempt_summary,
    exercise_stats,
    export_results_csv,
)
from activities.services import ServiceError, NotFoundError, ValidationError, PermissionDenied
from activities.api.permissions import IsAdminOrReadOnly
import os
import time
import requests

# Models used for permission checks or lookups (optional)
from django.apps import apps
ExerciseModel = apps.get_model("activities", "Exercise")
ExerciseAttemptModel = apps.get_model("activities", "ExerciseAttempt")
ExerciseAnswerModel = apps.get_model("activities", "ExerciseAnswer")


class ExerciseListCreateView(APIView):
    """
    GET /api/activities/exercises/  -> list exercises (optional filtering by lesson)
    POST /api/activities/exercises/ -> create exercise (admin/instructor)
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request):
        lesson_id = request.query_params.get("lesson_id")
        include_stats = request.query_params.get("include_stats", "false").lower() == "true"
        filters = {}
        if lesson_id:
            filters["lesson_id"] = lesson_id
        domains = list_exercises(filters=filters)
        data = [ExerciseModelSerializer.from_domain(d) for d in domains]
        
        # Add stats if requested
        if include_stats:
            from activities.services.analytic_service import exercise_stats
            for item in data:
                try:
                    stats = exercise_stats(str(item["id"]))
                    item["submissions"] = stats.get("submissions", 0)
                    item["avgScore"] = stats.get("avgScore", 0)
                    item["avg_score"] = stats.get("avgScore", 0)  # Alias
                    item["passRate"] = stats.get("passRate", 0)
                    item["pass_rate"] = stats.get("passRate", 0)  # Alias
                except Exception:
                    item["submissions"] = 0
                    item["avgScore"] = 0
                    item["avg_score"] = 0
                    item["passRate"] = 0
                    item["pass_rate"] = 0

        # Attach current user's latest attempt info so FE biết đã làm hay chưa
        if request.user and request.user.is_authenticated and data:
            ex_ids = [item["id"] for item in data if item.get("id")]
            attempt_map = {}
            qs = ExerciseAttemptModel.objects.filter(
                exercise_id__in=ex_ids,
                student=request.user
            ).order_by("exercise_id", "-started_at")
            for att in qs:
                key = str(att.exercise_id)
                # keep first (latest ordered by started_at desc per exercise)
                if key not in attempt_map:
                    attempt_map[key] = att
            for item in data:
                att = attempt_map.get(str(item.get("id")))
                if att:
                    item["my_attempt"] = {
                        "id": str(att.id),
                        "finished_at": att.finished_at.isoformat() if att.finished_at else None,
                        "score": float(att.score) if att.score is not None else None,
                    }
                    item["done"] = bool(att.finished_at)
                else:
                    item["my_attempt"] = None
                    item["done"] = False
        
        return Response(data)

    def post(self, request: Request):
        serializer = ExerciseModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # map to domain
        domain = serializer.to_domain()
        try:
            created = save_exercise(domain)
        except (ValidationError, ServiceError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ExerciseModelSerializer.from_domain(created), status=status.HTTP_201_CREATED)


class ExerciseDetailView(APIView):
    """
    GET /api/activities/exercises/{id}/
    PATCH /api/activities/exercises/{id}/
    DELETE /api/activities/exercises/{id}/
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request, exercise_id: str):
        try:
            domain = get_exercise(exercise_id)
        except NotFoundError:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(ExerciseModelSerializer.from_domain(domain))

    def patch(self, request: Request, exercise_id: str):
        # partial update; load model, then merge changes using serializer
        try:
            model = ExerciseModel.objects.prefetch_related("questions__choices").get(id=exercise_id)
        except ExerciseModel.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExerciseModelSerializer(instance=model, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        domain = serializer.to_domain()
        try:
            updated = save_exercise(domain)
        except (ValidationError, ServiceError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ExerciseModelSerializer.from_domain(updated))

    def delete(self, request: Request, exercise_id: str):
        try:
            delete_exercise(exercise_id)
        except NotFoundError:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenerateQuestionsAIView(APIView):
    """
    POST /api/activities/ai/generate-questions/
    Body: {title, level, description, count, hint, model}
    Calls Gemini from backend using GEMINI_API_KEY env.
    """
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    def post(self, request: Request):
        # Ưu tiên ENV, fallback về settings; không nhúng khóa mặc định
        api_key = os.getenv("GEMINI_API_KEY") or getattr(settings, "GEMINI_API_KEY", "")
        if not api_key:
            return Response({"detail": "Missing GEMINI_API_KEY on server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        title = request.data.get("title", "")
        level = request.data.get("level", "")
        description = request.data.get("description", "")
        count = int(request.data.get("count") or 5)
        hint = request.data.get("hint", "")
        model = request.data.get("model") or os.getenv("GEMINI_MODEL") or "gemini-2.5-flash"

        count = max(1, min(count, 10))

        prompt = (
            f"Bạn là trợ lý tạo đề thi tiểu học. Hãy tạo {count} câu hỏi trắc nghiệm, phù hợp trình độ \"{level}\".\n"
            f"Tiêu đề bài kiểm tra: {title}.\n"
            f"Mô tả: {description or 'Không có'}.\n"
            f"Yêu cầu thêm từ giáo viên: {hint or 'Không có'}.\n\n"
            "QUY TẮC BẮT BUỘC:\n"
            "- CHỈ tạo câu hỏi loại 'single' (trắc nghiệm 1 đáp án đúng) hoặc 'boolean' (đúng/sai).\n"
            "- Mỗi câu hỏi 'single' phải có 3-4 choices và correct_indices chứa index đáp án đúng.\n"
            "- Câu hỏi 'boolean' có correct_answer là true hoặc false.\n\n"
            "Trả về JSON thuần (KHÔNG có markdown code block):\n"
            "{\n"
            '  "questions": [\n'
            '    {"type": "single", "text": "Câu hỏi?", "score": 1, "choices": ["A", "B", "C", "D"], "correct_indices": [0]},\n'
            '    {"type": "boolean", "text": "Đúng hay sai?", "score": 1, "correct_answer": true}\n'
            "  ]\n"
            "}\n"
        )

        # Gọi Gemini API trước (ổn định hơn), fallback sang DeepSeek nếu lỗi
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        try:
            resp = requests.post(
                url,
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"maxOutputTokens": 2048},
                },
                timeout=60,
            )
            
            if resp.status_code == 200:
                data = resp.json()
                text = ""
                try:
                    text = data.get("candidates", [])[0].get("content", {}).get("parts", [])[0].get("text", "")
                except Exception:
                    text = ""
                if text and text.strip():
                    return Response({"model": model, "text": text, "raw": data})
                return Response({"detail": "AI không trả về kết quả"}, status=status.HTTP_502_BAD_GATEWAY)
            
            if resp.status_code == 429:
                # Gemini quá tải -> fallback sang DeepSeek
                deepseek_result = self._call_deepseek_api(prompt)
                if deepseek_result.get("success"):
                    return Response({
                        "model": deepseek_result.get("model", "deepseek"),
                        "text": deepseek_result.get("text", ""),
                        "raw": deepseek_result.get("raw", {}),
                    })
                return Response({"detail": "AI đang quá tải. Vui lòng thử lại sau."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            
            # Gemini lỗi khác -> fallback sang DeepSeek
            deepseek_result = self._call_deepseek_api(prompt)
            if deepseek_result.get("success"):
                return Response({
                    "model": deepseek_result.get("model", "deepseek"),
                    "text": deepseek_result.get("text", ""),
                    "raw": deepseek_result.get("raw", {}),
                })
            return Response({"detail": f"AI trả về lỗi {resp.status_code}", "raw": resp.text}, status=resp.status_code)
            
        except Exception as e:
            # Gemini lỗi kết nối -> fallback sang DeepSeek
            deepseek_result = self._call_deepseek_api(prompt)
            if deepseek_result.get("success"):
                return Response({
                    "model": deepseek_result.get("model", "deepseek"),
                    "text": deepseek_result.get("text", ""),
                    "raw": deepseek_result.get("raw", {}),
                })
            return Response({"detail": f"Lỗi kết nối AI: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)
    
    def _call_deepseek_api(self, prompt):
        """Gọi DeepSeek API (OpenRouter) làm fallback khi Gemini quá tải"""
        # DeepSeek API key qua OpenRouter
        deepseek_api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
        if not deepseek_api_key:
            return {"error": "DeepSeek API chưa được cấu hình"}
        
        deepseek_model = os.getenv("DEEPSEEK_MODEL") or "deepseek/deepseek-chat-v3-0324"
        
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {deepseek_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://sunedu.local",
            "X-Title": "SunEdu AI Question Generator",
        }
        
        try:
            resp = requests.post(
                url,
                headers=headers,
                json={
                    "model": deepseek_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 2048,
                },
                timeout=60,
            )
            
            if resp.status_code == 200:
                data = resp.json()
                try:
                    text = data.get("choices", [])[0].get("message", {}).get("content", "")
                    if text and text.strip():
                        return {"success": True, "text": text.strip(), "model": deepseek_model, "raw": data}
                    return {"error": "DeepSeek trả về nội dung rỗng"}
                except (IndexError, KeyError, TypeError) as e:
                    return {"error": f"Lỗi parse DeepSeek: {str(e)}"}
            
            # Xử lý lỗi
            try:
                error_data = resp.json()
                error_msg = error_data.get("error", {}).get("message", f"Lỗi {resp.status_code}")
            except:
                error_msg = f"Lỗi DeepSeek API {resp.status_code}"
            return {"error": error_msg}
            
        except Exception as e:
            return {"error": f"Lỗi kết nối DeepSeek: {str(e)}"}
