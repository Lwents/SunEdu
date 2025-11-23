<!-- src/pages/teacher/exams/Exams.vue -->
<template>
  <div class="min-h-screen w-full overflow-x-hidden bg-slate-50">
    <main class="w-full mx-auto max-w-screen-2xl px-4 py-6 sm:px-6 md:px-10 md:py-8">
      <!-- Header -->
      <div class="mb-4 sm:mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h1 class="text-xl font-semibold sm:text-2xl">Bài kiểm tra</h1>
        <button
          class="w-full sm:w-auto rounded-lg bg-slate-900 px-4 py-2.5 font-semibold text-white hover:bg-slate-800"
          @click="createExam"
        >
          + Tạo bài kiểm tra
        </button>
      </div>

      <!-- Tools -->
      <div class="mb-5 grid grid-cols-1 gap-2 sm:gap-3 md:grid-cols-3">
        <!-- Search -->
        <div class="md:col-span-2">
          <label class="flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-3 py-2.5">
            <svg viewBox="0 0 24 24" class="h-5 w-5 shrink-0 text-slate-400" fill="none" stroke="currentColor" aria-hidden="true">
              <circle cx="11" cy="11" r="8" stroke-width="2" />
              <path d="M21 21l-4.3-4.3" stroke-width="2" />
            </svg>
            <input
              v-model.trim="q"
              type="text"
              placeholder="Tìm đề theo tên/khoá…"
              class="w-full bg-transparent outline-none text-sm sm:text-base"
              @input="debouncedFetch"
            />
          </label>
        </div>

        <!-- Filters -->
        <div class="grid grid-cols-2 gap-2">
          <!-- Status -->
          <div class="relative">
            <select
              v-model="status"
              class="select-base"
              @change="fetchList(1)"
            >
              <option value="">Tất cả trạng thái</option>
              <option value="published">Đã phát hành</option>
              <option value="scheduled">Đã lên lịch</option>
              <option value="draft">Nháp</option>
            </select>
            <span class="select-chevron" aria-hidden="true">
              <svg viewBox="0 0 20 20" fill="currentColor" class="h-4 w-4">
                <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.17l3.71-2.94a.75.75 0 111.04 1.08l-4.24 3.36a.75.75 0 01-.94 0L5.21 8.31a.75.75 0 01.02-1.1z" clip-rule="evenodd"/>
              </svg>
            </span>
          </div>

          <!-- Sort -->
          <div class="relative">
            <select
              v-model="sort"
              class="select-base"
              @change="fetchList(1)"
            >
              <option value="updated">Mới cập nhật</option>
              <option value="title">A → Z</option>
              <option value="subs">Bài nộp nhiều</option>
            </select>
            <span class="select-chevron" aria-hidden="true">
              <svg viewBox="0 0 20 20" fill="currentColor" class="h-4 w-4">
                <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.17l3.71-2.94a.75.75 0 111.04 1.08l-4.24 3.36a.75.75 0 01-.94 0L5.21 8.31a.75.75 0 01.02-1.1z" clip-rule="evenodd"/>
              </svg>
            </span>
          </div>
        </div>
      </div>

      <!-- Loading skeleton -->
      <div v-if="loading" class="grid grid-cols-1 gap-3 sm:gap-4">
        <div
          v-for="i in pageSize"
          :key="'skel-'+i"
          class="flex items-center gap-3 sm:gap-4 rounded-2xl border border-slate-200 bg-white p-3 sm:p-4"
        >
          <div class="h-12 w-12 sm:h-16 sm:w-16 rounded-xl bg-slate-200 animate-pulse"></div>
          <div class="min-w-0 flex-1">
            <div class="h-4 w-44 sm:w-56 rounded bg-slate-200 animate-pulse mb-2"></div>
            <div class="h-3 w-60 sm:w-80 rounded bg-slate-100 animate-pulse"></div>
          </div>
          <div class="h-8 w-20 sm:w-24 rounded bg-slate-100 animate-pulse"></div>
        </div>
      </div>

      <!-- List -->
      <div v-else-if="items.length" class="grid grid-cols-1 gap-3 sm:gap-4">
        <article
          v-for="e in items"
          :key="e.id"
          class="flex flex-wrap items-center gap-3 sm:gap-4 rounded-2xl border border-slate-200 bg-white p-3 sm:p-4 hover:shadow-sm transition-shadow"
        >
          <div class="grid h-12 w-12 sm:h-16 sm:w-16 place-items-center rounded-xl bg-slate-100 text-base sm:text-lg font-semibold text-slate-600">
            {{ e.totalQuestions }}
          </div>

          <div class="min-w-0 flex-1">
            <div class="flex flex-wrap items-center gap-2">
              <h3 class="truncate font-semibold text-slate-900">{{ e.title }}</h3>
              <span
                class="rounded-full border px-2 py-0.5 text-xs"
                :class="e.status==='published'
                         ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                         : e.status === 'scheduled'
                         ? 'bg-blue-50 text-blue-700 border-blue-200'
                         : 'bg-amber-50 text-amber-700 border-amber-200'"
              >
                {{ e.status === 'published' ? 'Đã phát hành' : e.status === 'scheduled' ? 'Đã lên lịch' : 'Nháp' }}
              </span>
            </div>
            <div class="mt-1 text-xs sm:text-sm text-slate-500">
              Khoá: <span class="font-medium text-slate-700">{{ e.course }}</span> ·
              {{ e.durationMin }} phút
            </div>
          </div>

          <div class="flex shrink-0 gap-2 w-full sm:w-auto">
            <button
              class="flex-1 sm:flex-none rounded-xl border px-3 py-2 text-sm hover:bg-slate-50 active:bg-slate-100"
              @click="openDetail(e.id)"
            >
              Chi tiết
            </button>
            <button
              class="flex-1 sm:flex-none rounded-xl border px-3 py-2 text-sm hover:bg-slate-50 active:bg-slate-100"
              @click="openEdit(e.id)"
            >
              Sửa
            </button>
            <button
              class="flex-1 sm:flex-none rounded-xl border border-rose-200 px-3 py-2 text-sm text-rose-600 hover:bg-rose-50 active:bg-rose-100"
              @click="handleDelete(e.id, e.title)"
            >
              Xóa
            </button>
          </div>
        </article>
      </div>

      <p v-else class="mt-10 text-center text-slate-500">Không có đề phù hợp.</p>

      <!-- Pager -->
      <div v-if="!loading && totalPages > 1" class="mt-6">
        <!-- Compact pager for small screens -->
        <div v-if="isCompact" class="flex items-center justify-center gap-2">
          <button
            class="rounded-xl border px-3 py-2 text-sm disabled:opacity-50"
            :disabled="page<=1"
            @click="fetchList(page-1)"
            aria-label="Trang trước"
          >
            ‹
          </button>
          <span class="text-sm text-slate-600">Trang {{ page }} / {{ totalPages }}</span>
          <button
            class="rounded-xl border px-3 py-2 text-sm disabled:opacity-50"
            :disabled="page>=totalPages"
            @click="fetchList(page+1)"
            aria-label="Trang sau"
          >
            ›
          </button>
        </div>

        <!-- Full pager for medium+ screens -->
        <div v-else class="flex items-center justify-center gap-2">
          <button class="rounded-xl border px-3 py-2 text-sm disabled:opacity-50" :disabled="page<=1" @click="fetchList(page-1)">‹</button>
          <div class="flex max-w-full overflow-x-auto whitespace-nowrap rounded-xl">
            <button
              v-for="p in pagesToShow"
              :key="p.key"
              class="mx-0.5 rounded-xl border px-3 py-2 text-sm"
              :class="{ 'bg-slate-900 text-white border-slate-900': p.num===page, 'opacity-70 cursor-default': p.sep }"
              :disabled="p.sep"
              @click="!p.sep && fetchList(p.num!)"
            >
              {{ p.text }}
            </button>
          </div>
          <button class="rounded-xl border px-3 py-2 text-sm disabled:opacity-50" :disabled="page>=totalPages" @click="fetchList(page+1)">›</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onBeforeUnmount, onActivated, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from '@/utils/toast'
import { showConfirm } from '@/utils/confirm'

/** ===== Types ===== */
type ExamStatus = 'published' | 'draft' | 'scheduled'
type ExamRow = {
  id: number | string  // Can be UUID (string) or number
  title: string
  course: string
  status: ExamStatus
  totalQuestions: number
  durationMin: number
  submissions: number
  avgScore: number
  updatedAt: string
}

/** ===== Router ===== */
const router = useRouter()

/** ===== State (filters + paging) ===== */
const q = ref('')
const status = ref<'' | ExamStatus>('')        // '' = tất cả
const sort = ref<'updated' | 'title' | 'subs'>('updated')

const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const loading = ref(true)
const items = ref<ExamRow[]>([])

/** ===== Responsive helpers ===== */
const isCompact = ref(false)
function updateCompactFlag() {
  isCompact.value = window.innerWidth < 640
}

/** ===== Service adapter ===== */
type ServiceList = (params?: { level?: any; q?: string; status?: string; page?: number; pageSize?: number; includeStats?: boolean }) => Promise<{ items: any[]; total: number }>
let serviceList: ServiceList | undefined

async function tryInitService() {
  try {
    const mod = await import('@/services/exam.service')
    if (mod?.examService?.list) {
      serviceList = mod.examService.list as ServiceList
    }
  } catch (e) {
    console.error('Failed to load exam service:', e)
    throw new Error('Không thể tải dịch vụ bài kiểm tra')
  }
}

/** Map ExamSummary(service) -> ExamRow(component) */
function mapSummaryToRow(s: any): ExamRow {
  const durMin = Math.max(1, Math.round((Number(s.durationSec) || 0) / 60))
  const st: ExamStatus = s.status === 'published' ? 'published' : (s.status === 'scheduled' ? 'scheduled' : 'draft')
  // Keep ID as string if it's UUID, otherwise convert to number
  const id = typeof s.id === 'string' && s.id.includes('-') ? s.id : (Number(s.id) || s.id)
  
  return {
    id,
    title: String(s.title || `Đề #${id}`),
    course: String(s.level || '—'),
    status: st,
    totalQuestions: Number(s.questionsCount || 0),
    durationMin: durMin,
    submissions: Number(s.submissions || 0),
    avgScore: Number(s.avgScore || 0),
    updatedAt: new Date(s.updatedAt || Date.now()).toLocaleString('vi-VN'),
    }
}

/** Lọc + sắp xếp + phân trang (dùng chung) */
function applyViewParams(
  all: ExamRow[],
  params: { q?: string; status?: '' | ExamStatus; sort?: 'updated'|'title'|'subs'; page?: number; pageSize?: number }
) {
  let filtered = all.slice()

  if (params.q) {
    const key = params.q.toLowerCase()
    filtered = filtered.filter(e =>
      e.title.toLowerCase().includes(key) || e.course.toLowerCase().includes(key)
    )
  }
  if (params.status) filtered = filtered.filter(e => e.status === params.status)

  if (params.sort === 'title') filtered.sort((a,b)=>a.title.localeCompare(b.title))
  else if (params.sort === 'subs') filtered.sort((a,b)=>b.submissions - a.submissions)

  const pg = params.page ?? 1
  const size = params.pageSize ?? 10
  const start = (pg - 1) * size
  return {
    items: filtered.slice(start, start + size),
    total: filtered.length
  }
}

/** ===== Fetch (token chống race) ===== */
let fetchToken = 0
async function fetchList(p = page.value) {
  const token = ++fetchToken
  loading.value = true
  page.value = p
  try {
    if (!serviceList) {
      await tryInitService()
    }
    if (!serviceList) {
      throw new Error('Không thể khởi tạo dịch vụ bài kiểm tra')
    }
    
    // Build API params (no pagination - we do client-side pagination)
    const params: any = { includeStats: true }
    if (q.value) params.q = q.value
    // Note: status filter is done client-side via applyViewParams
    
    const result = await serviceList(params)
      if (token !== fetchToken) return
    
    // Extract items from result
    const summaries = result?.items || []
    
    // Map summaries to rows (stats already included from backend)
    const pool = summaries.map(mapSummaryToRow)
    
    // Apply client-side filtering, sorting, and pagination
    const res = applyViewParams(pool, {
      q: q.value || undefined,
      status: status.value,
      sort: sort.value,
      page: page.value,
      pageSize: pageSize.value
    })
    if (token !== fetchToken) return
    items.value = res.items
    total.value = res.total
  } catch (e: any) {
    console.error('Error fetching exams:', e)
    items.value = []
    total.value = 0
  } finally {
    if (token === fetchToken) loading.value = false
  }
}

/** Debounce search */
let debounceTimer: number | null = null
function debouncedFetch() {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = window.setTimeout(() => fetchList(1), 250) as unknown as number
}

/** Pager helpers */
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))
const pagesToShow = computed(() => {
  const max = totalPages.value
  const cur = page.value
  const windowSize = 7
  const arr: { key: string; num?: number; text: string; sep?: boolean }[] = []
  const push = (n: number) => arr.push({ key: 'p' + n, num: n, text: String(n) })
  const sep = (k: string) => arr.push({ key: k, text: '…', sep: true })

  if (max <= windowSize + 2) {
    for (let i = 1; i <= max; i++) push(i)
  } else {
    push(1)
    const start = Math.max(2, cur - 2)
    const end   = Math.min(max - 1, cur + 2)
    if (start > 2) sep('s')
    for (let i = start; i <= end; i++) push(i)
    if (end < max - 1) sep('e')
    push(max)
  }
  return arr
})

/** Actions */
function createExam()           { router.push({ path: '/teacher/exams/new' }) }
function openDetail(id: number | string) { router.push({ path: `/teacher/exams/${id}` }) }
function openEdit(id: number | string)   { router.push({ path: `/teacher/exams/${id}/edit` }) }

async function handleDelete(id: number | string, title: string) {
  const confirmed = await showConfirm({
    message: `Bạn có chắc muốn xóa bài kiểm tra "${title}"? Hành động này không thể hoàn tác.`,
    title: 'Xác nhận xóa bài kiểm tra',
    type: 'danger',
    confirmText: 'Xóa',
    cancelText: 'Hủy'
  })
  
  if (!confirmed) return
  
  try {
    const { examService } = await import('@/services/exam.service')
    await examService.delete(id)
    showToast('Đã xóa bài kiểm tra thành công', 'success')
    // Refresh list after deletion
    await fetchList(page.value)
  } catch (e: any) {
    showToast('Không thể xóa bài kiểm tra: ' + (e?.message || 'Lỗi không xác định'), 'error')
    console.error('Delete exam error:', e)
  }
}

/** Mount */
function onResize() { updateCompactFlag() }
onMounted(async () => {
  updateCompactFlag()
  window.addEventListener('resize', onResize, { passive: true })
  await tryInitService()
  await fetchList(1)
})

// Refresh list when returning from edit page
onActivated(async () => {
  await fetchList(page.value)
})

onBeforeUnmount(() => {
  if (debounceTimer) clearTimeout(debounceTimer)
  window.removeEventListener('resize', onResize)
})
</script>

<style scoped>
:host, .min-h-screen { overflow-x: hidden; }

/* ===== Custom select (fix icon & height cross-browser) ===== */
.select-base{
  @apply w-full rounded-2xl border border-slate-200 bg-white px-3 pr-8 py-2 text-sm leading-6 outline-none;
  @apply focus:ring-2 focus:ring-slate-200 focus:border-slate-900;
  appearance: none;          /* Chrome/Safari */
  -webkit-appearance: none;  /* iOS Safari */
  -moz-appearance: none;     /* Firefox */
  background-image: none;
}
.select-chevron{
  @apply pointer-events-none absolute inset-y-0 right-3 flex items-center text-slate-400;
}

/* Improve momentum scroll for pager row */
[role="navigation"] { -webkit-overflow-scrolling: touch; }
</style>
