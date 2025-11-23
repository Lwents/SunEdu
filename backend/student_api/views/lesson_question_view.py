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


def serialize_reply(rep: LessonQuestionReply, user=None, request=None):
    return {
        "id": str(rep.id),
        "user": rep.user.username,
        "avatar": avatar_for(rep.user, request),
        "user_id": rep.user.id,
        "is_owner": bool(user and user.id == rep.user.id),
        "is_teacher": rep.is_teacher,
        "content": rep.content,
        "created_at": rep.created_at.isoformat(),
        "reactions_count": rep.reactions.count() if hasattr(rep, "reactions") else 0,
        "reacted": bool(user and rep.reactions.filter(user=user).exists()),
    }


def serialize_question(q: LessonQuestion, user=None, request=None):
    return {
        "id": str(q.id),
        "lesson_id": str(q.lesson_id),
        "student_id": q.student_id,
        "student": q.student.username,
        "avatar": avatar_for(q.student, request),
        "is_owner": bool(user and user.id == q.student_id),
        "content": q.content,
        "created_at": q.created_at.isoformat(),
        "replies": [serialize_reply(r, user=user, request=request) for r in q.replies.all()],
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

        qs = LessonQuestion.objects.filter(lesson_id=lesson_id).select_related("student").prefetch_related(
            "replies__user",
            "replies__reactions",
        )
        data = [serialize_question(q, user=request.user, request=request) for q in qs.order_by("-created_at")]
        return Response({"items": data}, status=status.HTTP_200_OK)

    def post(self, request):
        content = (request.data.get("content") or "").strip()
        lesson_id = request.data.get("lesson_id")

        if not lesson_id:
            return Response({"detail": "lesson_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        if len(content) < 3:
            return Response({"detail": "Nội dung quá ngắn"}, status=status.HTTP_400_BAD_REQUEST)

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
        if len(content) < 3:
            return Response({"detail": "Nội dung quá ngắn"}, status=status.HTTP_400_BAD_REQUEST)
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
        if len(content) < 2:
            return Response({"detail": "Nội dung quá ngắn"}, status=status.HTTP_400_BAD_REQUEST)

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
        if len(content) < 2:
            return Response({"detail": "Nội dung quá ngắn"}, status=status.HTTP_400_BAD_REQUEST)
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
        admins = User.objects.filter(is_staff=True)
        for admin in admins:
            Notification.objects.create(
                user=admin,
                title="Báo cáo vi phạm hỏi đáp",
                message=reason,
                type="warning",
                category="lesson_question_report",
                metadata={
                    "report_id": str(report.id),
                    "question_id": str(question.id) if question else None,
                    "reply_id": str(reply.id) if reply else None,
                    "reporter_id": str(request.user.id),
                    "reporter": request.user.username,
                    "detail": detail,
                },
            )

        return Response({"detail": "Đã gửi báo cáo"}, status=status.HTTP_201_CREATED)
