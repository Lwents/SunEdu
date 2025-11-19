import api from '@/config/axios'

// Flag dùng cho code mock cũ – hiện tại luôn dùng API thật nhưng cần khai báo để TS không lỗi
const USE_MOCK = false

export type ID = string | number
export type Grade = 1 | 2 | 3 | 4 | 5
export type Subject = 'math' | 'vietnamese' | 'english' | 'science' | 'history'
export type Level = 'basic' | 'advanced'
export type CourseStatus = 'draft' | 'pending_review' | 'published' | 'rejected' | 'archived'

export interface CourseSummary {
  id: ID
  title: string
  grade: Grade
  subject: Subject
  teacherId: ID
  teacherName: string
  lessonsCount: number
  enrollments: number
  status: CourseStatus
  createdAt: string
  updatedAt: string
  thumbnail?: string
  price?: number
}

export interface Lesson {
  id: ID
  title: string
  type: 'video' | 'pdf' | 'quiz'
  durationMinutes?: number
  isPreview?: boolean
}

export interface Section {
  id: ID
  title: string
  order: number
  lessons: Lesson[]
}

export interface CourseDetail extends CourseSummary {
  description?: string
  introduction?: string
  level?: Level
  durationMinutes?: number
  sections: Section[]
  video_url?: string
  video_file?: string
  price?: number
  thumbnail?: string
}

export interface PageParams {
  q?: string
  grade?: Grade
  subject?: Subject
  teacherId?: ID
  status?: CourseStatus
  from?: string
  to?: string
  page?: number
  pageSize?: number
  sortBy?: 'createdAt' | 'updatedAt' | 'title' | 'enrollments'
  sortDir?: 'ascending' | 'descending'
}
export interface PageResult<T> { items: T[]; total: number }

export interface StudentMyCourse extends Partial<Omit<CourseSummary, 'grade' | 'subject'>> {
  grade: Grade | string | number
  subject?: string
  subjectSlug?: string
  gradeLabel?: string
  gradeNumber?: number | null
  price?: number
  progress?: number
  done?: boolean
  isEnrolled?: boolean
}

export interface StudentMyCoursesResponse {
  base: StudentMyCourse[]
  supp: StudentMyCourse[]
  all: StudentMyCourse[]
}

export interface StudentMyCoursesFilters {
  q?: string
  grade?: string
  level?: 'main' | 'supp'
}

const SUBJECTS: Subject[] = ['math', 'vietnamese', 'english', 'science', 'history']
function subjectLabel(s: Subject) {
  return s === 'math'
    ? 'Toán'
    : s === 'vietnamese'
      ? 'Tiếng Việt'
      : s === 'english'
        ? 'Tiếng Anh'
        : s === 'science'
          ? 'Khoa học'
          : 'Lịch sử'
}

// ====== SERVICE ======
export const courseService = {
  // LIST - Support both admin and student endpoints
  async list(params: PageParams, useAdminEndpoint = false): Promise<PageResult<CourseSummary>> {
    const endpoint = useAdminEndpoint ? '/admin/courses/' : '/content/courses/'
    const { data } = await api.get(endpoint, { params })
    if (Array.isArray(data)) {
      return { items: data, total: data.length }
    }
    return {
      items: data.results || data.items || [],
      total: data.count || data.total || 0,
    }
  },

  // DETAIL - Support both admin and student endpoints
  async detail(id: ID, useAdminEndpoint = false): Promise<CourseDetail> {
    const endpoint = useAdminEndpoint ? `/admin/courses/${id}/` : `/content/courses/${id}/`
    const { data } = await api.get(endpoint)
    return data
  },

  async myCourses(params: StudentMyCoursesFilters = {}): Promise<StudentMyCoursesResponse> {
    const { data } = await api.get('/student/courses/', { params })
    return {
      base: data.base || [],
      supp: data.supp || [],
      all: data.all || [],
    }
  },

  // CREATE / UPDATE
  create(payload: Partial<CourseDetail> | FormData, useAdminEndpoint = false) {
    const endpoint = useAdminEndpoint ? '/admin/courses/' : '/content/courses/'
    const config = payload instanceof FormData ? { headers: { 'Content-Type': 'multipart/form-data' } } : {}
    return api.post(endpoint, payload, config).then((res) => res.data)
  },
  update(id: ID, payload: Partial<CourseDetail> | FormData, useAdminEndpoint = false) {
    const endpoint = useAdminEndpoint ? `/admin/courses/${id}/` : `/content/courses/${id}/`
    return api.patch(endpoint, payload)
  },
  
  // DELETE
  async delete(id: ID, useAdminEndpoint = false): Promise<void> {
    const endpoint = useAdminEndpoint ? `/admin/courses/${id}/` : `/content/courses/${id}/`
    await api.delete(endpoint)
  },
  
  // ENROLL (student only)
  async enroll(courseId: ID): Promise<{ success: boolean }> {
    const { data } = await api.post(`/content/courses/${courseId}/enroll/`)
    return data
  },
  async unenroll(courseId: ID): Promise<{ success: boolean }> {
    const { data } = await api.delete(`/content/courses/${courseId}/enroll/`)
    return data
  },

  // STATUS / ACTIONS (Admin)
  approve(id: ID) { return api.post(`/admin/courses/${id}/approve/`) },
  reject(id: ID, reason?: string) { return api.post(`/admin/courses/${id}/reject/`, { reason }) },
  publish(id: ID) { return api.post(`/admin/courses/${id}/publish/`) },
  unpublish(id: ID) { return api.post(`/admin/courses/${id}/unpublish/`) },
  archive(id: ID) { return api.post(`/admin/courses/${id}/archive/`) },
  restore(id: ID) { return api.post(`/admin/courses/${id}/restore/`) },
  
  // STATUS / ACTIONS (Teacher - use content endpoint)
  async publishCourse(id: ID): Promise<any> {
    const { data } = await api.post(`/content/courses/${id}/publish/`, { published: true })
    return data
  },
  async unpublishCourse(id: ID): Promise<any> {
    const { data } = await api.patch(`/content/courses/${id}/`, { published: false })
    return data
  },
  async archiveCourse(id: ID): Promise<any> {
    const { data } = await api.patch(`/content/courses/${id}/`, { published: false })
    return data
  },
  async restoreCourse(id: ID): Promise<any> {
    const { data } = await api.post(`/content/courses/${id}/publish/`, { published: true })
    return data
  },

  // BULK (tuỳ chọn dùng ở trang duyệt)
  bulkApprove(ids: ID[]) { return api.post('/admin/courses/bulk/', { action: 'approve', ids }) },
  bulkReject(ids: ID[], reason?: string) { return api.post('/admin/courses/bulk/', { action: 'reject', ids, reason }) },
  bulkPublish(ids: ID[]) { return api.post('/admin/courses/bulk/', { action: 'publish', ids }) },
  bulkArchive(ids: ID[]) { return api.post('/admin/courses/bulk/', { action: 'archive', ids }) },

  // FILTER OPTIONS
  async listTeachers(): Promise<{ id: ID; name: string }[]> {
    const { data } = await api.get('/account/admin/users/', { params: { role: 'instructor', pageSize: 50 } })
    const users = data.results || data || []
    return users.map((u: any) => ({ id: u.id, name: u.email || u.username }))
  },
  subjects(): { label: string; value: Subject }[] {
    return SUBJECTS.map((s) => ({ value: s, label: subjectLabel(s) }))
  },
}
