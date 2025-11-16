from django.db.models import Count, Q, Avg, Max
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from student_api.permissions import IsStudent
from activities.models import Exercise, ExerciseAttempt, ExerciseAnswer, Question, Choice
from activities.services import (
    get_exercise,
    start_attempt,
    submit_answer,
    finalize_attempt,
    get_attempt_summary,
    exercise_stats,
)
from activities.services import NotFoundError, ValidationError, PermissionDenied


class StudentExamsListView(APIView):
    """
    GET /api/student/exams/
    Returns list of available exams (exercises) for student
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        """Get list of exams"""
        student = request.user
        
        # Get query parameters
        level = request.query_params.get('level', '').strip()  # 'Khối 1–2' or 'Khối 3–5'
        q = request.query_params.get('q', '').strip()
        
        # Get all exercises
        exercises = Exercise.objects.all()
        
        # Apply filters
        if q:
            exercises = exercises.filter(title__icontains=q)
        
        # Note: Exercise model doesn't have grade/level field directly
        # This would need to be added to the model or stored in metadata
        
        exams_data = []
        for exercise in exercises:
            # Get settings if exists
            duration_sec = 1800  # Default 30 minutes
            pass_score = 12  # Default
            grade = 'Khối 1–2'  # Default (Exercise model doesn't have grade field)
            
            try:
                if hasattr(exercise, 'settings') and exercise.settings:
                    duration_sec = exercise.settings.time_limit_seconds or duration_sec
                    pass_score = exercise.settings.pass_score or pass_score
            except:
                pass
            
            # Filter by level if specified (Note: Exercise doesn't have grade, so skip filter for now)
            # if level and grade != level:
            #     continue
            
            questions_count = Question.objects.filter(exercise=exercise).count()
            
            exams_data.append({
                'id': str(exercise.id),
                'title': exercise.title,
                'level': grade,
                'durationSec': duration_sec,
                'passScore': pass_score,
                'questionsCount': questions_count,
                'status': 'published',  # All exercises are considered published for students
                'updatedAt': None,  # Exercise model doesn't have updated_at
            })
        
        return Response(exams_data, status=status.HTTP_200_OK)


class StudentExamDetailView(APIView):
    """
    GET /api/student/exams/{id}/
    Returns exam detail for student
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, pk):
        """Get exam detail"""
        try:
            exercise_domain = get_exercise(str(pk))
        except NotFoundError:
            return Response(
                {'detail': 'Exam not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Convert domain to response format
        exercise_data = {
            'id': str(exercise_domain.id),
            'title': exercise_domain.title,
            'level': 'Khối 1–2',  # Default, should be in domain
            'durationSec': 1800,  # Default
            'passScore': 12,  # Default
            'questionsCount': len(exercise_domain.questions) if hasattr(exercise_domain, 'questions') else 0,
            'status': 'published' if exercise_domain.published else 'draft',
            'updatedAt': None,
            'description': getattr(exercise_domain, 'description', ''),
            'shuffleQuestions': True,  # Default
            'shuffleChoices': True,  # Default
            'questions': [],
        }
        
        # Get questions with choices
        exercise = Exercise.objects.prefetch_related('questions__choices').get(id=pk)
        questions_data = []
        
        for question in exercise.questions.all():
            question_data = {
                'id': str(question.id),
                'type': 'single',  # Default, should be determined from question
                'text': question.prompt,
                'score': 1,  # Default
                'choices': [],
            }
            
            # Get choices
            choices = question.choices.all()
            correct_answers = []
            for choice in choices:
                question_data['choices'].append({
                    'id': str(choice.id),
                    'text': choice.text,
                })
                if choice.is_correct:
                    correct_answers.append(str(choice.id))
            
            question_data['answer'] = correct_answers
            questions_data.append(question_data)
        
        exercise_data['questions'] = questions_data
        
        return Response(exercise_data, status=status.HTTP_200_OK)


class StudentExamStartView(APIView):
    """
    POST /api/student/exams/{id}/start/
    Starts an exam attempt for student
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, pk):
        """Start exam attempt"""
        try:
            attempt_domain = start_attempt(str(pk), request.user)
        except NotFoundError:
            return Response(
                {'detail': 'Exam not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except PermissionDenied as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Convert to response format
        attempt_data = {
            'id': str(attempt_domain.id),
            'examId': str(attempt_domain.exercise_id),
            'startedAt': attempt_domain.started_at.isoformat() if hasattr(attempt_domain, 'started_at') else None,
            'deadlineAt': None,  # Calculate from duration
            'questions': [],
            'answers': {},
        }
        
        # Get questions for attempt
        exercise = Exercise.objects.prefetch_related('questions__choices').get(id=pk)
        for question in exercise.questions.all():
            question_data = {
                'id': str(question.id),
                'type': 'single',  # Default
                'text': question.prompt,
                'score': 1,
                'choices': [],
            }
            
            choices = question.choices.all()
            for choice in choices:
                question_data['choices'].append({
                    'id': str(choice.id),
                    'text': choice.text,
                })
            
            attempt_data['questions'].append(question_data)
        
        return Response(attempt_data, status=status.HTTP_201_CREATED)


class StudentExamSubmitView(APIView):
    """
    POST /api/student/exams/{id}/submit/
    Submits exam answers and finalizes attempt
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, pk, attempt_id):
        """Submit exam answers"""
        student = request.user
        
        # Submit all answers
        answers = request.data.get('answers', {})
        for question_id, answer in answers.items():
            try:
                submit_answer(
                    attempt_id=str(attempt_id),
                    question_id=str(question_id),
                    answer_payload=answer,
                    actor_user=student,
                )
            except (NotFoundError, ValidationError, PermissionDenied) as e:
                return Response(
                    {'detail': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Finalize attempt
        try:
            summary = finalize_attempt(str(attempt_id), actor_user=student, force=False)
        except (NotFoundError, ValidationError, PermissionDenied) as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert summary to response format
        result_data = {
            'attemptId': str(attempt_id),
            'examId': str(pk),
            'totalScore': summary.get('total_score', 0),
            'maxScore': summary.get('max_score', 0),
            'correctCount': summary.get('correct_count', 0),
            'totalCount': summary.get('total_count', 0),
            'passed': summary.get('passed', False),
            'detail': summary.get('detail', []),
        }
        
        return Response(result_data, status=status.HTTP_200_OK)


class StudentExamResultView(APIView):
    """
    GET /api/student/exams/{id}/result/{attempt_id}/
    Returns exam result for student
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, pk, attempt_id):
        """Get exam result"""
        try:
            summary = get_attempt_summary(str(attempt_id))
        except NotFoundError:
            return Response(
                {'detail': 'Attempt not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Convert to response format
        result_data = {
            'attemptId': str(attempt_id),
            'examId': str(pk),
            'totalScore': summary.get('total_score', 0),
            'maxScore': summary.get('max_score', 0),
            'correctCount': summary.get('correct_count', 0),
            'totalCount': summary.get('total_count', 0),
            'passed': summary.get('passed', False),
            'detail': summary.get('detail', []),
        }
        
        return Response(result_data, status=status.HTTP_200_OK)


class StudentExamRankingView(APIView):
    """
    GET /api/student/exams/{id}/ranking/
    Returns ranking for exam
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, pk):
        """Get exam ranking"""
        student = request.user
        
        try:
            stats = exercise_stats(str(pk))
        except NotFoundError:
            return Response(
                {'detail': 'Exam not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get top students
        top_attempts = ExerciseAttempt.objects.filter(
            exercise_id=pk,
            finished_at__isnull=False
        ).select_related('student').order_by('-score')[:10]
        
        top = []
        for idx, attempt in enumerate(top_attempts):
            top.append({
                'id': idx + 1,
                'name': attempt.student.get_full_name() or attempt.student.username if attempt.student else 'Unknown',
                'score': float(attempt.score) if attempt.score else 0,
                'correct': 0,  # Would need to calculate from answers
                'total': 0,  # Would need to get from exercise
                'time': '00:00',  # Would need to calculate from metadata
            })
        
        # Get student's rank
        student_attempts = ExerciseAttempt.objects.filter(
            exercise_id=pk,
            student=student,
            finished_at__isnull=False
        ).order_by('-score')
        
        me = None
        if student_attempts.exists():
            best_attempt = student_attempts.first()
            # Calculate rank (simplified)
            rank = ExerciseAttempt.objects.filter(
                exercise_id=pk,
                finished_at__isnull=False,
                score__gt=best_attempt.score if best_attempt.score else 0
            ).count() + 1
            
            me = {
                'rank': rank,
                'score': float(best_attempt.score) if best_attempt.score else 0,
                'correct': 0,
                'total': 0,
                'time': '00:00',
            }
        
        return Response({
            'top': top,
            'me': me,
        }, status=status.HTTP_200_OK)


class StudentCertificatesView(APIView):
    """
    GET /api/student/exams/certificates/
    Returns certificates for student
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        """Get student certificates"""
        student = request.user
        
        # Get completed attempts with passing scores
        attempts = ExerciseAttempt.objects.filter(
            student=student,
            finished_at__isnull=False,
            score__gte=50  # Passing score threshold
        ).select_related('exercise').order_by('-finished_at')
        
        certificates = []
        for attempt in attempts:
            certificates.append({
                'id': str(attempt.id),
                'title': f'Chứng chỉ {attempt.exercise.title}',
                'score': float(attempt.score) if attempt.score else 0,
                'total': 100,  # Default
                'issuedAt': attempt.finished_at.isoformat() if attempt.finished_at else None,
                'thumbnail': None,
                'image': None,
                'pdf': None,
            })
        
        return Response(certificates, status=status.HTTP_200_OK)

