from typing import Any, Dict
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from custom_account.api.permissions import IsOwnerOrAdmin
from content import models
from content.serializers import (
    SubjectSerializer, CourseSerializer, ModuleSerializer, LessonSerializer,
    LessonVersionSerializer, ContentBlockSerializer, ExplorationSerializer,
    ExplorationStateSerializer, ExplorationTransitionSerializer,
    CreateCourseInputSerializer, AddModuleInputSerializer, CreateLessonInputSerializer,
    CreateLessonVersionInputSerializer, PublishLessonVersionInputSerializer,
    AddContentBlockInputSerializer, CreateExplorationInputSerializer,
    AddExplorationStateInputSerializer, AddExplorationTransitionInputSerializer,
    CourseDetailReadSerializer, ModuleReadSerializer, LessonReadSerializer,
    LessonVersionReadSerializer
)

from content.services.subject_service import SubjectService
from content.services.course_service import CourseService
from content.services.module_service import ModuleService
from content.services.lesson_service import LessonService
from content.services.lesson_version_service import LessonVersionService
from content.services.content_block_service import ContentBlockService
from content.services.exploration_service import (
    ExplorationService, ExplorationStateService, ExplorationTransitionService
)

# Create service instances
lesson_service = LessonService()

class LessonListCreateView(generics.ListCreateAPIView):
    """
    GET /api/modules/{module_id}/lessons/
    POST /api/modules/{module_id}/lessons/
    """
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Cho phép upload file

    def get_queryset(self):
        module_id = self.kwargs.get("module_id")
        return models.Lesson.objects.filter(module_id=module_id)

    def create(self, request, module_id=None, *args, **kwargs):
        # Merge module_id from URL into data if not provided
        data = request.data.copy()
        if module_id and 'module' not in data:
            data['module'] = module_id
        
        # Remove empty file fields
        for field in ['video_file']:
            if field in data:
                value = data[field]
                if value == '' or value is None or (hasattr(value, 'name') and not value.name):
                    data.pop(field, None)
        
        serializer = CreateLessonInputSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # Convert to CreateLessonDomain
        from content.domains.lesson_domain import CreateLessonDomain
        cmd = CreateLessonDomain(
            module_id=str(module_id) if module_id else str(serializer.validated_data.get('module').id),
            title=serializer.validated_data['title'],
            position=serializer.validated_data.get('position', 0),
            content_type=serializer.validated_data.get('content_type', 'lesson')
        )
        # Truyền author_id nếu có user đăng nhập
        author_id = request.user.id if request.user.is_authenticated else None
        try:
            created_domain = lesson_service.create_lesson(cmd, author_id=author_id)
        except Exception as e:
            import traceback
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error creating lesson: {str(e)}\n{traceback.format_exc()}")
            return Response(
                {"detail": f"Error creating lesson: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Update model with new fields
        from content.models import Lesson
        try:
            lesson_model = Lesson.objects.prefetch_related('versions').get(id=created_domain.id)
            if 'introduction' in data:
                lesson_model.introduction = data['introduction']
            if 'video_url' in data:
                lesson_model.video_url = data['video_url']
            if 'video_file' in request.FILES and request.FILES['video_file']:
                lesson_model.video_file = request.FILES['video_file']
            if 'requires_exercise_completion' in data:
                lesson_model.requires_exercise_completion = bool(data['requires_exercise_completion'])
            # Nếu có published trong request, dùng giá trị đó, nếu không thì giữ mặc định True từ service
            if 'published' in data:
                lesson_model.published = bool(data['published'])
            lesson_model.save()
        except Exception as e:
            import traceback
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error updating lesson fields: {str(e)}\n{traceback.format_exc()}")
            # Vẫn trả về lesson đã tạo được, chỉ cảnh báo
            lesson_model = Lesson.objects.prefetch_related('versions').get(id=created_domain.id)
        
        # Return with new fields
        from content.domains.lesson_domain import LessonDomain
        lesson_domain = LessonDomain.from_model(lesson_model)
        result = LessonSerializer.from_domain(lesson_domain)
        from django.conf import settings
        if lesson_model.video_file:
            result['video_file'] = f"{settings.MEDIA_URL}{lesson_model.video_file}" if not str(lesson_model.video_file).startswith('http') else str(lesson_model.video_file)
        return Response(result, status=status.HTTP_201_CREATED)


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/lessons/{id}/
    PATCH /api/lessons/{id}/   (owner/admin)
    DELETE /api/lessons/{id}/
    """
    queryset = models.Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Cho phép upload file

    def check_object_permissions(self, request, obj):
        """
        Override to check if user is owner of the course (via module) or admin.
        """
        if request.method in permissions.SAFE_METHODS:
            # Allow read for all authenticated users
            if not request.user or not request.user.is_authenticated:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("Authentication required")
            return
        
        # For write/delete, check if user is owner of course or admin
        if request.user.is_staff or request.user.is_superuser:
            return
        
        # Check if user is owner of the course (lesson -> module -> course -> owner)
        if hasattr(obj, 'module') and obj.module and hasattr(obj.module, 'course'):
            course = obj.module.course
            if hasattr(course, 'owner') and course.owner == request.user:
                return
            elif hasattr(course, 'owner_id') and course.owner_id == request.user.id:
                return
        
        # Default deny
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied("You do not have permission to perform this action")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        
        # Handle FormData for file uploads
        if hasattr(request.data, 'copy'):
            data = request.data.copy()
        else:
            data = dict(request.data)
        
        # Remove empty file fields
        for field in ['video_file']:
            if field in data:
                value = data[field]
                if value == '' or value is None or (hasattr(value, 'name') and not value.name):
                    data.pop(field, None)
        
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updates = serializer.validated_data
        
        # Update model directly for new fields
        if 'introduction' in updates:
            instance.introduction = updates['introduction']
        if 'video_url' in updates:
            instance.video_url = updates['video_url']
        if 'video_file' in request.FILES and request.FILES['video_file']:
            instance.video_file = request.FILES['video_file']
        if 'requires_exercise_completion' in updates:
            instance.requires_exercise_completion = updates['requires_exercise_completion']
        instance.save()
        
        # Also update via service for domain logic (convert dict to UpdateLessonDomain)
        from content.domains.lesson_domain import UpdateLessonDomain
        update_domain = UpdateLessonDomain(
            title=updates.get('title'),
            position=updates.get('position'),
            content_type=updates.get('content_type')
        )
        updated_domain = lesson_service.update_lesson(lesson_id=instance.id, update_data=update_domain)
        if not updated_domain:
            return Response({"detail": "Cannot update lesson"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Return updated model data
        from content.domains.lesson_domain import LessonDomain
        lesson_domain = LessonDomain.from_model(instance)
        result = LessonSerializer.from_domain(lesson_domain)
        # Add file URLs
        from django.conf import settings
        if instance.video_file:
            result['video_file'] = f"{settings.MEDIA_URL}{instance.video_file}" if not str(instance.video_file).startswith('http') else str(instance.video_file)
        return Response(result)


class LessonPublishView(APIView):
    """
    POST /api/lessons/{id}/publish/
    body example: {"published": true}
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def post(self, request, lesson_id: str):
        published_flag = request.data.get("published", True)
        try:
            # Get lesson to find latest version
            lesson = models.Lesson.objects.get(id=lesson_id)
            # Get latest version or use 1
            latest_version = lesson.versions.order_by('-version').first()
            version = latest_version.version if latest_version else 1
            # Convert to PublishLessonDomain
            from content.domains.lesson_domain import PublishLessonDomain
            publish_domain = PublishLessonDomain(
                lesson_id=lesson_id,
                version=version
            )
            updated = lesson_service.publish_lesson(lesson_id=lesson_id, publish_data=publish_domain)
            if not updated:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(LessonSerializer.from_domain(updated))
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)