<template>
  <div class="min-h-screen bg-slate-50">
    <div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <!-- Error Message -->
      <div v-if="errMsg" class="mb-6 rounded-lg border border-red-200 bg-red-50 p-4">
        <div class="flex items-start gap-3">
          <svg class="h-5 w-5 shrink-0 text-red-600 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <div class="flex-1">
            <p class="font-semibold text-red-900">Đã xảy ra lỗi khi tải Dashboard</p>
            <pre class="mt-2 whitespace-pre-wrap font-mono text-xs text-red-700">{{ errMsg }}</pre>
          </div>
        </div>
      </div>

      <!-- Welcome Section -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900">Chào mừng trở lại! 👋</h1>
        <p class="mt-2 text-slate-600">Tiếp tục hành trình học tập của bạn</p>
      </div>

      <!-- Stats Cards -->
      <div class="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div class="rounded-lg border border-slate-200 bg-white p-6 shadow-sm transition hover:shadow-md hover:-translate-y-1 cursor-pointer">
          <p class="text-sm font-medium text-slate-600">Khóa học</p>
          <p class="mt-2 text-3xl font-bold text-slate-900">{{ featured.length }}</p>
          <p class="mt-1 text-sm text-slate-500">Đang tham gia</p>
        </div>

        <div class="rounded-lg border border-slate-200 bg-white p-6 shadow-sm transition hover:shadow-md hover:-translate-y-1 cursor-pointer">
          <p class="text-sm font-medium text-slate-600">Hoàn thành</p>
          <p class="mt-2 text-3xl font-bold text-slate-900">{{ completedCount }}</p>
          <p class="mt-1 text-sm text-slate-500">Khóa học</p>
        </div>

        <div class="rounded-lg border border-slate-200 bg-white p-6 shadow-sm transition hover:shadow-md hover:-translate-y-1 cursor-pointer">
          <p class="text-sm font-medium text-slate-600">Đề thi</p>
          <p class="mt-2 text-3xl font-bold text-slate-900">{{ previewExams.length }}</p>
          <p class="mt-1 text-sm text-slate-500">Có sẵn</p>
        </div>
              </div>

      <!-- Learning Progress Table -->
      <section class="mb-8 overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm">
        <div class="border-b border-slate-200 bg-slate-50 px-6 py-4">
          <div class="flex items-center justify-between">
            <div>
              <h2 class="text-xl font-semibold text-slate-900">Tiến độ học tập</h2>
              <p class="mt-1 text-sm text-slate-600">Theo dõi tiến độ của bạn trong từng khóa học</p>
            </div>
            <button
              type="button"
              class="hidden rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition sm:inline-flex"
              @click="goToCourses"
            >
              Xem tất cả
            </button>
          </div>
        </div>

        <div v-if="featured.length" class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-slate-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-700">Khóa học</th>
                <th class="px-6 py-3 text-center text-xs font-semibold uppercase tracking-wider text-slate-700">Tiến độ</th>
                <th class="px-6 py-3 text-center text-xs font-semibold uppercase tracking-wider text-slate-700">Trạng thái</th>
                <th class="px-6 py-3 text-center text-xs font-semibold uppercase tracking-wider text-slate-700">Thao tác</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr
                v-for="c in featured"
                :key="String(c.id)"
                class="hover:bg-slate-50 transition-colors"
              >
                <td class="px-6 py-4">
                  <div class="flex items-center gap-4">
                    <div class="relative h-16 w-16 shrink-0 overflow-hidden rounded-lg">
                      <img
                        v-if="c.thumbnail"
                        class="h-full w-full object-cover"
                        :src="getThumbnailUrl(c.thumbnail)"
                        :alt="c.title"
                        @error="handleImageError"
                      />
                      <div v-else class="flex h-full w-full items-center justify-center bg-slate-200">
                        <svg class="h-8 w-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                        </svg>
                      </div>
                    </div>
                    <div class="min-w-0 flex-1">
                      <h3 class="font-semibold text-slate-900 line-clamp-1">{{ c.title }}</h3>
                      <p class="mt-1 text-sm text-slate-500">{{ c.grade }}</p>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4">
                  <div class="flex flex-col items-center gap-2">
                    <div class="w-full max-w-[180px]">
                      <div class="relative h-2 overflow-hidden rounded-full bg-slate-200">
                        <div
                          class="h-full rounded-full bg-blue-600 transition-all duration-1000 ease-out"
                          :style="{ width: `${animatedProgress[c.id] || 0}%` }"
                        ></div>
                      </div>
                    </div>
                    <span class="text-sm font-semibold text-slate-900">
                      {{ Math.round(animatedProgress[c.id] || 0) }}%
                    </span>
                  </div>
                </td>
                <td class="px-6 py-4 text-center">
                  <span
                    class="inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium"
                    :class="c.done
                      ? 'bg-green-100 text-green-700'
                      : 'bg-amber-100 text-amber-700'"
                  >
                    <span
                      class="h-1.5 w-1.5 rounded-full"
                      :class="c.done ? 'bg-green-500' : 'bg-amber-500'"
                    ></span>
                    {{ c.done ? 'Hoàn thành' : 'Đang học' }}
                  </span>
                </td>
                <td class="px-6 py-4 text-center">
                  <button
                    type="button"
                    class="inline-flex items-center gap-2 rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
                    @click="openCourse(Number(c.id))"
                  >
                    {{ c.done ? 'Xem lại' : 'Tiếp tục' }}
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="px-6 py-16 text-center">
          <div class="mx-auto max-w-md">
            <div class="mx-auto h-20 w-20 rounded-full bg-slate-100 flex items-center justify-center mb-4">
              <svg class="h-10 w-10 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-slate-900">Chưa có khóa học</h3>
            <p class="mt-2 text-sm text-slate-600">Bắt đầu khám phá các khóa học mới ngay hôm nay!</p>
          <button
            type="button"
              class="mt-6 inline-flex items-center gap-2 rounded-lg bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
            @click="goToCourses"
          >
              Khám phá khóa học
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
          </button>
          </div>
        </div>
      </section>

      <!-- My Courses Grid -->
      <section class="mb-8">
        <div class="mb-6 flex items-center justify-between">
          <div>
            <h2 class="text-xl font-semibold text-slate-900">Khóa học của tôi</h2>
            <p class="mt-1 text-sm text-slate-600">Tất cả khóa học bạn đang tham gia</p>
          </div>
          <button
            type="button"
            class="hidden items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50 sm:inline-flex"
            @click="goToCourses"
          >
            Xem tất cả
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        <div v-if="featured.length" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          <article
            v-for="c in featured.slice(0, 8)"
            :key="String(c.id)"
            class="group overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-y-1 cursor-pointer"
            @click="openCourse(Number(c.id))"
          >
            <!-- Image -->
            <div class="relative h-40 overflow-hidden bg-slate-200">
            <img
              v-if="c.thumbnail"
                class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
              :src="getThumbnailUrl(c.thumbnail)"
              :alt="c.title"
              @error="handleImageError"
            />
              <div v-else class="flex h-full w-full items-center justify-center">
                <svg class="h-12 w-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <!-- Progress Badge -->
              <div class="absolute right-2 top-2 rounded bg-white/90 px-2 py-1 text-xs font-semibold text-slate-900 shadow">
                {{ c.done ? 100 : c.progress }}%
              </div>
            </div>

            <!-- Content -->
            <div class="p-4">
              <h3 class="mb-3 line-clamp-2 font-semibold text-slate-900">
                {{ c.title }}
              </h3>
              <div class="mb-4 space-y-2">
                <div class="flex items-center justify-between text-xs text-slate-600">
                  <span>Tiến độ</span>
                  <span class="font-semibold text-slate-900">{{ Math.round(animatedProgress[c.id] || 0) }}%</span>
                </div>
                <div class="h-1.5 overflow-hidden rounded-full bg-slate-100">
                  <div
                    class="h-full rounded-full bg-blue-600 transition-all duration-1000 ease-out"
                    :style="{ width: `${animatedProgress[c.id] || 0}%` }"
                  ></div>
                </div>
              </div>
              <div class="flex items-center justify-between">
                <span
                  class="rounded-full px-2.5 py-1 text-xs font-medium"
                  :class="c.done
                    ? 'bg-green-100 text-green-700'
                    : 'bg-amber-100 text-amber-700'"
                >
                  {{ c.done ? 'Hoàn thành' : 'Đang học' }}
                </span>
                <button
                  type="button"
                  class="rounded-lg bg-slate-900 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-slate-800"
                  @click.stop="openCourse(Number(c.id))"
                >
                  {{ c.done ? 'Xem lại' : 'Tiếp tục' }}
                </button>
              </div>
            </div>
          </article>
        </div>
        <div v-else class="rounded-lg border-2 border-dashed border-slate-300 bg-slate-50 p-12 text-center">
          <p class="text-slate-600">Chưa có khóa học nào.</p>
        </div>
      </section>

      <!-- Practice Exams -->
      <section class="mb-8">
        <div class="mb-6 flex items-center justify-between">
          <div>
            <h2 class="text-xl font-semibold text-slate-900">Luyện tập & Thi</h2>
            <p class="mt-1 text-sm text-slate-600">Các đề thi và bài tập luyện tập</p>
          </div>
          <button
            type="button"
            class="hidden items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50 sm:inline-flex"
            @click="openExamsList"
          >
            Xem thêm
            <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>

        <div v-if="previewExams.length" class="grid gap-4 sm:grid-cols-2">
          <div
            v-for="e in previewExams"
            :key="String(e.id)"
            class="overflow-hidden rounded-lg border border-slate-200 bg-white p-5 shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-y-1 cursor-pointer"
          >
            <div class="mb-4">
              <h3 class="mb-3 text-lg font-semibold text-slate-900">
                {{ e.title }}
              </h3>
              <div class="flex flex-wrap items-center gap-3 text-sm text-slate-600">
                <span class="flex items-center gap-1.5">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {{ toMin(e.duration) }} phút
                </span>
                <span class="flex items-center gap-1.5">
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Đạt ≥ {{ e.pass }} câu
                </span>
              </div>
            </div>
            <button
              type="button"
              class="w-full rounded-lg bg-slate-900 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800"
              @click="openExamDetail(e.id)"
            >
              Bắt đầu làm bài
            </button>
          </div>
        </div>
        <div v-else class="rounded-lg border-2 border-dashed border-slate-300 bg-slate-50 p-12 text-center">
          <p class="text-slate-600">Hiện chưa có đề thi phù hợp.</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { courseService, type CourseSummary } from '@/services/course.service'
import { useExamStore } from '@/store/exam.store'

type CourseCard = CourseSummary & { progress: number; done: boolean }

const router = useRouter()
const errMsg = ref('')

// ===== Courses =====
const featured = ref<CourseCard[]>([])
const resumeCourse = ref<CourseCard | null>(null)
const animatedProgress = ref<Record<string, number>>({})

const completedCount = computed(() => featured.value.filter(c => c.done).length)

function animateProgress(courseId: string, target: number, duration = 1000) {
  const start = 0
  const startTime = Date.now()
  
  function update() {
    const elapsed = Date.now() - startTime
    const progress = Math.min(elapsed / duration, 1)
    const current = start + (target - start) * easeOutCubic(progress)
    
    animatedProgress.value[courseId] = current
    
    if (progress < 1) {
      requestAnimationFrame(update)
    } else {
      animatedProgress.value[courseId] = target
    }
  }
  
  requestAnimationFrame(update)
}

function easeOutCubic(t: number): number {
  return 1 - Math.pow(1 - t, 3)
}

async function fetchCourses() {
  try {
    // Use student-specific endpoint that returns progress
    const response = await courseService.myCourses({})
    const allCourses = response.all || []
    
    const mapped: CourseCard[] = allCourses.map((c) => {
      const progress = c.progress ?? 0
      const done = c.done ?? (progress >= 100)
      return {
        ...c,
        progress,
        done
      } as CourseCard
    })
    
    featured.value = mapped.slice(0, 10)
    resumeCourse.value = mapped.find((c) => c.progress > 0 && c.progress < 100) || mapped[0] || null
    
    // Animate progress bars
    await nextTick()
    featured.value.forEach((c) => {
      const target = c.done ? 100 : c.progress
      animateProgress(String(c.id), target)
    })
  } catch (e: any) {
    console.error('Error fetching courses:', e)
    errMsg.value = `courseService.myCourses lỗi: ${e?.message || String(e)}`
    featured.value = []
    resumeCourse.value = null
  }
}

// ===== Exams =====
const examStore = useExamStore()
const previewExams = computed(() => {
  const list: any[] = (examStore.exams as any[]) || []
  if (!list.length) return []
  const grade = resumeCourse.value?.grade
  const prioritized = grade
    ? [...list.filter((e) => e.grade === grade), ...list.filter((e) => e.grade !== grade)]
    : list.slice()
  return prioritized.slice(0, 2)
})

function toMin(s: number) {
  return Math.round((Number(s) || 0) / 60)
}

// ===== Navigation =====
function hasRoute(name: string) {
  return router.hasRoute(name as any)
}
function goToCourses() {
  if (hasRoute('MyCourses')) router.push({ name: 'MyCourses' })
  else router.push('/student/courses')
}
function openCourse(id: number) {
  if (hasRoute('MyCourses')) router.push({ name: 'MyCourses', query: { highlight: String(id) } })
  else router.push({ path: '/student/courses', query: { highlight: String(id) } })
}
function openExamsList() {
  if (hasRoute('student-exams')) router.push({ name: 'student-exams' })
  else router.push('/student/exams')
}
function openExamDetail(id: number | string) {
  if (hasRoute('student-exam-detail')) router.push({ name: 'student-exam-detail', params: { id } })
  else router.push(`/student/exams/${id}`)
}

function getThumbnailUrl(thumbnail?: string): string {
  if (!thumbnail) return ''
  if (thumbnail.startsWith('http://') || thumbnail.startsWith('https://')) {
    return thumbnail
  }
  const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  return `${apiBase}/media/${thumbnail}`
}

function handleImageError(event: Event) {
  const img = event.target as HTMLImageElement
  img.src = 'https://via.placeholder.com/400x300?text=No+Image'
}

onMounted(async () => {
  await fetchCourses()
  try {
    await examStore.fetchExams()
  } catch (e: any) {
    errMsg.value = `examStore.fetchExams lỗi: ${e?.message || String(e)}`
  }
})
</script>
