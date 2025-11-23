<template>
  <div class="min-h-screen bg-slate-50 py-8">
    <div class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
      <header class="mb-6 rounded-lg border border-slate-200 bg-white px-5 py-4 shadow-sm">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 class="text-2xl font-bold text-slate-900">{{ exam?.title || 'Đề luyện tập' }}</h1>
            <p class="mt-1 flex flex-wrap gap-3 text-sm text-slate-600">
              <span>{{ labelLevel(exam?.level) }}</span>
              <span>• {{ Math.round((exam?.durationSec || 0) / 60) }} phút</span>
              <span>• {{ questions.length }} câu</span>
              <span>• Đạt ≥ {{ exam?.passScore || 10 }} điểm</span>
            </p>
          </div>
          <div class="flex items-center gap-3">
            <div
              class="inline-flex items-center gap-2 rounded-lg border px-4 py-2 text-sm font-semibold"
              :class="
                timeLeft <= 300
                  ? 'border-red-300 bg-red-50 text-red-700'
                  : 'border-slate-200 bg-white text-slate-900'
              "
            >
              <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                <path
                  fill-rule="evenodd"
                  d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zM12.75 6a.75.75 0 00-1.5 0v6c0 .414.336.75.75.75h4.5a.75.75 0 000-1.5h-3.75V6z"
                  clip-rule="evenodd"
                />
              </svg>
              <span>{{ fmtTime(timeLeft) }}</span>
            </div>
            <button
              type="button"
              class="rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition"
              @click="goBack"
            >
              Thoát
            </button>
            <button
              v-if="questions.length"
              type="button"
              class="rounded-lg border border-amber-300 bg-amber-50 px-4 py-2 text-sm font-semibold text-amber-700 hover:bg-amber-100 transition"
              @click="goFirstUnanswered"
            >
              Tới câu chưa làm
            </button>
          </div>
        </div>
      </header>

      <div v-if="loading" class="space-y-3">
        <div class="h-4 w-2/3 animate-pulse rounded bg-slate-200"></div>
        <div class="h-32 animate-pulse rounded-lg bg-slate-100"></div>
        <div class="h-4 w-3/4 animate-pulse rounded bg-slate-200"></div>
      </div>

      <main v-else class="grid gap-6 lg:grid-cols-[minmax(260px,320px)_minmax(0,1fr)]">
        <section class="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <h3 class="text-base font-semibold text-slate-900 mb-4">Danh sách câu hỏi</h3>
            <div class="grid grid-cols-5 gap-2 sm:grid-cols-6">
            <button
              v-for="(q, i) in questions"
              :key="q.id"
              class="flex h-10 items-center justify-center rounded-lg border text-sm font-semibold transition"
              :class="[
                i === idx
                  ? 'border-slate-900 bg-slate-900 text-white'
                  : 'border-slate-200 bg-white text-slate-900',
                isAnswered(q.id) && i !== idx ? 'border-blue-500 bg-blue-50 text-blue-700' : '',
                !isAnswered(q.id) && i !== idx ? 'border-amber-200 bg-amber-50 text-amber-700' : '',
              ]"
              @click="go(i)"
            >
              {{ i + 1 }}
            </button>
          </div>
        </section>

        <section class="space-y-4">
          <div class="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <div class="flex items-center justify-between text-sm font-semibold text-slate-600 mb-4">
              <span class="text-slate-900">Câu {{ idx + 1 }}</span>
              <span class="rounded-full border border-slate-200 px-3 py-1 text-xs uppercase">
                {{ getQuestionTypeLabel(q?.type) }}
              </span>
            </div>
            <div class="space-y-4">
              <div class="prose prose-sm max-w-none text-slate-900" v-html="q?.text"></div>

              <template v-if="q?.type === 'single' || q?.type === 'multi'">
                <ul class="space-y-3">
                  <li
                    v-for="opt in q.choices"
                    :key="opt.id"
                    class="rounded-lg border transition cursor-pointer"
                    :class="getAnswer(q.id) === opt.id || (Array.isArray(getAnswer(q.id)) && getAnswer(q.id).includes(opt.id))
                      ? 'border-slate-900 bg-slate-50 ring-2 ring-slate-200' 
                      : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50'"
                  >
                    <label
                      class="flex items-center gap-3 px-4 py-3 text-sm font-semibold cursor-pointer"
                      :class="getAnswer(q.id) === opt.id || (Array.isArray(getAnswer(q.id)) && getAnswer(q.id).includes(opt.id)) ? 'text-slate-900' : 'text-slate-700'"
                    >
                      <input
                        :type="q.type === 'single' ? 'radio' : 'checkbox'"
                        class="h-4 w-4 text-slate-900 focus:ring-slate-200"
                        :name="'q_' + q.id"
                        :value="opt.id"
                        :checked="getAnswer(q.id) === opt.id || (Array.isArray(getAnswer(q.id)) && getAnswer(q.id).includes(opt.id))"
                        @change="handleChoiceChange(q.id, opt.id, q.type === 'multi')"
                      />
                      <span
                        class="inline-flex h-7 w-7 items-center justify-center rounded-full text-sm font-bold"
                        :class="getAnswer(q.id) === opt.id || (Array.isArray(getAnswer(q.id)) && getAnswer(q.id).includes(opt.id)) ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-700'"
                      >
                        {{ String.fromCharCode(65 + (q.choices?.indexOf(opt) || 0)) }}
                      </span>
                      <span class="flex-1" v-html="opt.text"></span>
                    </label>
                  </li>
                </ul>
              </template>

              <template v-else-if="q?.type === 'boolean'">
                <div class="grid gap-3 sm:grid-cols-2">
                  <label
                    class="flex items-center justify-center rounded-lg border px-4 py-3 text-sm font-semibold transition cursor-pointer"
                    :class="getAnswer(q.id) === true || getAnswer(q.id) === 'true' || getAnswer(q.id) === 'T'
                      ? 'border-slate-900 bg-slate-50 text-slate-900 ring-2 ring-slate-200'
                      : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300 hover:bg-slate-50'"
                  >
                    <input
                      type="radio"
                      class="sr-only"
                      :name="'q_' + q.id"
                      value="T"
                      :checked="getAnswer(q.id) === true || getAnswer(q.id) === 'true' || getAnswer(q.id) === 'T'"
                      @change="setAnswer(q.id, true)"
                    />
                    Đúng
                  </label>
                  <label
                    class="flex items-center justify-center rounded-lg border px-4 py-3 text-sm font-semibold transition cursor-pointer"
                    :class="getAnswer(q.id) === false || getAnswer(q.id) === 'false' || getAnswer(q.id) === 'F'
                      ? 'border-slate-900 bg-slate-50 text-slate-900 ring-2 ring-slate-200'
                      : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300 hover:bg-slate-50'"
                  >
                    <input
                      type="radio"
                      class="sr-only"
                      :name="'q_' + q.id"
                      value="F"
                      :checked="getAnswer(q.id) === false || getAnswer(q.id) === 'false' || getAnswer(q.id) === 'F'"
                      @change="setAnswer(q.id, false)"
                    />
                    Sai
                  </label>
                </div>
              </template>

              <template v-else-if="q?.type === 'fill'">
                <div class="space-y-2">
                  <input
                    v-for="(blank, blankIdx) in Array(q.blanks || 1)"
                    :key="blankIdx"
                    class="w-full rounded-lg border border-slate-300 px-4 py-3 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
                    :value="Array.isArray(getAnswer(q.id)) ? getAnswer(q.id)[blankIdx] : (blankIdx === 0 ? getAnswer(q.id) : '')"
                    @input="handleFillChange(q.id, blankIdx, ($event.target as HTMLInputElement).value, q.blanks || 1)"
                    :placeholder="`Nhập câu trả lời ${blankIdx + 1}...`"
                  />
                </div>
              </template>

              <template v-else>
                <input
                  class="w-full rounded-lg border border-slate-300 px-4 py-3 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
                  :value="getAnswer(q.id) ?? ''"
                  @input="setAnswer(q.id, ($event.target as HTMLInputElement).value)"
                  placeholder="Nhập câu trả lời của bạn..."
                />
              </template>
            </div>
          </div>

          <div class="flex flex-col gap-3 rounded-lg border border-slate-200 bg-white px-4 py-3 shadow-sm sm:flex-row sm:items-center sm:justify-between">
            <button
              type="button"
              class="inline-flex items-center justify-center rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition disabled:opacity-50"
              :disabled="idx === 0"
              @click="prev"
            >
              ‹ Câu trước
            </button>
            <div
              v-if="idx === questions.length - 1 && questions.length > 0"
              class="text-center text-sm font-semibold text-slate-600"
            >
              {{ answeredCount }}/{{ questions.length }} câu đã trả lời
            </div>
            <button
              v-if="idx === questions.length - 1 && questions.length > 0"
              type="button"
              class="inline-flex items-center justify-center rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-700 transition disabled:opacity-50"
              :disabled="submitting"
              @click="submit"
            >
              {{ submitting ? 'Đang nộp…' : 'Nộp bài' }}
            </button>
            <button
              v-else
              type="button"
              class="inline-flex items-center justify-center rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800 transition disabled:opacity-50"
              :disabled="idx === questions.length - 1"
              @click="next"
            >
              Câu tiếp ›
            </button>
          </div>
        </section>
      </main>
    </div>

    <transition
      enter-active-class="transition duration-200"
      leave-active-class="transition duration-150"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <div
        v-if="showSubmitModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 px-4"
        @click.self="showSubmitModal = false"
      >
        <div class="w-full max-w-md rounded-lg border border-slate-200 bg-white p-6 shadow-lg">
          <header class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-bold text-slate-900">Xác nhận nộp bài</h3>
            <button
              type="button"
              class="rounded-lg p-2 text-slate-600 hover:bg-slate-100"
              aria-label="Đóng"
              @click="showSubmitModal = false"
            >
              ×
            </button>
          </header>
          <section class="mb-6 text-sm text-slate-900">
            <p v-html="submitMsg"></p>
          </section>
          <footer class="flex flex-col gap-3 sm:flex-row sm:justify-end">
            <button
              type="button"
              class="rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition"
              :disabled="submitting"
              @click="showSubmitModal = false"
            >
              Tiếp tục làm
            </button>
            <button
              type="button"
              class="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-700 transition disabled:opacity-50"
              :disabled="submitting"
              @click="confirmSubmit"
            >
              {{ submitting ? 'Đang nộp…' : 'Nộp bài' }}
            </button>
          </footer>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, computed, shallowRef, ref, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from '@/utils/toast'
import { examService, type AttemptQuestion, type ExamDetail } from '@/services/exam.service'
import { useAuthStore } from '@/store/auth.store'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

// Exam info from API
const exam = ref<ExamDetail | null>(null)
const attemptId = ref<string | null>(null)

const loading = ref(true)
const questions = shallowRef<AttemptQuestion[]>([])
const answers = ref<Record<string, any>>({}) // Map questionId -> answer
const idx = ref(0)
const submitting = ref(false)
const duration = ref(0)
const timeLeft = ref(0)
let timer: number | null = null
let autosaveTimer: number | null = null
// Dùng khóa lưu trữ gắn với tài khoản (ưu tiên id, sau đó email/username) để tránh đè lẫn giữa các user
const userKey = computed(() => {
  const u = auth.user
  return String(
    u?.id ??
    u?.email ??
    u?.name ??
    'guest'
  )
})
const storageKey = computed(() => `exam_answers_${route.params.id || ''}_${userKey.value}`)
const doneKey = computed(() => `exam_done_${route.params.id || ''}_${userKey.value}`)

const q = computed(() => questions.value[idx.value])
const answeredCount = computed(
  () => Object.keys(answers.value).filter((qid) => {
    const ans = answers.value[qid]
    if (Array.isArray(ans)) return ans.length > 0
    return (ans ?? '').toString().trim() !== ''
  }).length,
)

function labelLevel(level?: string) {
  if (!level) return 'Cơ bản'
  const levelMap: Record<string, string> = {
    'Khối 1': 'Cơ bản',
    'Khối 2': 'Cơ bản',
    'Khối 3': 'Cơ bản',
    'Khối 4': 'Nâng cao',
    'Khối 5': 'Nâng cao',
  }
  return levelMap[level] || 'Cơ bản'
}
function fmtTime(s: number) {
  const m = Math.floor(s / 60)
  const ss = s % 60
  return `${m.toString().padStart(2, '0')}:${ss.toString().padStart(2, '0')}`
}

// ===== Popup nộp bài =====
const showSubmitModal = ref(false)
const submitMsg = computed(() => {
  const unanswered = questions.value.length - answeredCount.value
  return unanswered > 0
    ? `Bạn còn <b>${unanswered}</b> câu chưa trả lời. Bạn có chắc chắn muốn nộp bài không?`
    : 'Bạn đã trả lời hết các câu hỏi. Xác nhận nộp bài?'
})

// Mở popup khi ấn nút "Nộp bài"
function submit() {
  showSubmitModal.value = true
}

// Thực sự nộp bài khi người dùng xác nhận trong popup
async function confirmSubmit() {
  if (submitting.value || !attemptId.value) return
  submitting.value = true
  stopTimer()
  await nextTick()

  try {
    const result = await examService.submit(route.params.id as string, attemptId.value, answers.value)
    
    showSubmitModal.value = false
    showToast('Đã nộp bài thành công!', 'success')
    // đánh dấu đã hoàn thành để khóa làm lại
    try {
      localStorage.setItem(doneKey.value, attemptId.value)
    } catch (e) {
      console.warn('Cannot persist done flag', e)
    }

    router.push({
      name: 'student-exam-result',
      params: { id: route.params.id },
      query: { attemptId: attemptId.value },
    })
  } catch (err: any) {
    console.error('Submit error:', err)
    showToast(err?.message || 'Không thể nộp bài. Vui lòng thử lại.', 'error')
  } finally {
    submitting.value = false
  }
}

// ===== Các hàm sẵn có =====
function goBack() {
  // Show warning toast and go back after a short delay
  showToast('Mọi tiến trình làm bài sẽ không được lưu lại.', 'warning')
  setTimeout(() => {
    router.back()
  }, 1500)
}
function go(i: number) {
  if (i >= 0 && i < questions.value.length) idx.value = i
}
function next() {
  if (idx.value < questions.value.length - 1) idx.value++
}
function prev() {
  if (idx.value > 0) idx.value--
}
function goFirstUnanswered() {
  const first = questions.value.findIndex((question) => !isAnswered(question.id))
  if (first >= 0) idx.value = first
}
function isAnswered(qid: string | number) {
  const ans = answers.value[qid]
  if (Array.isArray(ans)) return ans.length > 0 && ans.some(a => (a ?? '').toString().trim() !== '')
  return (ans ?? '').toString().trim() !== ''
}
function stopTimer() {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
  if (autosaveTimer) {
    clearInterval(autosaveTimer)
    autosaveTimer = null
  }
}

function getAnswer(qid: string | number) {
  return answers.value[qid]
}

function setAnswer(qid: string | number, val: any) {
  answers.value = { ...answers.value, [qid]: val }
  try {
    localStorage.setItem(storageKey.value, JSON.stringify(answers.value))
  } catch (e) {
    console.warn('Cannot save draft', e)
  }
}

function handleChoiceChange(qid: string | number, choiceId: string, isMulti: boolean) {
  if (isMulti) {
    const current = Array.isArray(answers.value[qid]) ? answers.value[qid] : []
    const newAnswer = current.includes(choiceId)
      ? current.filter((id: string) => id !== choiceId)
      : [...current, choiceId]
    setAnswer(qid, newAnswer)
  } else {
    setAnswer(qid, choiceId)
  }
}

function handleFillChange(qid: string | number, blankIdx: number, value: string, totalBlanks: number) {
  const current = Array.isArray(answers.value[qid]) ? [...answers.value[qid]] : []
  while (current.length < totalBlanks) current.push('')
  current[blankIdx] = value
  setAnswer(qid, current)
}

function getQuestionTypeLabel(type?: string) {
  const labels: Record<string, string> = {
    'single': 'MCQ',
    'multi': 'MCQ',
    'boolean': 'TF',
    'fill': 'FILL',
    'match': 'MATCH',
    'order': 'ORDER',
  }
  return labels[type || ''] || type?.toUpperCase() || 'MCQ'
}

// Load exam and start attempt
async function loadExamAndStart() {
  try {
    loading.value = true
    const examId = route.params.id as string
    
    // Check if we're already on result page (shouldn't happen, but safety check)
    if (route.name === 'student-exam-result') {
      router.push({ name: 'student-exams' })
      return
    }
    
    // Load exam detail
    exam.value = await examService.detail(examId)
    
    // Start attempt to get questions
    try {
      const attempt = await examService.startAttempt(examId)
      attemptId.value = attempt.id
      questions.value = attempt.questions
      answers.value = { ...attempt.answers }
      // Merge any locally saved draft (last write wins)
      try {
        const cached = localStorage.getItem(storageKey.value)
        if (cached) {
          const parsed = JSON.parse(cached)
          if (parsed && typeof parsed === 'object') {
            answers.value = { ...answers.value, ...parsed }
          }
        }
      } catch (e) {
        console.warn('Cannot load draft', e)
      }
      
      // Calculate duration and time left
      const deadline = new Date(attempt.deadlineAt)
      const now = new Date()
      const secondsLeft = Math.max(0, Math.floor((deadline.getTime() - now.getTime()) / 1000))
      
      duration.value = exam.value.durationSec
      timeLeft.value = secondsLeft
      
      // Start timer
      timer = window.setInterval(() => {
        timeLeft.value--
        if (timeLeft.value <= 0) {
          stopTimer()
          // Hết giờ: tự động nộp
          confirmSubmit()
        }
      }, 1000) as unknown as number
      // Autosave every 15s
      autosaveTimer = window.setInterval(() => {
        try {
          localStorage.setItem(storageKey.value, JSON.stringify(answers.value))
        } catch (e) {
          console.warn('Cannot save draft', e)
        }
      }, 15000) as unknown as number
      
      loading.value = false
    } catch (attemptErr: any) {
      // Nếu đã có attempt finished, redirect đến result page
      const errorMsg = attemptErr?.message || attemptErr?.response?.data?.detail || ''
      if (errorMsg.includes('đã hoàn thành') || errorMsg.includes('already completed') || errorMsg.includes('chỉ được làm 1 lần')) {
        // Extract attempt ID from error message if available
        const attemptIdMatch = errorMsg.match(/Attempt ID: ([a-f0-9-]+)/i)
        const finishedAttemptId = attemptIdMatch ? attemptIdMatch[1] : null
        
        if (finishedAttemptId) {
          try {
            localStorage.setItem(`exam_done_${examId}_${userKey.value}`, finishedAttemptId)
          } catch (e) {
            console.warn('Cannot persist done flag', e)
          }
          // Redirect ngay lập tức, không cần toast và delay
          // Replace current route instead of push to avoid back button issues
          router.replace({
            name: 'student-exam-result',
            params: { id: examId },
            query: { attemptId: finishedAttemptId },
          })
          return
        } else {
          // Nếu không có attemptId, redirect về danh sách
          router.replace({ name: 'student-exams' })
          return
        }
      }
      if (errorMsg.toLowerCase().includes('expired') || errorMsg.includes('closed') || errorMsg.includes('deadline')) {
        showToast('Bài kiểm tra đã kết thúc hoặc quá hạn.', 'warning')
        router.replace({ name: 'student-exams' })
        return
      }
      // Các lỗi khác: hiển thị và quay lại
      throw attemptErr
    }
  } catch (err: any) {
    console.error('Load exam error:', err)
    showToast(err?.message || 'Không thể tải bài kiểm tra. Vui lòng thử lại.', 'error')
    router.back()
  }
}

onMounted(async () => {
  await loadExamAndStart()
  window.addEventListener('beforeunload', beforeUnload)
})

onBeforeUnmount(() => {
  stopTimer()
  window.removeEventListener('beforeunload', beforeUnload)
})

function beforeUnload(e: BeforeUnloadEvent) {
  if (answeredCount.value > 0 && !submitting.value) {
    e.preventDefault()
    e.returnValue = ''
  }
}
</script>
