import api from '@/config/axios'

export interface TeacherStudent {
  id: string
  name: string
  username: string
  email: string
  avatar?: string
  courses: {
    id: string
    title: string
    enrolledAt: string
    progress: number
    completedLessons: number
    totalLessons: number
    status: 'completed' | 'in_progress'
  }[]
}

export interface TeacherStudentsParams {
  q?: string
  courseId?: string
  page?: number
  pageSize?: number
}

export interface TeacherStudentsResponse {
  items: TeacherStudent[]
  total: number
  page: number
  pageSize: number
}

export interface SendFeedbackInput {
  studentId: string | number
  courseId?: string | number
  message: string
  rating: number
}

export interface FeedbackResponse {
  id: string
  teacher: string
  student: string
  course: string | null
  message: string
  rating: number
  created_at: string
  updated_at: string
  is_read: boolean
}

class TeacherService {
  async getStudents(params?: TeacherStudentsParams): Promise<TeacherStudentsResponse> {
    const { data } = await api.get('/teacher/students/', { params })
    return data
  }

  async sendFeedback(input: SendFeedbackInput): Promise<FeedbackResponse> {
    const { data } = await api.post('/teacher/students/feedback/', input)
    return data
  }

  async getFeedbacks(params?: { studentId?: string; courseId?: string }): Promise<{ items: FeedbackResponse[] }> {
    const { data } = await api.get('/teacher/students/feedback/list/', { params })
    return data
  }
}

export const teacherService = new TeacherService()
