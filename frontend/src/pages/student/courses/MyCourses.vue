<template>
  <div class="min-h-screen bg-slate-50">
    <div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
      <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
            <h1 class="text-3xl font-bold text-slate-900">Khóa học của tôi</h1>
            <p class="mt-2 text-slate-600">
              Các khóa học bạn đang tham gia được chia theo từng cấp trình độ
          </p>
        </div>
          <div class="flex gap-3">
          <router-link
              class="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition"
            :to="{ name: 'student-learning-path' }"
          >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
              </svg>
            Lộ trình
          </router-link>
          <router-link
              class="inline-flex items-center gap-2 rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800 transition"
            :to="{ name: 'student-catalog' }"
          >
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            Catalog
          </router-link>
          </div>
        </div>
      </div>

      <!-- Filters & Tabs -->
      <div class="mb-8 rounded-lg border border-slate-200 bg-white shadow-sm">
        <div class="border-b border-slate-200 bg-slate-50 px-6 py-4">
          <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <!-- Tabs -->
        <div class="flex gap-2">
          <button
                class="rounded-lg px-5 py-2.5 text-sm font-semibold transition"
                :class="activeTab === 'main'
                  ? 'bg-slate-900 text-white'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200'"
            @click="activeTab = 'main'"
          >
            Khóa học chính
          </button>
          <button
                class="rounded-lg px-5 py-2.5 text-sm font-semibold transition"
                :class="activeTab === 'supp'
                  ? 'bg-slate-900 text-white'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200'"
            @click="activeTab = 'supp'"
          >
            Khóa học bổ trợ
          </button>
        </div>

            <!-- Search & Filter -->
        <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
          <div class="relative" @mouseleave="open = false">
            <button
              type="button"
                  class="inline-flex w-full items-center justify-between gap-3 rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-medium text-slate-900 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-200 sm:w-48"
              @click="open = !open"
            >
              <span>{{ level || 'Tất cả trình độ' }}</span>
                  <svg class="h-4 w-4 transition-transform" :class="open ? 'rotate-180' : ''" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 9l6 6 6-6" />
              </svg>
            </button>
            <ul
              v-show="open"
                  class="absolute z-20 mt-2 w-full rounded-lg border border-slate-200 bg-white p-2 shadow-lg"
            >
              <li
                v-for="lvl in ['', 'Khối 1–2', 'Khối 3–5']"
                :key="lvl || 'all'"
                    class="cursor-pointer rounded-lg px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
                @click="setLevel(lvl as '' | 'Khối 1–2' | 'Khối 3–5')"
              >
                {{ lvl || 'Tất cả trình độ' }}
              </li>
            </ul>
          </div>

              <div class="flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2.5">
                <svg class="h-5 w-5 text-slate-400" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 21l-4.3-4.3" />
                <circle cx="11" cy="11" r="7" />
              </svg>
              <input
                v-model.trim="q"
                placeholder="Tìm khóa học..."
                  class="w-full border-none bg-transparent text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none"
              />
              </div>
            </div>
            </div>
        </div>
      </div>

      <!-- Main Courses Tab -->
      <template v-if="activeTab === 'main'">
        <template v-if="hasMainCourses">
          <template v-for="section in gradeSections" :key="section.grade">
            <section
              v-if="section.courses.length"
              class="mb-8"
            >
            <div class="mb-6 flex items-center justify-between">
              <div>
                <h2 class="text-xl font-semibold text-slate-900">
                  Lớp {{ section.grade }} <span class="text-sm font-normal text-slate-500">({{ section.subtitle }})</span>
                </h2>
                <p class="mt-1 text-sm text-slate-600">{{ section.courses.length }} khóa học</p>
              </div>
              <div class="flex items-center gap-4">
                <div class="flex items-center gap-2 rounded-lg bg-amber-50 px-3 py-1.5 border border-amber-200">
                  <span class="text-lg">🏆</span>
                  <span class="text-sm font-semibold text-amber-900">
                    {{ section.trophies.earned }}/{{ section.trophies.total || 5 * section.courses.length }}
                  </span>
                </div>
                <router-link
                  class="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition"
                  :to="{ name: 'student-catalog', query: { grade: section.grade } }"
                >
                  Xem tất cả
                  <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </router-link>
              </div>
            </div>

            <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              <article
                v-for="c in section.courses"
                :key="c.id"
                class="group overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-y-1 cursor-pointer"
                @click="openDetail(c.id)"
              >
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
                  <button
                    type="button"
                    class="absolute right-3 top-3 inline-flex items-center justify-center rounded-full bg-white/95 p-2.5 text-slate-700 shadow-md transition hover:bg-white"
                    title="Vào học"
                    @click.stop="playFirst(c.id)"
                  >
                    <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M8 5v14l11-7z" />
                    </svg>
                  </button>
                  <div class="absolute bottom-0 left-0 right-0 bg-black/40 p-3">
                    <div class="mb-1.5 h-1 overflow-hidden rounded-full bg-white/30">
                      <div
                        class="h-full rounded-full bg-white transition-all duration-1000 ease-out"
                        :style="{ width: `${animatedProgress[String(c.id)] || 0}%` }"
                      ></div>
                    </div>
                    <p class="text-xs font-semibold text-white">{{ Math.round(animatedProgress[String(c.id)] || 0) }}% hoàn thành</p>
                  </div>
                </div>
                <div class="p-4">
                  <h3 class="mb-3 line-clamp-2 font-semibold text-slate-900">
                    {{ c.title }}
                  </h3>
                  <div class="flex items-center justify-between">
                    <span
                      class="inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium"
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
                    <div class="flex items-center gap-1 rounded-full bg-amber-50 px-2.5 py-1 border border-amber-200">
                      <span class="text-sm">🏆</span>
                      <span class="text-xs font-semibold text-amber-900">{{ c.score }}</span>
                    </div>
                  </div>
                </div>
              </article>
            </div>
          </section>
          </template>
        </template>

        <div v-else class="rounded-lg border-2 border-dashed border-slate-300 bg-slate-50 p-16 text-center">
          <div class="mx-auto max-w-md">
            <div class="mx-auto mb-4 h-20 w-20 rounded-full bg-slate-200 flex items-center justify-center">
              <svg class="h-10 w-10 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-slate-900">Chưa có khóa học nào</h3>
            <p class="mt-2 text-sm text-slate-600">Bắt đầu khám phá các khóa học mới ngay hôm nay!</p>
            <button
              type="button"
              class="mt-6 inline-flex items-center gap-2 rounded-lg bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
              @click="router.push({ name: 'student-catalog' })"
            >
              Khám phá khóa học
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
          </div>
        </div>
      </template>

      <!-- Supplementary Courses Tab -->
      <template v-else>
        <section v-if="suppList.length" class="mb-8">
          <div class="mb-6 flex items-center justify-between">
            <div>
              <h2 class="text-xl font-semibold text-slate-900">Khóa học bổ trợ</h2>
              <p class="mt-1 text-sm text-slate-600">{{ suppList.length }} khóa học</p>
            </div>
            <router-link
              class="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition"
              :to="{ name: 'student-catalog' }"
            >
              Tìm thêm
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </router-link>
          </div>

          <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <article
              v-for="s in suppList"
              :key="s.id"
              class="group overflow-hidden rounded-lg border border-slate-200 bg-white shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-y-1"
            >
              <div class="relative h-40 overflow-hidden bg-slate-200">
                <img 
                  v-if="s.thumbnail" 
                  class="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
                  :src="getThumbnailUrl(s.thumbnail)" 
                  :alt="s.title" 
                  @error="handleImageError"
                />
                <div v-else class="flex h-full w-full items-center justify-center">
                  <svg class="h-12 w-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <span
                  class="absolute left-3 top-3 rounded bg-white/95 px-2.5 py-1 text-xs font-semibold text-slate-900 shadow"
                >
                  {{ s.tag || (s.grade ? `Lớp ${s.grade}` : 'Bổ trợ') }}
                </span>
                <div
                  class="absolute right-3 top-3 rounded px-2.5 py-1 text-xs font-semibold shadow"
                  :class="(Number(s.price) || 0) === 0
                    ? 'bg-green-500 text-white'
                    : 'bg-amber-500 text-white'"
                >
                  {{ (Number(s.price) || 0) === 0 ? 'Miễn phí' : formatPrice(s.price) }}
                </div>
              </div>
              <div class="p-4 space-y-3">
                <h3 class="line-clamp-2 font-semibold text-slate-900">
                  {{ s.title }}
                </h3>
                <p class="text-sm text-slate-600">Phù hợp {{ toLevelLabel(s.grade) }}</p>
                <div class="flex flex-col gap-2 sm:flex-row">
                  <button
                    type="button"
                    class="flex-1 rounded-lg border border-slate-300 px-4 py-2 text-xs font-semibold text-slate-700 hover:bg-slate-50"
                    @click="openDetail(s.id)"
                  >
                    Xem chi tiết
                  </button>
                  <button
                    type="button"
                    class="flex-1 rounded-lg bg-slate-900 px-4 py-2 text-xs font-semibold text-white hover:bg-slate-800"
                    @click="enroll(s.id)"
                  >
                    Tham gia
                  </button>
                </div>
              </div>
            </article>
          </div>
        </section>
      </template>

      <!-- Empty State -->
      <div
        v-if="(activeTab === 'main' && mainCoursesCount === 0) || (activeTab === 'supp' && !suppList.length)"
        class="rounded-lg border-2 border-dashed border-slate-300 bg-slate-50 p-16 text-center"
      >
        <div class="mx-auto max-w-md">
          <div class="mx-auto mb-4 h-20 w-20 rounded-full bg-slate-200 flex items-center justify-center">
            <svg class="h-10 w-10 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-slate-900">Không có khóa học phù hợp</h3>
          <p class="mt-2 text-sm text-slate-600">Hãy thử thay đổi bộ lọc hoặc tìm kiếm khác</p>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="err" class="rounded-lg border border-red-200 bg-red-50 p-4">
        <div class="flex items-start gap-3">
          <svg class="h-5 w-5 shrink-0 text-red-600 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <p class="font-medium text-red-900">{{ err }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { courseService, type CourseSummary, type CourseDetail, type StudentMyCourse, type ID } from '@/services/course.service'
import { resolveMediaUrl } from '@/utils/media'

const router = useRouter()

/* Tabs */
const activeTab = ref<'main'|'supp'>('main')

/* Tìm kiếm / lọc */
const q = ref('')
const level = ref<'' | 'Khối 1–2' | 'Khối 3–5'>('')
const open = ref(false)
function setLevel(v: '' | 'Khối 1–2' | 'Khối 3–5'){ level.value = v; open.value = false }

const err = ref('')

/* Animation */
const animatedProgress = ref<Record<string, number>>({})
const mainCoursesCount = computed(() => gradeSections.value.reduce((sum, section) => sum + section.courses.length, 0))

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

/* ====== LOAD COURSES FROM SERVICE ====== */
type EnrolledItem = {
  id: ID
  title: string
  grade: number
  subject?: string
  teacherName?: string
  lessonsCount?: number
  enrollments?: number
  thumbnail?: string
  price?: number
  progress: number
  done: boolean
  score: string
  tag?: string
}

type SuggestionItem = CourseSummary & { tag?: string }

const enrolled = ref<EnrolledItem[]>([])
const suggestions = ref<SuggestionItem[]>([])
const detailsMap = ref(new Map<string, CourseDetail>())

function toLevelLabel(grade: number) { return grade <= 2 ? 'Khối 1–2' : 'Khối 3–5' }

function calcScore(progress: number) {
  const earned = Math.max(0, Math.min(5, Math.round(progress / 20)))
  return `${earned}/5`
}

function clampProgress(value?: number | null) {
  if (typeof value !== 'number' || Number.isNaN(value)) return 0
  return Math.max(0, Math.min(100, Math.round(value)))
}

function toGradeNumber(value: StudentMyCourse['grade']): number {
  const num = Number(value)
  if (!Number.isNaN(num) && num >= 1 && num <= 5) return num
  if (typeof value === 'string') {
    const match = value.match(/\d/)
    if (match) {
      const parsed = Number(match[0])
      if (!Number.isNaN(parsed) && parsed >= 1 && parsed <= 5) return parsed
    }
  }
  return 1
}

function normalizeEnrolledCourse(course: StudentMyCourse): EnrolledItem {
  const grade = toGradeNumber(course.grade)
  const progress = clampProgress(course.progress)
  const id = (course.id ?? '') as ID
  return {
    id,
    title: course.title || 'Khóa học',
    grade,
    subject: course.subject || '',
    teacherName: course.teacherName || '',
    lessonsCount: course.lessonsCount || 0,
    enrollments: course.enrollments || 0,
    thumbnail: course.thumbnail,
    price: course.price ?? 0,
    progress,
    done: course.done ?? progress >= 100,
    score: calcScore(progress),
    tag: (course.subject || '').toUpperCase()
  }
}

async function load() {
  try {
    err.value = ''
    const [myCourses, catalog] = await Promise.all([
      courseService.myCourses(),
      courseService.list({
        page: 1,
        pageSize: 20,
        status: 'published',
        sortBy: 'updatedAt',
        sortDir: 'descending'
      })
    ])

    enrolled.value = (myCourses.all || []).map(normalizeEnrolledCourse)
    suggestions.value = (catalog.items || []).map((item) => ({
      ...item,
      price: Number((item as any).price) || 0,
      tag: item.subject?.toUpperCase?.()
    }))
    
    // Animate progress bars and trophies
    await nextTick()
    enrolled.value.forEach((c) => {
      animateProgress(String(c.id), c.progress)
    })
    
  } catch (e: any) {
    err.value = e?.message || String(e)
  }
}

/* ====== FILTERING ====== */
const filteredMain = computed(() => {
  let arr = enrolled.value.slice()
  if (q.value) {
    const key = q.value.toLowerCase()
    arr = arr.filter(x => x.title.toLowerCase().includes(key))
  }
  if (level.value) {
    arr = arr.filter(x => toLevelLabel(x.grade) === level.value)
  }
  return arr
})
const gradeOrder = [1, 2, 3, 4, 5] as const
function parseScore(s: string){ const [a,b] = s.split('/').map(n=>parseInt(n)); return { earned: a||0, total: b||0 } }
function sumTrophies(list: EnrolledItem[]){ return list.reduce((acc,c)=>{ const s=parseScore(c.score); acc.earned+=s.earned; acc.total+=s.total; return acc }, {earned:0,total:0}) }
const gradeSections = computed(() => {
  return gradeOrder.map((grade) => {
    const courses = filteredMain.value.filter((c) => c.grade === grade)
    return {
      grade,
      title: `Lớp ${grade}`,
      subtitle: grade <= 2 ? 'Cơ bản' : 'Nâng cao',
      courses,
      trophies: sumTrophies(courses),
    }
  })
})
const hasMainCourses = computed(() => gradeSections.value.some((section) => section.courses.length > 0))

/** Supp tab */
const enrolledIdSet = computed(() => new Set(enrolled.value.map(c => String(c.id))))
const suppList = computed(() => {
  let arr = suggestions.value
    .filter(c => !enrolledIdSet.value.has(String(c.id)))
    .map(c => ({ ...c, tag: c.tag || 'Bổ trợ' }))
  if (level.value) arr = arr.filter(s => toLevelLabel(s.grade) === level.value)
  if (q.value){
    const key=q.value.toLowerCase()
    arr = arr.filter(s => s.title.toLowerCase().includes(key) || (s.tag||'').toLowerCase().includes(key))
  }
  return arr
})

/* ====== ACTIONS ====== */
function openDetail(id: number | string){
  if (router.hasRoute('student-course-detail')) router.push({ name:'student-course-detail', params:{ id } })
  else router.push(`/student/courses/${id}`)
}

async function playFirst(id: number | string){
  let d = detailsMap.value.get(String(id))
  if (!d) {
    d = await courseService.detail(id)
    detailsMap.value.set(String(id), d)
  }
  const first = d.sections?.[0]?.lessons?.[0]?.id
  if (!first) return openDetail(id)
  if (router.hasRoute('student-course-player'))
    router.push({ name:'student-course-player', params:{ id, lessonId: first } })
  else
    router.push(`/student/courses/${id}/player/${first}`)
}


async function enroll(id: number | string){
  try {
    const course = await courseService.detail(id)
    const price = Number(course.price) || 0
    
    // Nếu khóa học miễn phí, enroll trực tiếp
    if (price === 0) {
      try {
        await courseService.enroll(id)
        await load() // Reload danh sách
        // Sau khi enroll thành công, tự động mở khóa học để xem
        playFirst(id)
      } catch (e: any) {
        alert(e?.message || 'Đăng ký khóa học thất bại')
      }
    } else {
      // Nếu có phí, thêm vào giỏ hàng
      if (router.hasRoute('student-payments-cart')) {
        router.push({ name: 'student-payments-cart', query: { add: String(id) } })
      } else {
        router.push({ path: '/student/payments/cart', query: { add: String(id) } })
      }
    }
  } catch (e: any) {
    alert(e?.message || 'Không thể đăng ký khóa học')
  }
}

const getThumbnailUrl = (thumbnail?: string) => resolveMediaUrl(thumbnail)

function handleImageError(event: Event) {
  const img = event.target as HTMLImageElement
  img.src = 'https://placehold.co/400x300?text=No+Image'
}

function formatPrice(price?: number | string): string {
  if (!price || price === 0 || price === '0') return 'Miễn phí'
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(numPrice)
}

onMounted(load)
</script>
