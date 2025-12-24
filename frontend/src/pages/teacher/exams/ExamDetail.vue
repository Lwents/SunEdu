<!-- src/pages/teacher/exams/ExamDetail.vue -->
<template>
  <div class="min-h-screen w-full overflow-x-hidden" :class="isDark ? 'bg-slate-950' : 'bg-slate-50'">
    <!-- Đang tải -->
    <main v-if="loading" class="mx-auto max-w-screen-md px-6 py-16">
      <div class="mb-4 h-7 w-64 animate-pulse rounded bg-slate-200"></div>
      <div class="mb-8 h-4 w-80 animate-pulse rounded bg-slate-100"></div>
      <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
        <div class="rounded-2xl border border-slate-200 bg-white p-4 md:col-span-2 space-y-2">
          <div v-for="i in 6" :key="'skel-q-'+i" class="rounded-xl border p-3">
            <div class="mb-2 flex items-center justify-between">
              <div class="h-4 w-40 animate-pulse rounded bg-slate-200"></div>
              <div class="h-3 w-16 animate-pulse rounded bg-slate-100"></div>
            </div>
            <div class="h-4 w-3/4 animate-pulse rounded bg-slate-100"></div>
          </div>
        </div>
        <div class="rounded-2xl border border-slate-200 bg-white p-4 space-y-2">
          <div class="h-5 w-32 animate-pulse rounded bg-slate-200"></div>
          <div v-for="i in 5" :key="'skel-r-'+i" class="h-4 w-48 animate-pulse rounded bg-slate-100"></div>
        </div>
      </div>
    </main>

    <!-- Có dữ liệu -->
    <main v-else-if="exam" class="w-full mx-auto max-w-screen-2xl px-4 py-6 sm:px-6 md:px-10 md:py-8">
      <!-- Header với thông tin tổng quan -->
      <div class="mb-6 rounded-2xl border border-slate-200 bg-white p-6">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div class="flex-1">
            <div class="mb-3 flex items-center gap-3">
              <h1 class="text-2xl font-bold text-slate-900">{{ exam.title }}</h1>
              <span
                class="rounded-full border px-3 py-1 text-xs font-medium"
                :class="exam.status==='published'
                         ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                         : exam.status === 'scheduled'
                         ? 'bg-blue-50 text-blue-700 border-blue-200'
                         : 'bg-amber-50 text-amber-700 border-amber-200'"
              >
                {{ exam.status === 'published' ? 'Đã phát hành' : exam.status === 'scheduled' ? 'Đã lên lịch' : 'Nháp' }}
              </span>
            </div>
            
            <!-- Thông tin cơ bản -->
            <div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
              <div>
                <div class="text-xs text-slate-500">Khối lớp</div>
                <div class="text-sm font-semibold text-slate-900">{{ exam.course }}</div>
              </div>
              <div>
                <div class="text-xs text-slate-500">Thời gian</div>
                <div class="text-sm font-semibold text-slate-900">{{ exam.durationMin }} phút</div>
              </div>
              <div>
                <div class="text-xs text-slate-500">Số câu hỏi</div>
                <div class="text-sm font-semibold text-slate-900">{{ exam.totalQuestions }}</div>
              </div>
              <div>
                <div class="text-xs text-slate-500">Tổng điểm</div>
                <div class="text-sm font-semibold text-slate-900">{{ totalPoints }}</div>
              </div>
            </div>

            <!-- Mô tả -->
            <div v-if="exam.description" class="mt-4 rounded-lg bg-slate-50 p-3">
              <div class="text-xs font-medium text-slate-600 mb-1">Mô tả</div>
              <p class="text-sm text-slate-700 whitespace-pre-wrap">{{ exam.description }}</p>
            </div>
          </div>

          <!-- Action buttons -->
          <div class="flex flex-col gap-2 sm:flex-row">
            <button 
              class="rounded-xl border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 transition-colors" 
              @click="toGrading"
            >
              Xem bài làm
            </button>
            <button 
              class="rounded-xl bg-sky-600 px-4 py-2 text-sm font-semibold text-white hover:bg-sky-700 transition-colors" 
              @click="toEdit"
            >
              Sửa đề
            </button>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <!-- Danh sách câu hỏi -->
        <div class="lg:col-span-2">
          <div class="rounded-2xl border border-slate-200 bg-white p-6">
            <div class="mb-4 flex items-center justify-between">
              <h2 class="text-lg font-semibold text-slate-900">Danh sách câu hỏi</h2>
              <span class="text-sm text-slate-500">{{ questions.length }} câu</span>
            </div>
            
            <div v-if="questions.length > 0" class="space-y-4">
              <div 
                v-for="q in questions" 
                :key="q.no" 
                class="rounded-xl border border-slate-200 bg-slate-50 p-5 hover:border-slate-300 hover:shadow-sm transition-all"
              >
                <!-- Header câu hỏi -->
                <div class="mb-3 flex items-center justify-between border-b border-slate-200 pb-2">
                  <div class="flex items-center gap-2">
                    <span class="flex h-8 w-8 items-center justify-center rounded-full bg-sky-100 text-sm font-bold text-sky-700">
                      {{ q.no }}
                    </span>
                    <span class="rounded-full bg-white border border-slate-300 px-2 py-0.5 text-xs font-medium text-slate-700">
                      {{ getQuestionTypeLabel(q.type) }}
                    </span>
                  </div>
                  <span class="text-sm font-semibold text-slate-700">{{ q.points }} điểm</span>
                </div>

                <!-- Nội dung câu hỏi -->
                <div class="mb-3">
                  <p class="text-sm font-medium text-slate-900 leading-relaxed">{{ q.questionText }}</p>
                </div>

                <!-- Đáp án (nếu có) -->
                <div v-if="q.choices && q.choices.length > 0" class="space-y-2">
                  <div class="text-xs font-medium text-slate-600 mb-2">Đáp án:</div>
                  <div 
                    v-for="(choice, idx) in q.choices" 
                    :key="idx"
                    class="flex items-start gap-2 rounded-lg p-2"
                    :class="choice.is_correct ? 'bg-emerald-50 border border-emerald-200' : 'bg-white border border-slate-200'"
                  >
                    <span class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-semibold"
                      :class="choice.is_correct ? 'bg-emerald-600 text-white' : 'bg-slate-200 text-slate-700'"
                    >
                      {{ String.fromCharCode(65 + idx) }}
                    </span>
                    <span class="flex-1 text-sm text-slate-700">{{ choice.text }}</span>
                    <span v-if="choice.is_correct" class="text-emerald-600 font-semibold">✓</span>
                  </div>
                </div>

                <!-- Đáp án đúng cho các loại câu hỏi khác -->
                <div v-if="q.correctAnswer" class="mt-3 rounded-lg bg-emerald-50 border border-emerald-200 p-2">
                  <div class="text-xs font-medium text-emerald-700 mb-1">Đáp án đúng:</div>
                  <div class="text-sm text-emerald-900">{{ q.correctAnswer }}</div>
                </div>
              </div>
            </div>
            
            <div v-else class="py-12 text-center">
              <p class="text-sm text-slate-500">Chưa có câu hỏi nào</p>
            </div>
          </div>
        </div>

        <!-- Sidebar - Thông tin tổng quan -->
        <div class="space-y-4">
          <!-- Thống kê -->
          <div class="rounded-2xl border border-slate-200 bg-white p-5">
            <h3 class="mb-4 text-base font-semibold text-slate-900">Thống kê</h3>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <span class="text-sm text-slate-600">Bài nộp</span>
                <span class="text-sm font-semibold text-slate-900">{{ exam.submissions }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-slate-600">Điểm trung bình</span>
                <span class="text-sm font-semibold text-slate-900">{{ exam.avgScore }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-slate-600">Điểm đạt tối thiểu</span>
                <span class="text-sm font-semibold text-slate-900">{{ exam.passScore || 10 }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-slate-600">Tổng điểm</span>
                <span class="text-sm font-semibold text-sky-600">{{ totalPoints }}</span>
              </div>
            </div>
          </div>

          <!-- Thông tin khác -->
          <div class="rounded-2xl border border-slate-200 bg-white p-5">
            <h3 class="mb-4 text-base font-semibold text-slate-900">Thông tin</h3>
            <div class="space-y-3 text-sm">
              <div>
                <div class="text-slate-500 mb-1">Cập nhật lần cuối</div>
                <div class="font-medium text-slate-900">{{ exam.updatedAt }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Không tìm thấy -->
    <main v-else class="mx-auto max-w-screen-md px-6 py-16 text-center">
      <h1 class="text-xl font-semibold">Không tìm thấy đề</h1>
      <p class="mt-2 text-slate-500">Vui lòng quay lại danh sách bài kiểm tra.</p>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThemeStore } from '@/store/theme.store'

/** View models */
type ExamStatus = 'published' | 'scheduled' | 'draft'
type ExamVM = {
  id: number
  title: string
  course: string     // dùng level từ service nếu không có course
  durationMin: number
  totalQuestions: number
  status: ExamStatus
  submissions: number
  avgScore: number | string
  updatedAt: string
  scheduledAt: string
  passScore?: number
  description?: string
}
type QVM = { 
  no: number
  type: string
  points: number
  text: string
  questionText?: string
  choices?: Array<{ text: string; is_correct: boolean }>
  correctAnswer?: string
}

/** Router & state */
const route = useRoute()
const router = useRouter()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

// Helper function to parse ID from route params
function parseId(paramId: string | string[]): string | number {
  const idStr = Array.isArray(paramId) ? paramId[0] : paramId
  if (typeof idStr === 'string' && idStr.includes('-')) {
    return idStr
  }
  const numId = Number(idStr)
  return isNaN(numId) ? idStr : numId
}

const id = ref<string | number>(parseId(route.params.id))

const loading = ref(true)
const exam = ref<ExamVM | null>(null)
const questions = ref<QVM[]>([])

// Computed
const totalPoints = computed(() => {
  return questions.value.reduce((sum, q) => sum + q.points, 0)
})

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

/** Optional service (không sửa service) */
type DetailFn = (id: string | number) => Promise<any>
let detailFn: DetailFn | undefined

async function tryInitService() {
  try {
    const mod = await import('@/services/exam.service')
    if (mod?.examService?.detail) {
      detailFn = mod.examService.detail as DetailFn
    }
  } catch {
    // fallback mock
  }
}

/** Map ExamDetail (service) -> ExamVM/QVM */
function mapFromService(d: any): { exam: ExamVM; questions: QVM[] } {
  const durationMin = Math.max(1, Math.round((Number(d.durationSec) || 0) / 60))
  const st: ExamStatus = d.status === 'published' ? 'published' : (d.status === 'scheduled' ? 'scheduled' : 'draft')
  const examId = typeof d.id === 'string' && d.id.includes('-') ? d.id : (Number(d.id) || d.id)
  
  const vm: ExamVM = {
    id: typeof examId === 'string' ? 0 : examId, // For display, use 0 for UUID
    title: String(d.title || `Đề #${examId}`),
    course: String(d.level || d.settings?.level || d.metadata?.level || '—'),
    durationMin,
    totalQuestions: Number(d.questionsCount || (d.questions?.length ?? 0)),
    status: st,
    submissions: Number(d.submissions || 0),
    avgScore: Number(d.avgScore || 0).toFixed(1),
    updatedAt: new Date(d.updatedAt || Date.now()).toLocaleString('vi-VN'),
    scheduledAt: d.scheduledAt || new Date(d.updatedAt || Date.now()).toLocaleString('vi-VN'),
    passScore: Number(d.passScore || d.settings?.pass_score || 10),
    description: d.description || d.settings?.description || ''
  }
  
  const qs: QVM[] = (d.questions || []).map((q: any, i: number) => {
    const questionType = q.meta?.type || q.type || 'single'
    const questionScore = q.meta?.score || q.score || 1
    const questionText = String(q.prompt || q.text || `Câu hỏi #${i + 1}`)
    
    const result: QVM = {
    no: i + 1,
      type: String(questionType),
      points: Number(questionScore),
      text: questionText,
      questionText: questionText
    }
    
    // Add choices for single/multi questions
    if ((questionType === 'single' || questionType === 'multi') && q.choices && q.choices.length > 0) {
      result.choices = q.choices.map((c: any) => ({
        text: c.text || '',
        is_correct: c.is_correct || false
      }))
    }
    
    // Add correct answer for other question types
    // Note: answers are stored in the question data from backend
    if (questionType === 'boolean') {
      // For boolean, check if there's an answer in meta or direct
      const answer = q.meta?.answer !== undefined ? q.meta.answer : (q.answer !== undefined ? q.answer : null)
      if (answer !== null) {
        result.correctAnswer = answer === true ? 'Đúng' : 'Sai'
      }
    } else if (questionType === 'fill') {
      // For fill, answer is usually in meta or as answer field
      const answer = q.meta?.answer || q.answer
      if (Array.isArray(answer)) {
        result.correctAnswer = answer.join(', ')
      }
    } else if (questionType === 'match') {
      // For match, pairs are in the question
      if (q.pairs && Array.isArray(q.pairs)) {
        result.correctAnswer = q.pairs.map((p: any) => `${p.left} → ${p.right}`).join('; ')
      }
    } else if (questionType === 'order') {
      // For order, answer is the correct order
      const answer = q.meta?.answer || q.answer
      if (Array.isArray(answer)) {
        result.correctAnswer = answer.join(' → ')
      }
    }
    
    return result
  })
  
  return { exam: vm, questions: qs }
}

/** Mock khi không có service */
function mockDetail(examId: number): { exam: ExamVM; questions: QVM[] } {
  const published = examId % 3 !== 1
  const vm: ExamVM = {
    id: examId,
    title: `Đề kiểm tra #${examId}`,
    course: `Khoá ${(examId % 6) + 1}`,
    durationMin: 20 + (examId % 6) * 5,
    totalQuestions: 24,
    status: published ? 'published' : 'draft',
    submissions: (examId * 13) % 120,
    avgScore: ((60 + (examId % 40)) / 10).toFixed(1),
    updatedAt: new Date(Date.now() - examId * 36e5).toLocaleString(),
    scheduledAt: new Date(Date.now() + (examId % 5) * 864e5).toLocaleString()
  }
  const types = ['single', 'multi', 'boolean', 'fill', 'match', 'order']
  const qs: QVM[] = Array.from({ length: vm.totalQuestions }).map((_, i) => ({
    no: i + 1,
    type: types[(i + examId) % types.length],
    points: 1 + ((i + examId) % 3),
    text: `Nội dung câu hỏi mẫu số ${i + 1}`
  }))
  return { exam: vm, questions: qs }
}

/** Fetch detail (chống race) */
let loadToken = 0
async function load(currentId = id.value) {
  const token = ++loadToken
  loading.value = true
  try {
    if (!currentId) {
      exam.value = null
      questions.value = []
      return
    }

    if (!detailFn) {
      await tryInitService()
      if (!detailFn) {
        // Fallback to mock only if service really doesn't exist
        const examId = typeof currentId === 'string' ? 0 : Number(currentId)
        if (examId > 0) {
      const mapped = mockDetail(examId)
      if (token !== loadToken) return
      exam.value = mapped.exam
      questions.value = mapped.questions
        }
      return
      }
    }

    const d = await detailFn(currentId)
    if (token !== loadToken) return
    const mapped = mapFromService(d)
    exam.value = mapped.exam
    questions.value = mapped.questions
  } catch (e: any) {
    console.error('Load exam detail error:', e)
    if (token === loadToken) {
      exam.value = null
      questions.value = []
    }
  } finally {
    if (token === loadToken) loading.value = false
  }
}

/** Actions */
function toGrading() {
  router.push({ path: `/teacher/exams/${id.value}/grading` })
}
function toEdit() {
  router.push({ path: `/teacher/exams/${id.value}/edit` })
}

/** Lifecycle */
onMounted(async () => {
  await tryInitService()
  await load(id.value)
})

watch(() => route.params.id, (nv) => {
  id.value = parseId(nv)
  load(id.value)
})
</script>

<style scoped>
:host, .min-h-screen { overflow-x: hidden; }
</style>
