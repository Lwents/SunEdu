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
        num_exercises = min(request.data.get('num_exercises', 15), 20)  # Mặc định 15 câu, tối đa 20
        wrong_questions = request.data.get('wrong_questions', [])  # Câu hỏi sai cụ thể
        
        # Get student grade
        student_grade = 1
        if hasattr(request.user, 'profile'):
            student_grade = getattr(request.user.profile, 'grade', 1) or 1
        
        # Nếu có wrong_questions từ weaknesses, sử dụng chúng
        if not wrong_questions and weaknesses:
            # Lấy wrong_questions từ weaknesses nếu có
            all_wrong_questions = []
            for w in weaknesses:
                if w.get('wrong_questions'):
                    all_wrong_questions.extend(w.get('wrong_questions', []))
            if all_wrong_questions:
                wrong_questions = all_wrong_questions[:15]  # Lấy tối đa 15 câu sai
        
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
            num_exercises=num_exercises,
            wrong_questions=wrong_questions  # Truyền câu hỏi sai vào
        )
        
        # Cache exercises for this user
        if result.get('success'):
            cache_key = f"ai_practice:{request.user.id}"
            cache.set(cache_key, result.get('exercises', []), 3600)
        
        return Response(result)


class AITutorPracticeSubmitView(APIView):
    """
    POST /api/student/ai/tutor/practice/submit/
    
    Submit kết quả bài luyện tập AI và tạo ExerciseAttempt để tính vào streak/daily goal
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        from activities.models import Exercise, ExerciseAttempt, ExerciseAnswer, Question, Choice
        from activities.services import start_attempt, finalize_attempt
        from django.utils import timezone
        
        exercises_data = request.data.get('exercises', [])  # Danh sách câu hỏi đã làm
        score = request.data.get('score', 0)  # Điểm số tổng (0-100)
        time_spent = request.data.get('time_spent', 0)  # Thời gian làm bài (giây)
        
        if not exercises_data:
            return Response(
                {'error': 'Không có dữ liệu bài tập'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Tạo Exercise mới cho bài luyện tập AI (mỗi lần submit tạo Exercise mới)
            # Sử dụng Exercise với title đặc biệt để phân biệt bài luyện tập AI
            exercise_title = f"AI Practice - {request.user.username} - {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
            exercise = Exercise.objects.create(
                title=exercise_title,
                type='mcq',
                published=True,
            )
            
            # Tạo ExerciseAttempt
            attempt = ExerciseAttempt.objects.create(
                exercise=exercise,
                student=request.user,
                score=score,
                finished_at=timezone.now(),
                metadata={
                    'type': 'ai_practice',
                    'time_spent': time_spent,
                    'num_questions': len(exercises_data),
                    'created_at': timezone.now().isoformat()
                }
            )
            
            # Tạo ExerciseAnswer cho mỗi câu hỏi (nếu cần)
            # Lưu ý: Bài luyện tập AI có thể không có Question model, chỉ lưu metadata
            for idx, ex_data in enumerate(exercises_data):
                # Tạo Question tạm thời nếu chưa có
                question_text = ex_data.get('question', '')
                correct_answer = ex_data.get('correct_answer', '')
                student_answer = ex_data.get('student_answer', '')
                is_correct = ex_data.get('is_correct', False)
                
                if question_text:
                    question, _ = Question.objects.get_or_create(
                        exercise=exercise,
                        prompt=question_text,
                        defaults={'meta': {'type': 'ai_practice', 'index': idx}}
                    )
                    
                    # Tạo ExerciseAnswer
                    ExerciseAnswer.objects.create(
                        attempt=attempt,
                        question=question,
                        answer={'text': student_answer, 'selected_choice': correct_answer},
                        correct=is_correct
                    )
            
            return Response({
                'success': True,
                'attempt_id': str(attempt.id),
                'score': score,
                'message': 'Đã lưu kết quả bài luyện tập!'
            })
        
        except Exception as e:
            logger.error(f"Error submitting AI practice: {e}")
            return Response(
                {'error': f'Lỗi khi lưu kết quả: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        # Sử dụng localdate() để đảm bảo đúng timezone local (Asia/Ho_Chi_Minh)
        today = timezone.localdate()
        
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
    
    def _extract_transcript_at_timestamp(self, transcript: str, target_timestamp: int) -> str:
        """
        Extract transcript tại timestamp cụ thể (±90 giây, ưu tiên ±30 giây)
        Hỗ trợ video dài hơn 1 giờ (parse HH:MM:SS)
        Nếu transcript có format SRT/VTT với timestamp, parse và extract
        Ưu tiên các segments gần timestamp nhưng vẫn lấy đủ context để nhận diện bài hát
        """
        import re
        
        # Kiểm tra xem transcript có format SRT/VTT không
        # Pattern: HH:MM:SS,mmm --> HH:MM:SS,mmm hoặc HH:MM:SS.mmm --> HH:MM:SS.mmm
        # Hỗ trợ video dài hơn 1 giờ (HH có thể > 00)
        timestamp_pattern = r'(\d{1,2}):(\d{2}):(\d{2})[,\.](\d{3})\s*-->\s*(\d{1,2}):(\d{2}):(\d{2})[,\.](\d{3})'
        
        if not re.search(timestamp_pattern, transcript):
            # Không có timestamp format, không thể extract
            return None
        
        # Parse SRT/VTT format
        lines = transcript.split('\n')
        segments = []
        current_segment = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            
            # Tìm timestamp line
            match = re.match(timestamp_pattern, line)
            if match:
                # Parse start time
                h1, m1, s1, ms1 = map(int, match.groups()[:4])
                start_seconds = h1 * 3600 + m1 * 60 + s1
                
                # Parse end time
                h2, m2, s2, ms2 = map(int, match.groups()[4:])
                end_seconds = h2 * 3600 + m2 * 60 + s2
                
                # Lấy text sau timestamp (các dòng tiếp theo cho đến khi gặp dòng trống hoặc timestamp mới)
                text_lines = []
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    if not next_line or re.match(timestamp_pattern, next_line):
                        break
                    # Bỏ qua HTML tags
                    clean_line = re.sub(r'<[^>]+>', '', next_line)
                    if clean_line:
                        text_lines.append(clean_line)
                    j += 1
                
                if text_lines:
                    segments.append({
                        'start': start_seconds,
                        'end': end_seconds,
                        'text': ' '.join(text_lines)
                    })
        
        if not segments:
            return None
        
        # Tìm segments trong khoảng ±90 giây từ target_timestamp (tăng để có đủ context nhận diện bài hát)
        # Ưu tiên các segments gần timestamp hơn (±30 giây đầu tiên) nhưng vẫn lấy đủ context
        # Hỗ trợ video dài hơn 1 giờ - target_timestamp có thể > 3600 giây
        
        # Khoảng ưu tiên: ±30 giây (gần timestamp nhất)
        priority_start = max(0, target_timestamp - 30)
        priority_end = target_timestamp + 30
        
        # Khoảng mở rộng: ±90 giây (để có đủ context nhận diện bài hát, hook, điệp khúc)
        extended_start = max(0, target_timestamp - 90)
        extended_end = target_timestamp + 90
        
        priority_segments = []
        extended_segments = []
        
        for seg in segments:
            # Tính khoảng cách từ segment đến target_timestamp
            seg_center = (seg['start'] + seg['end']) / 2
            distance = abs(seg_center - target_timestamp)
            
            # Segment trong khoảng ưu tiên (±30 giây) - lấy tất cả
            if seg['start'] <= priority_end and seg['end'] >= priority_start:
                priority_segments.append((distance, seg))
            # Segment trong khoảng mở rộng (±90 giây) nhưng không trong khoảng ưu tiên
            elif seg['start'] <= extended_end and seg['end'] >= extended_start:
                extended_segments.append((distance, seg))
        
        # Sắp xếp theo khoảng cách (gần timestamp hơn = ưu tiên hơn)
        priority_segments.sort(key=lambda x: x[0])
        extended_segments.sort(key=lambda x: x[0])
        
        # Ưu tiên lấy từ khoảng ±30 giây trước, sau đó mở rộng để có đủ context
        selected_segments = []
        
        # Lấy TẤT CẢ segments trong khoảng ưu tiên (±30 giây)
        for _, seg in priority_segments:
            selected_segments.append(seg)
        
        # Lấy thêm từ khoảng mở rộng (±90 giây) để có đủ context nhận diện bài hát
        # Ưu tiên các segments gần timestamp hơn (trong ±60 giây trước, sau đó mở rộng)
        for _, seg in extended_segments:
            if seg not in selected_segments:
                selected_segments.append(seg)
        
        if selected_segments:
            # Combine các segments đã chọn, giữ nguyên thứ tự thời gian
            selected_segments.sort(key=lambda x: x['start'])
            combined_text = ' '.join([seg['text'] for seg in selected_segments])
            # Tăng lên 6000 ký tự để có đủ context nhận diện bài hát (hook, điệp khúc, lời bài hát đầy đủ)
            return combined_text[:6000]
        
        return None
    
    def _get_youtube_subtitle_with_timestamp(self, youtube_url: str) -> str:
        """
        Lấy subtitle từ YouTube với timestamp (SRT/VTT format)
        """
        import subprocess
        import tempfile
        import os
        import shutil
        
        try:
            temp_dir = tempfile.mkdtemp()
            output_template = os.path.join(temp_dir, 'subtitle')
            
            # Lấy phụ đề với timestamp
            cmd = [
                'yt-dlp',
                '--skip-download',
                '--write-sub',
                '--write-auto-sub',
                '--sub-lang', 'vi,en',
                '--sub-format', 'srt',
                '-o', output_template,
                '--no-playlist',
                youtube_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                return None
            
            # Tìm file SRT
            for filename in os.listdir(temp_dir):
                if filename.endswith('.srt'):
                    filepath = os.path.join(temp_dir, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        raw_subtitle = f.read()
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    return raw_subtitle
            
            shutil.rmtree(temp_dir, ignore_errors=True)
            return None
            
        except Exception as e:
            logger.warning(f"Error getting YouTube subtitle with timestamp: {e}")
            if 'temp_dir' in locals():
                shutil.rmtree(temp_dir, ignore_errors=True)
            return None
    
    def post(self, request):
        from content.models import Lesson
        
        lesson_id = request.data.get('lesson_id')
        question = request.data.get('question', '').strip()
        timestamp = request.data.get('timestamp', 0)  # Giây
        video_title = request.data.get('video_title', '')
        clear_history = request.data.get('clear_history', False)  # Flag để clear history khi chuyển bài học
        
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
        
        # Validate lesson_id - bắt buộc phải có để tránh dùng chung cache
        if not lesson_id:
            return Response(
                {'error': 'lesson_id là bắt buộc để đảm bảo context đúng cho từng bài học'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get student grade from profile
        student_grade = 1
        if hasattr(request.user, 'profile'):
            student_grade = getattr(request.user.profile, 'grade', 1) or 1
        
        # Format timestamp thành HH:MM:SS hoặc MM:SS (hỗ trợ video dài hơn 1 giờ)
        total_seconds = int(timestamp)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            # Video dài hơn 1 giờ: format HH:MM:SS
            timestamp_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            time_label = "giờ:phút:giây"
        else:
            # Video ngắn hơn 1 giờ: format MM:SS
            timestamp_str = f"{minutes:02d}:{seconds:02d}"
            time_label = "phút:giây"
        
        # Lấy context từ lesson nếu có
        lesson_context = ""
        lesson_title = ""
        course_title = ""
        song_info = ""  # Thông tin về bài hát nếu có
        
        if lesson_id:
            try:
                lesson = Lesson.objects.select_related('module__course').get(id=lesson_id)
                lesson_title = lesson.title
                if lesson.module and lesson.module.course:
                    course = lesson.module.course
                    course_title = course.title
                    if course.description:
                        lesson_context += f"Mô tả khóa học: {course.description[:300]}\n"
                
                # Lấy nội dung bài học
                if lesson.introduction:
                    lesson_context += f"Giới thiệu bài học: {lesson.introduction[:500]}\n"
                    # Kiểm tra xem introduction có chứa thông tin về bài hát không
                    intro_lower = lesson.introduction.lower()
                    if any(keyword in intro_lower for keyword in ['bài hát', 'ca sĩ', 'nhạc sĩ', 'sáng tác', 'remix', 'cover']):
                        song_info += f"Thông tin bài hát từ giới thiệu: {lesson.introduction[:500]}\n"
                
                if lesson.text_content:
                    lesson_context += f"Nội dung: {lesson.text_content[:1000]}\n"
                    # Kiểm tra xem text_content có chứa thông tin về bài hát không
                    text_lower = lesson.text_content.lower()
                    if any(keyword in text_lower for keyword in ['bài hát', 'ca sĩ', 'nhạc sĩ', 'sáng tác', 'remix', 'cover']):
                        song_info += f"Thông tin bài hát từ nội dung: {lesson.text_content[:500]}\n"
                
                # Kiểm tra title có chứa thông tin về bài hát không
                title_lower = lesson_title.lower()
                if any(keyword in title_lower for keyword in ['remix', 'cover', 'bài hát', 'nhạc']):
                    song_info += f"Tiêu đề bài học có thể liên quan đến bài hát: {lesson_title}\n"
                
                # Ưu tiên lấy video_transcript từ field nếu có
                # Cải thiện: Extract transcript tại timestamp cụ thể nếu có thể
                if lesson.video_transcript:
                    # Thử extract transcript tại timestamp cụ thể (±90 giây, ưu tiên ±30 giây)
                    transcript_at_timestamp = self._extract_transcript_at_timestamp(
                        lesson.video_transcript, 
                        timestamp
                    )
                    if transcript_at_timestamp:
                        # Đảm bảo transcript tại timestamp này có đủ context để nhận diện bài hát
                        lesson_context += f"[NỘI DUNG VIDEO TẠI {timestamp_str} (±90 giây, ưu tiên ±30 giây) - LỜI BÀI HÁT TẠI THỜI ĐIỂM NÀY]:\n{transcript_at_timestamp}\n"
                        # Cập nhật format timestamp trong message
                        time_label = "giờ:phút:giây" if hours > 0 else "phút:giây"
                        lesson_context += f"\nLƯU Ý: Đây là nội dung TẠI {timestamp_str} ({time_label}). Nếu học sinh hỏi về bài hát tại thời điểm này, bạn PHẢI nhận biết từ lời bài hát ở trên.\n"
                        lesson_context += f"\nHƯỚNG DẪN NHẬN BIẾT BÀI HÁT:\n"
                        lesson_context += f"- Đọc kỹ từng câu trong lời bài hát ở trên\n"
                        lesson_context += f"- Tìm các câu/đoạn đặc trưng, hook, điệp khúc (thường lặp lại)\n"
                        lesson_context += f"- Tìm tên bài hát có thể xuất hiện trong lời (ví dụ: 'bài hát tên là...', 'đây là bài...')\n"
                        lesson_context += f"- So sánh với kiến thức về các bài hát Việt Nam phổ biến\n"
                        lesson_context += f"- Nếu có câu đặc trưng, dùng để nhận biết bài hát\n"
                    else:
                        # Fallback: transcript không có timestamp format SRT/VTT
                        # Cố gắng tìm nội dung gần timestamp bằng cách ước tính vị trí trong transcript
                        transcript_length = len(lesson.video_transcript)
                        
                        # Nếu transcript rất dài (>10000 ký tự) và có timestamp, cố gắng ước tính vị trí
                        if transcript_length > 10000 and timestamp > 0:
                            # Ước tính: mỗi giây video ≈ 10-20 ký tự transcript (tùy tốc độ nói)
                            # Với video dài hơn 1 giờ, cần tính chính xác hơn
                            estimated_video_duration = max(3600, timestamp + 300)  # Ước tính độ dài video
                            chars_per_second = transcript_length / estimated_video_duration
                            estimated_position = int(timestamp * chars_per_second)
                            
                            # Lấy ±2000 ký tự quanh vị trí ước tính (tương đương ±100-200 giây)
                            start_pos = max(0, estimated_position - 2000)
                            end_pos = min(transcript_length, estimated_position + 2000)
                            
                            # Lấy phần đầu (có thể chứa intro về bài hát) + phần gần timestamp
                            transcript_part1 = lesson.video_transcript[:2000]  # Phần đầu
                            transcript_part2 = lesson.video_transcript[start_pos:end_pos]  # Phần gần timestamp
                            
                            lesson_context += f"[Nội dung video - Học sinh đang xem tại {timestamp_str} ({time_label}) - LỜI BÀI HÁT (ước tính vị trí)]:\n"
                            lesson_context += f"Phần đầu (có thể chứa thông tin bài hát): {transcript_part1}\n\n"
                            lesson_context += f"Phần tại {timestamp_str} (ước tính, gần nhất với thời điểm đang xem): {transcript_part2}\n"
                        else:
                            # Video ngắn hoặc không có timestamp: lấy toàn bộ (giới hạn 8000 ký tự để có nhiều context hơn)
                            lesson_context += f"[Nội dung video - Học sinh đang xem tại {timestamp_str} ({time_label}) - LỜI BÀI HÁT]:\n{lesson.video_transcript[:8000]}\n"
                        
                        lesson_context += f"\nCẢNH BÁO: Transcript không có timestamp format SRT/VTT, nên không thể xác định CHÍNH XÁC nội dung tại {timestamp_str} ({time_label}).\n"
                        lesson_context += f"Hãy TÌM KIẾM trong transcript ở trên các từ khóa, câu hát đặc trưng để nhận biết bài hát.\n"
                        if transcript_length > 10000 and timestamp > 0:
                            lesson_context += f"Với video dài, phần 'Phần tại {timestamp_str}' là phần GẦN NHẤT với thời điểm học sinh đang xem (ước tính).\n"
                        lesson_context += f"\nHƯỚNG DẪN NHẬN BIẾT BÀI HÁT:\n"
                        lesson_context += f"- Đọc kỹ từng câu trong lời bài hát ở trên\n"
                        lesson_context += f"- Tìm các câu/đoạn đặc trưng, hook, điệp khúc (thường lặp lại)\n"
                        lesson_context += f"- Tìm tên bài hát có thể xuất hiện trong lời\n"
                        lesson_context += f"- So sánh với kiến thức về các bài hát Việt Nam phổ biến\n"
                
                # Thử lấy transcript với timestamp từ YouTube nếu có video_url
                # (Chỉ khi transcript trong DB không có timestamp format)
                if lesson.video_url and ('youtube' in lesson.video_url.lower() or 'youtu.be' in lesson.video_url.lower()):
                    # Kiểm tra xem transcript hiện tại có timestamp format không
                    # Hỗ trợ video dài hơn 1 giờ: dùng \d{1,2} cho giờ (giống pattern parse)
                    import re
                    has_timestamp_format = re.search(
                        r'\d{1,2}:\d{2}:\d{2}[,\.]\d{3}\s*-->\s*\d{1,2}:\d{2}:\d{2}[,\.]\d{3}',
                        lesson.video_transcript or ''
                    )
                    
                    if not has_timestamp_format:
                        # Transcript không có timestamp, thử lấy từ YouTube
                        try:
                            raw_subtitle = self._get_youtube_subtitle_with_timestamp(lesson.video_url)
                            if raw_subtitle:
                                # Extract transcript tại timestamp từ raw subtitle
                                transcript_at_timestamp = self._extract_transcript_at_timestamp(
                                    raw_subtitle,
                                    timestamp
                                )
                                if transcript_at_timestamp:
                                    lesson_context = f"[Nội dung video tại {timestamp_str} (±90 giây, ưu tiên ±30 giây) - từ YouTube - LỜI BÀI HÁT]:\n{transcript_at_timestamp}\n" + lesson_context
                        except Exception as e:
                            logger.warning(f"Could not get YouTube subtitle with timestamp: {e}")
                            pass
                
                # Lấy nội dung chi tiết từ content_blocks (giống phần bình luận)
                try:
                    latest_version = lesson.versions.filter(status='published').order_by('-version').first()
                    if not latest_version:
                        latest_version = lesson.versions.order_by('-version').first()
                    
                    if latest_version:
                        content_blocks = latest_version.content_blocks.order_by('position')
                        
                        for block in content_blocks[:15]:
                            payload = block.payload or {}
                            
                            if block.type == 'text':
                                text = payload.get('text', '') or payload.get('content', '')
                                if text:
                                    lesson_context += f"{text[:800]}\n"
                            
                            elif block.type == 'introduction':
                                intro_text = payload.get('text', '') or payload.get('content', '')
                                if intro_text:
                                    lesson_context += f"[Giới thiệu] {intro_text[:500]}\n"
                            
                            elif block.type == 'video':
                                transcript = payload.get('transcript', '') or payload.get('captions', '') or payload.get('tts_text', '')
                                if transcript:
                                    lesson_context += f"[Nội dung video] {transcript[:1500]}\n"
                            
                            elif block.type == 'quiz':
                                quiz_text = payload.get('question', '') or payload.get('text', '')
                                if quiz_text:
                                    lesson_context += f"[Câu hỏi] {quiz_text[:300]}\n"
                        
                        # Lấy thêm từ content JSON nếu có
                        if latest_version.content and isinstance(latest_version.content, dict):
                            json_content = latest_version.content
                            
                            # Lấy text từ các key phổ biến
                            for key in ['content', 'text', 'body', 'description', 'summary']:
                                if key in json_content and json_content[key]:
                                    val = json_content[key]
                                    if isinstance(val, str) and len(val) > 20:
                                        lesson_context += f"{val[:500]}\n"
                            
                            # Lấy từ content_blocks trong JSON
                            json_blocks = json_content.get('content_blocks', []) or json_content.get('blocks', [])
                            for jblock in json_blocks[:10]:
                                if isinstance(jblock, dict):
                                    jtext = jblock.get('text', '') or jblock.get('content', '') or jblock.get('body', '')
                                    if jtext and len(jtext) > 20:
                                        lesson_context += f"{jtext[:400]}\n"
                except Exception:
                    pass
            except Lesson.DoesNotExist:
                pass
        
        # Build context cho AI
        # Tăng độ dài context để AI có nhiều thông tin hơn để nhận biết bài hát
        context = {
            'lesson_title': lesson_title or video_title,
            'course_title': course_title,
            'video_timestamp': timestamp_str,
            'lesson_content': lesson_context[:4000] if lesson_context else None,  # Tăng từ 2000 lên 4000
        }
        
        # Build prompt đặc biệt cho câu hỏi về video với ngữ cảnh timestamp
        video_prompt = f"""Bạn là trợ lý học tập AI của SmartEdu.

Học sinh đang xem video bài học "{lesson_title or video_title}" tại thời điểm {timestamp_str} ({time_label}).

Câu hỏi của học sinh: "{question}"

{f'Khóa học: {course_title}' if course_title else ''}

{f'THÔNG TIN VỀ BÀI HÁT (nếu có):\n{song_info}' if song_info else ''}

{f'NGỮ CẢNH VIDEO (nội dung tại {timestamp_str} ±90 giây, ưu tiên ±30 giây - LỜI BÀI HÁT):\n{lesson_context[:8000]}' if lesson_context else 'Không có transcript video. Hãy trả lời dựa trên kiến thức chung về chủ đề này.'}

LƯU Ý QUAN TRỌNG:
- Học sinh đang hỏi về nội dung tại thời điểm {timestamp_str} ({time_label}) trong video
- MỖI TIMESTAMP LÀ KHÁC NHAU - nội dung tại {timestamp_str} KHÁC với nội dung tại các timestamp khác
- Nếu có transcript ở trên (được đánh dấu "LỜI BÀI HÁT TẠI THỜI ĐIỂM NÀY"), đó là LỜI BÀI HÁT TẠI {timestamp_str} - KHÔNG phải timestamp khác
- Nếu học sinh hỏi "bài hát tên gì" hoặc "bài hát này là gì", bạn CẦN PHẢI:
  * CHỈ nhận biết từ lời bài hát trong transcript TẠI {timestamp_str}
  * KHÔNG được đoán mò hoặc dùng thông tin từ timestamp khác
  * Đọc KỸ TỪNG CÂU trong lời bài hát ở trên
  * Đọc KỸ TỪNG CÂU trong lời bài hát ở trên, đặc biệt chú ý các câu lặp lại nhiều lần
  * Tìm các câu/đoạn ĐẶC TRƯNG của bài hát (hook, điệp khúc, câu nổi tiếng) - đây là chìa khóa để nhận biết
  * Tìm tên bài hát có thể xuất hiện trong lời (ví dụ: "bài hát tên là...", "đây là bài...", "bài...")
  * Tìm tên ca sĩ có thể xuất hiện trong lời
  * So sánh với kiến thức về các bài hát Việt Nam phổ biến (nhạc trẻ, nhạc vàng, remix, cover, bài hát học tiếng Anh)
  * Nếu có câu đặc trưng (ví dụ: "Một sương hai nắng dãi dầu cùng nhau", "i nhớ em trong tim anh lại càng buồn thêm"), 
    DÙNG CÂU ĐÓ để tìm kiếm trong kiến thức của bạn về các bài hát Việt Nam
  * Nếu câu đặc trưng khớp với một bài hát cụ thể mà bạn biết, HÃY TỰ TIN trả lời tên bài hát đó
  * Nếu nhận biết được (dù chỉ 70-80% chắc chắn): Trả lời RÕ RÀNG "Bài hát này là [TÊN BÀI HÁT] của [TÊN CA SĨ]"
  * Nếu có câu đặc trưng nhưng không chắc chắn tên bài hát: Trả lời "Dựa vào lời bài hát, đây có thể là bài [TÊN BÀI HÁT] của [TÊN CA SĨ]. Câu hát đặc trưng là '[CÂU HÁT]'."
  * CHỈ nói "Mình chưa nhận biết được" khi transcript hoàn toàn không có câu đặc trưng nào hoặc không đủ thông tin
- Nếu có thông tin về bài hát ở phần "THÔNG TIN VỀ BÀI HÁT", chỉ sử dụng nếu phù hợp với nội dung tại {timestamp_str}
- CẤM trả lời dựa trên timestamp khác hoặc đoán mò
- Hãy tập trung trả lời dựa trên ngữ cảnh TẠI {timestamp_str} này

YÊU CẦU TRẢ LỜI (QUAN TRỌNG - PHẢI TUÂN THỦ):
1. TRẢ LỜI TRỰC TIẾP, KHÔNG HỎI LẠI HỌC SINH
   - KHÔNG được hỏi "em đang tò mò đúng không?", "em muốn biết gì?"
   - TRẢ LỜI NGAY câu hỏi của học sinh, không vòng vo

2. Nếu học sinh hỏi về tên bài hát:
   - PHẢI CỐ GẮNG NHẬN BIẾT từ lời bài hát trong transcript TẠI {timestamp_str}
   - CHỈ sử dụng transcript được đánh dấu "TẠI {timestamp_str}" - KHÔNG dùng transcript từ timestamp khác
   - QUY TRÌNH NHẬN BIẾT (PHẢI LÀM ĐẦY ĐỦ):
     a) Đọc KỸ TỪNG CÂU trong lời bài hát ở trên, đặc biệt chú ý các câu lặp lại nhiều lần
     b) Tìm các câu/đoạn ĐẶC TRƯNG (hook, điệp khúc, câu nổi tiếng) - đây là dấu hiệu quan trọng nhất
     c) Tìm tên bài hát có thể xuất hiện trong lời (ví dụ: "bài hát tên là...", "đây là bài...", "bài...")
     d) Tìm tên ca sĩ có thể xuất hiện trong lời
     e) SO SÁNH với kiến thức về các bài hát Việt Nam phổ biến:
        - Nhạc trẻ Việt Nam: Sơn Tùng M-TP, Đen Vâu, Đức Phúc, Hương Tràm, Đông Nhi, etc.
        - Nhạc vàng: Chế Linh, Như Quỳnh, Giao Linh, etc.
        - Nhạc trữ tình: Trịnh Công Sơn, Phạm Duy, etc.
        - Remix, cover các bài hát nổi tiếng
        - Bài hát thiếu nhi, dân ca
        - Bài hát quen thuộc trong giáo dục, học tiếng Anh qua bài hát
     f) Nếu có câu đặc trưng (ví dụ: "Một sương hai nắng dãi dầu cùng nhau", "i nhớ em trong tim anh lại càng buồn thêm"), 
        DÙNG CÂU ĐÓ để tìm kiếm trong kiến thức của bạn về các bài hát Việt Nam
     g) Nếu câu đặc trưng khớp với một bài hát cụ thể mà bạn biết, HÃY TỰ TIN trả lời tên bài hát đó
   - Nếu nhận biết được (dù chỉ 70-80% chắc chắn): Trả lời NGAY "Bài hát này là [TÊN BÀI HÁT] của [TÊN CA SĨ]" (nếu biết)
   - Nếu có câu đặc trưng nhưng không chắc chắn tên bài hát: Trả lời "Dựa vào lời bài hát, đây có thể là bài [TÊN BÀI HÁT] của [TÊN CA SĨ]. Câu hát đặc trưng là '[CÂU HÁT]'."
   - CHỈ nói "Mình chưa nhận biết được" khi transcript hoàn toàn không có câu đặc trưng nào hoặc không đủ thông tin
   - KHÔNG được đoán mò hoặc trả lời dựa trên timestamp khác
   - KHÔNG được trả lời chung chung như "Bài hát mà em đang nghe ở đoạn O"
   - Nếu transcript có câu đặc trưng rõ ràng, PHẢI cố gắng nhận biết và trả lời, không được quá thận trọng

3. Nếu học sinh hỏi về nội dung khác:
   - Đọc kỹ transcript và trả lời DỰA TRỰC TIẾP vào nội dung đó
   - Trả lời CỤ THỂ, không chung chung
   - Tập trung vào nội dung tại {timestamp_str}

4. Format trả lời:
   - Trả lời ngắn gọn (2-4 câu), đi thẳng vào vấn đề
   - Ngôn ngữ đơn giản, phù hợp học sinh lớp {student_grade}
   - Thêm 1 emoji phù hợp 🌟
   - Xưng "mình", gọi học sinh là "bạn" hoặc "em"
   - BẮT ĐẦU trả lời NGAY, không có câu mở đầu dài dòng

5. CẤM:
   - Hỏi lại học sinh
   - Trả lời chung chung, không cụ thể
   - Lặp lại câu hỏi của học sinh
   - Nói vòng vo, không đi vào trọng tâm

Trả lời (bắt đầu ngay, không có câu mở đầu):"""

        # Get conversation history from cache - MỖI BÀI HỌC CÓ CACHE RIÊNG
        # Đảm bảo lesson_id luôn có để tránh dùng chung cache giữa các bài học
        if not lesson_id:
            lesson_id = 'unknown'
        
        cache_key = f"ai_video_chat:{request.user.id}:{lesson_id}"
        
        # Clear history nếu được yêu cầu (khi chuyển sang bài học mới)
        if clear_history:
            cache.delete(cache_key)
            conversation_history = []
        else:
            conversation_history = cache.get(cache_key, [])

        # Lọc conversation history - chỉ lấy những câu hỏi gần đây
        # Tránh dùng thông tin từ timestamp quá xa để tránh trả lời sai
        filtered_history = []
        for msg in conversation_history[-5:]:  # Chỉ lấy 5 tin nhắn gần nhất
            if isinstance(msg, dict) and 'role' in msg and 'content' in msg:
                filtered_history.append(msg)
        
        # Call AI Tutor
        try:
            result = ai_tutor.chat(
                user_message=video_prompt,
                context=context,
                conversation_history=filtered_history if filtered_history else [],  # Dùng filtered history
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
