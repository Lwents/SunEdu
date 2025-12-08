/**
 * AI Tutor Service
 * - Chat với AI trợ lý học tập
 * - Lấy gợi ý khi làm bài
 * - Giải thích khái niệm
 * - Lấy lời động viên
 */
import api from '@/config/axios'

export interface ChatContext {
  lesson_id?: string
  lesson_title?: string
  subject?: string
  current_question?: string
  course_id?: string
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}

export interface ChatResponse {
  success: boolean
  message: string
  conversation_id: string
  error?: string
}

export interface HintRequest {
  question_text: string
  question_type?: 'multiple_choice' | 'fill_blank' | 'true_false' | 'short_answer'
  choices?: string[]
  student_answer?: string
  correct_answer?: string
  hint_level?: number
  question_id?: string | number
}

export interface HintResponse {
  success: boolean
  hint: string
  hint_level: number
  can_get_more_hints: boolean
  hints_remaining: number
  error?: string
}

export interface ExplainRequest {
  concept: string
  subject?: string
  use_examples?: boolean
}

export interface ExplainResponse {
  success: boolean
  explanation: string
  concept: string
  subject: string
  error?: string
}

export interface EncourageResponse {
  message: string
  situation: string
}

export const aiTutorService = {
  /**
   * Chat với AI Tutor
   */
  async chat(
    message: string,
    context?: ChatContext,
    conversationId?: string
  ): Promise<ChatResponse> {
    const response = await api.post('/student/ai/tutor/chat/', {
      message,
      context,
      conversation_id: conversationId,
    })
    return response.data
  },

  /**
   * Lấy gợi ý cho câu hỏi
   */
  async getHint(request: HintRequest): Promise<HintResponse> {
    const response = await api.post('/student/ai/tutor/hint/', request)
    return response.data
  },

  /**
   * Giải thích khái niệm
   */
  async explain(request: ExplainRequest): Promise<ExplainResponse> {
    const response = await api.post('/student/ai/tutor/explain/', request)
    return response.data
  },

  /**
   * Lấy lời động viên
   */
  async encourage(
    situation: 'correct' | 'incorrect' | 'streak' | 'completed' | 'struggling',
    score?: number
  ): Promise<EncourageResponse> {
    const response = await api.post('/student/ai/tutor/encourage/', {
      situation,
      score,
    })
    return response.data
  },

  /**
   * Xóa lịch sử chat
   */
  async clearHistory(conversationId?: string): Promise<{ success: boolean }> {
    const response = await api.delete('/student/ai/tutor/history/', {
      params: { conversation_id: conversationId },
    })
    return response.data
  },

  /**
   * Phân tích điểm yếu của học sinh
   */
  async analyzeWeaknesses(): Promise<AnalyzeResponse> {
    const response = await api.get('/student/ai/tutor/analyze/')
    return response.data
  },

  /**
   * Tạo bài luyện tập dựa trên điểm yếu
   */
  async generatePractice(
    weaknesses?: Weakness[],
    numExercises?: number
  ): Promise<PracticeResponse> {
    const response = await api.post('/student/ai/tutor/practice/', {
      weaknesses,
      num_exercises: numExercises || 5,
    })
    return response.data
  },

  /**
   * Lấy báo cáo học tập hàng ngày
   */
  async getDailyReport(): Promise<DailyReportResponse> {
    const response = await api.get('/student/ai/tutor/daily-report/')
    return response.data
  },
}

// Additional types
export interface Weakness {
  topic: string
  subject: string
  severity?: 'high' | 'medium' | 'low'
  suggestion?: string
}

export interface AnalyzeResponse {
  success: boolean
  analysis: {
    weaknesses: Weakness[]
    strengths: string[]
    overall_message: string
    encouragement: string
  }
  performance_summary: {
    subjects: Array<{ name: string; score: number; wrong_topics: string[] }>
    recent_exercises: Array<{ topic: string; correct: boolean; score: number }>
    total_completed: number
  }
}

export interface PracticeExercise {
  question: string
  topic: string
  choices: string[]
  correct_answer: string
  explanation: string
  difficulty: 'easy' | 'medium' | 'hard'
}

export interface PracticeResponse {
  success: boolean
  exercises: PracticeExercise[]
  topics: string[]
  error?: string
}

export interface DailyReportResponse {
  success: boolean
  report: {
    title: string
    summary: string
    details: string
    suggestions: string[]
    student_message: string
  }
  performance: {
    completed: number
    avg_score: number
    time_spent: number
  }
  date: string
}

export default aiTutorService
