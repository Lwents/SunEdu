<template>
  <div class="min-h-screen bg-slate-50 pb-16 pt-10">
    <div class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
      <header class="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p class="text-sm font-semibold uppercase tracking-[0.2em] text-cyan-500 dark:text-cyan-400">
            Practice zone
          </p>
          <h1 class="text-3xl font-black text-slate-900 sm:text-4xl">Kho đề luyện tập</h1>
          <p class="mt-2 max-w-2xl text-base text-slate-600">
            Chọn một đề thi để bắt đầu thử thách và nâng cao kỹ năng của bạn.
          </p>
        </div>
        <div class="flex w-full flex-col gap-3 sm:flex-row sm:items-center lg:w-auto">
          <div class="relative flex-1">
            <span class="pointer-events-none absolute inset-y-0 left-3 flex items-center text-slate-400">
              <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
              </svg>
            </span>
            <input
              v-model.trim="q"
              @keydown.enter="applyFilters"
              placeholder="Tìm kiếm theo tên đề..."
              class="w-full rounded-2xl border border-slate-200 bg-white px-11 py-3 text-sm font-medium text-slate-900 shadow-sm shadow-slate-100 transition focus:border-cyan-500 dark:border-cyan-600 focus-visible:outline-none focus:ring-4 focus:ring-cyan-500/30"
            />
          </div>
          <div class="relative">
            <button
              type="button"
              class="inline-flex w-full items-center justify-between gap-2 rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm font-semibold text-slate-700 shadow-sm shadow-slate-100 transition hover:border-cyan-300 dark:border-cyan-600 focus:border-cyan-500 dark:border-cyan-600 focus-visible:outline-none focus:ring-4 focus:ring-cyan-500/30 sm:w-56"
              @click="open = !open"
              :aria-expanded="open"
            >
              <span>{{ levelLabel || 'Tất cả cấp độ' }}</span>
              <svg
                class="h-4 w-4 transition"
                :class="{ 'rotate-180': open }"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="2"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 15 12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9" />
              </svg>
            </button>
            <ul
              v-if="open"
              class="absolute right-0 z-20 mt-2 w-full rounded-2xl border border-slate-200 bg-white p-2 shadow-xl shadow-slate-200"
              @mouseleave="open = false"
            >
              <li
                v-for="(opt, idx) in levelOptions"
                :key="idx"
                class="cursor-pointer rounded-xl px-3 py-2 text-sm font-semibold text-slate-600 transition hover:bg-slate-50"
                @click="setLevel(opt.value)"
              >
                {{ opt.label }}
              </li>
            </ul>
          </div>
        </div>
      </header>

      <div v-if="loading" class="mt-10 grid gap-6 sm:grid-cols-2">
        <div
          v-for="i in pageSize"
          :key="i"
          class="h-48 animate-pulse rounded-3xl border border-slate-200 bg-white"
        ></div>
      </div>

      <div v-else-if="exams.length" class="mt-10 grid gap-6 sm:grid-cols-2">
        <article
          v-for="e in exams"
          :key="e.id"
          class="flex h-full flex-col justify-between rounded-3xl border border-slate-200 bg-white/90 p-5 shadow-lg shadow-slate-100 transition hover:-translate-y-1 hover:shadow-2xl"
        >
          <div class="space-y-4">
            <span
              :class="[
                'inline-flex items-center rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wide',
                getSubjectClass(subj(e)),
              ]"
            >
              {{ subj(e) }}
            </span>
            <h2 class="text-xl font-bold text-slate-900">{{ e.title }}</h2>
            <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm font-medium text-slate-500">
              <span>{{ qCount(e) }} câu</span>
              <span class="text-slate-300">•</span>
              <span>{{ toMin(e.durationSec) }} phút</span>
              <span class="text-slate-300">•</span>
              <span>Đạt ≥ {{ e.passCount }} câu</span>
            </div>
          </div>
          <div class="mt-6 flex items-center justify-between rounded-2xl bg-slate-50/70 px-4 py-3">
            <span
              :class="[
                'rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wide',
                e.level === 'advanced'
                  ? 'bg-rose-100 text-rose-700'
                  : 'bg-cyan-100 dark:bg-cyan-900/30 text-cyan-700 dark:text-cyan-300',
              ]"
            >
              {{ labelLevel(e.level) }}
            </span>
            <router-link
              class="relative inline-flex items-center justify-center rounded-2xl bg-slate-900 px-6 py-2 text-sm font-semibold text-white transition hover:bg-slate-700"
              :to="{ name: 'student-exam-detail', params: { id: e.id } }"
            >
              <span class="pointer-events-none">Bắt đầu</span>
              <svg class="absolute right-3 h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5 21 12l-7.5 7.5M21 12H3" />
              </svg>
            </router-link>
          </div>
        </article>
      </div>

      <div v-else class="mt-16 flex flex-col items-center rounded-3xl border border-dashed border-slate-200 bg-white/80 px-6 py-14 text-center">
        <img
          src="https://res.cloudinary.com/dapvicdpm/image/upload/v1727116801/temp/no-results_s3fb6c.svg"
          alt="Không có dữ liệu"
          class="h-32 w-32"
        />
        <h3 class="mt-6 text-xl font-bold text-slate-900">Không tìm thấy đề thi phù hợp</h3>
        <p class="mt-2 max-w-md text-sm text-slate-500">
          Vui lòng thử lại với từ khóa hoặc bộ lọc khác.
        </p>
      </div>
    </div>

    <div
      v-if="totalPages > 1"
      class="mt-12 flex items-center justify-center gap-2 px-4"
    >
      <button
        class="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-sm font-bold text-slate-600 transition hover:border-cyan-300 dark:border-cyan-600 disabled:cursor-not-allowed disabled:opacity-40"
        :disabled="page <= 1"
        @click="go(page - 1)"
      >
        ‹
      </button>
      <button
        v-for="p in pagesToShow"
        :key="p.key"
        class="inline-flex h-10 min-w-[40px] items-center justify-center rounded-xl border text-sm font-semibold transition"
        :class="p.sep
          ? 'border-transparent bg-transparent text-slate-400'
          : p.num === page
            ? 'border-cyan-500 dark:border-cyan-600 bg-cyan-50 dark:bg-cyan-900/200 text-white shadow-lg shadow-ocean-glow'
            : 'border-slate-200 bg-white text-slate-700 hover:border-cyan-300 dark:border-cyan-600'"
        :disabled="p.sep"
        @click="!p.sep && go(p.num!)"
      >
        {{ p.text }}
      </button>
      <button
        class="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-slate-200 bg-white text-sm font-bold text-slate-600 transition hover:border-cyan-300 dark:border-cyan-600 disabled:cursor-not-allowed disabled:opacity-40"
        :disabled="page >= totalPages"
        @click="go(page + 1)"
      >
        ›
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useExamStore } from '@/store/exam.store'
import { storeToRefs } from 'pinia'

const store = useExamStore()
const { exams, total, page, pageSize, loading } = storeToRefs(store)

const q = ref(store.q)
const level = ref<'' | 'basic' | 'advanced'>(store.level)
const open = ref(false)
const levelOptions: Array<{ value: '' | 'basic' | 'advanced'; label: string }> = [
  { value: '', label: 'Tất cả cấp độ' },
  { value: 'basic', label: 'Cơ bản' },
  { value: 'advanced', label: 'Nâng cao' },
]

const levelLabel = computed(() =>
  level.value === 'basic' ? 'Cơ bản' : level.value === 'advanced' ? 'Nâng cao' : ''
)

function setLevel(v: '' | 'basic' | 'advanced') {
  level.value = v
  open.value = false
  applyFilters()
}

function applyFilters() {
  store.q = q.value
  store.level = level.value
  store.fetchExamsPage(1, pageSize.value)
}

onMounted(() => {
  store.fetchExamsPage()
})

function go(p: number) {
  store.fetchExamsPage(p, pageSize.value)
}

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))

const pagesToShow = computed(() => {
  const max = totalPages.value
  const cur = page.value
  const windowSize = 5
  const arr: { key: string; num?: number; text: string; sep?: boolean }[] = []

  const push = (n: number) => arr.push({ key: 'p' + n, num: n, text: String(n) })
  const sep = (k: string) => arr.push({ key: k, text: '…', sep: true })

  if (max <= windowSize + 2) {
    for (let i = 1; i <= max; i++) push(i)
  } else {
    push(1)
    const start = Math.max(2, cur - 1)
    const end = Math.min(max - 1, cur + 1)
    if (start > 2) sep('s')
    for (let i = start; i <= end; i++) push(i)
    if (end < max - 1) sep('e')
    push(max)
  }
  return arr
})

// --- Helpers ---
function qCount(e: any) { return (e?.questionsCount ?? e?.questions ?? 0) as number }
function toMin(s: number) { return Math.round(s / 60) }
function labelLevel(l: 'basic' | 'advanced') { return l === 'advanced' ? 'Nâng cao' : 'Cơ bản' }

// Định nghĩa một đối tượng để map giá trị subject với nhãn hiển thị
const subjectLabels: Record<string, string> = {
  math: 'Toán học',
  vietnamese: 'Tiếng Việt',
  english: 'Tiếng Anh',
  science: 'Khoa học'
};
const subjectBadgeMap: Record<string, string> = {
  math: 'bg-rose-500/90 text-white',
  vietnamese: 'bg-amber-500 text-white',
  english: 'bg-blue-500 text-white',
  science: 'bg-teal-500 text-white',
  default: 'bg-slate-500 text-white'
}

function subj(e: any) {
  if (e && 'subject' in e && e.subject) {
    return labelSubject(e.subject);
  }
  return e?.level === 'advanced' ? 'Nâng cao' : 'Cơ bản';
}

function labelSubject(s: keyof typeof subjectLabels) {
  return subjectLabels[s] || 'Khác';
}

// THÊM HÀM MỚI ĐỂ SỬA LỖI
function getSubjectClass(subjectLabel: string) {
  const subjectKey = Object.keys(subjectLabels).find((key) => subjectLabels[key] === subjectLabel)
  return subjectBadgeMap[subjectKey as keyof typeof subjectBadgeMap] || subjectBadgeMap.default
}


watch(pageSize, () => store.fetchExamsPage(1, pageSize.value))
</script>
