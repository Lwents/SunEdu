<template>
  <div class="page-wrapper" :class="isDark ? 'dark-mode' : 'light-mode'">
    <!-- Background Elements -->
    <div v-if="isDark" class="bg-elements">
      <div class="glow glow-1"></div>
      <div class="glow glow-2"></div>
    </div>

    <div class="page-content">
      <header class="exam-header">
        <div class="header-content">
          <div class="header-info">
            <h1 class="exam-title">{{ exam?.title || 'Đề luyện tập' }}</h1>
            <p class="exam-meta">
              <span>{{ labelLevel(exam?.level) }}</span>
              <span>• {{ Math.round((exam?.durationSec || 0) / 60) }} phút</span>
              <span>• {{ questions.length }} câu</span>
              <span>• Đạt ≥ {{ exam?.passScore || 10 }} điểm</span>
            </p>
          </div>
          <div class="header-actions">
            <div class="timer-badge" :class="{ 'timer-warning': timeLeft <= 300 }">
              <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zM12.75 6a.75.75 0 00-1.5 0v6c0 .414.336.75.75.75h4.5a.75.75 0 000-1.5h-3.75V6z" clip-rule="evenodd" />
              </svg>
              <span>{{ fmtTime(timeLeft) }}</span>
            </div>
            <button v-if="questions.length" type="button" class="btn-warning" @click="goFirstUnanswered">Tới câu chưa làm</button>
          </div>
        </div>
      </header>

      <div v-if="loading" class="loading-state">
        <div class="skeleton skeleton-title"></div>
        <div class="skeleton skeleton-content"></div>
        <div class="skeleton skeleton-text"></div>
      </div>

      <main v-else class="exam-main">
        <section class="questions-sidebar">
          <h3 class="sidebar-title">Danh sách câu hỏi</h3>
          <div class="questions-grid">
            <button
              v-for="(q, i) in questions"
              :key="q.id"
              class="question-num-btn"
              :class="{
                'active': i === idx,
                'answered': isAnswered(q.id) && i !== idx,
                'unanswered': !isAnswered(q.id) && i !== idx
              }"
              @click="go(i)"
            >
              {{ i + 1 }}
            </button>
          </div>
        </section>

        <section class="question-area">
          <div class="question-card">
            <div class="question-header">
              <span class="question-number">Câu {{ idx + 1 }}</span>
              <span class="question-type">{{ getQuestionTypeLabel(q?.type) }}</span>
            </div>
            <div class="question-body">
              <div class="question-text" v-html="q?.text"></div>

              <template v-if="q?.type === 'single' || q?.type === 'multi'">
                <ul class="choices-list">
                  <li
                    v-for="opt in q.choices"
                    :key="opt.id"
                    class="choice-item"
                    :class="{ 'selected': getAnswer(q.id) === opt.id || (Array.isArray(getAnswer(q.id)) && getAnswer(q.id).includes(opt.id)) }"
                  >
                    <label class="choice-label">
                      <input
                        :type="q.type === 'single' ? 'radio' : 'checkbox'"
                        class="choice-input"
                        :name="'q_' + q.id"
                        :value="opt.id"
                        :checked="getAnswer(q.id) === opt.id || (Array.isArray(getAnswer(q.id)) && getAnswer(q.id).includes(opt.id))"
                        @change="handleChoiceChange(q.id, opt.id, q.type === 'multi')"
                      />
                      <span class="choice-letter" :class="{ 'selected': getAnswer(q.id) === opt.id || (Array.isArray(getAnswer(q.id)) && getAnswer(q.id).includes(opt.id)) }">
                        {{ String.fromCharCode(65 + (q.choices?.indexOf(opt) || 0)) }}
                      </span>
                      <span class="choice-text" v-html="opt.text"></span>
                    </label>
                  </li>
                </ul>
              </template>

              <template v-else-if="q?.type === 'boolean'">
                <div class="boolean-options">
                  <label class="boolean-option" :class="{ 'selected': getAnswer(q.id) === true || getAnswer(q.id) === 'true' || getAnswer(q.id) === 'T' }">
                    <input type="radio" class="sr-only" :name="'q_' + q.id" value="T" :checked="getAnswer(q.id) === true || getAnswer(q.id) === 'true' || getAnswer(q.id) === 'T'" @change="setAnswer(q.id, true)" />
                    Đúng
                  </label>
                  <label class="boolean-option" :class="{ 'selected': getAnswer(q.id) === false || getAnswer(q.id) === 'false' || getAnswer(q.id) === 'F' }">
                    <input type="radio" class="sr-only" :name="'q_' + q.id" value="F" :checked="getAnswer(q.id) === false || getAnswer(q.id) === 'false' || getAnswer(q.id) === 'F'" @change="setAnswer(q.id, false)" />
                    Sai
                  </label>
                </div>
              </template>

              <template v-else-if="q?.type === 'fill'">
                <div class="fill-inputs">
                  <input
                    v-for="(blank, blankIdx) in Array(q.blanks || 1)"
                    :key="blankIdx"
                    class="fill-input"
                    :value="Array.isArray(getAnswer(q.id)) ? getAnswer(q.id)[blankIdx] : (blankIdx === 0 ? getAnswer(q.id) : '')"
                    @input="handleFillChange(q.id, blankIdx, ($event.target as HTMLInputElement).value, q.blanks || 1)"
                    :placeholder="`Nhập câu trả lời ${blankIdx + 1}...`"
                  />
                </div>
              </template>

              <template v-else>
                <input
                  class="text-input"
                  :value="getAnswer(q.id) ?? ''"
                  @input="setAnswer(q.id, ($event.target as HTMLInputElement).value)"
                  placeholder="Nhập câu trả lời của bạn..."
                />
              </template>
            </div>
          </div>

          <div class="navigation-bar">
            <button type="button" class="btn-outline" :disabled="idx === 0" @click="prev">‹ Câu trước</button>
            <div v-if="idx === questions.length - 1 && questions.length > 0" class="progress-text">
              {{ answeredCount }}/{{ questions.length }} câu đã trả lời
            </div>
            <button
              v-if="idx === questions.length - 1 && questions.length > 0"
              type="button"
              class="btn-danger"
              :disabled="submitting"
              @click="submit"
            >
              {{ submitting ? 'Đang nộp…' : 'Nộp bài' }}
            </button>
            <button
              v-else
              type="button"
              class="btn-primary"
              :disabled="idx === questions.length - 1"
              @click="next"
            >
              Câu tiếp ›
            </button>
          </div>
        </section>
      </main>
    </div>

    <!-- Submit Modal -->
    <transition enter-active-class="transition duration-200" leave-active-class="transition duration-150" enter-from-class="opacity-0" leave-to-class="opacity-0">
      <div v-if="showSubmitModal" class="modal-overlay" @click.self="showSubmitModal = false">
        <div class="modal-content">
          <header class="modal-header">
            <h3 class="modal-title">Xác nhận nộp bài</h3>
            <button type="button" class="modal-close" @click="showSubmitModal = false">×</button>
          </header>
          <section class="modal-body" v-html="submitMsg"></section>
          <footer class="modal-footer">
            <button type="button" class="btn-outline" :disabled="submitting" @click="showSubmitModal = false">Tiếp tục làm</button>
            <button type="button" class="btn-danger" :disabled="submitting" @click="confirmSubmit">{{ submitting ? 'Đang nộp…' : 'Nộp bài' }}</button>
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
import { useThemeStore } from '@/store/theme.store'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const exam = ref<ExamDetail | null>(null)
const attemptId = ref<string | null>(null)
const loading = ref(true)
const questions = shallowRef<AttemptQuestion[]>([])
const answers = ref<Record<string, any>>({})
const idx = ref(0)
const submitting = ref(false)
const duration = ref(0)
const timeLeft = ref(0)
let timer: number | null = null
let autosaveTimer: number | null = null

const userKey = computed(() => {
  const u = auth.user
  return String(u?.id ?? u?.email ?? u?.name ?? 'guest')
})
const storageKey = computed(() => `exam_answers_${route.params.id || ''}_${userKey.value}`)
const doneKey = computed(() => `exam_done_${route.params.id || ''}_${userKey.value}`)

const q = computed(() => questions.value[idx.value])
const answeredCount = computed(() => Object.keys(answers.value).filter((qid) => {
  const ans = answers.value[qid]
  if (Array.isArray(ans)) return ans.length > 0
  return (ans ?? '').toString().trim() !== ''
}).length)

function labelLevel(level?: string) {
  if (!level) return 'Cơ bản'
  const levelMap: Record<string, string> = { 'Khối 1': 'Cơ bản', 'Khối 2': 'Cơ bản', 'Khối 3': 'Cơ bản', 'Khối 4': 'Nâng cao', 'Khối 5': 'Nâng cao' }
  return levelMap[level] || 'Cơ bản'
}

function fmtTime(s: number) {
  const m = Math.floor(s / 60)
  const ss = s % 60
  return `${m.toString().padStart(2, '0')}:${ss.toString().padStart(2, '0')}`
}

const showSubmitModal = ref(false)
const submitMsg = computed(() => {
  const unanswered = questions.value.length - answeredCount.value
  return unanswered > 0
    ? `Bạn còn <b>${unanswered}</b> câu chưa trả lời. Bạn có chắc chắn muốn nộp bài không?`
    : 'Bạn đã trả lời hết các câu hỏi. Xác nhận nộp bài?'
})

function submit() { showSubmitModal.value = true }

async function confirmSubmit() {
  if (submitting.value || !attemptId.value) return
  submitting.value = true
  stopTimer()
  await nextTick()
  try {
    const result = await examService.submit(route.params.id as string, attemptId.value, answers.value)
    showSubmitModal.value = false
    showToast('Đã nộp bài thành công!', 'success')
    try { localStorage.setItem(doneKey.value, attemptId.value) } catch (e) {}
    router.push({ name: 'student-exam-result', params: { id: route.params.id }, query: { attemptId: attemptId.value } })
  } catch (err: any) {
    showToast(err?.message || 'Không thể nộp bài. Vui lòng thử lại.', 'error')
  } finally {
    submitting.value = false
  }
}

function goBack() {
  showToast('Mọi tiến trình làm bài sẽ không được lưu lại.', 'warning')
  setTimeout(() => { router.back() }, 1500)
}

function go(i: number) { if (i >= 0 && i < questions.value.length) idx.value = i }
function next() { if (idx.value < questions.value.length - 1) idx.value++ }
function prev() { if (idx.value > 0) idx.value-- }
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
  if (timer) { clearInterval(timer); timer = null }
  if (autosaveTimer) { clearInterval(autosaveTimer); autosaveTimer = null }
}
function getAnswer(qid: string | number) { return answers.value[qid] }
function setAnswer(qid: string | number, val: any) {
  answers.value = { ...answers.value, [qid]: val }
  try { localStorage.setItem(storageKey.value, JSON.stringify(answers.value)) } catch (e) {}
}
function handleChoiceChange(qid: string | number, choiceId: string, isMulti: boolean) {
  if (isMulti) {
    const current = Array.isArray(answers.value[qid]) ? answers.value[qid] : []
    const newAnswer = current.includes(choiceId) ? current.filter((id: string) => id !== choiceId) : [...current, choiceId]
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
  const labels: Record<string, string> = { 'single': 'MCQ', 'multi': 'MCQ', 'boolean': 'TF', 'fill': 'FILL', 'match': 'MATCH', 'order': 'ORDER' }
  return labels[type || ''] || type?.toUpperCase() || 'MCQ'
}

async function loadExamAndStart() {
  try {
    loading.value = true
    const examId = route.params.id as string
    if (route.name === 'student-exam-result' || route.path.includes('/result')) {
      const attemptId = route.query.attemptId as string
      router.replace({ name: 'student-exam-result', params: { id: examId }, query: attemptId ? { attemptId } : {} })
      return
    }
    exam.value = await examService.detail(examId)
    try {
      const attempt = await examService.startAttempt(examId)
      attemptId.value = attempt.id
      questions.value = attempt.questions
      answers.value = { ...attempt.answers }
      try {
        const cached = localStorage.getItem(storageKey.value)
        if (cached) {
          const parsed = JSON.parse(cached)
          if (parsed && typeof parsed === 'object') answers.value = { ...answers.value, ...parsed }
        }
      } catch (e) {}
      const deadline = new Date(attempt.deadlineAt)
      const now = new Date()
      const secondsLeft = Math.max(0, Math.floor((deadline.getTime() - now.getTime()) / 1000))
      duration.value = exam.value.durationSec
      timeLeft.value = secondsLeft
      timer = window.setInterval(() => {
        timeLeft.value--
        if (timeLeft.value <= 0) { stopTimer(); confirmSubmit() }
      }, 1000) as unknown as number
      autosaveTimer = window.setInterval(() => {
        try { localStorage.setItem(storageKey.value, JSON.stringify(answers.value)) } catch (e) {}
      }, 15000) as unknown as number
      loading.value = false
    } catch (attemptErr: any) {
      const errorMsg = attemptErr?.message || attemptErr?.response?.data?.detail || ''
      if (errorMsg.includes('đã hoàn thành') || errorMsg.includes('already completed') || errorMsg.includes('chỉ được làm 1 lần')) {
        const attemptIdMatch = errorMsg.match(/Attempt ID: ([a-f0-9-]+)/i)
        const finishedAttemptId = attemptIdMatch ? attemptIdMatch[1] : null
        if (finishedAttemptId) {
          try { localStorage.setItem(`exam_done_${examId}_${userKey.value}`, finishedAttemptId) } catch (e) {}
          router.replace({ name: 'student-exam-result', params: { id: examId }, query: { attemptId: finishedAttemptId } })
          return
        } else {
          router.replace({ name: 'student-exams' })
          return
        }
      }
      if (errorMsg.toLowerCase().includes('expired') || errorMsg.includes('closed') || errorMsg.includes('deadline')) {
        showToast('Bài kiểm tra đã kết thúc hoặc quá hạn.', 'warning')
        router.replace({ name: 'student-exams' })
        return
      }
      throw attemptErr
    }
  } catch (err: any) {
    showToast(err?.message || 'Không thể tải bài kiểm tra. Vui lòng thử lại.', 'error')
    router.back()
  }
}

onMounted(async () => {
  if (route.name === 'student-exam-result' || route.path.includes('/result')) {
    const examId = route.params.id as string
    const attemptId = route.query.attemptId as string
    router.replace({ name: 'student-exam-result', params: { id: examId }, query: attemptId ? { attemptId } : {} })
    return
  }
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

<style scoped>
.page-wrapper { min-height: 100vh; position: relative; transition: background-color 0.3s ease; }
.page-wrapper.dark-mode { background: #020617 !important; color: white; }
.page-wrapper.light-mode { background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%); }

.bg-elements { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.glow { position: absolute; border-radius: 50%; filter: blur(100px); }
.glow-1 { top: 10%; left: -5%; width: 300px; height: 300px; background: rgba(6, 182, 212, 0.1); }
.glow-2 { bottom: 10%; right: -5%; width: 250px; height: 250px; background: rgba(139, 92, 246, 0.1); }

.page-content { position: relative; z-index: 10; max-width: 1200px; margin: 0 auto; padding: 32px 24px; }

.exam-header { margin-bottom: 24px; padding: 20px; border-radius: 16px; }
.dark-mode .exam-header { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .exam-header { background: white; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }

.header-content { display: flex; flex-direction: column; gap: 16px; }
@media (min-width: 640px) { .header-content { flex-direction: row; align-items: center; justify-content: space-between; } }

.exam-title { font-size: 22px; font-weight: 700; margin: 0; }
.dark-mode .exam-title { color: white; }
.light-mode .exam-title { color: #1e293b; }

.exam-meta { display: flex; flex-wrap: wrap; gap: 8px; font-size: 14px; margin: 8px 0 0; }
.dark-mode .exam-meta { color: #94a3b8; }
.light-mode .exam-meta { color: #64748b; }

.header-actions { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }

.timer-badge { display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 10px; font-size: 14px; font-weight: 600; }
.dark-mode .timer-badge { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; }
.light-mode .timer-badge { background: white; border: 1px solid #e2e8f0; color: #1e293b; }
.timer-badge.timer-warning { }
.dark-mode .timer-badge.timer-warning { background: rgba(239,68,68,0.1); border-color: rgba(239,68,68,0.3); color: #f87171; }
.light-mode .timer-badge.timer-warning { background: #fef2f2; border-color: #fecaca; color: #dc2626; }

.btn-exit { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; border: none; }
.dark-mode .btn-exit { background: rgba(239, 68, 68, 0.1); color: #f87171; }
.light-mode .btn-exit { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
.btn-exit:hover { transform: translateY(-1px); }
.dark-mode .btn-exit:hover { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
.light-mode .btn-exit:hover { background: #fee2e2; }

.btn-outline { display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.dark-mode .btn-outline { background: transparent; border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .btn-outline { background: transparent; border: 1px solid #e2e8f0; color: #64748b; }
.btn-outline:hover { transform: translateY(-1px); }
.dark-mode .btn-outline:hover { border-color: #06b6d4; color: #06b6d4; }
.light-mode .btn-outline:hover { border-color: #6366f1; color: #6366f1; }
.btn-outline:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

.btn-warning { display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; border: none; }
.dark-mode .btn-warning { background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.3); color: #fbbf24; }
.light-mode .btn-warning { background: #fef3c7; border: 1px solid #fde68a; color: #d97706; }
.btn-warning:hover { transform: translateY(-1px); }

.btn-primary { display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 10px; font-size: 14px; font-weight: 600; border: none; cursor: pointer; transition: all 0.3s; }
.dark-mode .btn-primary { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; }
.light-mode .btn-primary { background: #1e293b; color: white; }
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

.btn-danger { display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 10px; font-size: 14px; font-weight: 600; border: none; cursor: pointer; transition: all 0.3s; background: #dc2626; color: white; }
.btn-danger:hover { background: #b91c1c; transform: translateY(-1px); }
.btn-danger:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

.loading-state { display: flex; flex-direction: column; gap: 12px; }
.skeleton { border-radius: 8px; animation: pulse 2s infinite; }
.dark-mode .skeleton { background: rgba(255,255,255,0.05); }
.light-mode .skeleton { background: #e2e8f0; }
.skeleton-title { height: 16px; width: 66%; }
.skeleton-content { height: 128px; }
.skeleton-text { height: 16px; width: 75%; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

.exam-main { display: grid; gap: 24px; }
@media (min-width: 1024px) { .exam-main { grid-template-columns: minmax(260px, 320px) minmax(0, 1fr); } }

.questions-sidebar { padding: 20px; border-radius: 16px; }
.dark-mode .questions-sidebar { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .questions-sidebar { background: white; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }

.sidebar-title { font-size: 16px; font-weight: 600; margin: 0 0 16px; }
.dark-mode .sidebar-title { color: white; }
.light-mode .sidebar-title { color: #1e293b; }

.questions-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; }
@media (min-width: 640px) { .questions-grid { grid-template-columns: repeat(6, 1fr); } }

.question-num-btn { display: flex; height: 40px; align-items: center; justify-content: center; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; border: 1px solid; }
.dark-mode .question-num-btn { background: rgba(255,255,255,0.03); border-color: rgba(255,255,255,0.08); color: white; }
.light-mode .question-num-btn { background: white; border-color: #e2e8f0; color: #1e293b; }

/* Active state - currently selected question */
.dark-mode .question-num-btn.active { background: linear-gradient(135deg, #06b6d4, #8b5cf6); border-color: transparent; color: white; }
.light-mode .question-num-btn.active { background: #1e293b; border-color: #1e293b; color: white; }

/* Answered state - question has been answered */
.dark-mode .question-num-btn.answered { background: rgba(34, 197, 94, 0.15); border-color: rgba(34, 197, 94, 0.4); color: #22c55e; }
.light-mode .question-num-btn.answered { background: #dcfce7; border-color: #86efac; color: #16a34a; }

/* Unanswered state - question not yet answered */
.dark-mode .question-num-btn.unanswered { background: rgba(251,191,36,0.1); border-color: rgba(251,191,36,0.3); color: #fbbf24; }
.light-mode .question-num-btn.unanswered { background: #fef3c7; border-color: #fde68a; color: #d97706; }

.question-area { display: flex; flex-direction: column; gap: 16px; }

.question-card { padding: 20px; border-radius: 16px; }
.dark-mode .question-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .question-card { background: white; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }

.question-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.question-number { font-size: 14px; font-weight: 600; }
.dark-mode .question-number { color: white; }
.light-mode .question-number { color: #1e293b; }
.question-type { padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 600; text-transform: uppercase; }
.dark-mode .question-type { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .question-type { background: #f8fafc; border: 1px solid #e2e8f0; color: #64748b; }

.question-body { display: flex; flex-direction: column; gap: 16px; }
.question-text { font-size: 15px; line-height: 1.6; }
.dark-mode .question-text { color: white; }
.light-mode .question-text { color: #1e293b; }

.choices-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }
.choice-item { border-radius: 12px; transition: all 0.3s; cursor: pointer; }
.dark-mode .choice-item { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .choice-item { background: white; border: 1px solid #e2e8f0; }
.choice-item:hover { }
.dark-mode .choice-item:hover { border-color: rgba(255,255,255,0.15); }
.light-mode .choice-item:hover { border-color: #cbd5e1; background: #f8fafc; }
.choice-item.selected { }
.dark-mode .choice-item.selected { background: rgba(6,182,212,0.1); border-color: #06b6d4; }
.light-mode .choice-item.selected { background: #f8fafc; border-color: #1e293b; box-shadow: 0 0 0 2px rgba(30,41,59,0.1); }

.choice-label { display: flex; align-items: center; gap: 12px; padding: 12px 16px; cursor: pointer; }
.choice-input { width: 16px; height: 16px; }
.dark-mode .choice-input { accent-color: #06b6d4; }
.light-mode .choice-input { accent-color: #1e293b; }

.choice-letter { display: inline-flex; width: 28px; height: 28px; align-items: center; justify-content: center; border-radius: 50%; font-size: 13px; font-weight: 700; }
.dark-mode .choice-letter { background: rgba(255,255,255,0.05); color: #94a3b8; }
.light-mode .choice-letter { background: #f1f5f9; color: #64748b; }
.choice-letter.selected { }
.dark-mode .choice-letter.selected { background: #06b6d4; color: white; }
.light-mode .choice-letter.selected { background: #1e293b; color: white; }

.choice-text { flex: 1; font-size: 14px; font-weight: 600; }
.dark-mode .choice-text { color: #94a3b8; }
.light-mode .choice-text { color: #64748b; }
.choice-item.selected .choice-text { }
.dark-mode .choice-item.selected .choice-text { color: white; }
.light-mode .choice-item.selected .choice-text { color: #1e293b; }

.boolean-options { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.boolean-option { display: flex; align-items: center; justify-content: center; padding: 12px 16px; border-radius: 12px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.dark-mode .boolean-option { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08); color: #94a3b8; }
.light-mode .boolean-option { background: white; border: 1px solid #e2e8f0; color: #64748b; }
.boolean-option:hover { }
.dark-mode .boolean-option:hover { border-color: rgba(255,255,255,0.15); }
.light-mode .boolean-option:hover { border-color: #cbd5e1; background: #f8fafc; }
.boolean-option.selected { }
.dark-mode .boolean-option.selected { background: rgba(6,182,212,0.1); border-color: #06b6d4; color: white; }
.light-mode .boolean-option.selected { background: #f8fafc; border-color: #1e293b; color: #1e293b; box-shadow: 0 0 0 2px rgba(30,41,59,0.1); }

.fill-inputs { display: flex; flex-direction: column; gap: 8px; }
.fill-input, .text-input { width: 100%; padding: 12px 16px; border-radius: 12px; font-size: 14px; outline: none; transition: all 0.3s; }
.dark-mode .fill-input, .dark-mode .text-input { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; }
.light-mode .fill-input, .light-mode .text-input { background: #f8fafc; border: 1px solid #e2e8f0; color: #1e293b; }
.fill-input:focus, .text-input:focus { }
.dark-mode .fill-input:focus, .dark-mode .text-input:focus { border-color: #06b6d4; }
.light-mode .fill-input:focus, .light-mode .text-input:focus { border-color: #6366f1; }

.navigation-bar { display: flex; flex-direction: column; gap: 12px; padding: 16px; border-radius: 16px; }
@media (min-width: 640px) { .navigation-bar { flex-direction: row; align-items: center; justify-content: space-between; } }
.dark-mode .navigation-bar { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .navigation-bar { background: white; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }

.progress-text { text-align: center; font-size: 14px; font-weight: 600; }
.dark-mode .progress-text { color: #94a3b8; }
.light-mode .progress-text { color: #64748b; }

.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); white-space: nowrap; border-width: 0; }

.modal-overlay { position: fixed; inset: 0; z-index: 50; display: flex; align-items: center; justify-content: center; padding: 16px; }
.dark-mode .modal-overlay { background: rgba(0,0,0,0.7); }
.light-mode .modal-overlay { background: rgba(15,23,42,0.4); }

.modal-content { width: 100%; max-width: 400px; border-radius: 16px; }
.dark-mode .modal-content { background: #0f172a; border: 1px solid rgba(255,255,255,0.1); }
.light-mode .modal-content { background: white; border: 1px solid #e2e8f0; box-shadow: 0 20px 40px rgba(0,0,0,0.15); }

.modal-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; border-bottom: 1px solid; }
.dark-mode .modal-header { border-color: rgba(255,255,255,0.08); }
.light-mode .modal-header { border-color: #e2e8f0; }

.modal-title { font-size: 18px; font-weight: 700; margin: 0; }
.dark-mode .modal-title { color: white; }
.light-mode .modal-title { color: #1e293b; }

.modal-close { width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; border-radius: 8px; font-size: 20px; border: none; cursor: pointer; transition: all 0.3s; }
.dark-mode .modal-close { background: transparent; color: #94a3b8; }
.light-mode .modal-close { background: transparent; color: #64748b; }
.modal-close:hover { }
.dark-mode .modal-close:hover { background: rgba(255,255,255,0.05); }
.light-mode .modal-close:hover { background: #f1f5f9; }

.modal-body { padding: 20px; font-size: 14px; }
.dark-mode .modal-body { color: white; }
.light-mode .modal-body { color: #1e293b; }

.modal-footer { display: flex; flex-direction: column; gap: 12px; padding: 16px 20px; }
@media (min-width: 640px) { .modal-footer { flex-direction: row; justify-content: flex-end; } }

@media (max-width: 640px) {
  .page-content { padding: 20px 16px; }
  .exam-title { font-size: 18px; }
}
</style>
