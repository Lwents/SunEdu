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
              :src="course.thumbnail"
              :alt="course.title"
              class="h-48 w-full rounded-2xl object-cover md:h-64 md:w-80"
            />
            <div class="flex-1 space-y-4">
              <div>
                <h1 class="text-3xl font-bold text-slate-900">{{ course.title }}</h1>
                <p class="mt-2 text-slate-600">{{ course.description }}</p>
              </div>

              <div class="flex flex-wrap items-center gap-3">
                <span class="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-sm font-semibold">
                  Khối {{ course.grade }}
                </span>
                <span class="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-sm font-semibold">
                  {{ subjectLabel(course.subject) }}
                </span>
                <span class="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-sm font-semibold">
                  {{ course.lessonsCount || 0 }} bài học
                </span>
                <span class="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-sm font-semibold">
                  {{ course.enrollments || 0 }} học viên
                </span>
              </div>

              <div class="flex items-center gap-4">
                <div class="flex items-center gap-1">
                  <svg class="h-5 w-5 text-amber-400" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  <span class="font-semibold text-slate-900">{{ avgRating.toFixed(1) }}</span>
                  <span class="text-sm text-slate-600">({{ reviews.length }} đánh giá)</span>
                </div>
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
                <button
                  class="rounded-xl border border-slate-200 px-6 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
                  @click="toggleFavorite"
                >
                  {{ isFavorite ? '❤️ Đã yêu thích' : '🤍 Yêu thích' }}
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
                @click="activeTab = tab.id as 'overview' | 'reviews' | 'students'"
              >
                {{ tab.label }}
              </button>
            </div>
          </div>

          <div class="p-6">
            <!-- Overview Tab -->
            <div v-if="activeTab === 'overview'" class="space-y-6">
              <div>
                <h3 class="mb-3 text-lg font-semibold">Mô tả khóa học</h3>
                <p class="text-slate-700 whitespace-pre-line">{{ course.description || 'Chưa có mô tả.' }}</p>
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

            <!-- Reviews Tab -->
            <div v-if="activeTab === 'reviews'" class="space-y-6">
              <div class="flex items-center justify-between">
                <h3 class="text-lg font-semibold">Đánh giá ({{ reviews.length }})</h3>
                <button
                  v-if="isEnrolled && !hasReviewed"
                  class="rounded-xl bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700"
                  @click="showReviewModal = true"
                >
                  Viết đánh giá
                </button>
              </div>

              <div v-if="reviews.length" class="space-y-4">
                <div
                  v-for="review in reviews"
                  :key="review.id"
                  class="rounded-xl border border-slate-200 p-4"
                >
                  <div class="mb-2 flex items-center justify-between">
                    <div class="flex items-center gap-3">
                      <img
                        :src="review.avatar"
                        :alt="review.name"
                        class="h-10 w-10 rounded-full object-cover"
                      />
                      <div>
                        <div class="font-semibold text-slate-900">{{ review.name }}</div>
                        <div class="flex items-center gap-1">
                          <div class="flex">
                            <svg
                              v-for="i in 5"
                              :key="i"
                              class="h-4 w-4"
                              :class="i <= review.rating ? 'text-amber-400' : 'text-slate-300'"
                              fill="currentColor"
                              viewBox="0 0 20 20"
                            >
                              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                          </div>
                          <span class="text-xs text-slate-500">{{ formatDate(review.createdAt) }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <p class="text-sm text-slate-700">{{ review.comment }}</p>
                </div>
              </div>
              <p v-else class="text-center text-slate-500">Chưa có đánh giá nào.</p>
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
import { computed, ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { courseService, type CourseDetail, type Subject } from '@/services/course.service'
import { useAuthStore } from '@/store/auth.store'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const loading = ref(true)
const course = ref<CourseDetail | null>(null)
const activeTab = ref<'overview' | 'reviews' | 'students'>('overview')
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
  { id: 'reviews', label: 'Đánh giá' },
  { id: 'students', label: 'Học viên' },
]

const avgRating = computed(() => {
  if (reviews.value.length === 0) return 0
  const sum = reviews.value.reduce((acc, r) => acc + r.rating, 0)
  return sum / reviews.value.length
})

function subjectLabel(s?: Subject) {
  const labels: Record<string, string> = {
    math: 'Toán học',
    vietnamese: 'Tiếng Việt',
    english: 'Tiếng Anh',
    science: 'Khoa học',
    history: 'Lịch sử',
  }
  return s ? labels[s] || s : 'Khác'
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

async function loadCourse() {
  loading.value = true
  try {
    const id = Array.isArray(route.params.id) ? route.params.id[0] : route.params.id
    const d = await courseService.detail(id)
    course.value = d

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

    // Check enrollment
    isEnrolled.value = (Number(id) % 2 === 0)
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
  const firstSection = course.value.sections?.[0]
  const firstLesson = firstSection?.lessons?.[0]
  if (firstLesson) {
    router.push({
      name: 'student-course-player',
      params: { id: course.value.id, lessonId: firstLesson.id },
    })
  } else {
    router.push({ name: 'student-course-player', params: { id: course.value.id } })
  }
}

function enrollCourse() {
  router.push({ name: 'student-payments-cart', query: { add: String(course.value?.id) } })
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
  loadCourse()
})
</script>

<style scoped>
:host, .student-shell { overflow-x: hidden; }
</style>
