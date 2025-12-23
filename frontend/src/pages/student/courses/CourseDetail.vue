<template>
  <div class="page-wrapper" :class="isDark ? 'dark-mode' : 'light-mode'">
    <!-- Background Elements -->
    <div v-if="isDark" class="bg-elements">
      <div class="glow glow-1"></div>
      <div class="glow glow-2"></div>
    </div>

    <div class="page-content">
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Đang tải...</p>
      </div>

      <div v-else-if="course" class="space-y-6">
        <!-- Header Card -->
        <div class="header-card">
          <div class="header-content">
            <div class="thumbnail-wrapper">
              <img
                v-if="course.thumbnail && !thumbnailError"
                :src="getThumbnailUrl(course.thumbnail)"
                :alt="course.title"
                class="thumbnail-img"
                loading="lazy"
                @error="handleImageError"
              />
              <div v-else class="thumbnail-placeholder">
                <svg class="h-16 w-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>Không có ảnh</span>
              </div>
            </div>
            <div class="course-info">
              <div>
                <h1 class="course-title">{{ course.title }}</h1>
                <p class="course-desc">{{ course.description }}</p>
              </div>

              <div class="tags-row">
                <span class="tag">Khối {{ course.grade }}</span>
                <span v-if="subjectLabel(course.subject)" class="tag">{{ subjectLabel(course.subject) }}</span>
                <span class="tag">{{ course.lessonsCount || 0 }} bài học</span>
                <span class="tag">{{ course.enrollments || 0 }} học viên</span>
                <span class="tag" :class="(course.price || 0) === 0 ? 'tag-free' : 'tag-paid'">
                  {{ (course.price || 0) === 0 ? 'Miễn phí' : formatPrice(course.price) }}
                </span>
              </div>

              <div class="action-buttons">
                <button v-if="isEnrolled" class="btn-primary" @click="startLearning">
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Vào học ngay
                </button>
                <button v-else class="btn-primary" @click="enrollCourse">
                  <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  Đăng ký khóa học
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Tabs Card -->
        <div class="tabs-card">
          <div class="tabs-header">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              class="tab-btn"
              :class="{ active: activeTab === tab.id }"
              @click="activeTab = tab.id as 'overview' | 'students'"
            >
              {{ tab.label }}
            </button>
          </div>

          <div class="tabs-content">
            <!-- Overview Tab -->
            <div v-if="activeTab === 'overview'" class="tab-panel">
              <div class="section">
                <h3 class="section-title">Giới thiệu khóa học</h3>
                <div class="section-content">{{ course.introduction || course.description || 'Chưa có giới thiệu.' }}</div>
              </div>

              <div class="section">
                <h3 class="section-title">Nội dung khóa học</h3>
                <div class="sections-list">
                  <div
                    v-for="(section, si) in course.sections"
                    :key="section.id"
                    class="section-item"
                  >
                    <h4 class="section-item-title">{{ si + 1 }}. {{ section.title }}</h4>
                    <ul class="lessons-list">
                      <li
                        v-for="(lesson, li) in section.lessons"
                        :key="lesson.id"
                        class="lesson-item"
                      >
                        <svg v-if="getLessonKind(lesson) === 'video'" class="lesson-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span v-else-if="getLessonKind(lesson) === 'pdf'" class="lesson-icon-emoji">📄</span>
                        <span v-else-if="getLessonKind(lesson) === 'doc'" class="lesson-icon-emoji">📑</span>
                        <span v-else-if="getLessonKind(lesson) === 'text'" class="lesson-icon-emoji">📝</span>
                        <svg v-else-if="getLessonKind(lesson) === 'quiz'" class="lesson-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                        </svg>
                        <svg v-else class="lesson-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <span class="lesson-title">{{ lesson.title }}</span>
                        <span class="lesson-duration">{{ formatDuration(lesson.durationMinutes) }}</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <!-- Students Tab -->
            <div v-if="activeTab === 'students'" class="tab-panel">
              <h3 class="section-title">Học viên ({{ students.length }})</h3>
              <div v-if="students.length" class="students-grid">
                <div
                  v-for="student in students"
                  :key="student.id"
                  class="student-card"
                >
                  <img
                    :src="getStudentAvatar(student)"
                    :alt="student.name"
                    class="student-avatar"
                  />
                  <div class="student-info">
                    <div class="student-name">{{ student.name }}</div>
                    <div class="student-progress">{{ student.progress }}% hoàn thành</div>
                  </div>
                </div>
              </div>
              <div v-else class="empty-students">
                <p>Chưa có học viên nào tham gia khóa học này.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="empty-state">
        <div class="empty-icon">📚</div>
        <h3>Không tìm thấy khóa học</h3>
        <p>Khóa học này không tồn tại hoặc đã bị xóa.</p>
      </div>
    </div>

    <!-- Review Modal -->
    <div
      v-if="showReviewModal"
      class="modal-overlay"
      @click.self="showReviewModal = false"
    >
      <div class="modal-content">
        <h3 class="modal-title">Viết đánh giá</h3>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Đánh giá</label>
            <div class="rating-stars">
              <button
                v-for="i in 5"
                :key="i"
                type="button"
                class="star-btn"
                @click="reviewRating = i"
              >
                <svg
                  class="star-icon"
                  :class="i <= reviewRating ? 'star-active' : 'star-inactive'"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </button>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Nhận xét</label>
            <textarea
              v-model.trim="reviewComment"
              rows="4"
              class="form-textarea"
              placeholder="Chia sẻ trải nghiệm của bạn..."
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-outline" @click="showReviewModal = false">Hủy</button>
          <button class="btn-primary" @click="submitReview">Gửi đánh giá</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, watch, onActivated, nextTick } from 'vue'
import { useRouter, useRoute, onBeforeRouteUpdate } from 'vue-router'
import { courseService, type CourseDetail, type Subject } from '@/services/course.service'
import { useAuthStore } from '@/store/auth.store'
import { useThemeStore } from '@/store/theme.store'
import { showToast } from '@/utils/toast'
import api from '@/config/axios'
import { getAvatarSrc } from '@/utils/avatar'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const routeCourseId = () => {
  const raw = route.params.id
  return Array.isArray(raw) ? raw[0] : raw
}
const currentCourseId = ref<string>(String(routeCourseId() || ''))

const loading = ref(true)
const course = ref<CourseDetail | null>(null)
const activeTab = ref<'overview' | 'students'>('overview')
const isEnrolled = ref(false)
const isFavorite = ref(false)
const hasReviewed = ref(false)

const reviews = ref<Array<{
  id: number
  name: string
  avatar: string
  rating: number
  comment: string
  createdAt: string
}>>([])

const students = ref<Array<{
  id: number
  name: string
  avatar: string
  gender?: 'male' | 'female' | 'other' | null
  progress: number
}>>([])

const showReviewModal = ref(false)
const reviewRating = ref(5)
const reviewComment = ref('')

const tabs = [
  { id: 'overview', label: 'Tổng quan' },
  { id: 'students', label: 'Học viên' },
]

function enrollmentStorageKey(id?: string) {
  const cid = id || currentCourseId.value
  return cid ? `course-enrolled-${cid}` : ''
}

function restoreCachedEnrollment() {
  const key = enrollmentStorageKey()
  if (!key) return
  const raw = localStorage.getItem(key)
  if (raw === 'true') isEnrolled.value = true
  else if (raw === 'false') isEnrolled.value = false
}

function persistEnrollment(state: boolean | null) {
  const key = enrollmentStorageKey()
  if (!key) return
  if (state === null) localStorage.removeItem(key)
  else localStorage.setItem(key, String(state))
}

function normalizeEnrollmentFlag(enrolled: any) {
  if (enrolled === undefined || enrolled === null) return
  const bool =
    enrolled === true ||
    enrolled === 'true' ||
    enrolled === 1 ||
    enrolled === '1' ||
    enrolled === 'True'
  isEnrolled.value = bool
  persistEnrollment(bool)
}

restoreCachedEnrollment()

const avgRating = computed(() => {
  if (reviews.value.length === 0) return 0
  const sum = reviews.value.reduce((acc, r) => acc + r.rating, 0)
  return sum / reviews.value.length
})

function subjectLabel(s?: Subject | string | null) {
  const labels: Record<string, string> = {
    math: 'Toán học',
    vietnamese: 'Tiếng Việt',
    english: 'Tiếng Anh',
    science: 'Khoa học',
    history: 'Lịch sử',
  }
  if (!s) return ''
  const key = String(s).toLowerCase()
  if (labels[key as Subject]) return labels[key as Subject]
  if (/[0-9a-f-]{8,}/i.test(key)) return ''
  return s
}

function formatDuration(min?: number) {
  if (!min || min <= 0) return '—'
  const mm = Math.floor(min)
  const ss = Math.round((min % 1) * 60)
  const mmStr = mm < 10 ? '0' + mm : String(mm)
  const ssStr = ss < 10 ? '0' + ss : String(ss)
  return `${mmStr}:${ssStr}`
}

function getLessonKind(lesson: any): string {
  const contentType = lesson?.content_type?.toLowerCase()
  if (contentType) {
    if (contentType === 'exercise' || contentType === 'quiz') return 'quiz'
    if (contentType === 'pdf') return 'pdf'
    if (contentType === 'text') return 'text'
    if (contentType === 'document') return 'doc'
    if (contentType === 'video') return 'video'
  }
  const type = lesson?.type?.toLowerCase()
  if (type) {
    if (type === 'quiz' || type === 'exercise') return 'quiz'
    if (type === 'pdf') return 'pdf'
    if (type === 'doc') return 'doc'
    if (type === 'text') return 'text'
    if (type === 'video') return 'video'
  }
  return 'video'
}

function formatPrice(price?: number) {
  if (!price || price === 0) return 'Miễn phí'
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price)
}

function getThumbnailUrl(thumbnail?: string): string {
  if (!thumbnail) return ''
  if (thumbnail.startsWith('http://') || thumbnail.startsWith('https://')) return thumbnail
  if (thumbnail.startsWith('data:')) return thumbnail
  const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  const cleanThumbnail = thumbnail.startsWith('/') ? thumbnail.slice(1) : thumbnail
  return `${apiBase}/media/${cleanThumbnail}`
}

const thumbnailError = ref(false)
function handleImageError() { thumbnailError.value = true }

function getStudentAvatar(student: typeof students.value[0]): string {
  return getAvatarSrc(student.avatar, student.gender, 'student')
}

async function loadCourse() {
  loading.value = true
  try {
    currentCourseId.value = String(routeCourseId() || '')
    restoreCachedEnrollment()
    const id = currentCourseId.value
    try {
      const { data } = await api.get(`/student/courses/${id}/`, {
        params: { _t: Date.now() },
        headers: { 'Cache-Control': 'no-cache', 'Pragma': 'no-cache' }
      })
      course.value = data
      normalizeEnrollmentFlag(data.isEnrolled)
    } catch (e: any) {
      const d = await courseService.detail(id)
      course.value = d
    }

    reviews.value = [
      { id: 1, name: 'Nguyễn Văn A', avatar: 'https://i.pravatar.cc/100?img=1', rating: 5, comment: 'Khóa học rất hay và dễ hiểu!', createdAt: new Date().toISOString() },
      { id: 2, name: 'Trần Thị B', avatar: 'https://i.pravatar.cc/100?img=2', rating: 4, comment: 'Nội dung phong phú, giáo viên giảng dạy tốt.', createdAt: new Date(Date.now() - 86400000).toISOString() },
    ]

    if (course.value && (course.value as any).students && Array.isArray((course.value as any).students)) {
      const studentsFromApi = (course.value as any).students
      students.value = studentsFromApi.map((s: any) => ({
        id: s.id || s.student_id,
        name: s.name || s.display_name || 'Học viên',
        avatar: s.avatar || s.avatar_url || null,
        gender: s.gender || null,
        progress: s.progress || 0,
      }))
    } else {
      students.value = []
    }

    if (course.value) {
      const enrolled = (course.value as any).isEnrolled
      if (enrolled !== undefined && enrolled !== null) {
        normalizeEnrollmentFlag(enrolled)
      }
    }
    isFavorite.value = false
    hasReviewed.value = false
  } catch (e: any) {
    console.error('Load course error:', e)
  } finally {
    loading.value = false
  }
}

function startLearning() {
  if (!course.value) return
  const courseId = course.value.id
  if (!isEnrolled.value) {
    showToast('Bạn cần đăng ký khóa học trước', 'warning')
    return
  }
  if (course.value.video_url || course.value.video_file) {
    router.push({ name: 'student-course-player', params: { id: String(courseId) } }).catch((err) => {
      showToast('Không thể vào khóa học. Vui lòng thử lại.', 'error')
    })
    return
  }
  const sections = course.value.sections || []
  let firstLesson = null
  for (const section of sections) {
    if (section.lessons && section.lessons.length > 0) {
      firstLesson = section.lessons[0]
      break
    }
  }
  const hasLessons = sections.some(s => s.lessons && s.lessons.length > 0)
  const lessonsCount = course.value.lessonsCount || 0
  const hasCourseVideo = !!(course.value.video_url || course.value.video_file)
  const hasContent = firstLesson || hasLessons || lessonsCount > 0 || hasCourseVideo

  if (hasContent) {
    if (firstLesson) {
      router.push({ name: 'student-course-player', params: { id: String(courseId), lessonId: String(firstLesson.id) } }).catch(() => {
        showToast('Không thể vào khóa học. Vui lòng thử lại.', 'error')
      })
    } else {
      router.push({ name: 'student-course-player', params: { id: String(courseId) } }).catch(() => {
        showToast('Không thể vào khóa học. Vui lòng thử lại.', 'error')
      })
    }
  } else {
    showToast('Khóa học chưa có nội dung. Vui lòng thử lại sau.', 'warning')
  }
}

async function enrollCourse() {
  if (!course.value) return
  const courseId = course.value.id
  const price = Number(course.value.price) || 0
  if (price === 0) {
    try {
      await courseService.enroll(courseId)
      normalizeEnrollmentFlag(true)
      await nextTick()
      showToast('Đăng ký khóa học thành công!', 'success')
      api.get(`/student/courses/${courseId}/`, { params: { _t: Date.now() } }).then(({ data }) => {
        if (data) {
          course.value = data
          normalizeEnrollmentFlag(data.isEnrolled)
        }
      }).catch(() => {})
    } catch (e: any) {
      normalizeEnrollmentFlag(false)
      showToast(e?.message || 'Đăng ký khóa học thất bại', 'error')
    }
  } else {
    router.push({ name: 'student-payments-cart', query: { add: String(courseId) } })
  }
}

async function submitReview() {
  if (!reviewComment.value.trim()) {
    alert('Vui lòng nhập nhận xét')
    return
  }
  reviews.value.unshift({
    id: Date.now(),
    name: auth.user?.name || 'Học viên',
    avatar: auth.user?.avatar || 'https://i.pravatar.cc/100',
    rating: reviewRating.value,
    comment: reviewComment.value,
    createdAt: new Date().toISOString(),
  })
  hasReviewed.value = true
  showReviewModal.value = false
  reviewComment.value = ''
  reviewRating.value = 5
}

onMounted(() => {
  restoreCachedEnrollment()
  loadCourse()
})

watch(() => route.params.id, () => {
  currentCourseId.value = String(routeCourseId() || '')
  restoreCachedEnrollment()
}, { immediate: false })

onActivated(() => { loadCourse() })

watch(() => route.params.id, (newId, oldId) => {
  if (newId !== oldId) loadCourse()
}, { immediate: false })

const previousRoute = ref<string | null>(null)
watch(() => route.fullPath, (newPath) => {
  if (previousRoute.value && previousRoute.value.includes('/player') && 
      newPath.includes('/student/courses/') && !newPath.includes('/player')) {
    const courseId = route.params.id
    if (courseId) setTimeout(() => { loadCourse() }, 100)
  }
  previousRoute.value = newPath
}, { immediate: true })

onBeforeRouteUpdate((to, from) => {
  if (from.path.includes('/player') && to.path.includes('/student/courses/') && !to.path.includes('/player')) {
    loadCourse()
  }
})
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  position: relative;
  transition: background-color 0.3s ease;
}
.page-wrapper.dark-mode { background: #020617; }
.page-wrapper.light-mode { background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%); }

.bg-elements { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.glow { position: absolute; border-radius: 50%; filter: blur(100px); }
.glow-1 { top: 10%; left: -5%; width: 300px; height: 300px; background: rgba(6, 182, 212, 0.1); }
.glow-2 { bottom: 10%; right: -5%; width: 250px; height: 250px; background: rgba(139, 92, 246, 0.1); }

.page-content { position: relative; z-index: 10; max-width: 1200px; margin: 0 auto; padding: 32px 24px; }

.loading-state { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 80px 20px; gap: 16px; }
.spinner { width: 40px; height: 40px; border: 3px solid rgba(6, 182, 212, 0.2); border-top-color: #06b6d4; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.loading-state p { font-size: 14px; }
.dark-mode .loading-state p { color: #94a3b8; }
.light-mode .loading-state p { color: #64748b; }

.space-y-6 > * + * { margin-top: 24px; }

.header-card { border-radius: 24px; overflow: hidden; }
.dark-mode .header-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .header-card { background: white; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }

.header-content { display: flex; flex-direction: column; gap: 24px; padding: 24px; }
@media (min-width: 768px) { .header-content { flex-direction: row; align-items: flex-start; } }

.thumbnail-wrapper { width: 100%; height: 200px; border-radius: 16px; overflow: hidden; flex-shrink: 0; }
@media (min-width: 768px) { .thumbnail-wrapper { width: 320px; height: 220px; } }
.dark-mode .thumbnail-wrapper { background: rgba(255,255,255,0.05); }
.light-mode .thumbnail-wrapper { background: #f1f5f9; }

.thumbnail-img { width: 100%; height: 100%; object-fit: cover; }
.thumbnail-placeholder { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; gap: 8px; }
.dark-mode .thumbnail-placeholder { color: #475569; }
.light-mode .thumbnail-placeholder { color: #94a3b8; }
.thumbnail-placeholder span { font-size: 14px; font-weight: 500; }

.course-info { flex: 1; display: flex; flex-direction: column; gap: 20px; }
.course-title { font-size: 28px; font-weight: 800; margin: 0; line-height: 1.3; }
.dark-mode .course-title { color: white; }
.light-mode .course-title { color: #1e293b; }

.course-desc { font-size: 15px; margin: 8px 0 0; line-height: 1.6; }
.dark-mode .course-desc { color: #94a3b8; }
.light-mode .course-desc { color: #64748b; }

.tags-row { display: flex; flex-wrap: wrap; gap: 8px; }
.tag { padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; }
.dark-mode .tag { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .tag { background: #f8fafc; border: 1px solid #e2e8f0; color: #64748b; }
.tag-free { }
.dark-mode .tag-free { background: rgba(34,197,94,0.1); border-color: rgba(34,197,94,0.3); color: #4ade80; }
.light-mode .tag-free { background: #dcfce7; border-color: #bbf7d0; color: #16a34a; }
.tag-paid { }
.dark-mode .tag-paid { background: rgba(251,191,36,0.1); border-color: rgba(251,191,36,0.3); color: #fbbf24; }
.light-mode .tag-paid { background: #fef3c7; border-color: #fde68a; color: #d97706; }

.action-buttons { display: flex; gap: 12px; }
.btn-primary {
  display: inline-flex; align-items: center; gap: 8px; padding: 12px 24px;
  border-radius: 12px; font-size: 14px; font-weight: 600; border: none; cursor: pointer; transition: all 0.3s;
}
.dark-mode .btn-primary { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; }
.light-mode .btn-primary { background: #1e293b; color: white; }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }

.btn-outline {
  display: inline-flex; align-items: center; gap: 8px; padding: 12px 24px;
  border-radius: 12px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s;
}
.dark-mode .btn-outline { background: transparent; border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .btn-outline { background: transparent; border: 1px solid #e2e8f0; color: #64748b; }
.btn-outline:hover { transform: translateY(-1px); }
.dark-mode .btn-outline:hover { border-color: #06b6d4; color: #06b6d4; }
.light-mode .btn-outline:hover { border-color: #6366f1; color: #6366f1; }

.tabs-card { border-radius: 24px; overflow: hidden; }
.dark-mode .tabs-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .tabs-card { background: white; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }

.tabs-header { display: flex; gap: 8px; padding: 16px; }
.dark-mode .tabs-header { background: rgba(255,255,255,0.02); border-bottom: 1px solid rgba(255,255,255,0.05); }
.light-mode .tabs-header { background: #f8fafc; border-bottom: 1px solid #e2e8f0; }

.tab-btn { padding: 10px 20px; border-radius: 10px; font-size: 14px; font-weight: 600; border: none; cursor: pointer; transition: all 0.3s; }
.dark-mode .tab-btn { background: transparent; color: #64748b; }
.light-mode .tab-btn { background: transparent; color: #64748b; }
.tab-btn:hover { }
.dark-mode .tab-btn:hover { color: white; }
.light-mode .tab-btn:hover { color: #1e293b; }
.tab-btn.active { }
.dark-mode .tab-btn.active { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; }
.light-mode .tab-btn.active { background: #1e293b; color: white; }

.tabs-content { padding: 24px; }
.tab-panel { }

.section { margin-bottom: 24px; }
.section:last-child { margin-bottom: 0; }
.section-title { font-size: 18px; font-weight: 700; margin: 0 0 12px; }
.dark-mode .section-title { color: white; }
.light-mode .section-title { color: #1e293b; }

.section-content { font-size: 15px; line-height: 1.7; white-space: pre-line; }
.dark-mode .section-content { color: #94a3b8; }
.light-mode .section-content { color: #64748b; }

.sections-list { display: flex; flex-direction: column; gap: 16px; }
.section-item { padding: 16px; border-radius: 16px; }
.dark-mode .section-item { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); }
.light-mode .section-item { background: #f8fafc; border: 1px solid #e2e8f0; }

.section-item-title { font-size: 15px; font-weight: 600; margin: 0 0 12px; }
.dark-mode .section-item-title { color: white; }
.light-mode .section-item-title { color: #1e293b; }

.lessons-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px; }
.lesson-item { display: flex; align-items: center; gap: 10px; font-size: 14px; }
.dark-mode .lesson-item { color: #94a3b8; }
.light-mode .lesson-item { color: #64748b; }

.lesson-icon { width: 16px; height: 16px; flex-shrink: 0; }
.lesson-icon-emoji { font-size: 14px; flex-shrink: 0; }
.lesson-title { flex: 1; }
.lesson-duration { font-size: 12px; }
.dark-mode .lesson-duration { color: #64748b; }
.light-mode .lesson-duration { color: #94a3b8; }

.students-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
@media (min-width: 640px) { .students-grid { grid-template-columns: repeat(3, 1fr); } }
@media (min-width: 768px) { .students-grid { grid-template-columns: repeat(4, 1fr); } }

.student-card { display: flex; flex-direction: column; align-items: center; gap: 8px; padding: 16px; border-radius: 16px; }
.dark-mode .student-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); }
.light-mode .student-card { background: #f8fafc; border: 1px solid #e2e8f0; }

.student-avatar { width: 48px; height: 48px; border-radius: 50%; object-fit: cover; }
.student-info { text-align: center; }
.student-name { font-size: 14px; font-weight: 600; }
.dark-mode .student-name { color: white; }
.light-mode .student-name { color: #1e293b; }
.student-progress { font-size: 12px; margin-top: 2px; }
.dark-mode .student-progress { color: #64748b; }
.light-mode .student-progress { color: #94a3b8; }

.empty-students { text-align: center; padding: 40px 20px; }
.empty-students p { font-size: 14px; }
.dark-mode .empty-students p { color: #64748b; }
.light-mode .empty-students p { color: #94a3b8; }

.empty-state { text-align: center; padding: 80px 20px; border-radius: 24px; }
.dark-mode .empty-state { background: rgba(255,255,255,0.02); border: 2px dashed rgba(255,255,255,0.1); }
.light-mode .empty-state { background: #f8fafc; border: 2px dashed #e2e8f0; }
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-state h3 { font-size: 18px; font-weight: 600; margin: 0 0 8px; }
.dark-mode .empty-state h3 { color: white; }
.light-mode .empty-state h3 { color: #1e293b; }
.empty-state p { font-size: 14px; margin: 0; }
.dark-mode .empty-state p { color: #64748b; }
.light-mode .empty-state p { color: #64748b; }

.modal-overlay { position: fixed; inset: 0; z-index: 50; display: flex; align-items: center; justify-content: center; padding: 16px; }
.dark-mode .modal-overlay { background: rgba(0,0,0,0.7); }
.light-mode .modal-overlay { background: rgba(0,0,0,0.5); }

.modal-content { width: 100%; max-width: 400px; border-radius: 20px; padding: 24px; }
.dark-mode .modal-content { background: #0f172a; border: 1px solid rgba(255,255,255,0.1); }
.light-mode .modal-content { background: white; box-shadow: 0 20px 40px rgba(0,0,0,0.15); }

.modal-title { font-size: 18px; font-weight: 700; margin: 0 0 20px; }
.dark-mode .modal-title { color: white; }
.light-mode .modal-title { color: #1e293b; }

.modal-body { display: flex; flex-direction: column; gap: 16px; }
.form-group { }
.form-label { display: block; font-size: 14px; font-weight: 500; margin-bottom: 8px; }
.dark-mode .form-label { color: #94a3b8; }
.light-mode .form-label { color: #64748b; }

.rating-stars { display: flex; gap: 4px; }
.star-btn { width: 32px; height: 32px; padding: 0; border: none; background: transparent; cursor: pointer; }
.star-icon { width: 100%; height: 100%; }
.star-active { color: #fbbf24; }
.star-inactive { color: #475569; }

.form-textarea { width: 100%; padding: 12px; border-radius: 12px; font-size: 14px; resize: vertical; outline: none; }
.dark-mode .form-textarea { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; }
.light-mode .form-textarea { background: #f8fafc; border: 1px solid #e2e8f0; color: #1e293b; }
.form-textarea:focus { }
.dark-mode .form-textarea:focus { border-color: #06b6d4; }
.light-mode .form-textarea:focus { border-color: #6366f1; }

.modal-footer { display: flex; justify-content: flex-end; gap: 12px; margin-top: 24px; }

@media (max-width: 640px) {
  .page-content { padding: 20px 16px; }
  .course-title { font-size: 22px; }
  .header-content { padding: 16px; }
  .tabs-content { padding: 16px; }
}
</style>
