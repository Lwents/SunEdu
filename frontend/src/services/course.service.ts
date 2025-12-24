import api from '@/config/axios'

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

function normalizeCourseSummary(row: any): CourseSummary {
  const rawThumbnail =
    row.thumbnail ??
    row.thumbnail_url ??
    row.thumbnailUrl ??
    row.thumbnail?.url ??
    row.thumbnail?.path ??
    row.thumbnail_path
  const thumbnail =
    typeof rawThumbnail === 'string'
      ? rawThumbnail
      : rawThumbnail?.url ?? rawThumbnail?.path

  return {
    id: row.id,
    title: row.title,
    grade: (row.grade as Grade) ?? (row.grade_label as any) ?? row.gradeNumber ?? row.gradeNumber,
    subject: (row.subject as Subject) ?? row.subjectSlug ?? row.subject_name ?? row.subject_label,
    teacherId: row.teacherId ?? row.teacher_id ?? row.teacher?.id ?? null,
    teacherName: row.teacherName ?? row.teacher_name ?? row.teacher?.name ?? row.teacher?.full_name ?? '',
    lessonsCount: row.lessonsCount ?? row.lessons_count ?? 0,
    enrollments: row.enrollments ?? row.enrollments_count ?? 0,
    status: (row.status as CourseStatus) ?? 'draft',
    createdAt: row.createdAt || row.created_at || row.created_on || '',
    updatedAt: row.updatedAt || row.updated_at || row.updated_on || '',
    thumbnail,
    price: row.price,
  }
}

export interface StudentMyCoursesFilters {
  q?: string
  grade?: string
  level?: 'main' | 'supp'
}

const USE_MOCK = false
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

function buildMockList(params: PageParams = {}): PageResult<CourseSummary> {
  const size = params.pageSize ?? 20
  const page = params.page ?? 1
  const total = 173

  const items: CourseSummary[] = Array.from({ length: size }).map((_, i) => {
    const id = (page - 1) * size + i + 1
    const grade = ((id % 5) + 1) as Grade
    const subject = SUBJECTS[id % SUBJECTS.length]
    const teacherId = (id % 15) + 1
    const isPublished = id % 2 === 0 || grade <= 2
    const status: CourseStatus = isPublished ? 'published' : 'draft'

    return {
      id,
      title: `Khoá học #${id} - ${subjectLabel(subject)} lớp ${grade}`,
      grade,
      subject,
      teacherId,
      teacherName: `GV ${teacherId}`,
      lessonsCount: (id % 10) + 12,
      enrollments: (id * 7) % 320,
      status,
      createdAt: new Date(Date.now() - id * 864e5).toISOString(),
      updatedAt: new Date(Date.now() - id * 36e5).toISOString(),
      thumbnail: `https://picsum.photos/seed/course-${id}/320/180`,
    }
  })

  let list = items
  if (params.q) {
    const q = params.q.toLowerCase()
    list = list.filter(
      (c) =>
        c.title.toLowerCase().includes(q) ||
        String(c.id).includes(q) ||
        c.teacherName.toLowerCase().includes(q),
    )
  }
  if (params.grade) list = list.filter((c) => c.grade === params.grade)
  if (params.subject) list = list.filter((c) => c.subject === params.subject)
  if (params.teacherId) list = list.filter((c) => String(c.teacherId) === String(params.teacherId))
  if (params.status) list = list.filter((c) => c.status === params.status)

  return { items: list, total }
}

function buildMockDetail(id: ID): CourseDetail {
  const numericId = Number(id) || 1
  const grade = ((numericId % 5) + 1) as Grade
  const subject = SUBJECTS[numericId % SUBJECTS.length]
  const sections: Section[] = Array.from({ length: 4 }).map((_, sIdx) => ({
    id: `S${numericId}-${sIdx + 1}`,
    title: `Chương ${sIdx + 1}`,
    order: sIdx + 1,
    lessons: Array.from({ length: 4 + (sIdx % 2) }).map((__, lIdx) => ({
      id: `L${numericId}-${sIdx + 1}-${lIdx + 1}`,
      title: `Bài ${sIdx + 1}.${lIdx + 1} – ${subjectLabel(subject)}`,
      type: (['video', 'pdf', 'quiz'] as Lesson['type'][])[(lIdx + sIdx) % 3],
      durationMinutes: 8 + ((lIdx + sIdx) % 5) * 5,
      isPreview: lIdx === 0,
    })),
  }))

  const isPublished = numericId % 2 === 0 || grade <= 2
  const status: CourseStatus = isPublished ? 'published' : 'draft'

  return {
    id: numericId,
    title: `Khoá học #${numericId} - ${subjectLabel(subject)} lớp ${grade}`,
    grade,
    subject,
    teacherId: 3,
    teacherName: 'GV 3',
    lessonsCount: sections.reduce((a, s) => a + s.lessons.length, 0),
    enrollments: (numericId * 7) % 320,
    status,
    createdAt: new Date(Date.now() - numericId * 864e5).toISOString(),
    updatedAt: new Date().toISOString(),
    thumbnail: `https://picsum.photos/seed/course-${numericId}/800/360`,
    description:
      'Mô tả ngắn gọn về khoá học. Nội dung thiết kế theo từng chương/bài, có video, tài liệu và quiz.',
    level: numericId % 2 ? 'basic' : 'advanced',
    durationMinutes: sections.reduce(
      (a, s) => a + s.lessons.reduce((b, l) => b + (l.durationMinutes || 0), 0),
      0,
    ),
    sections,
  }
}

// ====== SERVICE ======
export const courseService = {
  // LIST - GET /content/courses/ (teacher/student) hoặc /admin/courses/ (admin) kèm bộ lọc
  async list(params: PageParams, useAdminEndpoint = false): Promise<PageResult<CourseSummary>> {
    if (USE_MOCK) return buildMockList(params)
    const endpoint = useAdminEndpoint ? '/admin/courses/' : '/content/courses/'
    const { data } = await api.get(endpoint, { params })
    if (Array.isArray(data)) {
      return { items: data.map(normalizeCourseSummary), total: data.length }
    }
    return {
      items: (data.results || data.items || []).map(normalizeCourseSummary),
      total: data.count || data.total || 0,
    }
  },

  // DETAIL - GET /content/courses/:id/ hoặc /admin/courses/:id/
  async detail(id: ID, useAdminEndpoint = false): Promise<CourseDetail> {
    if (USE_MOCK) return buildMockDetail(id)
    const endpoint = useAdminEndpoint ? `/admin/courses/${id}/` : `/content/courses/${id}/`
    const { data } = await api.get(endpoint)
    return data
  },

  // STUDENT DETAIL - GET /student/courses/:id/ bao gồm tiến độ cá nhân
  async studentDetail(id: ID): Promise<CourseDetail> {
    if (USE_MOCK) return buildMockDetail(id)
    const { data } = await api.get(`/student/courses/${id}/`)
    return data
  },

  // GET /student/courses/ - danh sách khóa học của học sinh (cơ bản + bổ trợ)
  async myCourses(params: StudentMyCoursesFilters = {}): Promise<StudentMyCoursesResponse> {
    if (USE_MOCK) {
      return { base: [], supp: [], all: [] }
    }
    const { data } = await api.get('/student/courses/', { params })
    return {
      base: data.base || [],
      supp: data.supp || [],
      all: data.all || [],
    }
  },

  // CREATE / UPDATE
  // POST /content|admin/courses/ - tạo khoá học (hỗ trợ FormData để upload)
  create(payload: Partial<CourseDetail> | FormData, useAdminEndpoint = false) {
    if (USE_MOCK) return Promise.resolve({ ok: true, id: Date.now() })
    const endpoint = useAdminEndpoint ? '/admin/courses/' : '/content/courses/'
    const config = payload instanceof FormData ? { headers: { 'Content-Type': 'multipart/form-data' } } : {}
    return api.post(endpoint, payload, config).then((res) => res.data)
  },
  // PATCH /content|admin/courses/:id/ - chỉnh sửa khoá học
  update(id: ID, payload: Partial<CourseDetail> | FormData, useAdminEndpoint = false) {
    if (USE_MOCK) return Promise.resolve({ ok: true })
    const endpoint = useAdminEndpoint ? `/admin/courses/${id}/` : `/content/courses/${id}/`
    return api.patch(endpoint, payload)
  },

  // DELETE
  // DELETE /content|admin/courses/:id/ - xoá khoá học
  async delete(id: ID, useAdminEndpoint = false): Promise<void> {
    if (USE_MOCK) return
    const endpoint = useAdminEndpoint ? `/admin/courses/${id}/` : `/content/courses/${id}/`
    await api.delete(endpoint)
  },

  // ENROLL (student only)
  // POST /content/courses/:courseId/enroll/ - đăng ký khoá học
  async enroll(courseId: ID): Promise<{ success: boolean }> {
    if (USE_MOCK) return Promise.resolve({ success: true })
    const { data } = await api.post(`/content/courses/${courseId}/enroll/`)
    return data
  },
  // DELETE /content/courses/:courseId/enroll/ - huỷ đăng ký
  async unenroll(courseId: ID): Promise<{ success: boolean }> {
    if (USE_MOCK) return Promise.resolve({ success: true })
    const { data } = await api.delete(`/content/courses/${courseId}/enroll/`)
    return data
  },

  // STATUS / ACTIONS (Admin)
  // Các action duyệt/publish/khôi phục cho admin
  approve(id: ID) { return USE_MOCK ? Promise.resolve({ ok: true }) : api.post(`/admin/courses/${id}/approve/`) },
  reject(id: ID, reason?: string) {
    return USE_MOCK ? Promise.resolve({ ok: true }) : api.post(`/admin/courses/${id}/reject/`, { reason })
  },
  publish(id: ID) { return USE_MOCK ? Promise.resolve({ ok: true }) : api.post(`/admin/courses/${id}/publish/`) },
  unpublish(id: ID) { return USE_MOCK ? Promise.resolve({ ok: true }) : api.post(`/admin/courses/${id}/unpublish/`) },
  archive(id: ID) { return USE_MOCK ? Promise.resolve({ ok: true }) : api.post(`/admin/courses/${id}/archive/`) },
  restore(id: ID) { return USE_MOCK ? Promise.resolve({ ok: true }) : api.post(`/admin/courses/${id}/restore/`) },

  // STATUS / ACTIONS (Teacher - use content endpoint)
  // Giáo viên tự publish/unpublish/khôi phục qua content endpoint
  async publishCourse(id: ID): Promise<any> {
    if (USE_MOCK) return Promise.resolve({ ok: true })
    const { data } = await api.post(`/content/courses/${id}/publish/`, { published: true })
    return data
  },
  async unpublishCourse(id: ID): Promise<any> {
    if (USE_MOCK) return Promise.resolve({ ok: true })
    const { data } = await api.patch(`/content/courses/${id}/`, { published: false })
    return data
  },
  async archiveCourse(id: ID): Promise<any> {
    if (USE_MOCK) return Promise.resolve({ ok: true })
    const { data } = await api.patch(`/content/courses/${id}/`, { published: false })
    return data
  },
  async restoreCourse(id: ID): Promise<any> {
    if (USE_MOCK) return Promise.resolve({ ok: true })
    const { data } = await api.post(`/content/courses/${id}/publish/`, { published: true })
    return data
  },

  // BULK (tuỳ chọn dùng ở trang duyệt)
  // POST /admin/courses/bulk/ - xử lý nhiều khoá học cùng lúc
  bulkApprove(ids: ID[]) {
    return USE_MOCK ? Promise.resolve({ ok: true }) : api.post('/admin/courses/bulk/', { action: 'approve', ids })
  },
  bulkReject(ids: ID[], reason?: string) {
    return USE_MOCK ? Promise.resolve({ ok: true }) : api.post('/admin/courses/bulk/', { action: 'reject', ids, reason })
  },
  bulkPublish(ids: ID[]) {
    return USE_MOCK ? Promise.resolve({ ok: true }) : api.post('/admin/courses/bulk/', { action: 'publish', ids })
  },
  bulkArchive(ids: ID[]) {
    return USE_MOCK ? Promise.resolve({ ok: true }) : api.post('/admin/courses/bulk/', { action: 'archive', ids })
  },

  // FILTER OPTIONS
  // GET /account/admin/users/?role=instructor - lấy danh sách giáo viên cho bộ lọc
  async listTeachers(): Promise<{ id: ID; name: string }[]> {
    if (USE_MOCK) {
      return Array.from({ length: 15 }).map((_, i) => ({ id: i + 1, name: `GV ${i + 1}` }))
    }
    const { data } = await api.get('/account/admin/users/', { params: { role: 'instructor', pageSize: 50 } })
    const users = data.results || data || []
    return users.map((u: any) => ({ id: u.id, name: u.email || u.username }))
  },

  // Hardcoded subjects fallback
  subjects(): { label: string; value: Subject }[] {
    return SUBJECTS.map((s) => ({ value: s, label: subjectLabel(s) }))
  },

  // GET /content/subjects/ - lấy danh sách môn học từ API
  async listSubjects(): Promise<{ label: string; value: string }[]> {
    if (USE_MOCK) {
      return SUBJECTS.map((s) => ({ value: s, label: subjectLabel(s) }))
    }
    try {
      const { data } = await api.get('/content/subjects/')
      const subjects = data.results || data || []
      return subjects.map((s: any) => ({
        value: s.slug || s.id,
        label: s.title || s.name || s.slug
      }))
    } catch {
      // Fallback to hardcoded if API fails
      return SUBJECTS.map((s) => ({ value: s, label: subjectLabel(s) }))
    }
  },
}
