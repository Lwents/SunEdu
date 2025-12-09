# ai_personalization/api/tutor_views.py
"""
API Views cho AI Tutor
"""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
import logging

from ..ai_tutor import ai_tutor
from ..models import LearningEvent

logger = logging.getLogger(__name__)


class AITutorChatView(APIView):
    """
    POST /api/student/ai/tutor/chat/
    
    Chat với AI Tutor
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        message = request.data.get('message', '').strip()
        context = request.data.get('context', {})
        conversation_id = request.data.get('conversation_id')
        
        if not message:
            return Response(
                {'error': 'Tin nhắn không được để trống'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(message) > 1000:
            return Response(
                {'error': 'Tin nhắn quá dài (tối đa 1000 ký tự)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get student grade from profile
        student_grade = 1
        if hasattr(request.user, 'profile'):
            student_grade = getattr(request.user.profile, 'grade', 1) or 1
        
        # Get conversation history from cache
        cache_key = f"ai_chat:{request.user.id}:{conversation_id or 'default'}"
        conversation_history = cache.get(cache_key, [])
        
        # Call AI Tutor
        try:
            result = ai_tutor.chat(
                user_message=message,
                context=context,
                conversation_history=conversation_history,
                student_grade=student_grade
            )
        except Exception as e:
            logger.error(f"AI Tutor chat error: {e}")
            result = {
                'success': True,
                'message': f"Xin chào! 🌟 Mình đang học cách trả lời tốt hơn. Bạn hỏi gì vậy?",
                'provider': 'fallback'
            }
        
        if result['success']:
            # Update conversation history
            conversation_history.append({'role': 'user', 'content': message})
            conversation_history.append({'role': 'assistant', 'content': result['message']})
            
            # Keep only last 20 messages
            conversation_history = conversation_history[-20:]
            cache.set(cache_key, conversation_history, 3600)  # 1 hour
            
            # Log event
            try:
                LearningEvent.objects.create(
                    user=request.user,
                    event_type='ai_chat',
                    detail={
                        'message_length': len(message),
                        'context': context.get('lesson_id'),
                        'provider': result.get('provider')
                    }
                )
            except Exception as e:
                logger.warning(f"Failed to log AI chat event: {e}")
        
        return Response({
            'success': result['success'],
            'message': result['message'],
            'conversation_id': conversation_id or 'default'
        })


class AITutorHintView(APIView):
    """
    POST /api/student/ai/tutor/hint/
    
    Lấy gợi ý cho câu hỏi
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        question_text = request.data.get('question_text', '')
        question_type = request.data.get('question_type', 'multiple_choice')
        choices = request.data.get('choices', [])
        student_answer = request.data.get('student_answer')
        correct_answer = request.data.get('correct_answer')
        hint_level = request.data.get('hint_level', 1)
        question_id = request.data.get('question_id')
        
        if not question_text:
            return Response(
                {'error': 'Câu hỏi không được để trống'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Limit hint requests per question
        cache_key = f"hint_count:{request.user.id}:{question_id}"
        hint_count = cache.get(cache_key, 0)
        
        if hint_count >= 3:
            return Response({
                'success': True,
                'hint': "Con đã dùng hết 3 lượt gợi ý cho câu này rồi! 🌟 Hãy thử suy nghĩ thêm hoặc chuyển sang câu khác nhé!",
                'hint_level': 3,
                'can_get_more_hints': False,
                'hints_remaining': 0
            })
        
        # Get student grade
        student_grade = 1
        if hasattr(request.user, 'profile'):
            student_grade = getattr(request.user.profile, 'grade', 1) or 1
        
        # Get hint
        result = ai_tutor.get_hint(
            question_text=question_text,
            question_type=question_type,
            choices=choices,
            student_answer=student_answer,
            correct_answer=correct_answer,
            hint_level=min(hint_level, hint_count + 1),  # Progressive hints
            student_grade=student_grade
        )
        
        if result['success']:
            # Update hint count
            cache.set(cache_key, hint_count + 1, 3600)  # 1 hour
            
            # Log event
            try:
                LearningEvent.objects.create(
                    user=request.user,
                    event_type='hint_request',
                    detail={
                        'question_id': question_id,
                        'hint_level': result['hint_level'],
                        'had_wrong_answer': bool(student_answer)
                    }
                )
            except Exception as e:
                logger.warning(f"Failed to log hint event: {e}")
        
        return Response({
            'success': result['success'],
            'hint': result['hint'],
            'hint_level': result.get('hint_level', hint_count + 1),
            'can_get_more_hints': hint_count + 1 < 3,
            'hints_remaining': max(0, 2 - hint_count)
        })


class AITutorExplainView(APIView):
    """
    POST /api/student/ai/tutor/explain/
    
    Giải thích khái niệm
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        concept = request.data.get('concept', '').strip()
        subject = request.data.get('subject', 'general')
        use_examples = request.data.get('use_examples', True)
        
        if not concept:
            return Response(
                {'error': 'Khái niệm không được để trống'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get student grade
        student_grade = 1
        if hasattr(request.user, 'profile'):
            student_grade = getattr(request.user.profile, 'grade', 1) or 1
        
        result = ai_tutor.explain_concept(
            concept=concept,
            subject=subject,
            student_grade=student_grade,
            use_examples=use_examples
        )
        
        return Response(result)


class AITutorEncourageView(APIView):
    """
    POST /api/student/ai/tutor/encourage/
    
    Lấy lời động viên
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        situation = request.data.get('situation', 'correct')
        score = request.data.get('score')
        
        # Get student name
        student_name = "con"
        if hasattr(request.user, 'profile') and request.user.profile.name:
            student_name = request.user.profile.name.split()[0]  # First name
        elif request.user.first_name:
            student_name = request.user.first_name
        
        message = ai_tutor.encourage(
            situation=situation,
            student_name=student_name,
            score=score
        )
        
        return Response({
            'message': message,
            'situation': situation
        })


class AITutorClearHistoryView(APIView):
    """
    DELETE /api/student/ai/tutor/history/
    
    Xóa lịch sử chat
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        conversation_id = request.query_params.get('conversation_id', 'default')
        cache_key = f"ai_chat:{request.user.id}:{conversation_id}"
        cache.delete(cache_key)
        
        return Response({'success': True, 'message': 'Đã xóa lịch sử chat'})


class AITutorAnalyzeView(APIView):
    """
    GET /api/student/ai/tutor/analyze/
    
    Phân tích điểm yếu của học sinh
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        from activities.models import ExerciseAttempt
        
        user = request.user
        
        # Get student grade
        student_grade = 1
        if hasattr(user, 'profile'):
            student_grade = getattr(user.profile, 'grade', 1) or 1
        
        # Collect performance data
        recent_attempts = ExerciseAttempt.objects.filter(
            student=user,
            finished_at__isnull=False
        ).select_related('exercise').order_by('-finished_at')[:50]
        
        # Analyze by subject/topic
        subjects_data = {}
        wrong_topics = []
        
        for attempt in recent_attempts:
            exercise = attempt.exercise
            subject = exercise.lesson.module.course.title if exercise.lesson else 'Khác'
            
            if subject not in subjects_data:
                subjects_data[subject] = {'correct': 0, 'total': 0, 'wrong_topics': []}
            
            subjects_data[subject]['total'] += 1
            if attempt.score and attempt.score >= 70:
                subjects_data[subject]['correct'] += 1
            else:
                topic = exercise.title or 'Chung'
                if topic not in subjects_data[subject]['wrong_topics']:
                    subjects_data[subject]['wrong_topics'].append(topic)
                wrong_topics.append({'topic': topic, 'subject': subject})
        
        # Build performance summary
        subjects = []
        for name, data in subjects_data.items():
            score = (data['correct'] / data['total'] * 100) if data['total'] > 0 else 0
            subjects.append({
                'name': name,
                'score': round(score),
                'wrong_topics': data['wrong_topics'][:5]
            })
        
        performance = {
            'subjects': subjects,
            'recent_exercises': [
                {
                    'topic': a.exercise.title,
                    'correct': a.score >= 70 if a.score else False,
                    'score': a.score
                } for a in recent_attempts[:10]
            ],
            'total_completed': recent_attempts.count()
        }
        
        # Call AI to analyze
        result = ai_tutor.analyze_weaknesses(performance, student_grade)
        
        # Tự động tạo thông báo nếu có điểm yếu nghiêm trọng
        analysis = result.get('analysis', {})
        weaknesses = analysis.get('weaknesses', [])
        high_severity = [w for w in weaknesses if w.get('severity') == 'high']
        
        notification_sent = False
        if high_severity:
            from activities.models import Notification
            from django.utils import timezone
            from datetime import timedelta
            
            # Kiểm tra xem đã gửi thông báo trong 24h chưa
            recent_notification = Notification.objects.filter(
                user=user,
                category='ai_weakness',
                created_at__gte=timezone.now() - timedelta(hours=24)
            ).exists()
            
            if not recent_notification:
                try:
                    topics = [w.get('topic', '') for w in high_severity[:3]]
                    Notification.objects.create(
                        user=user,
                        title='📚 AI nhắc nhở',
                        message=f'Bạn cần ôn lại: {", ".join(topics)}. Hãy vào Lộ trình học tập để luyện tập nhé! 🌟',
                        type='warning',
                        category='ai_weakness',
                        metadata={
                            'weaknesses': high_severity,
                            'action': 'practice'
                        }
                    )
                    notification_sent = True
                except Exception as e:
                    logger.error(f"Create weakness notification error: {e}")
        
        return Response({
            'success': result.get('success', False),
            'analysis': analysis,
            'performance_summary': performance,
            'notification_sent': notification_sent
        })


class AITutorPracticeView(APIView):
    """
    POST /api/student/ai/tutor/practice/
    
    Tạo bài luyện tập dựa trên điểm yếu
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        weaknesses = request.data.get('weaknesses', [])
        num_exercises = min(request.data.get('num_exercises', 5), 10)
        
        # Get student grade
        student_grade = 1
        if hasattr(request.user, 'profile'):
            student_grade = getattr(request.user.profile, 'grade', 1) or 1
        
        # If no weaknesses provided, get from analysis
        if not weaknesses:
            # Quick analysis
            from activities.models import ExerciseAttempt
            recent_wrong = ExerciseAttempt.objects.filter(
                student=request.user,
                finished_at__isnull=False,
                score__lt=70
            ).select_related('exercise').order_by('-finished_at')[:10]
            
            seen_topics = set()
            for attempt in recent_wrong:
                topic = attempt.exercise.title
                subject = attempt.exercise.lesson.module.course.title if attempt.exercise.lesson else 'Toán'
                if topic not in seen_topics:
                    weaknesses.append({'topic': topic, 'subject': subject})
                    seen_topics.add(topic)
        
        if not weaknesses:
            # Default topics for grade
            default_topics = {
                1: [{'topic': 'Phép cộng trong phạm vi 10', 'subject': 'Toán'}],
                2: [{'topic': 'Phép cộng có nhớ', 'subject': 'Toán'}],
                3: [{'topic': 'Phép nhân', 'subject': 'Toán'}],
                4: [{'topic': 'Phân số', 'subject': 'Toán'}],
                5: [{'topic': 'Số thập phân', 'subject': 'Toán'}],
            }
            weaknesses = default_topics.get(student_grade, default_topics[1])
        
        result = ai_tutor.generate_practice_exercises(
            weaknesses=weaknesses,
            student_grade=student_grade,
            num_exercises=num_exercises
        )
        
        # Cache exercises for this user
        if result.get('success'):
            cache_key = f"ai_practice:{request.user.id}"
            cache.set(cache_key, result.get('exercises', []), 3600)
        
        return Response(result)


class AITutorDailyReportView(APIView):
    """
    GET /api/student/ai/tutor/daily-report/
    
    Tạo báo cáo học tập hàng ngày
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        from activities.models import ExerciseAttempt
        from django.utils import timezone
        from datetime import timedelta
        
        user = request.user
        today = timezone.now().date()
        
        # Get student info
        student_name = "con"
        student_grade = 1
        if hasattr(user, 'profile'):
            if user.profile.name:
                student_name = user.profile.name.split()[0]
            student_grade = getattr(user.profile, 'grade', 1) or 1
        elif user.first_name:
            student_name = user.first_name
        
        # Get today's performance
        today_attempts = ExerciseAttempt.objects.filter(
            student=user,
            finished_at__date=today
        )
        
        completed = today_attempts.count()
        scores = [a.score for a in today_attempts if a.score is not None]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        # Estimate time spent (assume 2 min per exercise)
        time_spent = completed * 2
        
        performance_today = {
            'completed': completed,
            'avg_score': round(avg_score),
            'time_spent': time_spent
        }
        
        # Get weaknesses
        wrong_attempts = today_attempts.filter(score__lt=70)
        weaknesses = []
        for attempt in wrong_attempts[:5]:
            weaknesses.append({
                'topic': attempt.exercise.title,
                'subject': attempt.exercise.lesson.module.course.title if attempt.exercise.lesson else 'Khác'
            })
        
        result = ai_tutor.generate_daily_report(
            student_name=student_name,
            performance_today=performance_today,
            weaknesses=weaknesses,
            student_grade=student_grade
        )
        
        # Create notification if report generated
        if result.get('success') and completed > 0:
            try:
                LearningEvent.objects.create(
                    user=user,
                    event_type='daily_report',
                    detail={
                        'completed': completed,
                        'avg_score': avg_score,
                        'date': str(today)
                    }
                )
            except Exception:
                pass
        
        return Response({
            'success': result.get('success', False),
            'report': result.get('report', {}),
            'performance': performance_today,
            'date': str(today)
        })


class AITutorWeaknessNotificationView(APIView):
    """
    POST /api/student/ai/tutor/notify-weakness/
    
    Gửi thông báo về điểm yếu cần cải thiện cho học sinh
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        from activities.models import Notification
        
        user = request.user
        weaknesses = request.data.get('weaknesses', [])
        
        if not weaknesses:
            return Response({
                'success': False,
                'error': 'Không có điểm yếu để thông báo'
            })
        
        # Tạo nội dung thông báo
        topics = [w.get('topic', '') for w in weaknesses[:3]]
        topics_str = ', '.join(topics)
        
        # Tạo thông báo
        try:
            notification = Notification.objects.create(
                user=user,
                title='📚 AI nhắc nhở',
                message=f'Bạn cần ôn lại: {topics_str}. Hãy vào Lộ trình học tập để luyện tập nhé! 🌟',
                type='info',
                category='ai_tutor',
                metadata={
                    'weaknesses': weaknesses,
                    'action': 'practice'
                }
            )
            
            return Response({
                'success': True,
                'notification_id': str(notification.id),
                'message': 'Đã gửi thông báo'
            })
        except Exception as e:
            logger.error(f"Create notification error: {e}")
            return Response({
                'success': False,
                'error': str(e)
            })


class AITutorVideoQuestionView(APIView):
    """
    POST /api/student/ai/tutor/video-question/
    
    Hỏi AI về đoạn video đang xem tại timestamp cụ thể
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        from content.models import Lesson
        
        lesson_id = request.data.get('lesson_id')
        question = request.data.get('question', '').strip()
        timestamp = request.data.get('timestamp', 0)  # Giây
        video_title = request.data.get('video_title', '')
        
        if not question:
            return Response(
                {'error': 'Câu hỏi không được để trống'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(question) > 1000:
            return Response(
                {'error': 'Câu hỏi quá dài (tối đa 1000 ký tự)'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get student grade from profile
        student_grade = 1
        if hasattr(request.user, 'profile'):
            student_grade = getattr(request.user.profile, 'grade', 1) or 1
        
        # Format timestamp thành MM:SS
        minutes = int(timestamp) // 60
        seconds = int(timestamp) % 60
        timestamp_str = f"{minutes:02d}:{seconds:02d}"
        
        # Lấy context từ lesson nếu có
        lesson_context = ""
        lesson_title = ""
        course_title = ""
        
        if lesson_id:
            try:
                lesson = Lesson.objects.select_related('module__course').get(id=lesson_id)
                lesson_title = lesson.title
                if lesson.module and lesson.module.course:
                    course_title = lesson.module.course.title
                
                # Lấy nội dung bài học
                if lesson.introduction:
                    lesson_context += f"Giới thiệu bài học: {lesson.introduction[:500]}\n"
                if lesson.text_content:
                    lesson_context += f"Nội dung: {lesson.text_content[:1000]}\n"
                
                # Lấy transcript từ content_blocks nếu có
                try:
                    latest_version = lesson.versions.filter(status='published').order_by('-version').first()
                    if latest_version:
                        for block in latest_version.content_blocks.filter(type='video'):
                            payload = block.payload or {}
                            transcript = payload.get('transcript', '') or payload.get('tts_text', '')
                            if transcript:
                                lesson_context += f"Nội dung video: {transcript[:1500]}\n"
                                break
                except Exception:
                    pass
            except Lesson.DoesNotExist:
                pass
        
        # Build context cho AI
        context = {
            'lesson_title': lesson_title or video_title,
            'course_title': course_title,
            'video_timestamp': timestamp_str,
            'lesson_content': lesson_context[:2000] if lesson_context else None,
        }
        
        # Build prompt đặc biệt cho câu hỏi về video
        video_prompt = f"""Bạn là trợ lý học tập AI của SmartEdu.

Học sinh đang xem video bài học "{lesson_title or video_title}" tại thời điểm {timestamp_str}.

Câu hỏi: "{question}"

{f'Khóa học: {course_title}' if course_title else ''}
{f'Thông tin bài học:\n{lesson_context[:2000]}' if lesson_context else ''}

YÊU CẦU TRẢ LỜI:
1. Trả lời vừa đủ (3-5 câu), dễ hiểu
2. Ngôn ngữ đơn giản, phù hợp học sinh lớp {student_grade}
3. Thêm 1-2 emoji 🌟
4. Xưng "mình", gọi học sinh là "bạn" hoặc "em"
5. Nếu không biết nội dung cụ thể trong video, thành thật nói và gợi ý học sinh xem lại hoặc hỏi giáo viên

Trả lời:"""

        # Get conversation history from cache
        cache_key = f"ai_video_chat:{request.user.id}:{lesson_id or 'default'}"
        conversation_history = cache.get(cache_key, [])
        
        # Call AI Tutor
        try:
            result = ai_tutor.chat(
                user_message=video_prompt,
                context=context,
                conversation_history=conversation_history,
                student_grade=student_grade
            )
        except Exception as e:
            logger.error(f"AI Video Question error: {e}")
            result = {
                'success': True,
                'message': f"Xin lỗi, AI đang bận! 🌟 Bạn đang hỏi về đoạn video tại {timestamp_str}. Hãy thử lại sau nhé!",
                'provider': 'fallback'
            }
        
        if result['success']:
            # Update conversation history
            conversation_history.append({
                'role': 'user', 
                'content': f"[Tại {timestamp_str}] {question}"
            })
            conversation_history.append({
                'role': 'assistant', 
                'content': result['message']
            })
            
            # Keep only last 10 messages for video context
            conversation_history = conversation_history[-10:]
            cache.set(cache_key, conversation_history, 1800)  # 30 minutes
            
            # Log event
            try:
                LearningEvent.objects.create(
                    user=request.user,
                    event_type='ai_video_question',
                    detail={
                        'lesson_id': str(lesson_id) if lesson_id else None,
                        'timestamp': timestamp,
                        'timestamp_str': timestamp_str,
                        'question_length': len(question),
                        'provider': result.get('provider')
                    }
                )
            except Exception as e:
                logger.warning(f"Failed to log AI video question event: {e}")
        
        return Response({
            'success': result['success'],
            'message': result['message'],
            'timestamp': timestamp_str,
            'lesson_id': str(lesson_id) if lesson_id else None
        })
