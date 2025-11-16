<!-- src/pages/student/courses/CourseDetail.vue -->
<template>
  <div class="student-shell">
    <div class="student-container max-w-6xl">
      <div v-if="loading" class="py-16 text-center text-slate-500">Đang tải...</div>

      <div v-else-if="course" class="space-y-6">
        <!-- Header -->
        <div class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div class="flex flex-col gap-4 md:flex-row md:items-start">
            <img
              v-if="course.thumbnail"
              :src="getThumbnailUrl(course.thumbnail)"
              :alt="course.title"
              class="h-48 w-full rounded-2xl object-cover md:h-64 md:w-80"
              @error="handleImageError"
            />
            <div v-else class="flex h-48 w-full items-center justify-center rounded-2xl bg-slate-200 md:h-64 md:w-80">
              <span class="text-slate-400">Chưa có ảnh</span>
            </div>
            <div class="flex-1 space-y-4">
              <div>
                <h1 class="text-3xl font-bold text-slate-900">{{ course.title }}</h1>
                <p class="mt-2 text-slate-600">{{ course.description }}</p>
              </div>

              <div class="flex flex-wrap items-center gap-3">
                <span class="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-sm font-semibold">
                  Khối {{ course.grade }}
                </span>
                <span v-if="subjectLabel(course.subject)" class="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-sm font-semibold">
                  {{ subjectLabel(course.subject) }}
                </span>
                <span class="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-sm font-semibold">
                  {{ course.lessonsCount || 0 }} bài học
                </span>
                <span class="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-sm font-semibold">
                  {{ course.enrollments || 0 }} học viên
                </span>
                <span class="rounded-full border px-3 py-1 text-sm font-semibold"
                  :class="(course.price || 0) === 0 
                    ? 'border-green-200 bg-green-50 text-green-700' 
                    : 'border-amber-200 bg-amber-50 text-amber-700'">
                  {{ (course.price || 0) === 0 ? 'Miễn phí' : formatPrice(course.price) }}
                </span>
              </div>


              <div class="flex gap-3">
                <button
                  v-if="isEnrolled"
                  class="rounded-xl bg-cyan-600 px-6 py-3 text-sm font-semibold text-white hover:bg-cyan-700"
                  @click="startLearning"
                >
                  Vào học ngay
                </button>
                <button
                  v-else
                  class="rounded-xl bg-cyan-600 px-6 py-3 text-sm font-semibold text-white hover:bg-cyan-700"
                  @click="enrollCourse"
                >
                  Đăng ký khóa học
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Tabs -->
        <div class="rounded-3xl border border-slate-200 bg-white shadow-sm">
          <div class="border-b border-slate-200">
            <div class="flex gap-2 p-4">
              <button
                v-for="tab in tabs"
                :key="tab.id"
                class="rounded-lg px-4 py-2 text-sm font-semibold transition"
                :class="
                  activeTab === tab.id
                    ? 'bg-cyan-50 text-cyan-700'
                    : 'text-slate-600 hover:bg-slate-50'
                "
                @click="activeTab = tab.id as 'overview' | 'students'"
              >
                {{ tab.label }}
              </button>
            </div>
          </div>

          <div class="p-6">
            <!-- Overview Tab -->
            <div v-if="activeTab === 'overview'" class="space-y-6">
              <!-- Giới thiệu chi tiết -->
              <div>
                <h3 class="mb-3 text-lg font-semibold">Giới thiệu khóa học</h3>
                <div class="text-slate-700 whitespace-pre-line">{{ course.introduction || course.description || 'Chưa có giới thiệu.' }}</div>
              </div>

              <div>
                <h3 class="mb-3 text-lg font-semibold">Nội dung khóa học</h3>
                <div class="space-y-3">
                  <div
                    v-for="(section, si) in course.sections"
                    :key="section.id"
                    class="rounded-xl border border-slate-200 p-4"
                  >
                    <h4 class="font-semibold text-slate-900">{{ si + 1 }}. {{ section.title }}</h4>
                    <ul class="mt-2 space-y-2">
                      <li
                        v-for="(lesson, li) in section.lessons"
                        :key="lesson.id"
                        class="flex items-center gap-2 text-sm text-slate-600"
                      >
                        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
                          />
                          <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                          />
                        </svg>
                        <span>{{ lesson.title }}</span>
                        <span class="text-xs text-slate-400">{{ formatDuration(lesson.durationMinutes) }}</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>


            <!-- Students Tab -->
            <div v-if="activeTab === 'students'" class="space-y-4">
              <h3 class="text-lg font-semibold">Học viên ({{ students.length }})</h3>
              <div class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4">
                <div
                  v-for="student in students"
                  :key="student.id"
                  class="flex flex-col items-center gap-2 rounded-xl border border-slate-200 p-3"
                >
                  <img
                    :src="student.avatar"
                    :alt="student.name"
                    class="h-12 w-12 rounded-full object-cover"
                  />
                  <div class="text-center">
                    <div class="text-sm font-semibold text-slate-900">{{ student.name }}</div>
                    <div class="text-xs text-slate-500">{{ student.progress }}% hoàn thành</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="py-16 text-center text-slate-500">Không tìm thấy khóa học.</div>

      <!-- Review Modal -->
      <div
        v-if="showReviewModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
        @click.self="showReviewModal = false"
      >
        <div class="w-full max-w-md rounded-2xl bg-white p-6">
          <h3 class="mb-4 text-lg font-semibold">Viết đánh giá</h3>
          <div class="space-y-4">
            <div>
              <label class="mb-1 block text-sm font-medium">Đánh giá</label>
              <div class="flex gap-1">
                <button
                  v-for="i in 5"
                  :key="i"
                  type="button"
                  class="h-8 w-8"
                  @click="reviewRating = i"
                >
                  <svg
                    class="h-full w-full"
                    :class="i <= reviewRating ? 'text-amber-400' : 'text-slate-300'"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                </button>
              </div>
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium">Nhận xét</label>
              <textarea
                v-model.trim="reviewComment"
                rows="4"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none"
                placeholder="Chia sẻ trải nghiệm của bạn..."
              ></textarea>
            </div>
          </div>
          <div class="mt-6 flex justify-end gap-3">
            <button
              class="rounded-xl border px-4 py-2 text-sm hover:bg-slate-50"
              @click="showReviewModal = false"
            >
              Hủy
            </button>
            <button
              class="rounded-xl bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700"
              @click="submitReview"
            >
              Gửi đánh giá
            </button>
          </div>
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
import { showToast } from '@/utils/toast'
import api from '@/config/axios'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
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
  // Nếu backend trả về UUID hoặc chuỗi lạ, không hiển thị
  if (/[0-9a-f-]{8,}/i.test(key)) return ''
  return s
}

function formatDate(iso?: string) {
  if (!iso) return ''
  try {
    return new Date(iso).toLocaleDateString('vi-VN')
  } catch {
    return iso
  }
}

function formatDuration(min?: number) {
  if (!min || min <= 0) return '—'
  const mm = Math.floor(min)
  const ss = Math.round((min % 1) * 60)
  const mmStr = mm < 10 ? '0' + mm : String(mm)
  const ssStr = ss < 10 ? '0' + ss : String(ss)
  return `${mmStr}:${ssStr}`
}

function formatPrice(price?: number) {
  if (!price || price === 0) return 'Miễn phí'
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price)
}

function isYouTubeUrl(url?: string): boolean {
  if (!url) return false
  return url.includes('youtube.com') || url.includes('youtu.be')
}

function getYouTubeEmbedUrl(url: string): string {
  if (!url) return ''
  // Extract video ID from various YouTube URL formats
  let videoId = ''
  if (url.includes('youtube.com/watch?v=')) {
    videoId = url.split('v=')[1]?.split('&')[0] || ''
  } else if (url.includes('youtu.be/')) {
    videoId = url.split('youtu.be/')[1]?.split('?')[0] || ''
  } else if (url.includes('youtube.com/embed/')) {
    videoId = url.split('embed/')[1]?.split('?')[0] || ''
  }
  return videoId ? `https://www.youtube.com/embed/${videoId}` : url
}

function getThumbnailUrl(thumbnail?: string): string {
  if (!thumbnail) return ''
  // If already a full URL, return as is
  if (thumbnail.startsWith('http://') || thumbnail.startsWith('https://')) {
    return thumbnail
  }
  // Otherwise, prepend media URL
  const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  return `${apiBase}/media/${thumbnail}`
}

function handleImageError(event: Event) {
  const img = event.target as HTMLImageElement
  img.src = 'https://via.placeholder.com/400x300?text=No+Image'
}

function getVideoFileUrl(videoFile?: string): string {
  if (!videoFile) return ''
  if (videoFile.startsWith('http://') || videoFile.startsWith('https://')) {
    return videoFile
  }
  const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  return `${apiBase}/media/${videoFile}`
}

async function loadCourse() {
  loading.value = true
  try {
    currentCourseId.value = String(routeCourseId() || '')
    restoreCachedEnrollment()
    const id = currentCourseId.value
    // Sử dụng student API endpoint để lấy isEnrolled
    // Thêm timestamp để tránh cache - LUÔN force reload
    try {
      const { data } = await api.get(`/student/courses/${id}/`, {
        params: { _t: Date.now() }, // Cache busting
        headers: {
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache'
        }
      })
      course.value = data
      console.log('Course loaded from student API:', data)
      console.log('isEnrolled from API:', data.isEnrolled)
      normalizeEnrollmentFlag(data.isEnrolled)
    } catch (e: any) {
      console.error('Error loading from student API:', e)
      // Fallback to regular endpoint nếu student endpoint không có
      const d = await courseService.detail(id)
      course.value = d
    }

    // Load reviews
    reviews.value = [
      {
        id: 1,
        name: 'Nguyễn Văn A',
        avatar: 'https://i.pravatar.cc/100?img=1',
        rating: 5,
        comment: 'Khóa học rất hay và dễ hiểu!',
        createdAt: new Date().toISOString(),
      },
      {
        id: 2,
        name: 'Trần Thị B',
        avatar: 'https://i.pravatar.cc/100?img=2',
        rating: 4,
        comment: 'Nội dung phong phú, giáo viên giảng dạy tốt.',
        createdAt: new Date(Date.now() - 86400000).toISOString(),
      },
    ]

    // Load students
    const studentsList = []
    for (let i = 0; i < 12; i++) {
      studentsList.push({
        id: i + 1,
        name: `Học viên ${i + 1}`,
        avatar: `https://i.pravatar.cc/100?img=${i + 3}`,
        progress: 20 + (i * 7) % 80,
      })
    }
    students.value = studentsList

    // Check enrollment from course data
    // Đảm bảo isEnrolled được set đúng từ API response
    if (course.value) {
      const enrolled = (course.value as any).isEnrolled
      if (enrolled === undefined || enrolled === null) {
        console.warn('isEnrolled not in API response, keeping previous value')
      } else {
        normalizeEnrollmentFlag(enrolled)
      }
      console.log('Course loaded - isEnrolled:', isEnrolled.value, 'from API:', enrolled, 'type:', typeof enrolled, 'course data:', course.value)
    } else {
      console.log('Course not loaded from API')
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
  if (!course.value) {
    console.error('Course not loaded')
    return
  }
  
  const courseId = course.value.id
  console.log('Starting learning for course:', courseId)
  
  // Kiểm tra enrollment trước khi vào học
  if (!isEnrolled.value) {
    showToast('Bạn cần đăng ký khóa học trước', 'warning')
    return
  }
  
  // Nếu có video_url hoặc video_file, vào trang player để xem video
  if (course.value.video_url || course.value.video_file) {
    console.log('Navigating to player with course video')
    router.push({ name: 'student-course-player', params: { id: String(courseId) } }).catch((err) => {
      console.error('Navigation error:', err)
      showToast('Không thể vào khóa học. Vui lòng thử lại.', 'error')
    })
    return
  }
  
  // Kiểm tra nội dung từ sections (backend trả về sections với lessons)
  const sections = course.value.sections || []
  
  // Tìm lesson đầu tiên từ tất cả sections
  let firstLesson = null
  for (const section of sections) {
    if (section.lessons && section.lessons.length > 0) {
      firstLesson = section.lessons[0]
      break
    }
  }
  
  // Kiểm tra xem có nội dung không:
  // 1. Có lesson đầu tiên
  // 2. Hoặc có lessonsCount > 0 (backend đã tính)
  // 3. Hoặc có sections với lessons
  const hasLessons = sections.some(s => s.lessons && s.lessons.length > 0)
  const lessonsCount = course.value.lessonsCount || 0
  
  // Nếu có video_url hoặc video_file ở course level, coi như có nội dung
  const hasCourseVideo = !!(course.value.video_url || course.value.video_file)
  
  const hasContent = firstLesson || hasLessons || lessonsCount > 0 || hasCourseVideo
  
  // Nếu có nội dung (lessonsCount > 0 hoặc có sections với lessons), cho phép vào học
  // Backend sẽ tự tìm lesson đầu tiên khi vào player nếu không có lessonId
  if (hasContent) {
    if (firstLesson) {
      router.push({
        name: 'student-course-player',
        params: { id: String(courseId), lessonId: String(firstLesson.id) },
      }).catch((err) => {
        console.error('Navigation error:', err)
        showToast('Không thể vào khóa học. Vui lòng thử lại.', 'error')
      })
    } else {
      // Có nội dung (lessonsCount > 0) nhưng chưa có lesson cụ thể trong sections
      // Backend sẽ tự tìm lesson đầu tiên khi vào player
      router.push({ name: 'student-course-player', params: { id: String(courseId) } }).catch((err) => {
        console.error('Navigation error:', err)
        showToast('Không thể vào khóa học. Vui lòng thử lại.', 'error')
      })
    }
  } else {
    // Không có nội dung nào
    showToast('Khóa học chưa có nội dung. Vui lòng thử lại sau.', 'warning')
  }
}

async function enrollCourse() {
  if (!course.value) return
  
  const courseId = course.value.id
  const price = Number(course.value.price) || 0
  
  // Nếu khóa học miễn phí, enroll trực tiếp
  if (price === 0) {
    try {
      await courseService.enroll(courseId)
      
      // Cập nhật trạng thái enrolled NGAY LẬP TỨC để UI phản hồi ngay
      // Không cần chờ API response
      normalizeEnrollmentFlag(true)
      
      // Force Vue reactivity update ngay lập tức
      await nextTick()
      
      // Hiển thị toast thông báo thành công
      showToast('Đăng ký khóa học thành công!', 'success')
      
      // Reload lại course data để đồng bộ với backend (chạy background)
      // Không block UI, chỉ để đảm bảo data đồng bộ
      api.get(`/student/courses/${courseId}/`, {
        params: { _t: Date.now() } // Cache busting
      }).then(({ data }) => {
        if (data) {
          course.value = data
          // Đảm bảo isEnrolled được set đúng từ API response
          normalizeEnrollmentFlag(data.isEnrolled)
          console.log('After enroll reload - isEnrolled:', isEnrolled.value, 'from API:', data.isEnrolled)
        }
      }).catch((e: any) => {
        console.error('Error reloading course after enroll:', e)
        // Giữ nguyên isEnrolled = true nếu reload fail
      })
    } catch (e: any) {
      console.error('Enroll error:', e)
      // Nếu enroll fail, reset lại isEnrolled
      normalizeEnrollmentFlag(false)
      showToast(e?.message || 'Đăng ký khóa học thất bại', 'error')
    }
  } else {
    // Nếu có phí, thêm vào giỏ hàng
    router.push({ name: 'student-payments-cart', query: { add: String(courseId) } })
  }
}

function toggleFavorite() {
  isFavorite.value = !isFavorite.value
  console.log('Toggle favorite:', isFavorite.value)
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

// Reload khi quay lại trang (nếu dùng keep-alive)
onActivated(() => {
  // Force reload khi quay lại từ player hoặc bất kỳ đâu
  console.log('Component activated, reloading course data...')
  loadCourse()
})

// Watch route params để reload khi chuyển course khác
watch(() => route.params.id, (newId, oldId) => {
  if (newId !== oldId) {
    console.log('Course ID changed, reloading...')
    loadCourse()
  }
}, { immediate: false })

// Watch route để reload khi quay lại từ player
const previousRoute = ref<string | null>(null)
watch(() => route.fullPath, (newPath) => {
  // Nếu quay lại từ player (cùng course ID), reload data
  if (previousRoute.value && previousRoute.value.includes('/player') && 
      newPath.includes('/student/courses/') && !newPath.includes('/player')) {
    const courseId = route.params.id
    if (courseId) {
      console.log('Returned from player, reloading course data...')
      // Force reload với delay nhỏ để đảm bảo route đã update
      setTimeout(() => {
        loadCourse()
      }, 100)
    }
  }
  previousRoute.value = newPath
}, { immediate: true })

// Thêm onBeforeRouteUpdate để reload khi navigate vào
onBeforeRouteUpdate((to, from) => {
  // Nếu quay lại từ player, reload
  if (from.path.includes('/player') && to.path.includes('/student/courses/') && !to.path.includes('/player')) {
    console.log('Route update: returned from player, will reload')
    loadCourse()
  }
})
</script>

<style scoped>
:host, .student-shell { overflow-x: hidden; }
</style>
