<!-- src/pages/teacher/exams/ExamGrading.vue -->
<template>
  <div class="min-h-screen w-full overflow-x-hidden bg-slate-50">
    <main class="w-full mx-auto max-w-screen-2xl px-4 py-6 sm:px-6 md:px-10 md:py-8">
      <!-- Header -->
      <div class="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h1 class="text-xl font-semibold sm:text-2xl">Xem bài làm · {{ header }}</h1>

        <!-- Tools -->
        <div class="grid grid-cols-1 gap-2 sm:auto-cols-fr sm:grid-flow-col">
          <label class="sr-only" for="search">Tìm theo tên/lớp</label>
          <div class="flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-3 py-2">
            <svg viewBox="0 0 24 24" class="h-5 w-5 text-slate-400" fill="none" stroke="currentColor" aria-hidden="true">
              <circle cx="11" cy="11" r="8" stroke-width="2" />
              <path d="M21 21l-4.3-4.3" stroke-width="2" />
            </svg>
            <input
              id="search"
              v-model.trim="q"
              type="text"
              placeholder="Tìm theo tên/lớp…"
              class="w-full bg-transparent text-sm outline-none placeholder:text-slate-400"
              @input="debouncedFilter()"
            />
          </div>

          <select
            v-model="only"
            class="rounded-2xl border border-slate-200 bg-white px-3 py-2 text-sm"
            @change="touchFilterToken()"
          >
            <option value="all">Tất cả</option>
            <option value="pending">Chưa nộp</option>
            <option value="submitted">Đã nộp</option>
          </select>
        </div>
      </div>

      <!-- Skeleton -->
      <div v-if="loading" class="space-y-2">
        <div v-for="i in 6" :key="'skel-'+i" class="rounded-2xl border border-slate-200 bg-white p-4">
          <div class="mb-2 h-4 w-40 animate-pulse rounded bg-slate-200"></div>
          <div class="h-3 w-3/4 animate-pulse rounded bg-slate-100"></div>
        </div>
      </div>

      <!-- Content -->
      <template v-else>
        <!-- Mobile: Card list -->
        <div class="grid grid-cols-1 gap-3 md:hidden">
          <article
            v-for="s in filtered"
            :key="s.id"
            class="rounded-2xl border border-slate-200 bg-white p-4"
          >
            <div class="flex items-start justify-between gap-3">
              <div class="min-w-0">
                <h3 class="font-semibold truncate" :title="s.studentName">{{ s.studentName }}</h3>
                <p class="mt-0.5 text-sm text-slate-500">
                  Lớp: <span class="font-medium">{{ s.classCode }}</span>
                </p>
              </div>
              <span
                class="shrink-0 rounded-full border px-2 py-0.5 text-xs"
                :class="s.status==='submitted'
                         ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                         : 'bg-amber-50 text-amber-700 border-amber-200'"
              >
                {{ s.status === 'submitted' ? 'Đã nộp' : 'Chưa nộp' }}
              </span>
            </div>

            <div class="mt-3 grid grid-cols-2 gap-2 text-sm text-slate-600">
              <div class="space-y-1">
                <div class="text-slate-500">Nộp lúc</div>
                <div class="font-medium leading-5">{{ s.submittedAt || '—' }}</div>
              </div>
              <div class="space-y-1">
                <div class="text-slate-500">Điểm</div>
                <div class="font-semibold">{{ s.score !== null ? s.score.toFixed(1) : '—' }}</div>
              </div>
            </div>

            <div class="mt-4">
              <button
                v-if="s.status === 'submitted'"
                class="w-full rounded-lg bg-slate-900 px-3 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
                @click="openView(s)"
              >
                Xem bài làm
              </button>
              <p v-else class="text-center text-sm text-slate-400">Học sinh chưa nộp bài</p>
            </div>
          </article>

          <p v-if="!filtered.length" class="p-6 text-center text-slate-500">
            Không có bài nộp phù hợp.
          </p>
        </div>

        <!-- Desktop: Table -->
        <div class="hidden md:block rounded-2xl border border-slate-200 bg-white">
          <div class="overflow-x-auto">
            <table class="w-full table-fixed">
              <thead class="sticky top-0 z-10 bg-slate-50 text-left text-sm text-slate-600">
                <tr>
                  <th class="p-3 w-[28%]">Học sinh</th>
                  <th class="p-3 w-[12%]">Lớp</th>
                  <th class="p-3 w-[24%]">Thời gian nộp</th>
                  <th class="p-3 w-[10%]">Điểm</th>
                  <th class="p-3 w-[14%]">Trạng thái</th>
                  <th class="p-3 w-[22%]">Thao tác</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="s in filtered" :key="s.id" class="border-t text-sm">
                  <td class="p-3 font-medium truncate" :title="s.studentName">{{ s.studentName }}</td>
                  <td class="p-3 truncate">{{ s.classCode }}</td>
                  <td class="p-3 truncate" :title="s.submittedAt || '—'">{{ s.submittedAt || '—' }}</td>
                  <td class="p-3">{{ s.score !== null ? s.score.toFixed(1) : '—' }}</td>
                  <td class="p-3">
                    <span
                      class="rounded-full border px-2 py-0.5 text-xs whitespace-nowrap"
                      :class="s.status==='submitted'
                               ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                               : 'bg-amber-50 text-amber-700 border-amber-200'"
                    >
                      {{ s.status === 'submitted' ? 'Đã nộp' : 'Chưa nộp' }}
                    </span>
                  </td>
                  <td class="p-3">
                      <button
                      v-if="s.status === 'submitted'"
                      class="rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-slate-800 whitespace-nowrap"
                      @click="openView(s)"
                      >
                      Xem bài làm
                      </button>
                    <span v-else class="text-sm text-slate-400">Chưa nộp</span>
                  </td>
                </tr>
              </tbody>
            </table>

            <p v-if="!filtered.length" class="p-6 text-center text-slate-500">
              Không có bài nộp phù hợp.
            </p>
          </div>
        </div>
      </template>

      <!-- Modal xem bài làm -->
      <div
        v-if="viewingRow"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
        @click.self="closeView"
      >
        <div class="w-full max-w-4xl rounded-2xl bg-white p-6 max-h-[90vh] overflow-y-auto">
          <div class="mb-4 flex items-center justify-between">
            <h3 class="text-lg font-semibold">Bài làm của: {{ viewingRow.studentName }}</h3>
            <button
              class="rounded-lg border px-3 py-1.5 text-sm hover:bg-slate-50"
              @click="closeView"
            >
              ✕
            </button>
          </div>

          <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4 rounded-xl bg-slate-50 p-4 text-sm">
              <div>
                <span class="text-slate-500">Lớp:</span>
                <span class="ml-2 font-medium">{{ viewingRow.classCode }}</span>
              </div>
              <div>
                <span class="text-slate-500">Nộp lúc:</span>
                <span class="ml-2 font-medium">{{ viewingRow.submittedAt }}</span>
              </div>
              <div>
                <span class="text-slate-500">Điểm:</span>
                <span class="ml-2 font-bold text-cyan-600">
                  {{ viewingRow.score !== null ? viewingRow.score.toFixed(1) : 'Chưa có điểm' }}
                </span>
              </div>
              <div>
                <span class="text-slate-500">Trạng thái:</span>
                <span class="ml-2 font-medium text-emerald-600">Đã chấm tự động</span>
              </div>
            </div>

            <div class="space-y-3">
              <div
                v-for="(q, idx) in mockQuestions"
                :key="idx"
                class="rounded-xl border border-slate-200 p-4"
              >
                <div class="mb-2 flex items-center justify-between">
                  <span class="font-semibold">Câu {{ idx + 1 }}</span>
                  <div class="flex items-center gap-2">
                  <span class="text-sm text-slate-500">{{ q.score }} điểm</span>
                    <span
                      class="rounded-full px-2 py-0.5 text-xs font-semibold"
                      :class="mockScores[idx] === q.score
                        ? 'bg-emerald-100 text-emerald-700'
                        : 'bg-rose-100 text-rose-700'"
                    >
                      {{ mockScores[idx] === q.score ? 'Đúng' : 'Sai' }}
                    </span>
                  </div>
                </div>
                <p class="mb-3 text-sm font-medium">{{ q.text }}</p>
                <div class="rounded-lg bg-slate-50 p-3 mb-2">
                  <div class="mb-2 text-xs font-medium text-slate-600">Câu trả lời của học sinh:</div>
                  <div class="text-sm font-semibold">{{ mockAnswers[idx] || 'Chưa trả lời' }}</div>
                </div>
                <div class="rounded-lg bg-emerald-50 p-3">
                  <div class="mb-1 text-xs font-medium text-emerald-700">Đáp án đúng:</div>
                  <div class="text-sm font-semibold text-emerald-900">{{ q.correctAnswer }}</div>
                </div>
                <div class="mt-2 text-xs text-slate-500">
                  Điểm đạt: {{ mockScores[idx] }} / {{ q.score }}
                </div>
              </div>
            </div>

            <div class="flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50 p-4">
              <span class="font-semibold text-slate-900">Tổng điểm:</span>
              <span class="text-xl font-bold text-slate-900">
                {{ totalScore.toFixed(1) }} / {{ maxScore }}
              </span>
            </div>
          </div>

          <div class="mt-6 flex justify-end gap-3">
            <button
              class="rounded-xl border px-4 py-2 text-sm hover:bg-slate-50"
              @click="closeView"
            >
              Đóng
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onBeforeUnmount, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

type RowStatus = 'pending' | 'submitted'
type Row = {
  id: number
  studentName: string
  classCode: string
  submittedAt: string | null
  score: number | null
  status: RowStatus
}

const route = useRoute()
const id = ref<number>(Number(route.params.id))

const header = ref(`Đề #${id.value}`)
const loading = ref(true)
const rows = ref<Row[]>([])

const q = ref('')
const only = ref<'all' | RowStatus>('all')

const viewingRow = ref<Row | null>(null)
const mockQuestions = ref<Array<{ text: string; score: number; correctAnswer: string }>>([])
const mockAnswers = ref<string[]>([])
const mockScores = ref<number[]>([])

type DetailFn = (id: string | number) => Promise<any>
let detailFn: DetailFn | undefined

async function tryInitService() {
  try {
    const mod = await import('@/services/exam.service')
    if (mod?.examService?.detail) detailFn = mod.examService.detail as DetailFn
  } catch {}
}

function makeMockRows(examId: number): Row[] {
  const total = (examId % 7) + 9
  return Array.from({ length: total }).map((_, i) => {
    const sid = examId * 1000 + i + 1
    const submitted = (i + examId) % 3 !== 0
    const score = submitted ? Math.round(((6 + ((i + examId) % 5)) + 0.1) * 10) / 10 : null
    const cls = `L${(examId % 4) + 1}${String((i % 3) + 1).padStart(2, '0')}`
    const name = `HS ${(examId % 9) + 1}${String(i + 1).padStart(2, '0')}`
    const submittedAt = submitted ? new Date(Date.now() - (i + 1) * 36e5).toLocaleString() : null
    return { id: sid, studentName: name, classCode: cls, submittedAt, score, status: submitted ? 'submitted' : 'pending' }
  })
}

let loadToken = 0
async function load(examId = id.value) {
  const token = ++loadToken
  loading.value = true
  try {
    if (detailFn) {
      try {
        const d = await detailFn(examId)
        if (token === loadToken && d?.title) header.value = String(d.title)
      } catch {}
    } else header.value = `Đề #${examId}`

    const data = makeMockRows(examId)
    if (token !== loadToken) return
    rows.value = data
  } finally {
    if (token === loadToken) loading.value = false
  }
}

/** Debounce filter */
let ft: number | null = null
const filterToken = ref(0)
function debouncedFilter() {
  if (ft) window.clearTimeout(ft)
  ft = window.setTimeout(() => { filterToken.value++ }, 250) as unknown as number
}
function touchFilterToken() { filterToken.value++ }

/** Filtering */
const filtered = computed(() => {
  void filterToken.value
  const key = q.value.toLowerCase()
  let arr = rows.value
  if (only.value !== 'all') arr = arr.filter(s => s.status === only.value)
  if (key) {
    arr = arr.filter(s =>
      s.studentName.toLowerCase().includes(key) ||
      s.classCode.toLowerCase().includes(key)
    )
  }
  return arr
})

onMounted(async () => {
  await tryInitService()
  await load(id.value)
})
watch(() => route.params.id, (nv) => {
  id.value = Number(nv)
  load(id.value)
})
onBeforeUnmount(() => { if (ft) window.clearTimeout(ft) })

function openView(row: Row) {
  viewingRow.value = row
  // Mock: tạo câu hỏi và câu trả lời mẫu
  mockQuestions.value = Array.from({ length: 5 }).map((_, i) => ({
    text: `Câu hỏi mẫu số ${i + 1}?`,
    score: 2,
    correctAnswer: `Đáp án đúng ${i + 1}`
  }))
  mockAnswers.value = Array.from({ length: 5 }).map((_, i) => 
    `Đáp án ${i + 1} của học sinh}`
  )
  // Mock điểm - giả sử một số câu đúng, một số câu sai
  mockScores.value = Array.from({ length: 5 }).map((_, i) => {
    const isCorrect = (row.id + i) % 3 !== 0
    return isCorrect ? mockQuestions.value[i].score : 0
  })
}

function closeView() {
  viewingRow.value = null
  mockQuestions.value = []
  mockAnswers.value = []
  mockScores.value = []
}

const totalScore = computed(() => {
  return mockScores.value.reduce((sum, s) => sum + (s || 0), 0)
})

const maxScore = computed(() => {
  return mockQuestions.value.reduce((sum, q) => sum + q.score, 0)
})
</script>

<style scoped>
:host, .min-h-screen { overflow-x: hidden; }
table th, table td, h3 { word-break: break-word; }
@media (hover: none) {
  .hover\:bg-slate-50:hover { background: inherit; }
}
</style>
