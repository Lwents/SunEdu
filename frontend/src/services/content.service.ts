// src/services/content.service.ts
import http from '@/config/axios'

export type ID = string | number

export interface Module {
  id: ID
  title: string
  position: number
  course: ID
}

export interface Lesson {
  id: ID
  title: string
  position: number
  module: ID
  content_type: 'lesson' | 'exploration' | 'exercise'
  published: boolean
  video_url?: string
  video_file?: string
}

export interface CreateModuleInput {
  title: string
  course?: ID
  position?: number
}

export interface CreateLessonInput {
  title: string
  module: ID
  position?: number
  content_type?: 'lesson' | 'exploration' | 'exercise'
  video_url?: string
}

export const contentService = {
  // ====== MODULES (Chương) ======
  async listModules(courseId: ID): Promise<Module[]> {
    const { data } = await http.get(`/content/courses/${courseId}/modules/`)
    return Array.isArray(data) ? data : data.results || []
  },

  async createModule(courseId: ID, input: CreateModuleInput): Promise<Module> {
    const { data } = await http.post(`/content/courses/${courseId}/modules/`, {
      title: input.title,
      position: input.position
    })
    return data
  },

  async updateModule(moduleId: ID, input: Partial<CreateModuleInput>): Promise<Module> {
    const { data } = await http.patch(`/content/modules/${moduleId}/`, input)
    return data
  },

  async deleteModule(moduleId: ID): Promise<void> {
    await http.delete(`/content/modules/${moduleId}/`)
  },

  async reorderModules(courseId: ID, orderMap: Record<string, number>): Promise<void> {
    await http.post(`/content/courses/${courseId}/modules/reorder/`, { order_map: orderMap })
  },

  // ====== LESSONS (Bài học) ======
  async listLessons(moduleId: ID): Promise<Lesson[]> {
    const { data } = await http.get(`/content/modules/${moduleId}/lessons/`)
    return Array.isArray(data) ? data : data.results || []
  },

  async createLesson(moduleId: ID, input: CreateLessonInput | FormData): Promise<Lesson> {
    // If FormData, send directly (for file uploads)
    if (input instanceof FormData) {
      const { data } = await http.post(`/content/modules/${moduleId}/lessons/`, input)
      return data
    }
    // Otherwise, send as JSON
    const payload: Record<string, any> = {
      title: input.title,
      position: input.position,
      content_type: input.content_type || 'lesson'
    }
    if (input.video_url) payload.video_url = input.video_url
    const { data } = await http.post(`/content/modules/${moduleId}/lessons/`, payload)
    return data
  },

  async updateLesson(lessonId: ID, input: Partial<CreateLessonInput> | FormData): Promise<Lesson> {
    // Nếu là FormData (có video_file), gửi trực tiếp
    if (input instanceof FormData) {
      const { data } = await http.patch(`/content/lessons/${lessonId}/`, input, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      return data
    }
    // Nếu là object thông thường
    const payload: Record<string, any> = { ...input }
    if (input.video_url !== undefined) {
      payload.video_url = input.video_url || ''
    }
    const { data } = await http.patch(`/content/lessons/${lessonId}/`, payload)
    return data
  },

  async deleteLesson(lessonId: ID): Promise<void> {
    await http.delete(`/content/lessons/${lessonId}/`)
  },

  async reorderLessons(moduleId: ID, orderMap: Record<string, number>): Promise<void> {
    await http.post(`/content/modules/${moduleId}/lessons/reorder/`, { order_map: orderMap })
  },

  // ====== LESSON PROGRESS ======
  async getLessonProgress(lessonId: ID): Promise<any> {
    const { data } = await http.get(`/content/lessons/${lessonId}/progress/`)
    return data
  },

  async updateLessonProgress(lessonId: ID, progress: {
    video_watched?: boolean
    exercise_completed?: boolean
    exercise_score?: number
  }): Promise<any> {
    const { data } = await http.post(`/content/lessons/${lessonId}/progress/`, progress)
    return data
  },

  async checkLessonUnlock(lessonId: ID): Promise<{ can_unlock: boolean; reason?: string }> {
    const { data } = await http.get(`/content/lessons/${lessonId}/unlock-check/`)
    return data
  },

  // ====== CONTENT LIBRARY ======
  async listContentLibrary(params?: {
    q?: string
    gradeBand?: string
    type?: string
    page?: number
    pageSize?: number
  }): Promise<{ items: any[]; total: number; page: number; pageSize: number; totalPages: number }> {
    const { data } = await http.get('/content/content-library/', { params })
    return data
  },

  async createContentLibrary(input: {
    title: string
    subject: string
    type: string
    grade_band: string
    meta?: any
  }): Promise<any> {
    const { data } = await http.post('/content/content-library/', input)
    return data
  },

  async updateContentLibrary(id: ID, input: Partial<{
    title: string
    subject: string
    type: string
    grade_band: string
    meta?: any
  }>): Promise<any> {
    const { data } = await http.patch(`/content/content-library/${id}/`, input)
    return data
  },

  async deleteContentLibrary(id: ID): Promise<void> {
    await http.delete(`/content/content-library/${id}/`)
  }
}
