from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.conf import settings

from teacher_api.permissions import IsTeacher
from activities.models import LessonQuestion, LessonQuestionReply, Notification


def avatar_for(user, request=None):
    profile = getattr(user, "profile", None)
    avatar_path = getattr(profile, "avatar_url", None) if profile else None
    if not avatar_path:
        return None
    if avatar_path.startswith(("http://", "https://", "data:")):
        return avatar_path
    if avatar_path.startswith("/"):
        return request.build_absolute_uri(avatar_path) if request else avatar_path
    media_url = getattr(settings, "MEDIA_URL", "/media/").rstrip("/")
    base = request.build_absolute_uri(media_url + "/") if request else media_url + "/"
    return f"{base}{avatar_path}"


def serialize_reply(rep: LessonQuestionReply, user=None):
    return {
        "id": str(rep.id),
        "user": rep.user.username,
        "avatar": avatar_for(rep.user),
        "user_id": rep.user.id,
        "is_teacher": rep.is_teacher,
        "content": rep.content,
        "created_at": rep.created_at.isoformat(),
        "reactions_count": rep.reactions.count() if hasattr(rep, "reactions") else 0,
        "is_owner": bool(user and user.id == rep.user.id),
    }


def serialize_question(q: LessonQuestion, user=None):
    return {
        "id": str(q.id),
        "lesson_id": str(q.lesson_id),
        "student_id": q.student_id,
        "student": q.student.username,
        "avatar": avatar_for(q.student),
        "content": q.content,
        "created_at": q.created_at.isoformat(),
        "replies": [serialize_reply(r, user=user) for r in q.replies.all()],
    }


class TeacherLessonQuestionView(APIView):
    """
    GET: list questions for a lesson (or all)
    POST /reply/ on an existing question
    PATCH/DELETE reply by teacher (own reply)
    """
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        lesson_id = request.query_params.get("lesson_id")
        qs = LessonQuestion.objects.all().select_related("student", "lesson").prefetch_related("replies__user")
        if lesson_id:
            qs = qs.filter(lesson_id=lesson_id)
        data = [serialize_question(q, user=request.user) for q in qs.order_by("-created_at")]
        return Response({"items": data}, status=status.HTTP_200_OK)

    def post(self, request, pk):
        question = get_object_or_404(LessonQuestion, id=pk)
        content = (request.data.get("content") or "").strip()
        if len(content) < 2:
            return Response({"detail": "Nội dung quá ngắn"}, status=status.HTTP_400_BAD_REQUEST)

        rep = LessonQuestionReply.objects.create(
            question=question,
            user=request.user,
            content=content,
            is_teacher=True,
        )

        # Notify student
        Notification.objects.create(
            user=question.student,
            title=f"Giáo viên trả lời: {question.lesson.title}",
            message=content,
            type="info",
            category="lesson_question_reply",
            metadata={
                "lesson_question_id": str(question.id),
                "lesson_id": str(question.lesson_id),
                "course_id": str(question.lesson.module.course_id) if question.lesson.module else None,
                "teacher_id": str(request.user.id),
                "teacher": request.user.username,
                "reply_id": str(rep.id),
            },
        )

        return Response({"item": serialize_question(question, user=request.user)}, status=status.HTTP_201_CREATED)

    def patch(self, request, pk):
        rep = get_object_or_404(LessonQuestionReply, id=pk, user=request.user)
        content = (request.data.get("content") or "").strip()
        if len(content) < 2:
            return Response({"detail": "Nội dung quá ngắn"}, status=status.HTTP_400_BAD_REQUEST)
        rep.content = content
        rep.save(update_fields=["content"])
        return Response({"item": serialize_question(rep.question, user=request.user)}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        rep = get_object_or_404(LessonQuestionReply, id=pk, user=request.user)
        Notification.objects.filter(metadata__reply_id=str(rep.id)).delete()
        q = rep.question
        rep.delete()
        return Response({"item": serialize_question(q, user=request.user)}, status=status.HTTP_200_OK)
