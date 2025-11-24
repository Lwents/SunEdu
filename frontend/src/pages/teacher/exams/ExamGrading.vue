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
                  <span class="ml-2 font-medium">{{ displayClass }}</span>
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

            <div class="space-y-4">
              <div
                v-for="(q, idx) in questions"
                :key="q.id || idx"
                class="rounded-xl border border-slate-200 bg-white p-5"
              >
                <!-- Question header -->
                <div class="mb-3 flex items-center justify-between border-b border-slate-200 pb-2">
                  <div class="flex items-center gap-2">
                    <span class="flex h-7 w-7 items-center justify-center rounded-full bg-sky-100 text-sm font-bold text-sky-700">
                      {{ idx + 1 }}
                    </span>
                    <span class="rounded-full bg-slate-100 border border-slate-300 px-2 py-0.5 text-xs font-medium text-slate-700">
                      {{ getQuestionTypeLabel(q.type) }}
                    </span>
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="text-sm text-slate-500">{{ q.score || 0 }} điểm</span>
                    <span
                      class="rounded-full px-2 py-0.5 text-xs font-semibold"
                      :class="getQuestionScore(q.id) >= (q.score || 0)
                        ? 'bg-emerald-100 text-emerald-700'
                        : getQuestionScore(q.id) > 0
                        ? 'bg-amber-100 text-amber-700'
                        : 'bg-rose-100 text-rose-700'"
                    >
                      {{ getQuestionScore(q.id) >= (q.score || 0) ? 'Đúng' : getQuestionScore(q.id) > 0 ? 'Một phần' : 'Sai' }}
                    </span>
                  </div>
                </div>

                <!-- Question text -->
                <p class="mb-4 text-sm font-medium text-slate-900 leading-relaxed">{{ q.text }}</p>

                <!-- Choices (if available) -->
                <div v-if="q.choices && q.choices.length > 0" class="mb-4 space-y-2">
                  <div class="text-xs font-medium text-slate-600 mb-2">Các lựa chọn:</div>
                  <div
                    v-for="(choice, cIdx) in q.choices"
                    :key="cIdx"
                    class="flex items-start gap-2 rounded-lg p-2"
                    :class="isCorrectChoice(q, choice)
                      ? 'bg-emerald-50 border border-emerald-200'
                      : isStudentChoice(q, choice)
                      ? 'bg-amber-50 border border-amber-200'
                      : 'bg-slate-50 border border-slate-200'"
                  >
                    <span class="flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-xs font-semibold"
                      :class="isCorrectChoice(q, choice)
                        ? 'bg-emerald-600 text-white'
                        : isStudentChoice(q, choice)
                        ? 'bg-amber-600 text-white'
                        : 'bg-slate-300 text-slate-700'"
                    >
                      {{ String.fromCharCode(65 + cIdx) }}
                    </span>
                    <span class="flex-1 text-sm text-slate-700">{{ choice.text }}</span>
                    <span v-if="isCorrectChoice(q, choice)" class="text-emerald-600 font-semibold">✓</span>
                    <span v-else-if="isStudentChoice(q, choice) && !isCorrectChoice(q, choice)" class="text-amber-600 font-semibold">✗</span>
                  </div>
                </div>

                <!-- Student answer -->
                <div class="mb-3 rounded-lg border border-slate-300 bg-slate-50 p-3">
                  <div class="mb-1 text-xs font-medium text-slate-600">Câu trả lời của học sinh:</div>
                  <div class="text-sm font-semibold text-slate-900">{{ getStudentAnswer(q.id) }}</div>
                </div>

                <!-- Correct answer -->
                <div class="mb-3 rounded-lg border border-emerald-300 bg-emerald-50 p-3">
                  <div class="mb-1 text-xs font-medium text-emerald-700">Đáp án đúng:</div>
                  <div class="text-sm font-semibold text-emerald-900">{{ getCorrectAnswer(q) }}</div>
                </div>

                <!-- Score breakdown -->
                <div class="flex items-center justify-between rounded-lg bg-slate-100 p-2 text-xs">
                  <span class="text-slate-600">Điểm đạt:</span>
                  <span class="font-semibold text-slate-900">
                    {{ getQuestionScore(q.id).toFixed(1) }} / {{ q.score || 0 }}
                  </span>
                </div>
              </div>
            </div>

            <div v-if="questions.length > 0" class="flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50 p-4">
              <span class="font-semibold text-slate-900">Tổng điểm:</span>
              <span class="text-xl font-bold text-slate-900">
                {{ totalScore.toFixed(1) }} / {{ maxScore.toFixed(1) }}
              </span>
            </div>
            <div v-else class="rounded-lg border border-amber-200 bg-amber-50 p-4 text-center text-sm text-amber-700">
              Chưa có dữ liệu câu hỏi để hiển thị
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
import { showToast } from '@/utils/toast'

type RowStatus = 'pending' | 'submitted'
type Row = {
  id: number | string  // Support both number and UUID
  studentName: string
  classCode: string
  submittedAt: string | null
  score: number | null
  status: RowStatus
  attemptId?: string
}

const route = useRoute()

// Helper function to parse ID from route params (supports both UUID and number)
function parseId(paramId: string | string[]): string | number {
  const idStr = Array.isArray(paramId) ? paramId[0] : paramId
  if (typeof idStr === 'string' && idStr.includes('-')) {
    return idStr // UUID
  }
  const numId = Number(idStr)
  return isNaN(numId) ? idStr : numId
}

const id = ref<string | number>(parseId(route.params.id))
const header = ref(`Đề #${id.value}`)
const loading = ref(true)
const rows = ref<Row[]>([])

const q = ref('')
const only = ref<'all' | RowStatus>('all')

const viewingRow = ref<Row | null>(null)
const attemptDetail = ref<any>(null)
const questions = ref<any[]>([])
const answers = ref<Record<string, any>>({})
const displayClass = computed(() => {
  const ad = attemptDetail.value
  return (
    ad?.class_name ||
    ad?.student_class ||
    ad?.student?.class_name ||
    viewingRow.value?.classCode ||
    'Không rõ'
  )
})

type DetailFn = (id: string | number) => Promise<any>
type AttemptSummaryFn = (attemptId: string) => Promise<any>
let detailFn: DetailFn | undefined
let getAttemptSummaryFn: AttemptSummaryFn | undefined

async function tryInitService() {
  try {
    const mod = await import('@/services/exam.service')
    if (mod?.examService?.detail) detailFn = mod.examService.detail as DetailFn
    if (mod?.examService?.getAttemptSummary) getAttemptSummaryFn = mod.examService.getAttemptSummary as AttemptSummaryFn
  } catch (e) {
    console.error('Failed to load exam service:', e)
  }
}

let loadToken = 0
async function load(examId: string | number = id.value) {
  const token = ++loadToken
  loading.value = true
  try {
    // Load exam title
    if (detailFn) {
      try {
        const d = await detailFn(examId)
        if (token === loadToken && d?.title) header.value = String(d.title)
      } catch (e) {
        console.error('Failed to load exam detail:', e)
      }
    } else {
      const displayId = typeof examId === 'string' && examId.includes('-') ? examId.substring(0, 8) : examId
      header.value = `Đề #${displayId}`
    }

    // Load attempts list
    const api = (await import('@/config/axios')).default
    const { data } = await api.get(`/activities/exercises/${examId}/attempts/`)
    if (token !== loadToken) return
    
    // Map backend attempts to frontend rows
    const mappedRows: Row[] = (data || []).map((att: any) => {
      // Handle attempt ID - can be UUID or number
      const attemptId = String(att.id || '')
      const rowId = attemptId.includes('-') 
        ? attemptId.substring(0, 8) 
        : (Number(attemptId) || attemptId)
      
      return {
        id: rowId,
        studentName: att.student_name || 'Unknown',
        classCode: att.class_code || att.class_name || att.student_class_code || '—',
        submittedAt: att.submitted_at || (att.finished_at ? new Date(att.finished_at).toLocaleString('vi-VN') : null),
        score: att.score !== null && att.score !== undefined ? Number(att.score) : null,
        status: att.status === 'submitted' ? 'submitted' : 'pending',
        attemptId: attemptId, // Store attempt ID as string for detail view
      }
    })
    
    rows.value = mappedRows
  } catch (e: any) {
    console.error('Error loading attempts:', e)
    rows.value = []
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
  id.value = parseId(nv)
  load(id.value)
})
onBeforeUnmount(() => { if (ft) window.clearTimeout(ft) })

async function openView(row: Row) {
  viewingRow.value = row
  if (!row.attemptId) {
    console.error('No attempt ID for row:', row)
    return
  }
  
  try {
    // Load attempt summary using service
    if (!getAttemptSummaryFn) {
      await tryInitService()
      if (!getAttemptSummaryFn) {
        throw new Error('Service không khả dụng')
      }
    }
    
    const attemptData = await getAttemptSummaryFn(row.attemptId)
    attemptDetail.value = attemptData
    const classCodeFromAttempt =
      attemptData.class_name ||
      attemptData.student_class ||
      attemptData.student?.class_name ||
      attemptData.student_class_code ||
      row.classCode
    // Cập nhật điểm hiển thị theo tổng điểm thực
    viewingRow.value = {
      ...row,
      classCode: classCodeFromAttempt || row.classCode,
      score: attemptData.totalScore ?? row.score,
    }
    
    // Load exam detail to get full question info (choices, etc.)
    if (detailFn) {
      const examDetail = await detailFn(id.value)
      // Map exam questions with attempt data
      questions.value = (examDetail.questions || []).map((q: any) => {
        const attemptQ = attemptData.questions?.find((aq: any) => String(aq.id) === String(q.id))
        return {
          ...q,
          studentScore: attemptQ?.score || 0,
          studentCorrect: attemptQ?.correct || false,
        }
      })
    } else {
      // Fallback: use questions from attempt summary
      questions.value = (attemptData.questions || []).map((q: any) => ({
        id: q.id,
        text: q.prompt,
        type: 'single', // Default, should be inferred from exam detail
        score: q.points,
        choices: [],
      }))
    }
    
    // Map answers from attempt
    answers.value = attemptData.answers || {}
  } catch (e: any) {
    console.error('Error loading attempt detail:', e)
    const detail = e.response?.data?.detail || e.message || 'Lỗi không xác định'
    showToast(`Không thể tải chi tiết bài làm: ${detail}`, 'error')
    closeView()
  }
}

function closeView() {
  viewingRow.value = null
  attemptDetail.value = null
  questions.value = []
  answers.value = {}
}

const totalScore = computed(() => {
  return attemptDetail.value?.totalScore || attemptDetail.value?.score || 0
})

const maxScore = computed(() => {
  return attemptDetail.value?.maxScore || questions.value.reduce((sum, q) => sum + (q.score || 0), 0)
})

function getQuestionScore(questionId: string | number): number {
  if (!attemptDetail.value?.detail) {
    // Fallback: get from questions array
    const q = questions.value.find((q: any) => String(q.id) === String(questionId))
    return q?.studentScore || 0
  }
  const detail = attemptDetail.value.detail.find((d: any) => String(d.qid || d.question_id) === String(questionId))
  return detail?.score || 0
}

function getCorrectAnswer(q: any): string {
  if (q.type === 'single' || q.type === 'multi') {
    // Get correct choices from question answer field
    const correctChoiceIds = q.answer || []
    if (Array.isArray(correctChoiceIds) && correctChoiceIds.length > 0) {
      const correctChoices = q.choices?.filter((c: any) => correctChoiceIds.includes(c.id)) || []
      if (correctChoices.length > 0) {
        return correctChoices.map((c: any) => c.text).join(', ')
      }
    }
    // Fallback: show choice letters if we have choices
    if (q.choices && q.choices.length > 0) {
      const correctIndices = q.choices
        .map((c: any, idx: number) => (c.isCorrect || correctChoiceIds.includes(c.id)) ? idx : -1)
        .filter((idx: number) => idx >= 0)
      if (correctIndices.length > 0) {
        return correctIndices.map((idx: number) => String.fromCharCode(65 + idx)).join(', ')
      }
    }
    return '—'
  }
  if (q.type === 'boolean') {
    return q.answer === true || q.answer === 'true' ? 'Đúng' : 'Sai'
  }
  if (q.type === 'fill') {
    return Array.isArray(q.answer) ? q.answer.join(', ') : String(q.answer || '—')
  }
  if (q.type === 'match' && q.pairs) {
    return q.pairs.map((p: any) => `${p.left} → ${p.right}`).join('; ')
  }
  if (q.type === 'order' && Array.isArray(q.answer)) {
    return q.answer.join(' → ')
  }
  return String(q.answer || '—')
}

function getStudentAnswer(questionId: string | number): string {
  let answer: any = answers.value[String(questionId)]
  if (answer === null || answer === undefined || answer === '') {
    return 'Chưa trả lời'
  }
  // If answer is a JSON string, try parse
  if (typeof answer === 'string' && (answer.trim().startsWith('{') || answer.trim().startsWith('['))) {
    try {
      answer = JSON.parse(answer)
    } catch {
      // keep raw string
    }
  }
  // Array of objects
  if (Array.isArray(answer) && answer.some((v: any) => typeof v === 'object')) {
    const texts = answer.map((v: any) => v?.text || v?.value || v?.label || v?.id || String(v))
    return texts.join(', ')
  }
  // Object answer
  if (typeof answer === 'object' && !Array.isArray(answer)) {
    // Try choice id fields
    const obj = answer as any
    const choiceIds = obj.selected_choice_id
      ? [obj.selected_choice_id]
      : Array.isArray(obj.selected_choice_ids)
      ? obj.selected_choice_ids
      : Array.isArray(obj.selected_choices)
      ? obj.selected_choices
      : []
    // If we have choices, map to text
    if (choiceIds.length) {
      const q = questions.value.find((q: any) => String(q.id) === String(questionId))
      if (q?.choices?.length) {
        const found = q.choices.filter((c: any) => choiceIds.includes(c.id) || choiceIds.includes(String(c.id)))
        if (found.length) {
          return found.map((c: any) => c.text).join(', ')
        }
      }
    }
    const text = obj.text || obj.value || obj.label || obj.id
    if (text) return String(text)
    try {
      return JSON.stringify(answer)
    } catch {
      return String(answer)
    }
  }
  
  // Find question to get type and choices
  const q = questions.value.find((q: any) => String(q.id) === String(questionId))
  if (!q) {
    // Fallback: return raw answer
    return Array.isArray(answer) ? answer.join(', ') : String(answer)
  }
  
  if (q.type === 'single' || q.type === 'multi') {
    // Answer might be choice IDs or choice text
    const answerIds = Array.isArray(answer) ? answer : [answer]
    
    // Try to find choices by ID first
    if (q.choices && q.choices.length > 0) {
      const choices = q.choices.filter((c: any) => {
        return answerIds.includes(c.id) || answerIds.includes(String(c.id))
      })
      if (choices.length > 0) {
        return choices.map((c: any, idx: number) => {
          const letter = String.fromCharCode(65 + q.choices.indexOf(c))
          return `${letter}. ${c.text}`
        }).join(', ')
      }
      
      // Fallback: if answer is text, return as is
      if (typeof answer === 'string' || (Array.isArray(answer) && answer.every((a: any) => typeof a === 'string'))) {
        return Array.isArray(answer) ? answer.join(', ') : answer
      }
    }
    
    // If no choices available, return answer as is
    return Array.isArray(answer) ? answer.join(', ') : String(answer)
  }
  
  if (q.type === 'boolean') {
    return answer === true || answer === 'true' || answer === 1 ? 'Đúng' : 'Sai'
  }
  
  if (Array.isArray(answer)) {
    return answer.join(', ')
  }
  
  return String(answer)
}

function getQuestionTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    'single': 'Trắc nghiệm (1 đáp án)',
    'multi': 'Trắc nghiệm (nhiều đáp án)',
    'boolean': 'Đúng/Sai',
    'fill': 'Điền từ',
    'match': 'Nối cặp',
    'order': 'Sắp xếp'
  }
  return labels[type] || type.toUpperCase()
}

function isCorrectChoice(q: any, choice: any): boolean {
  if (q.type === 'single' || q.type === 'multi') {
    const correctIds = q.answer || []
    return correctIds.includes(choice.id) || (choice.isCorrect === true)
  }
  return false
}

function isStudentChoice(q: any, choice: any): boolean {
  const answer = answers.value[String(q.id)]
  if (!answer) return false
  
  if (q.type === 'single' || q.type === 'multi') {
    const answerIds = Array.isArray(answer) ? answer : [answer]
    return answerIds.includes(choice.id) || answerIds.includes(String(choice.id))
  }
  return false
}
</script>

<style scoped>
:host, .min-h-screen { overflow-x: hidden; }
table th, table td, h3 { word-break: break-word; }
@media (hover: none) {
  .hover\:bg-slate-50:hover { background: inherit; }
}
</style>
