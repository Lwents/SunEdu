from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from student_api.permissions import IsStudent
from django.conf import settings
from content.models import Lesson
from activities.models import Notification, LessonQuestion, LessonQuestionReply, LessonQuestionReport
from django.contrib.auth import get_user_model


def avatar_for(user, request):
    """Get avatar URL for user, with fallback to profile avatar_url and default avatar"""
    if not user:
        return None
    
    # Try to get from profile first
    try:
        profile = getattr(user, "profile", None)
        if profile:
            avatar_path = getattr(profile, "avatar_url", None)
            if avatar_path and avatar_path.strip():
                # Handle different avatar URL formats
                if avatar_path.startswith(("http://", "https://", "data:")):
                    return avatar_path
                if avatar_path.startswith("/"):
                    return request.build_absolute_uri(avatar_path) if request else avatar_path
                # Relative path - build full URL
                media_url = getattr(settings, "MEDIA_URL", "/media/").rstrip("/")
                base = request.build_absolute_uri(media_url + "/") if request else media_url + "/"
                return f"{base}{avatar_path.lstrip('/')}"
    except Exception:
        pass
    
    # Fallback: check if user has avatar attribute directly (for backward compatibility)
    try:
        if hasattr(user, "avatar") and user.avatar:
            avatar_path = str(user.avatar)
            if avatar_path.startswith(("http://", "https://", "data:")):
                return avatar_path
            if request:
                return request.build_absolute_uri(avatar_path)
            return avatar_path
    except Exception:
        pass
    
    # Return None to let frontend handle default avatar based on gender
    # Frontend will use getAvatarSrc() which handles boy/girl avatars based on gender
    return None


def serialize_reply(rep: LessonQuestionReply, user=None, request=None):
    profile = getattr(rep.user, "profile", None)
    gender = getattr(profile, "gender", None) if profile else None
    
    # Safely get reactions_count and reacted
    # If model hasn't been migrated yet, these will default to 0 and False
    reactions_count = 0
    reacted = False
    try:
        reactions_count = rep.reactions.count()
        if user:
            reacted = rep.reactions.filter(user=user).exists()
    except (AttributeError, Exception):
        # Reactions relation doesn't exist (migration not run) - silently use defaults
        pass
    
    return {
        "id": str(rep.id),
        "user": rep.user.username,
        "avatar": avatar_for(rep.user, request),
        "gender": gender,
        "user_id": rep.user.id,
        "is_owner": bool(user and user.id == rep.user.id),
        "is_teacher": rep.is_teacher,
        "content": rep.content,
        "created_at": rep.created_at.isoformat(),
        "reactions_count": reactions_count,
        "reacted": reacted,
    }


def serialize_question(q: LessonQuestion, user=None, request=None):
    try:
        profile = getattr(q.student, "profile", None)
        gender = getattr(profile, "gender", None) if profile else None
        
        # Safely get reactions_count and reacted
        # If model hasn't been migrated yet, these will default to 0 and False
        reactions_count = 0
        reacted = False
        try:
            reactions_count = q.reactions.count()
            if user:
                reacted = q.reactions.filter(user=user).exists()
        except (AttributeError, Exception):
            # Reactions relation doesn't exist (migration not run) - silently use defaults
            pass
        
        # Safely serialize replies
        replies = []
        try:
            replies = [serialize_reply(r, user=user, request=request) for r in q.replies.all()]
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error serializing replies for question {q.id}: {e}")
            replies = []
        
        return {
            "id": str(q.id),
            "lesson_id": str(q.lesson_id),
            "student_id": q.student_id,
            "student": q.student.username,
            "avatar": avatar_for(q.student, request),
            "gender": gender,
            "is_owner": bool(user and user.id == q.student_id),
            "content": q.content,
            "created_at": q.created_at.isoformat(),
            "reactions_count": reactions_count,
            "reacted": reacted,
            "replies": replies,
        }
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error serializing question {q.id if q else 'unknown'}: {e}", exc_info=True)
        # Return minimal data to prevent complete failure
        return {
            "id": str(q.id) if q else "",
            "lesson_id": str(q.lesson_id) if q else "",
            "student_id": q.student_id if q else None,
            "student": q.student.username if q and q.student else "",
            "avatar": None,
            "gender": None,
            "is_owner": False,
            "content": q.content if q else "",
            "created_at": q.created_at.isoformat() if q and hasattr(q, 'created_at') else "",
            "reactions_count": 0,
            "reacted": False,
            "replies": [],
        }


class StudentLessonQuestionView(APIView):
    """
    GET /api/student/lesson-questions/?lesson_id=...
    POST /api/student/lesson-questions/ { lesson_id, content }
    PATCH /api/student/lesson-questions/<id>/ { content }
    DELETE /api/student/lesson-questions/<id>/
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        lesson_id = request.query_params.get("lesson_id")
        if not lesson_id:
            return Response({"detail": "lesson_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        qs = LessonQuestion.objects.filter(lesson_id=lesson_id).select_related(
            "student", 
            "student__profile"
        ).prefetch_related(
            "replies__user",
            "replies__user__profile",
            "replies__reactions",
        )
        # Note: reactions for question will be handled safely in serialize_question
        data = [serialize_question(q, user=request.user, request=request) for q in qs.order_by("-created_at")]
        return Response({"items": data}, status=status.HTTP_200_OK)

    def post(self, request):
        content = (request.data.get("content") or "").strip()
        lesson_id = request.data.get("lesson_id")

        if not lesson_id:
            return Response({"detail": "lesson_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not content:
            return Response({"detail": "Nội dung không được để trống"}, status=status.HTTP_400_BAD_REQUEST)

        lesson = get_object_or_404(Lesson, id=lesson_id)
        course = lesson.module.course if lesson.module else None
        teacher = getattr(course, "owner", None)
        if teacher is None:
            return Response({"detail": "Không tìm thấy giáo viên phụ trách"}, status=status.HTTP_400_BAD_REQUEST)

        student = request.user
        q = LessonQuestion.objects.create(lesson=lesson, student=student, content=content)

        Notification.objects.create(
            user=teacher,
            title=f"Học sinh hỏi về bài {lesson.title}",
            message=content,
            type="info",
            category="lesson_question",
            metadata={
                "lesson_question_id": str(q.id),
                "lesson_id": str(lesson.id),
                "course_id": str(course.id) if course else None,
                "student_id": str(student.id),
                "student": student.username,
                "lesson_title": lesson.title,
                "course_title": course.title if course else "",
            },
        )

        return Response({"item": serialize_question(q, user=request.user, request=request)}, status=status.HTTP_201_CREATED)

    def patch(self, request, pk=None):
        if not pk:
            return Response({"detail": "question id required"}, status=status.HTTP_400_BAD_REQUEST)
        q = get_object_or_404(LessonQuestion, id=pk)
        if q.student_id != request.user.id:
            return Response({"detail": "Không được phép sửa"}, status=status.HTTP_403_FORBIDDEN)
        content = (request.data.get("content") or "").strip()
        if not content:
            return Response({"detail": "Nội dung không được để trống"}, status=status.HTTP_400_BAD_REQUEST)
        q.content = content
        q.save(update_fields=["content"])
        return Response({"item": serialize_question(q, user=request.user, request=request)}, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        if not pk:
            return Response({"detail": "question id required"}, status=status.HTTP_400_BAD_REQUEST)
        q = get_object_or_404(LessonQuestion, id=pk)
        if q.student_id != request.user.id:
            return Response({"detail": "Không được phép xóa"}, status=status.HTTP_403_FORBIDDEN)
        # Xóa notification liên quan đến câu hỏi và các reply con
        reply_ids = list(q.replies.values_list("id", flat=True))
        Notification.objects.filter(metadata__lesson_question_id=str(q.id)).delete()
        if reply_ids:
          Notification.objects.filter(metadata__reply_id__in=[str(rid) for rid in reply_ids]).delete()
        q.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentLessonQuestionReplyView(APIView):
    """
    POST /api/student/lesson-questions/<id>/reply/
    PATCH /api/student/lesson-questions/replies/<reply_id>/
    DELETE /api/student/lesson-questions/replies/<reply_id>/
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, pk):
        question = get_object_or_404(LessonQuestion, id=pk)
        content = (request.data.get("content") or "").strip()
        if not content:
            return Response({"detail": "Nội dung không được để trống"}, status=status.HTTP_400_BAD_REQUEST)

        rep = LessonQuestionReply.objects.create(
            question=question,
            user=request.user,
            content=content,
            is_teacher=False,
        )

        # Notify teacher if available
        course = question.lesson.module.course if question.lesson.module else None
        teacher = getattr(course, "owner", None)
        if teacher:
            Notification.objects.create(
                user=teacher,
                title=f"Học sinh trả lời thảo luận: {question.lesson.title}",
                message=content,
                type="info",
                category="lesson_question_reply",
                metadata={
                    "lesson_question_id": str(question.id),
                    "lesson_id": str(question.lesson_id),
                    "course_id": str(course.id) if course else None,
                    "student_id": str(request.user.id),
                    "student": request.user.username,
                },
            )

        question.refresh_from_db()
        return Response({"item": serialize_question(question, user=request.user, request=request)}, status=status.HTTP_201_CREATED)

    def patch(self, request, reply_id=None):
        if not reply_id:
            return Response({"detail": "reply id required"}, status=status.HTTP_400_BAD_REQUEST)
        rep = get_object_or_404(LessonQuestionReply, id=reply_id)
        if rep.user_id != request.user.id:
            return Response({"detail": "Không được phép sửa"}, status=status.HTTP_403_FORBIDDEN)
        content = (request.data.get("content") or "").strip()
        if not content:
            return Response({"detail": "Nội dung không được để trống"}, status=status.HTTP_400_BAD_REQUEST)
        rep.content = content
        rep.save(update_fields=["content"])
        question = rep.question
        question.refresh_from_db()
        return Response({"item": serialize_question(question, user=request.user, request=request)}, status=status.HTTP_200_OK)

    def delete(self, request, reply_id=None):
        if not reply_id:
            return Response({"detail": "reply id required"}, status=status.HTTP_400_BAD_REQUEST)
        rep = get_object_or_404(LessonQuestionReply, id=reply_id)
        if rep.user_id != request.user.id:
            return Response({"detail": "Không được phép xóa"}, status=status.HTTP_403_FORBIDDEN)
        question = rep.question
        Notification.objects.filter(metadata__reply_id=str(rep.id)).delete()
        rep.delete()
        return Response({"item": serialize_question(question, user=request.user, request=request)}, status=status.HTTP_200_OK)


class StudentLessonQuestionReactionView(APIView):
    """
    POST /api/student/lesson-question-replies/<reply_id>/react/
    Toggle like (emoji default 'like')
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, reply_id):
        emoji = (request.data.get("emoji") or "like")[:16]
        reply = get_object_or_404(LessonQuestionReply, id=reply_id)
        reaction, created = reply.reactions.get_or_create(user=request.user, defaults={"emoji": emoji})
        if not created:
            # toggle off
            reaction.delete()
            reacted = False
        else:
            reacted = True
        return Response(
            {
                "reacted": reacted,
                "reactions_count": reply.reactions.count(),
            },
            status=status.HTTP_200_OK,
        )


class StudentLessonQuestionQuestionReactionView(APIView):
    """
    POST /api/student/lesson-questions/<question_id>/react/
    Toggle like (emoji default 'like') for a question
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, question_id=None, pk=None):
        # Accept both path converters: question_id or pk (DRF may pass pk)
        question_id = question_id or pk
        emoji = (request.data.get("emoji") or "like")[:16]
        question = get_object_or_404(LessonQuestion, id=question_id)
        from activities.models import LessonQuestionReaction
        
        try:
            reaction, created = LessonQuestionReaction.objects.get_or_create(
                question=question,
                user=request.user,
                defaults={"emoji": emoji}
            )
            if not created:
                # toggle off
                reaction.delete()
                reacted = False
            else:
                reacted = True
            
            # Safely get reactions_count
            try:
                reactions_manager = getattr(question, 'reactions', None)
                if reactions_manager is not None:
                    reactions_count = reactions_manager.count()
                else:
                    reactions_count = 0
            except Exception:
                reactions_count = 0
        except Exception as e:
            # If model doesn't support question reactions yet (migration not run)
            return Response(
                {"detail": "Reaction feature not available. Please run migrations."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        return Response(
            {
                "reacted": reacted,
                "reactions_count": reactions_count,
            },
            status=status.HTTP_200_OK,
        )


class StudentLessonQuestionReportView(APIView):
    """
    POST /api/student/lesson-question-report/ {question_id|reply_id, reason, detail}
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        question_id = request.data.get("question_id")
        reply_id = request.data.get("reply_id")
        reason = (request.data.get("reason") or "Vi phạm nội dung")[:255]
        detail = (request.data.get("detail") or "").strip()
        if not question_id and not reply_id:
            return Response({"detail": "question_id hoặc reply_id là bắt buộc"}, status=status.HTTP_400_BAD_REQUEST)

        question = None
        reply = None
        if question_id:
            question = get_object_or_404(LessonQuestion, id=question_id)
        if reply_id:
            reply = get_object_or_404(LessonQuestionReply, id=reply_id)

        report = LessonQuestionReport.objects.create(
            reporter=request.user,
            question=question,
            reply=reply,
            reason=reason,
            detail=detail,
        )

        # Gửi thông báo cho admin/staff
        User = get_user_model()
        admins = User.objects.filter(is_staff=True, is_active=True)
        
        # Tạo message chi tiết hơn
        question_text = question.content[:100] if question else None
        reply_text = reply.content[:100] if reply else None
        
        # Lấy thông tin user bị báo cáo
        reported_user = None
        reported_username = "N/A"
        if question:
            reported_user = question.student
            reported_username = reported_user.username if reported_user else "N/A"
        elif reply:
            reported_user = reply.user
            reported_username = reported_user.username if reported_user else "N/A"
        
        report_message = f"Báo cáo vi phạm từ {request.user.username}\n"
        report_message += f"Người bị báo cáo: {reported_username}\n"
        report_message += f"Lý do: {reason}"
        if detail:
            report_message += f"\nChi tiết: {detail}"
        if question_text:
            report_message += f"\nNội dung câu hỏi: {question_text}"
        if reply_text:
            report_message += f"\nNội dung phản hồi: {reply_text}"
        
        for admin in admins:
            Notification.objects.create(
                user=admin,
                title="🚨 Báo cáo vi phạm hỏi đáp bài học",
                message=report_message,
                type="warning",
                category="lesson_question_report",
                metadata={
                    "report_id": str(report.id),
                    "question_id": str(question.id) if question else None,
                    "reply_id": str(reply.id) if reply else None,
                    "reporter_id": str(request.user.id),
                    "reporter": request.user.username,
                    "reporter_email": request.user.email,
                    "reported_user_id": str(reported_user.id) if reported_user else None,
                    "reported_username": reported_username,
                    "reported_email": reported_user.email if reported_user else None,
                    "reason": reason,
                    "detail": detail,
                    "lesson_id": str(question.lesson_id) if question else (str(reply.question.lesson_id) if reply else None),
                },
            )

        return Response({"detail": "Đã gửi báo cáo"}, status=status.HTTP_201_CREATED)
