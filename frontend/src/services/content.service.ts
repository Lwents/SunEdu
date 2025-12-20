// src/services/content.service.ts
import http from '@/config/axios'

export type ID = string | number

function sortByPosition<T extends { position?: number; title?: string }>(items: T[]): T[] {
  return [...items].sort((a, b) => {
    const posA = typeof a.position === 'number' ? a.position : 0
    const posB = typeof b.position === 'number' ? b.position : 0
    if (posA !== posB) return posA - posB
    if (a.title && b.title) {
      return String(a.title).localeCompare(String(b.title))
    }
    return 0
  })
}

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
  content_type: 'lesson' | 'exploration' | 'exercise' | 'video' | 'pdf' | 'text' | 'document'
  published: boolean
  video_url?: string
  video_file?: string
  document_file?: string
  text_content?: string
  introduction?: string
  requires_exercise_completion?: boolean
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
  content_type?: 'lesson' | 'exploration' | 'exercise' | 'video' | 'pdf' | 'text' | 'document'
  video_url?: string
  introduction?: string
  text_content?: string
  requires_exercise_completion?: boolean
}

export const contentService = {
  // ====== MODULES (Chương) ======
  // GET /content/courses/:courseId/modules/ - lấy danh sách chương và sắp xếp client-side
  async listModules(courseId: ID): Promise<Module[]> {
    const { data } = await http.get(`/content/courses/${courseId}/modules/`)
    const list = Array.isArray(data) ? data : data.results || []
    return sortByPosition(list)
  },

  // POST /content/courses/:courseId/modules/ - tạo chương mới
  async createModule(courseId: ID, input: CreateModuleInput): Promise<Module> {
    const payload: Record<string, any> = {
      title: input.title,
      course: input.course ?? courseId,
    }
    if (typeof input.position === 'number') {
      payload.position = input.position
    }
    const { data } = await http.post(`/content/courses/${courseId}/modules/`, payload)
    return data
  },

  // PATCH /content/modules/:moduleId/ - chỉnh sửa chương
  async updateModule(moduleId: ID, input: Partial<CreateModuleInput>): Promise<Module> {
    const { data } = await http.patch(`/content/modules/${moduleId}/`, input)
    return data
  },

  // DELETE /content/modules/:moduleId/ - xoá chương
  async deleteModule(moduleId: ID): Promise<void> {
    await http.delete(`/content/modules/${moduleId}/`)
  },

  // POST /content/courses/:courseId/modules/reorder/ - cập nhật vị trí chương
  async reorderModules(courseId: ID, orderMap: Record<string, number>): Promise<void> {
    await http.post(`/content/courses/${courseId}/modules/reorder/`, { order_map: orderMap })
  },

  // ====== LESSONS (Bài học) ======
  // GET /content/modules/:moduleId/lessons/ - lấy danh sách bài học đã sắp xếp
  async listLessons(moduleId: ID): Promise<Lesson[]> {
    const { data } = await http.get(`/content/modules/${moduleId}/lessons/`)
    const list = Array.isArray(data) ? data : data.results || []
    return sortByPosition(list)
  },

  // POST /content/modules/:moduleId/lessons/ - tạo bài học (hỗ trợ FormData để upload video)
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
    if (input.introduction !== undefined) payload.introduction = input.introduction
    if (input.text_content !== undefined) payload.text_content = input.text_content
    if (input.requires_exercise_completion !== undefined) {
      payload.requires_exercise_completion = input.requires_exercise_completion
    }
    const { data } = await http.post(`/content/modules/${moduleId}/lessons/`, payload)
    return data
  },

  // PATCH /content/lessons/:lessonId/ - chỉnh sửa bài học (JSON hoặc FormData)
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

  // DELETE /content/lessons/:lessonId/ - xoá bài học
  async deleteLesson(lessonId: ID): Promise<void> {
    await http.delete(`/content/lessons/${lessonId}/`)
  },

  // POST /content/modules/:moduleId/lessons/reorder/ - sắp xếp lại thứ tự bài học
  async reorderLessons(moduleId: ID, orderMap: Record<string, number>): Promise<void> {
    await http.post(`/content/modules/${moduleId}/lessons/reorder/`, { order_map: orderMap })
  },

  // ====== LESSON PROGRESS ======
  // GET /content/lessons/:lessonId/progress/ - lấy trạng thái hoàn thành của học sinh
  async getLessonProgress(lessonId: ID): Promise<any> {
    const { data } = await http.get(`/content/lessons/${lessonId}/progress/`)
    return data
  },

  // POST /content/lessons/:lessonId/progress/ - cập nhật tiến độ (xem video, làm bài)
  async updateLessonProgress(lessonId: ID, progress: {
    video_watched?: boolean
    exercise_completed?: boolean
    exercise_score?: number
    completed?: boolean
  }): Promise<any> {
    const { data } = await http.post(`/content/lessons/${lessonId}/progress/`, progress)
    return data
  },

  // GET /content/lessons/:lessonId/unlock-check/ - kiểm tra quyền mở bài học
  async checkLessonUnlock(lessonId: ID): Promise<{ can_unlock: boolean; reason?: string }> {
    const { data } = await http.get(`/content/lessons/${lessonId}/unlock-check/`)
    return data
  },

  // ====== CONTENT LIBRARY ======
  // GET /content/content-library/ - tra cứu thư viện nội dung (search + phân trang)
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

  // POST /content/content-library/ - thêm tài nguyên thư viện
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

  // PATCH /content/content-library/:id/ - cập nhật tài nguyên thư viện
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

  // DELETE /content/content-library/:id/ - xoá tài nguyên thư viện
  async deleteContentLibrary(id: ID): Promise<void> {
    await http.delete(`/content/content-library/${id}/`)
  }
}
