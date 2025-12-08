/**
 * AI Learning Service
 * - Phân tích tiến độ học tập
 * - Gợi ý bài học thông minh
 * - Đánh giá đầu vào
 * - Phát hiện điểm yếu
 */
import api from '@/config/axios'

export interface AISuggestion {
  type: 'continue' | 'review' | 'exercise'
  priority: 'high' | 'medium' | 'low'
  icon: string
  title: string
  subtitle: string
  reason: string
  lesson_id?: string
  course_id?: string
  exercise_id?: string
  estimated_time: number
}

export interface AIWeakness {
  topic: string
  course: string
  score: number
  suggestion: string
  lesson_id: string
  course_id: string
}

export interface AIAchievement {
  id: string
  name: string
  icon: string
  unlocked: boolean
}

export interface DailyGoal {
  target: number
  completed: number
  streak: number
}

export interface CourseProgress {
  course_id: string
  course_title: string
  total: number
  completed: number
  progress: number
}

export interface LearningAnalysis {
  total_lessons: number
  completed_lessons: number
  total_exercises: number
  completed_exercises: number
  overall_progress: number
  avg_score: number
  course_progress: CourseProgress[]
}

export interface AILearningData {
  has_courses: boolean
  message?: string
  analysis?: LearningAnalysis
  suggestions: AISuggestion[]
  weaknesses: AIWeakness[]
  achievements: AIAchievement[]
  daily_goal: DailyGoal
  ai_message?: string
}

export interface AssessmentQuestion {
  id: number
  type: string
  text: string
  choices: string[]
  module: string
  lesson_id: string
}

export interface AssessmentData {
  course_id: string
  course_title: string
  questions: AssessmentQuestion[]
  total_questions: number
  estimated_time: number
}

export interface AssessmentAnswer {
  question_id: number
  choice: number
  lesson_id: string
}

export interface SuggestedLesson {
  id: string
  title: string
  module: string
}

export interface AssessmentResult {
  level: 'beginner' | 'elementary' | 'intermediate' | 'advanced'
  level_text: string
  score: number
  max_score: number
  recommendation: string
  start_from_lesson: number
  suggested_lessons: SuggestedLesson[]
  personalized_path: {
    skip_intro: boolean
    focus_practice: boolean
    challenge_mode: boolean
  }
}

export const aiLearningService = {
  /**
   * Lấy phân tích tiến độ học tập và gợi ý AI
   */
  async getAnalysis(): Promise<AILearningData> {
    const response = await api.get('/student/ai/learning-analyzer/')
    return response.data
  },

  /**
   * Lấy câu hỏi đánh giá đầu vào cho khóa học
   */
  async getAssessment(courseId: string): Promise<AssessmentData> {
    const response = await api.post('/student/ai/assessment/', { course_id: courseId })
    return response.data
  },

  /**
   * Gửi kết quả đánh giá và nhận lộ trình cá nhân hóa
   */
  async submitAssessment(courseId: string, answers: AssessmentAnswer[]): Promise<AssessmentResult> {
    const response = await api.post('/student/ai/assessment/result/', {
      course_id: courseId,
      answers,
    })
    return response.data
  },
}

export default aiLearningService
