<template>
  <div class="min-h-screen bg-slate-50 pb-16 pt-10">
    <div class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">Kho đề luyện tập</h1>
        <p class="text-slate-600">Chọn một đề thi để bắt đầu thử thách và nâng cao kỹ năng của bạn</p>
      </div>

      <!-- Filters -->
      <div class="mb-6 flex flex-col sm:flex-row gap-4">
        <div class="relative flex-1">
          <span class="pointer-events-none absolute inset-y-0 left-3 flex items-center text-slate-400">
            <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
            </svg>
          </span>
          <input
            v-model.trim="q"
            @keydown.enter="applyFilters"
            placeholder="Tìm kiếm theo tên đề..."
            class="w-full rounded-lg border border-slate-300 bg-white px-10 py-2.5 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
          />
        </div>
        <div class="relative">
          <button
            type="button"
            class="inline-flex w-full items-center justify-between gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-200 sm:w-48"
            @click="open = !open"
          >
            <span>{{ levelLabel || 'Tất cả cấp độ' }}</span>
            <svg
              class="h-4 w-4 transition"
              :class="{ 'rotate-180': open }"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <ul
            v-if="open"
            class="absolute right-0 z-20 mt-2 w-full rounded-lg border border-slate-200 bg-white p-2 shadow-lg"
            @mouseleave="open = false"
          >
            <li
              v-for="(opt, idx) in levelOptions"
              :key="idx"
              class="cursor-pointer rounded-lg px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-50"
              @click="setLevel(opt.value)"
            >
              {{ opt.label }}
            </li>
          </ul>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="grid gap-4 sm:grid-cols-2">
        <div
          v-for="i in pageSize"
          :key="i"
          class="h-48 animate-pulse rounded-lg border border-slate-200 bg-white"
        ></div>
      </div>

      <!-- Exam Cards -->
      <div v-else-if="exams.length" class="grid gap-4 sm:grid-cols-2">
        <article
          v-for="e in exams"
          :key="e.id"
          class="flex flex-col justify-between rounded-lg border border-slate-200 bg-white p-5 shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-y-1 cursor-pointer"
        >
          <div class="space-y-3 mb-4">
            <span
              :class="[
                'inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold',
                getSubjectClass(subj(e)),
              ]"
            >
              {{ subj(e) }}
            </span>
            <h2 class="text-lg font-semibold text-slate-900">{{ e.title }}</h2>
            <div class="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-slate-600">
              <span>{{ qCount(e) }} câu</span>
              <span class="text-slate-300">•</span>
              <span>{{ toMin(e.durationSec) }} phút</span>
              <span class="text-slate-300">•</span>
              <span>Đạt ≥ {{ e.passCount }} câu</span>
            </div>
          </div>
          <div class="flex items-center justify-between rounded-lg bg-slate-50 px-4 py-3">
            <span
              :class="[
                'rounded-full px-3 py-1 text-xs font-semibold',
                e.level === 'advanced'
                  ? 'bg-red-100 text-red-700'
                  : 'bg-blue-100 text-blue-700',
              ]"
            >
              {{ labelLevel(e.level) }}
            </span>
            <router-link
              class="inline-flex items-center justify-center rounded-lg bg-slate-900 px-5 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
              :to="{ name: 'student-exam-detail', params: { id: e.id } }"
            >
              Bắt đầu
              <svg class="ml-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </router-link>
          </div>
        </article>
      </div>

      <!-- Empty State -->
      <div v-else class="mt-16 flex flex-col items-center rounded-lg border border-dashed border-slate-300 bg-white px-6 py-14 text-center">
        <div class="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mb-4">
          <svg class="w-10 h-10 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-slate-900 mb-2">Không tìm thấy đề thi phù hợp</h3>
        <p class="text-sm text-slate-500">Vui lòng thử lại với từ khóa hoặc bộ lọc khác</p>
      </div>

      <!-- Pagination -->
      <div
        v-if="totalPages > 1"
        class="mt-8 flex items-center justify-center gap-2"
      >
        <button
          class="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-slate-300 bg-white text-sm font-medium text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
          :disabled="page <= 1"
          @click="go(page - 1)"
        >
          ‹
        </button>
        <button
          v-for="p in pagesToShow"
          :key="p.key"
          class="inline-flex h-9 min-w-[36px] items-center justify-center rounded-lg border text-sm font-medium transition"
          :class="p.sep
            ? 'border-transparent bg-transparent text-slate-400'
            : p.num === page
              ? 'border-slate-900 bg-slate-900 text-white'
              : 'border-slate-300 bg-white text-slate-700 hover:bg-slate-50'"
          :disabled="p.sep"
          @click="!p.sep && go(p.num!)"
        >
          {{ p.text }}
        </button>
        <button
          class="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-slate-300 bg-white text-sm font-medium text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-40"
          :disabled="page >= totalPages"
          @click="go(page + 1)"
        >
          ›
        </button>
      </div>
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

const subjectLabels: Record<string, string> = {
  math: 'Toán học',
  vietnamese: 'Tiếng Việt',
  english: 'Tiếng Anh',
  science: 'Khoa học'
}
const subjectBadgeMap: Record<string, string> = {
  math: 'bg-red-100 text-red-700',
  vietnamese: 'bg-amber-100 text-amber-700',
  english: 'bg-blue-100 text-blue-700',
  science: 'bg-teal-100 text-teal-700',
  default: 'bg-slate-100 text-slate-700'
}

function subj(e: any) {
  if (e && 'subject' in e && e.subject) {
    return labelSubject(e.subject)
  }
  return e?.level === 'advanced' ? 'Nâng cao' : 'Cơ bản'
}

function labelSubject(s: keyof typeof subjectLabels) {
  return subjectLabels[s] || 'Khác'
}

function getSubjectClass(subjectLabel: string) {
  const subjectKey = Object.keys(subjectLabels).find((key) => subjectLabels[key] === subjectLabel)
  return subjectBadgeMap[subjectKey as keyof typeof subjectBadgeMap] || subjectBadgeMap.default
}

watch(pageSize, () => store.fetchExamsPage(1, pageSize.value))
</script>
