<!-- src/pages/teacher/exams/ExamReports.vue -->
<template>
  <div class="min-h-screen bg-gray-50">
    <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-gray-900">Báo cáo bài kiểm tra</h1>
        <p class="mt-1 text-sm text-gray-600">Thống kê và phân tích kết quả bài kiểm tra của học viên</p>
      </div>

      <!-- KPIs - Simple cards -->
      <div class="mb-6 grid grid-cols-2 gap-4 sm:grid-cols-4">
        <div class="rounded-lg border border-gray-200 bg-white p-4">
          <p class="text-xs text-gray-600">Tổng đề</p>
          <p class="mt-1 text-2xl font-bold text-gray-900">{{ kpi.total }}</p>
        </div>
        <div class="rounded-lg border border-gray-200 bg-white p-4">
          <p class="text-xs text-gray-600">Tổng bài nộp</p>
          <p class="mt-1 text-2xl font-bold text-gray-900">{{ kpi.subs }}</p>
        </div>
        <div class="rounded-lg border border-gray-200 bg-white p-4">
          <p class="text-xs text-gray-600">Điểm trung bình</p>
          <p class="mt-1 text-2xl font-bold text-gray-900">{{ kpi.avg }}</p>
        </div>
        <div class="rounded-lg border border-gray-200 bg-white p-4">
          <p class="text-xs text-gray-600">Tỉ lệ đạt</p>
          <p class="mt-1 text-2xl font-bold text-gray-900">{{ kpi.pass }}%</p>
        </div>
      </div>

      <!-- Filters -->
      <div class="mb-6 rounded-lg border border-gray-200 bg-white p-4">
        <div class="grid grid-cols-1 gap-4 lg:grid-cols-4">
        <!-- Search -->
          <div class="lg:col-span-2">
            <div class="flex items-center gap-2 rounded-lg border border-gray-300 px-3 py-2">
              <svg viewBox="0 0 24 24" class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor">
              <circle cx="11" cy="11" r="8" stroke-width="2" />
              <path d="M21 21l-4.3-4.3" stroke-width="2" />
            </svg>
            <input
              v-model.trim="q"
              type="text"
                placeholder="Tìm theo tên đề/khóa học…"
                class="w-full bg-transparent outline-none text-sm"
              @input="debouncedFetch"
            />
          </div>
        </div>

          <!-- Sort -->
          <div class="select-wrap">
          <select
            v-model="sort"
              class="select-base"
            @change="fetchList(1)"
          >
            <option value="updated">Mới cập nhật</option>
            <option value="title">A → Z</option>
            <option value="subs">Bài nộp nhiều</option>
            <option value="avg">Điểm TB cao</option>
            <option value="pass">Tỉ lệ đạt cao</option>
          </select>
            <span class="select-chevron" aria-hidden="true">
              <svg viewBox="0 0 20 20" fill="currentColor" class="h-4 w-4">
                <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 10.17l3.71-2.94a.75.75 0 111.04 1.08l-4.24 3.36a.75.75 0 01-.94 0L5.21 8.31a.75.75 0 01.02-1.1z" clip-rule="evenodd" />
              </svg>
            </span>
          </div>

          <!-- Refresh -->
          <button
            class="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            @click="refresh"
          >
            Làm mới
          </button>
        </div>

        <!-- Date range -->
        <div class="mt-4 grid grid-cols-1 gap-2 sm:grid-cols-3">
          <div class="rounded-lg border border-gray-300 bg-white px-3 py-2">
            <label class="block text-xs text-gray-600 mb-1">Từ ngày</label>
            <input
              v-model="from"
              type="date"
              class="w-full bg-transparent outline-none text-sm"
              @change="fetchList(1)"
            />
          </div>
          <div class="rounded-lg border border-gray-300 bg-white px-3 py-2">
            <label class="block text-xs text-gray-600 mb-1">Đến ngày</label>
            <input
              v-model="to"
              type="date"
              class="w-full bg-transparent outline-none text-sm"
              @change="fetchList(1)"
            />
          </div>
          <div class="rounded-lg border border-gray-300 bg-white px-3 py-2">
            <label class="block text-xs text-gray-600 mb-1">&nbsp;</label>
            <button
              class="w-full rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
              @click="clearDates"
            >
              Xóa lọc ngày
            </button>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="space-y-3">
        <div v-for="i in pageSize" :key="'skel-'+i" class="rounded-lg border border-gray-200 bg-white p-4">
          <div class="flex items-center gap-4">
            <div class="h-12 w-12 rounded bg-gray-200 animate-pulse"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 w-48 rounded bg-gray-200 animate-pulse"></div>
              <div class="h-3 w-64 rounded bg-gray-100 animate-pulse"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Table -->
      <div v-else-if="items.length" class="overflow-hidden rounded-lg border border-gray-200 bg-white">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Đề kiểm tra</th>
              <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Khóa học</th>
              <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Câu hỏi</th>
              <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Thời gian</th>
              <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Bài nộp</th>
              <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Điểm TB</th>
              <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Tỉ lệ đạt</th>
              <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Trạng thái</th>
              <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Thao tác</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="e in items" :key="e.id" class="hover:bg-gray-50">
              <td class="px-4 py-3 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ e.title }}</div>
                <div class="text-xs text-gray-500 mt-0.5">Cập nhật: {{ e.updatedAtDisplay }}</div>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-sm text-gray-600">{{ e.course }}</td>
              <td class="px-4 py-3 whitespace-nowrap text-center text-sm text-gray-900">{{ e.totalQuestions }}</td>
              <td class="px-4 py-3 whitespace-nowrap text-center text-sm text-gray-600">{{ e.durationMin }} phút</td>
              <td class="px-4 py-3 whitespace-nowrap text-center text-sm text-gray-900">{{ e.submissions }}</td>
              <td class="px-4 py-3 whitespace-nowrap text-center text-sm font-medium text-gray-900">{{ e.avgScore }}</td>
              <td class="px-4 py-3 whitespace-nowrap text-center text-sm text-gray-900">{{ e.passRate }}%</td>
              <td class="px-4 py-3 whitespace-nowrap text-center">
              <span
                  class="inline-flex rounded-full px-2 py-1 text-xs font-medium"
                  :class="e.status === 'published'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'"
              >
                {{ e.status === 'published' ? 'Đã phát hành' : 'Nháp' }}
              </span>
              </td>
              <td class="px-4 py-3 whitespace-nowrap text-right text-sm">
                <div class="flex items-center justify-end gap-2">
                  <button
                    class="text-blue-600 hover:text-blue-800 font-medium"
                    @click="openDetail(e.id)"
                  >
                    Chi tiết
                  </button>
                  <span class="text-gray-300">|</span>
                  <button
                    class="text-blue-600 hover:text-blue-800 font-medium"
                    @click="openView(e.id)"
                  >
                    Xem bài làm
                  </button>
            </div>
              </td>
            </tr>
          </tbody>
        </table>
            </div>

      <!-- Empty State -->
      <div v-else class="rounded-lg border border-gray-200 bg-white p-12 text-center">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="mt-4 text-sm font-medium text-gray-900">Không có dữ liệu</h3>
        <p class="mt-2 text-sm text-gray-500">Không có bài kiểm tra phù hợp với bộ lọc hiện tại.</p>
          </div>

      <!-- Pagination -->
      <div v-if="!loading && totalPages > 1" class="mt-6 flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6">
        <div class="flex flex-1 justify-between sm:hidden">
          <button
            class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
            :disabled="page <= 1"
            @click="fetchList(page - 1)"
          >
            Trước
          </button>
          <button
            class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50"
            :disabled="page >= totalPages"
            @click="fetchList(page + 1)"
          >
            Sau
          </button>
        </div>
        <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              Hiển thị <span class="font-medium">{{ (page - 1) * pageSize + 1 }}</span> đến
              <span class="font-medium">{{ Math.min(page * pageSize, total) }}</span> trong tổng
              <span class="font-medium">{{ total }}</span> kết quả
            </p>
          </div>
          <div>
            <nav class="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
              <button
                class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50"
                :disabled="page <= 1"
                @click="fetchList(page - 1)"
              >
                <span class="sr-only">Trước</span>
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M12.79 5.23a.75.75 0 01-.02 1.06L8.832 10l3.938 3.71a.75.75 0 11-1.04 1.08l-4.5-4.25a.75.75 0 010-1.08l4.5-4.25a.75.75 0 011.06.02z" clip-rule="evenodd" />
                </svg>
              </button>
        <button
          v-for="p in pagesToShow"
          :key="p.key"
                class="relative inline-flex items-center px-4 py-2 text-sm font-semibold ring-1 ring-inset ring-gray-300 focus:z-20 focus:outline-offset-0 disabled:opacity-50"
                :class="p.sep
                  ? 'text-gray-300 pointer-events-none'
                  : p.num === page
                    ? 'z-10 bg-blue-600 text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600'
                    : 'text-gray-900 hover:bg-gray-50'"
          :disabled="p.sep"
          @click="!p.sep && fetchList(p.num!)"
        >
          {{ p.text }}
        </button>
              <button
                class="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50"
                :disabled="page >= totalPages"
                @click="fetchList(page + 1)"
              >
                <span class="sr-only">Sau</span>
                <svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fill-rule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clip-rule="evenodd" />
                </svg>
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

/** ===== Types ===== */
type ExamStatus = 'published' | 'draft'
type ReportRow = {
  id: number
  title: string
  course: string
  status: ExamStatus
  totalQuestions: number
  durationMin: number
  submissions: number
  avgScore: number
  passRate: number
  updatedTs: number
  updatedAtDisplay: string
}

/** ===== Router ===== */
const router = useRouter()

/** ===== Filters & paging ===== */
const q = ref('')
const status = ref<'' | ExamStatus>('')
const sort = ref<'updated' | 'title' | 'subs' | 'avg' | 'pass'>('updated')
const from = ref<string>('')
const to = ref<string>('')

const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

const loading = ref(true)
const items = ref<ReportRow[]>([])

/** ===== Service adapter (lazy) ===== */
type ServiceList = (params?: { q?: string }) => Promise<any[]>
let serviceList: ServiceList | undefined

async function tryInitService() {
  try {
    const mod = await import('@/services/exam.service')
    if (mod?.examService?.list) {
      serviceList = mod.examService.list as ServiceList
    }
  } catch {
    // fallback to mock
  }
}

/** ===== Mapping helpers ===== */
function mapFromService(s: any): ReportRow {
  const id = Number(s.id)
  const st: ExamStatus = s.status === 'published' ? 'published' : 'draft'
  const durationMin = Math.max(1, Math.round((Number(s.durationSec) || 1800) / 60))
  const totalQuestions = Number(s.questionsCount ?? (20 + (id % 15)))
  const course = String(s.level || `Khoá ${((id % 6) + 1)}`)
  const submissions = (id * 13) % 160
  const avgScore = Number((6 + (id % 4) + (id % 3) * 0.5).toFixed(1))
  const passRate = Math.min(100, 50 + (id % 50))
  const updatedTs = s.updatedAt ? Date.parse(s.updatedAt) : (Date.now() - id * 36e5)
  const updatedAtDisplay = new Date(updatedTs).toLocaleString('vi-VN')
  return { id, title: String(s.title || `Đề #${id}`), course, status: st, totalQuestions, durationMin, submissions, avgScore, passRate, updatedTs, updatedAtDisplay }
}

function mockRows(): ReportRow[] {
  return Array.from({ length: 42 }).map((_, i) => {
    const id = i + 1
    const published = id % 3 !== 1
    const updatedTs = Date.now() - id * 36e5
    return {
      id,
      title: `Đề kiểm tra #${id}`,
      course: `Khoá ${((id % 6) + 1)}`,
      status: published ? 'published' : 'draft',
      totalQuestions: 20 + (id % 15),
      durationMin: 20 + (id % 6) * 5,
      submissions: (id * 13) % 160,
      avgScore: Number((6 + (id % 4) + (id % 3) * 0.5).toFixed(1)),
      passRate: Math.min(100, 50 + (id % 50)),
      updatedTs,
      updatedAtDisplay: new Date(updatedTs).toLocaleString('vi-VN')
    }
  })
}

/** ===== Fetch (chống race) ===== */
let fetchToken = 0
async function fetchList(p = page.value) {
  const token = ++fetchToken
  loading.value = true
  page.value = p
  try {
    let pool: ReportRow[] = []
    if (serviceList) {
      const summaries = await serviceList(q.value ? { q: q.value } : undefined)
      if (token !== fetchToken) return
      pool = (summaries || []).map(mapFromService)
    } else {
      pool = mockRows()
    }

    const key = q.value.toLowerCase()
    let filtered = key
      ? pool.filter(e => [e.title, e.course].some(x => String(x).toLowerCase().includes(key)))
      : pool

    if (status.value) filtered = filtered.filter(e => e.status === status.value)

    const fromTime = from.value ? Date.parse(from.value + 'T00:00:00') : 0
    const toTime = to.value ? Date.parse(to.value + 'T23:59:59') : Number.MAX_SAFE_INTEGER
    filtered = filtered.filter(e => e.updatedTs >= fromTime && e.updatedTs <= toTime)

    if (sort.value === 'title') filtered.sort((a, b) => a.title.localeCompare(b.title))
    else if (sort.value === 'subs') filtered.sort((a, b) => b.submissions - a.submissions)
    else if (sort.value === 'avg')  filtered.sort((a, b) => b.avgScore - a.avgScore)
    else if (sort.value === 'pass') filtered.sort((a, b) => b.passRate - a.passRate)
    else filtered.sort((a, b) => b.updatedTs - a.updatedTs)

    total.value = filtered.length
    const start = (page.value - 1) * pageSize.value
    items.value = filtered.slice(start, start + pageSize.value)
  } finally {
    if (token === fetchToken) loading.value = false
  }
}

function refresh() { fetchList(page.value) }

/** Debounce search */
let timer: number | null = null
function debouncedFetch() {
  if (timer) clearTimeout(timer)
  timer = window.setTimeout(() => fetchList(1), 250) as unknown as number
}

/** KPIs */
const kpi = computed(() => {
  const src = items.value
  const totalExams = total.value
  const subs = src.reduce((s, e) => s + e.submissions, 0)
  const avg = src.length ? (src.reduce((s, e) => s + e.avgScore, 0) / src.length).toFixed(1) : '0.0'
  const pass = src.length ? Math.round(src.reduce((s, e) => s + e.passRate, 0) / src.length) : 0
  return { total: totalExams, subs, avg, pass }
})

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
    const end = Math.min(max - 1, cur + 2)
    if (start > 2) sep('s')
    for (let i = start; i <= end; i++) push(i)
    if (end < max - 1) sep('e')
    push(max)
  }
  return arr
})

/** Actions */
function openDetail(id: number)  { router.push({ path: `/teacher/exams/${id}` }) }
function openView(id: number) { router.push({ path: `/teacher/exams/${id}/grading` }) }
function clearDates() { from.value = ''; to.value = ''; fetchList(1) }

/** Mount */
onMounted(async () => {
  await tryInitService()
  fetchList(1)
})

onBeforeUnmount(() => {
  if (timer) clearTimeout(timer)
})
</script>

<style scoped>
.select-wrap {
  position: relative;
}
.select-chevron {
  pointer-events: none;
  position: absolute;
  right: 10px;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  color: #94a3b8;
}
.select-base {
  width: 100%;
  border-radius: 0.5rem;
  border: 1px solid #d1d5db;
  background: #fff;
  padding: 0 2.5rem 0 0.75rem;
  height: 38px;
  font-size: 0.875rem;
  line-height: 1.25rem;
  background-clip: padding-box;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}
.select-base::-ms-expand {
  display: none;
}
.select-base:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 1px #3b82f6;
}
.select-base:hover {
  border-color: #9ca3af;
}
</style>
