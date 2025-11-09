<!-- src/pages/student/dashboard/dashboard.vue -->
<template>
  <div class="student-shell">
    <div class="student-container max-w-6xl">
      <div
        v-if="errMsg"
        class="mb-6 rounded-2xl border border-rose-200 bg-rose-50/80 p-4 text-sm text-rose-700 shadow-sm shadow-rose-100"
      >
        <p class="font-semibold">Đã xảy ra lỗi khi tải Dashboard</p>
        <pre class="mt-2 whitespace-pre-wrap font-mono text-xs">{{ errMsg }}</pre>
      </div>

      <section
        class="student-card overflow-hidden bg-gradient-to-br from-brand-600 via-emerald-500 to-teal-500 text-white shadow-student-card"
      >
        <div class="mb-4 text-sm font-semibold uppercase tracking-[0.3em] text-white/80">
          Continue learning
        </div>
        <div v-if="resumeCourse" class="space-y-4">
          <h2 class="text-2xl font-bold sm:text-3xl">{{ resumeCourse.title }}</h2>
          <p class="text-sm text-white/80">
            {{ resumeCourse.done ? 'Đã hoàn thành' : `Đang học · ${resumeCourse.progress}%` }}
          </p>
          <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
            <div class="flex flex-1 items-center gap-3">
              <span class="text-xs uppercase tracking-[0.2em] text-white/70">Progress</span>
              <div class="h-2 flex-1 overflow-hidden rounded-full bg-white/30">
                <div
                  class="h-full rounded-full bg-white"
                  :style="{ width: `${resumeCourse.done ? 100 : resumeCourse.progress}%` }"
                ></div>
              </div>
              <span class="text-sm font-semibold">{{ resumeCourse.progress }}%</span>
            </div>
            <button
              type="button"
              class="inline-flex items-center justify-center rounded-2xl bg-white px-5 py-2 text-sm font-bold uppercase tracking-wide text-brand-700 shadow-lg shadow-black/10 transition hover:-translate-y-0.5 hover:bg-white/90"
              @click="onResume"
            >
              Tiếp tục học
            </button>
          </div>
        </div>
        <div v-else class="space-y-4">
          <h2 class="text-2xl font-bold sm:text-3xl">Chưa có khóa học</h2>
          <p class="text-sm text-white/80">Bắt đầu khám phá từ trang Khoá học.</p>
          <button
            type="button"
            class="inline-flex items-center justify-center rounded-2xl bg-white px-5 py-2 text-sm font-bold uppercase tracking-wide text-brand-700 shadow-lg shadow-black/10 transition hover:-translate-y-0.5 hover:bg-white/90"
            @click="goToCourses"
          >
            Xem khóa học
          </button>
        </div>
      </section>

      <section class="student-card mt-6">
        <div class="mb-6 flex items-center justify-between gap-3">
          <div>
            <p class="student-section-title">Khoá học</p>
            <h2 class="text-2xl font-black text-brand-deep">My Courses</h2>
          </div>
          <button
            type="button"
            class="student-link flex items-center gap-1 text-sm"
            aria-label="view more"
            @click="goToCourses"
          >
            Xem tất cả
            <span aria-hidden="true">›</span>
          </button>
        </div>

        <div v-if="featured.length" class="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
          <article
            v-for="c in featured"
            :key="String(c.id)"
            class="group flex flex-col rounded-3xl border border-slate-200 bg-white/90 p-4 shadow-sm shadow-slate-100 transition hover:-translate-y-1 hover:shadow-xl"
            @click="openCourse(Number(c.id))"
          >
            <img
              class="h-36 w-full rounded-2xl object-cover object-center"
              :src="c.thumbnail"
              :alt="c.title"
            />
            <div class="mt-4 space-y-3">
              <h3 class="text-base font-semibold text-brand-deep line-clamp-2">{{ c.title }}</h3>
              <div class="space-y-1">
                <div class="flex items-center justify-between text-xs font-semibold uppercase tracking-[0.2em] text-brand-muted">
                  <span>Progress</span>
                  <span>{{ c.done ? 100 : c.progress }}%</span>
                </div>
                <div class="h-2 rounded-full bg-slate-100">
                  <div
                    class="h-2 rounded-full bg-brand-500 transition-all"
                    :style="{ width: `${(c.done ? 100 : c.progress) || 0}%` }"
                  ></div>
                </div>
              </div>
              <p class="text-sm font-medium text-brand-muted">
                {{ c.done ? 'Đã hoàn thành' : `Đang học · ${c.progress}%` }}
              </p>
            </div>
          </article>
        </div>
        <p v-else class="text-sm text-brand-muted">Chưa có khóa học nào.</p>
      </section>

      <section class="student-card mt-6">
        <div class="mb-4 flex items-center justify-between gap-3">
          <div>
            <p class="student-section-title">Luyện tập</p>
            <h2 class="text-2xl font-black text-brand-deep">Practice Exams</h2>
          </div>
          <button type="button" class="student-link flex items-center gap-1 text-sm" @click="openExamsList">
            Xem thêm
            <span aria-hidden="true">›</span>
          </button>
        </div>

        <ul v-if="previewExams.length" class="space-y-4">
          <li
            v-for="e in previewExams"
            :key="String(e.id)"
            class="flex flex-col gap-4 rounded-2xl border border-slate-200/80 bg-white/80 p-4 shadow-sm shadow-slate-100 sm:flex-row sm:items-center"
          >
            <div class="flex flex-1 flex-col">
              <h3 class="text-lg font-semibold text-brand-deep">{{ e.title }}</h3>
              <p class="text-sm text-brand-muted">
                Khối {{ e.grade }} · {{ toMin(e.duration) }} phút · Đạt ≥ {{ e.pass }} câu
              </p>
            </div>
            <button
              type="button"
              class="inline-flex items-center justify-center rounded-2xl border border-brand-200 px-4 py-2 text-sm font-semibold text-brand-600 transition hover:bg-brand-50"
              @click="openExamDetail(e.id)"
            >
              Làm bài
            </button>
          </li>
        </ul>
        <p v-else class="text-sm text-brand-muted">Hiện chưa có đề phù hợp.</p>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { courseService, type CourseSummary } from '@/services/course.service'
import { useExamStore } from '@/store/exam.store'
// ✅ CÁCH IMPORT ĐÚNG
import * as echarts from 'echarts/core'

// Import các loại biểu đồ bạn cần (ví dụ: BarChart, LineChart, PieChart)
import { BarChart } from 'echarts/charts'

// Import các component cần thiết (ví dụ: Title, Tooltip, Grid)
import { TitleComponent, TooltipComponent, GridComponent } from 'echarts/components'

// Import renderer (dùng Canvas hoặc SVG)
import { CanvasRenderer } from 'echarts/renderers'

// Đăng ký các component đã import
echarts.use([TitleComponent, TooltipComponent, GridComponent, BarChart, CanvasRenderer])
type CourseCard = CourseSummary & { progress: number; done: boolean }

const router = useRouter()
const errMsg = ref('')

// ===== Courses =====
const featured = ref<CourseCard[]>([])
const resumeCourse = ref<CourseCard | null>(null)

async function fetchCourses() {
  try {
    const { items } = await courseService.list({
      page: 1,
      pageSize: 12,
      status: 'published',
      sortBy: 'updatedAt',
      sortDir: 'descending',
    })
    const mapped: CourseCard[] = (items || []).map((c) => {
      const p = (Number(c.id) * 13) % 100
      return { ...c, progress: p, done: p >= 100 }
    })
    featured.value = mapped.slice(0, 6)
    resumeCourse.value = mapped.find((c) => c.progress > 0 && c.progress < 100) || mapped[0] || null
  } catch (e: any) {
    errMsg.value = `courseService.list lỗi: ${e?.message || String(e)}`
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

// ===== Navigation helpers with fallback =====
function hasRoute(name: string) {
  return router.hasRoute(name as any)
}
function goToCourses() {
  if (hasRoute('MyCourses')) router.push({ name: 'MyCourses' })
  else router.push('/student/courses') // đổi path theo router của bạn
}
function openCourse(id: number) {
  if (hasRoute('MyCourses')) router.push({ name: 'MyCourses', query: { highlight: String(id) } })
  else router.push({ path: '/student/courses', query: { highlight: String(id) } })
}
function onResume() {
  if (!resumeCourse.value) return
  openCourse(Number(resumeCourse.value.id))
}
function openExamsList() {
  if (hasRoute('student-exams')) router.push({ name: 'student-exams' })
  else router.push('/student/exams') // đổi path đúng với router của bạn
}
function openExamDetail(id: number | string) {
  if (hasRoute('student-exam-detail')) router.push({ name: 'student-exam-detail', params: { id } })
  else router.push(`/student/exams/${id}`)
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
