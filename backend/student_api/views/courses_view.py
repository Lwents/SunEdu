from django.db.models import Count, Q, Prefetch
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from student_api.permissions import IsStudent
from content.models import Course, Enrollment, Lesson, LessonProgress, Module


class StudentMyCoursesView(APIView):
    """
    GET /api/student/courses/
    Returns enrolled courses for the student with progress
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        """Get student's enrolled courses"""
        student = request.user
        
        # Get query parameters
        q = request.query_params.get('q', '').strip()
        grade = request.query_params.get('grade', '').strip()
        level = request.query_params.get('level', '').strip()  # 'main' or 'supp'
        
        # Get enrolled courses (only published courses)
        enrollments = Enrollment.objects.filter(
            student=student,
            course__published=True  # Only show published courses
        ).select_related('course', 'course__subject', 'course__owner')
        
        courses_data = []
        
        for enrollment in enrollments:
            course = enrollment.course
            
            grade_value = course.grade or ''
            grade_number = None
            try:
                grade_number = int(grade_value)
            except (ValueError, TypeError):
                grade_number = None
            
            if grade_number is not None:
                grade_label = 'Khối 1–2' if grade_number <= 2 else 'Khối 3–5'
            else:
                grade_label = 'Khối 1–2' if grade_value in ['1', '2', 'Khối 1–2', ''] else 'Khối 3–5'
            
            # Filter by search query
            if q and q.lower() not in course.title.lower():
                continue
            
            # Filter by grade
            if grade:
                if grade == 'Khối 1–2' and not (
                    (grade_number is not None and grade_number <= 2) or grade_value in ['1', '2', 'Khối 1–2']
                ):
                    continue
                if grade == 'Khối 3–5' and not (
                    (grade_number is not None and grade_number >= 3) or grade_value in ['3', '4', '5', 'Khối 3–5']
                ):
                    continue
            
            # Calculate progress
            total_lessons = Lesson.objects.filter(
                module__course=course,
                published=True
            ).count()
            
            completed_lessons = LessonProgress.objects.filter(
                lesson__module__course=course,
                student=student,
                completed=True
            ).count()
            
            progress = int((completed_lessons / total_lessons * 100)) if total_lessons > 0 else 0
            done = progress >= 100
            
            course_data = {
                'id': str(course.id),
                'title': course.title,
                'grade': grade_number if grade_number is not None else grade_value,
                'gradeLabel': grade_label,
                'gradeNumber': grade_number,
                'subject': course.subject.title if course.subject else '',
                'subjectSlug': course.subject.slug if course.subject else '',
                'teacherId': str(course.owner.id) if course.owner else '',
                'teacherName': (course.owner.profile.display_name if hasattr(course.owner, 'profile') and course.owner.profile.display_name else course.owner.username) if course.owner else '',
                'lessonsCount': total_lessons,
                'enrollments': course.enrollments.count(),
                'status': 'published' if course.published else 'draft',
                'createdAt': course.id.generation_time.isoformat() if hasattr(course.id, 'generation_time') else None,
                'updatedAt': None,
                'thumbnail': course.thumbnail.url if course.thumbnail else None,
                'price': float(course.price) if course.price else 0,
                'isEnrolled': True,
                'progress': progress,
                'done': done,
            }
            
            courses_data.append(course_data)
        
        # Group by grade for frontend
        base_courses = [
            c for c in courses_data
            if (c.get('gradeNumber') is not None and c['gradeNumber'] <= 2)
            or c.get('grade') in ['1', '2', 'Khối 1–2']
        ]
        supp_courses = [
            c for c in courses_data
            if (c.get('gradeNumber') is not None and c['gradeNumber'] >= 3)
            or c.get('grade') in ['3', '4', '5', 'Khối 3–5']
        ]
        
        return Response({
            'base': base_courses,
            'supp': supp_courses,
            'all': courses_data,
        }, status=status.HTTP_200_OK)


class StudentCourseCatalogView(APIView):
    """
    GET /api/student/catalog/
    Returns all published courses (catalog view)
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        """Get course catalog"""
        student = request.user
        
        # Get query parameters
        q = request.query_params.get('q', '').strip()
        grade = request.query_params.get('grade', '').strip()
        subject = request.query_params.get('subject', '').strip()
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('pageSize', 20))
        
        # Get all published courses
        courses = Course.objects.filter(
            published=True
        ).select_related('subject', 'owner')
        
        # Apply filters
        if q:
            courses = courses.filter(title__icontains=q)
        if grade:
            courses = courses.filter(grade=grade)
        if subject:
            courses = courses.filter(subject__slug=subject)
        
        # Pagination
        total = courses.count()
        start = (page - 1) * page_size
        end = start + page_size
        courses = courses[start:end]
        
        # Check enrollment status for each course
        enrolled_course_ids = set(
            Enrollment.objects.filter(student=student)
            .values_list('course_id', flat=True)
        )
        
        courses_data = []
        for course in courses:
            is_enrolled = str(course.id) in enrolled_course_ids
            
            courses_data.append({
                'id': str(course.id),
                'title': course.title,
                'grade': course.grade or '',
                'subject': course.subject.title if course.subject else '',
                'teacherId': str(course.owner.id) if course.owner else '',
                'teacherName': (course.owner.profile.display_name if hasattr(course.owner, 'profile') and course.owner.profile.display_name else course.owner.username) if course.owner else '',
                'lessonsCount': Lesson.objects.filter(module__course=course, published=True).count(),
                'enrollments': course.enrollments.count(),
                'status': 'published',
                'createdAt': course.id.generation_time.isoformat() if hasattr(course.id, 'generation_time') else None,
                'updatedAt': None,
                'thumbnail': course.thumbnail.url if course.thumbnail else None,
                'price': float(course.price) if course.price else 0,
                'description': course.description or '',
                'introduction': course.introduction or '',
                'isEnrolled': is_enrolled,
            })
        
        return Response({
            'items': courses_data,
            'total': total,
        }, status=status.HTTP_200_OK)


class StudentCourseDetailView(APIView):
    """
    GET /api/student/courses/{id}/
    Returns course detail for student
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, pk):
        """Get course detail"""
        student = request.user
        course = get_object_or_404(Course, pk=pk)
        
        # Students can only view published courses
        if not course.published:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("This course is not available yet.")
        
        # Check if student is enrolled
        is_enrolled = Enrollment.objects.filter(
            course=course,
            student=student
        ).exists()
        
        # Get modules and lessons
        modules = Module.objects.filter(course=course).prefetch_related(
            Prefetch(
                'lessons',
                queryset=Lesson.objects.filter(published=True).order_by('position')
            )
        ).order_by('position')
        
        sections = []
        for module in modules:
            lessons = []
            for lesson in module.lessons.all():
                # Get progress for this lesson
                progress = LessonProgress.objects.filter(
                    lesson=lesson,
                    student=student
                ).first()
                
                lessons.append({
                    'id': str(lesson.id),
                    'title': lesson.title,
                    'type': 'video' if lesson.video_url or lesson.video_file else 'pdf',
                    'durationMinutes': None,  # Could calculate from video if available
                    'isPreview': False,  # First lesson could be preview
                    'completed': progress.completed if progress else False,
                    'videoWatched': progress.video_watched if progress else False,
                    'exerciseCompleted': progress.exercise_completed if progress else False,
                })
            
            sections.append({
                'id': str(module.id),
                'title': module.title,
                'order': module.position,
                'lessons': lessons,
            })
        
        # Calculate overall progress
        total_lessons = Lesson.objects.filter(
            module__course=course,
            published=True
        ).count()
        
        completed_lessons = LessonProgress.objects.filter(
            lesson__module__course=course,
            student=student,
            completed=True
        ).count()
        
        progress = int((completed_lessons / total_lessons * 100)) if total_lessons > 0 else 0
        
        course_data = {
            'id': str(course.id),
            'title': course.title,
            'grade': course.grade or '',
            'subject': course.subject.title if course.subject else '',
            'teacherId': str(course.owner.id) if course.owner else '',
            'teacherName': (course.owner.profile.display_name if hasattr(course.owner, 'profile') and course.owner.profile.display_name else course.owner.username) if course.owner else '',
            'lessonsCount': total_lessons,
            'enrollments': course.enrollments.count(),
            'status': 'published' if course.published else 'draft',
            'createdAt': course.id.generation_time.isoformat() if hasattr(course.id, 'generation_time') else None,
            'updatedAt': None,
            'thumbnail': course.thumbnail.url if course.thumbnail else None,
            'price': float(course.price) if course.price else 0,
            'description': course.description or '',
            'introduction': course.introduction or '',
            'video_url': course.video_url or '',
            'video_file': course.video_file.url if course.video_file else None,
            'sections': sections,
            'isEnrolled': is_enrolled,
            'progress': progress,
        }
        
        return Response(course_data, status=status.HTTP_200_OK)


class StudentCoursePlayerView(APIView):
    """
    GET /api/student/courses/{id}/player/{lesson_id}/
    Returns lesson content for player
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, pk, lesson_id=None):
        """Get lesson content for player"""
        student = request.user
        course = get_object_or_404(Course, pk=pk)
        
        # Check enrollment
        enrollment = Enrollment.objects.filter(
            course=course,
            student=student
        ).first()
        
        if not enrollment:
            return Response(
                {'detail': 'You are not enrolled in this course'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get lesson if specified
        if lesson_id:
            lesson = get_object_or_404(Lesson, pk=lesson_id, module__course=course)
        else:
            # Get first lesson
            first_module = Module.objects.filter(course=course).order_by('position').first()
            if not first_module:
                return Response(
                    {'detail': 'No lessons in this course'},
                    status=status.HTTP_404_NOT_FOUND
                )
            lesson = Lesson.objects.filter(
                module=first_module,
                published=True
            ).order_by('position').first()
            
            if not lesson:
                return Response(
                    {'detail': 'No published lessons in this course'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Get or create progress
        progress, created = LessonProgress.objects.get_or_create(
            lesson=lesson,
            student=student
        )
        
        # Get lesson content
        lesson_data = {
            'id': str(lesson.id),
            'title': lesson.title,
            'content_type': lesson.content_type,
            'video_url': lesson.video_url or '',
            'video_file': lesson.video_file.url if lesson.video_file else None,
            'introduction': lesson.introduction or '',
            'requires_exercise_completion': lesson.requires_exercise_completion,
            'progress': {
                'completed': progress.completed,
                'video_watched': progress.video_watched,
                'exercise_completed': progress.exercise_completed,
                'exercise_score': progress.exercise_score,
                'started_at': progress.started_at.isoformat() if progress.started_at else None,
                'last_accessed_at': progress.last_accessed_at.isoformat() if progress.last_accessed_at else None,
            },
        }
        
        return Response(lesson_data, status=status.HTTP_200_OK)


class StudentLearningPathView(APIView):
    """
    GET /api/student/learning-path/
    Returns learning path for student
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        """Get learning path"""
        student = request.user
        
        # Get enrolled courses grouped by grade
        enrollments = Enrollment.objects.filter(
            student=student
        ).select_related('course', 'course__subject')
        
        # Group by grade
        path_data = {
            'grade_1_2': [],
            'grade_3_5': [],
        }
        
        for enrollment in enrollments:
            course = enrollment.course
            
            # Calculate progress
            total_lessons = Lesson.objects.filter(
                module__course=course,
                published=True
            ).count()
            
            completed_lessons = LessonProgress.objects.filter(
                lesson__module__course=course,
                student=student,
                completed=True
            ).count()
            
            progress = int((completed_lessons / total_lessons * 100)) if total_lessons > 0 else 0
            
            course_data = {
                'id': str(course.id),
                'title': course.title,
                'grade': course.grade or '',
                'subject': course.subject.title if course.subject else '',
                'progress': progress,
                'thumbnail': course.thumbnail.url if course.thumbnail else None,
            }
            
            if course.grade in ['1', '2', 'Khối 1–2']:
                path_data['grade_1_2'].append(course_data)
            else:
                path_data['grade_3_5'].append(course_data)
        
        return Response(path_data, status=status.HTTP_200_OK)
