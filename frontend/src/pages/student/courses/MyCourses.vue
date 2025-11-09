<!-- src/pages/student/courses/MyCourses.vue -->
<template>
  <div class="student-shell">
    <div class="student-container">
      <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p class="student-section-title">Học tập</p>
          <h1 class="text-3xl font-black text-brand-deep">Khoá học của tôi</h1>
          <p class="mt-2 text-sm text-brand-muted">
            Các khóa học bạn đang sở hữu được chia theo từng cấp trình độ, tương ứng với mỗi chặng mục tiêu.
            Hãy chọn trình độ mà bạn muốn bắt đầu nhé.
          </p>
        </div>
        <div class="flex gap-2">
          <router-link
            class="inline-flex items-center rounded-2xl border border-slate-200 px-4 py-2 text-sm font-semibold text-brand-600 transition hover:bg-slate-50"
            :to="{ name: 'student-learning-path' }"
          >
            Lộ trình
          </router-link>
          <router-link
            class="inline-flex items-center rounded-2xl border border-slate-200 px-4 py-2 text-sm font-semibold text-brand-600 transition hover:bg-slate-50"
            :to="{ name: 'student-catalog' }"
          >
            Catalog
          </router-link>
        </div>
      </div>

      <div
        class="mt-6 flex flex-col gap-4 rounded-3xl border border-slate-200/80 bg-white/90 p-4 shadow-sm shadow-slate-100 sm:p-5 lg:flex-row lg:items-center lg:justify-between"
      >
        <div class="flex gap-2">
          <button
            class="student-tab"
            :class="{ 'student-tab--active': activeTab === 'main' }"
            @click="activeTab = 'main'"
          >
            Khóa học chính
          </button>
          <button
            class="student-tab"
            :class="{ 'student-tab--active': activeTab === 'supp' }"
            @click="activeTab = 'supp'"
          >
            Khóa học bổ trợ
          </button>
        </div>

        <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
          <div class="relative" @mouseleave="open = false">
            <button
              type="button"
              class="inline-flex w-full items-center justify-between gap-3 rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-brand-deep shadow-sm shadow-slate-100 transition hover:border-brand-300 focus:border-brand-500 focus:outline-none focus:ring-4 focus:ring-brand-100 sm:w-56"
              @click="open = !open"
            >
              <span>{{ level || 'Tất cả trình độ' }}</span>
              <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M6 9l6 6 6-6" />
              </svg>
            </button>
            <ul
              v-show="open"
              class="absolute z-20 mt-2 w-full rounded-2xl border border-slate-200 bg-white p-2 shadow-xl shadow-slate-200"
            >
              <li
                v-for="lvl in ['', 'Khối 1–2', 'Khối 3–5']"
                :key="lvl || 'all'"
                class="cursor-pointer rounded-xl px-3 py-2 text-sm font-semibold text-brand-muted transition hover:bg-slate-50 hover:text-brand-600"
                @click="setLevel(lvl as '' | 'Khối 1–2' | 'Khối 3–5')"
              >
                {{ lvl || 'Tất cả trình độ' }}
              </li>
            </ul>
          </div>

            <div class="flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-brand-deep shadow-sm shadow-slate-100">
              <svg class="h-4 w-4 text-brand-muted" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 21l-4.3-4.3" />
                <circle cx="11" cy="11" r="7" />
              </svg>
              <input
                v-model.trim="q"
                placeholder="Tìm khóa học..."
                class="w-full border-none bg-transparent text-sm font-medium text-brand-deep placeholder:text-brand-muted focus:outline-none"
              />
            </div>
        </div>
      </div>

      <template v-if="activeTab === 'main'">
        <section v-if="baseList.length" class="student-card mt-6 space-y-6">
          <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h3 class="text-xl font-bold text-brand-deep">Khối 1–2 (Cơ bản)</h3>
              <p class="text-sm text-brand-muted">{{ baseList.length }} môn</p>
            </div>
            <div class="flex items-center gap-3 text-sm font-semibold text-brand-muted">
              <span>🏆 {{ baseTrophies.earned }}/{{ baseTrophies.total }}</span>
              <router-link
                class="student-link text-sm"
                :to="{ name: 'student-catalog', query: { grade: 1 } }"
              >
                Xem tất cả ›
              </router-link>
            </div>
          </div>

          <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <article
              v-for="c in baseList"
              :key="c.id"
              class="group flex flex-col rounded-3xl border border-slate-200 bg-white/90 p-4 shadow-sm shadow-slate-100 transition hover:-translate-y-1 hover:shadow-xl"
              @click="openDetail(c.id)"
            >
              <div class="relative overflow-hidden rounded-2xl">
                <img :src="c.thumbnail" :alt="c.title" class="h-40 w-full object-cover" />
                <button
                  type="button"
                  class="absolute right-3 top-3 inline-flex items-center justify-center rounded-full bg-white/90 p-2 text-brand-600 shadow-lg shadow-slate-300 transition hover:scale-105"
                  title="Vào học"
                  @click.stop="playFirst(c.id)"
                >
                  <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8 5v14l11-7z" />
                  </svg>
                </button>
              </div>
              <div class="mt-4 space-y-3">
                <h4 class="text-base font-semibold text-brand-deep line-clamp-2">{{ c.title }}</h4>
                <div class="flex items-center justify-between text-sm text-brand-muted">
                  <span class="inline-flex items-center gap-2 font-semibold" :class="c.done ? 'text-brand-600' : ''">
                    <span class="h-2 w-2 rounded-full" :class="c.done ? 'bg-brand-500' : 'bg-amber-400'"></span>
                    {{ c.done ? 'Đã hoàn thành' : `Đang học · ${c.progress}%` }}
                  </span>
                  <span class="font-semibold text-brand-deep">🏆 {{ c.score }}</span>
                </div>
              </div>
            </article>
          </div>
        </section>

        <section v-if="midList.length" class="student-card mt-6 space-y-6">
          <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h3 class="text-xl font-bold text-brand-deep">Khối 3–5 (Nâng cao)</h3>
              <p class="text-sm text-brand-muted">{{ midList.length }} môn</p>
            </div>
            <div class="flex items-center gap-3 text-sm font-semibold text-brand-muted">
              <span>🏆 {{ midTrophies.earned }}/{{ midTrophies.total }}</span>
              <router-link
                class="student-link text-sm"
                :to="{ name: 'student-catalog', query: { grade: 3 } }"
              >
                Xem tất cả ›
              </router-link>
            </div>
          </div>

          <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <article
              v-for="c in midList"
              :key="c.id"
              class="group flex flex-col rounded-3xl border border-slate-200 bg-white/90 p-4 shadow-sm shadow-slate-100 transition hover:-translate-y-1 hover:shadow-xl"
              @click="openDetail(c.id)"
            >
              <div class="relative overflow-hidden rounded-2xl">
                <img :src="c.thumbnail" :alt="c.title" class="h-40 w-full object-cover" />
                <button
                  type="button"
                  class="absolute right-3 top-3 inline-flex items-center justify-center rounded-full bg-white/90 p-2 text-brand-600 shadow-lg shadow-slate-300 transition hover:scale-105"
                  title="Vào học"
                  @click.stop="playFirst(c.id)"
                >
                  <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M8 5v14l11-7z" />
                  </svg>
                </button>
              </div>
              <div class="mt-4 space-y-3">
                <h4 class="text-base font-semibold text-brand-deep line-clamp-2">{{ c.title }}</h4>
                <div class="flex items-center justify-between text-sm text-brand-muted">
                  <span class="inline-flex items-center gap-2 font-semibold" :class="c.done ? 'text-brand-600' : ''">
                    <span class="h-2 w-2 rounded-full" :class="c.done ? 'bg-brand-500' : 'bg-amber-400'"></span>
                    {{ c.done ? 'Đã hoàn thành' : `Đang học · ${c.progress}%` }}
                  </span>
                  <span class="font-semibold text-brand-deep">🏆 {{ c.score }}</span>
                </div>
              </div>
            </article>
          </div>
        </section>
      </template>

      <template v-else>
        <section class="student-card mt-6 space-y-6">
          <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h3 class="text-xl font-bold text-brand-deep">Khóa học bổ trợ</h3>
              <p class="text-sm text-brand-muted">{{ suppList.length }} khóa</p>
            </div>
            <router-link class="student-link text-sm" :to="{ name: 'student-catalog' }">
              Tìm thêm ›
            </router-link>
          </div>

          <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <article
              v-for="s in suppList"
              :key="s.id"
              class="flex flex-col overflow-hidden rounded-3xl border border-slate-200 bg-white/90 shadow-sm shadow-slate-100 transition hover:-translate-y-1 hover:shadow-xl"
              @click="enroll(s.id)"
            >
              <div class="relative h-40 w-full overflow-hidden">
                <img :src="s.thumbnail" :alt="s.title" class="h-full w-full object-cover" />
                <span class="absolute left-3 top-3 rounded-full bg-white/90 px-3 py-1 text-xs font-semibold text-brand-deep">
                  {{ s.tag }}
                </span>
              </div>
              <div class="flex flex-1 flex-col space-y-3 p-4">
                <h4 class="text-base font-semibold text-brand-deep line-clamp-2">{{ s.title }}</h4>
                <div class="mt-auto flex items-center justify-between text-sm text-brand-muted">
                  <span class="inline-flex items-center gap-2 font-semibold text-brand-600">
                    <span class="h-2 w-2 rounded-full bg-brand-500"></span>
                    Phù hợp {{ toLevelLabel(s.grade) }}
                  </span>
                  <button
                    type="button"
                    class="rounded-2xl border border-brand-200 px-4 py-1.5 text-xs font-semibold text-brand-600 transition hover:bg-brand-50"
                    @click.stop="enroll(s.id)"
                  >
                    Tham gia
                  </button>
                </div>
              </div>
            </article>
          </div>
        </section>
      </template>

      <div
        v-if="activeTab === 'main' && (baseList.length || midList.length)"
        class="mt-6 flex flex-wrap items-center gap-3 rounded-3xl border border-slate-200 bg-white/80 px-4 py-3 text-sm text-brand-deep shadow-sm shadow-slate-100"
      >
        <span>🏆 Tổng số cúp đã đạt</span>
        <b>{{ baseTrophies.earned + midTrophies.earned }}/{{ baseTrophies.total + midTrophies.total }}</b>
      </div>

      <div
        v-if="(activeTab === 'main' && baseList.length + midList.length === 0) || (activeTab === 'supp' && !suppList.length)"
        class="mt-6 rounded-3xl border border-dashed border-slate-200 bg-white/80 px-6 py-10 text-center text-sm text-brand-muted"
      >
        Không có khóa học phù hợp.
      </div>

      <div v-if="err" class="mt-4 rounded-3xl border border-rose-200 bg-rose-50/80 px-4 py-3 text-sm text-rose-700">
        {{ err }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { courseService, type CourseSummary, type CourseDetail } from '@/services/course.service'

const router = useRouter()

/* Tabs */
const activeTab = ref<'main'|'supp'>('main')

/* Tìm kiếm / lọc */
const q = ref('')
const level = ref<'' | 'Khối 1–2' | 'Khối 3–5'>('')
const open = ref(false)
function setLevel(v: '' | 'Khối 1–2' | 'Khối 3–5'){ level.value = v; open.value = false }

const err = ref('')

/* ====== LOAD COURSES FROM SERVICE ====== */
type Item = CourseSummary & {
  progress: number
  done: boolean
  score: string
  tag?: string
  isPurchased?: boolean
}

const all = ref<Item[]>([])
const detailsMap = ref(new Map<string, CourseDetail>())

function toLevelLabel(grade: number) { return grade <= 2 ? 'Khối 1–2' : 'Khối 3–5' }

function calcScore(progress: number) {
  const earned = Math.max(0, Math.min(5, Math.round(progress / 20)))
  return `${earned}/5`
}

function calcProgressFromDetail(d: CourseDetail, id: number | string) {
  const total = d.lessonsCount || d.sections?.reduce((a, s) => a + (s.lessons?.length || 0), 0) || 0
  let done = Number(id) % (total || 1)
  if (total > 0 && done === 0) done = total
  const pct = total ? Math.round((done / total) * 100) : 0
  return Math.max(0, Math.min(100, pct))
}

async function load() {
  try {
    const { items } = await courseService.list({
      page: 1, pageSize: 20,
      status: 'published', sortBy: 'updatedAt', sortDir: 'descending'
    })

    const limited = (items || []).slice(0, 24)
    const details = await Promise.all(limited.map(i => courseService.detail(i.id)))
    const map = new Map<string, CourseDetail>()
    details.forEach(d => map.set(String(d.id), d))
    detailsMap.value = map

    all.value = (items || []).map(i => {
      const d = map.get(String(i.id))
      const progress = d ? calcProgressFromDetail(d, i.id) : ((Number(i.id) * 13) % 100)
      
      const isPurchased = i.grade <= 2
      
      return {
        ...i,
        progress,
        done: progress >= 100,
        score: calcScore(progress),
        tag: i.subject?.toUpperCase?.(),
        isPurchased
      }
    })
  } catch (e: any) {
    err.value = e?.message || String(e)
  }
}

/* ====== FILTERING ====== */
const filteredMain = computed(() => {
  let arr = all.value.slice()
  if (q.value) {
    const key = q.value.toLowerCase()
    arr = arr.filter(x => x.title.toLowerCase().includes(key))
  }
  if (level.value) {
    arr = arr.filter(x => toLevelLabel(x.grade) === level.value)
  }
  return arr
})
const baseList = computed(()=> filteredMain.value.filter(x=> x.grade <= 2))
const midList  = computed(()=> filteredMain.value.filter(x=> x.grade >= 3))
function parseScore(s: string){ const [a,b] = s.split('/').map(n=>parseInt(n)); return { earned: a||0, total: b||0 } }
function sumTrophies(list: Item[]){ return list.reduce((acc,c)=>{ const s=parseScore(c.score); acc.earned+=s.earned; acc.total+=s.total; return acc }, {earned:0,total:0}) }
const baseTrophies = computed(()=> sumTrophies(baseList.value))
const midTrophies  = computed(()=> sumTrophies(midList.value))

/** Supp tab */
const suppList = computed(() => {
  let arr = all.value.slice().map(c => ({ ...c, tag: c.tag || 'Bổ trợ' }))
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


function enroll(id: number | string){
  if (router.hasRoute('student-payments-cart')) router.push({ name: 'student-payments-cart', query: { add: String(id) } })
  else router.push({ path: '/student/payments/cart', query: { add: String(id) } })
}

onMounted(load)
</script>
