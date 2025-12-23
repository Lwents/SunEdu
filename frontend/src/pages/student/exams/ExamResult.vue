<template>
  <div class="page-wrapper" :class="isDark ? 'dark-mode' : 'light-mode'">
    <!-- Background Elements -->
    <div v-if="isDark" class="bg-elements">
      <div class="glow glow-1"></div>
      <div class="glow glow-2"></div>
    </div>

    <div class="page-content">
      <div class="result-card" :class="toneClass">
        <h1>Hoàn thành!</h1>
        <p class="lead">Đây là kết quả bài làm của bạn:</p>

        <div v-if="loading" class="loading-state">
          <p>Đang tải kết quả...</p>
        </div>
        <div v-else class="score-display">
          <span class="score-value">{{ formatScore(score) }}</span>
          <span class="score-total">/ {{ formatScore(total) }}</span>
        </div>

        <p class="percentage" :style="{ color: resultStatus.color }">
          Đạt {{ percentage.toFixed(0) }}%
        </p>

        <p class="message">{{ resultStatus.message }}</p>

        <div class="actions">
          <button v-if="canShowAnswers" class="btn ghost" @click="toggleReview">
            {{ showReview ? 'Ẩn đáp án' : 'Xem lại đáp án' }}
          </button>
          <span v-else-if="showAnswersSetting === 'after_duration'" class="hint-text">
            Đáp án sẽ được hiển thị sau khi hết thời gian làm bài
          </span>
          <span v-else-if="showAnswersSetting === 'after_end'" class="hint-text">
            Đáp án sẽ được hiển thị sau khi hết hạn bài thi
          </span>
          <span v-else-if="showAnswersSetting === 'never'" class="hint-text">
            Giáo viên không cho phép xem đáp án
          </span>
          <router-link class="btn primary" :to="{ name: 'student-exams-ranking', query: { examId: route.params.id } }">
            Xem bảng xếp hạng
          </router-link>
        </div>
      </div>

      <Transition name="fade">
        <div v-if="showReview && canShowAnswers" class="review-section">
          <div class="review-header">
            <h2>Chi tiết bài làm</h2>
            <p>Hiển thị {{ paginatedAnswers.length }} câu hỏi trên trang {{ currentPage }}</p>
          </div>

          <div
            v-for="(answer, index) in paginatedAnswers"
            :key="answer.originalIndex"
            class="question-review"
            :class="{ correct: isAnswerCorrect(answer), incorrect: !isAnswerCorrect(answer) }"
          >
            <div class="question-header">
              <strong>Câu {{ answer.originalIndex + 1 }}:</strong>
              <div class="q-text" v-html="answer.questionText"></div>
            </div>
            <div class="answer-details">
              <p>
                Đáp án của bạn:
                <span class="user-answer" :class="{ 'text-red': !answer.correct, 'text-green': answer.correct }">
                  {{ answer.userAnswer || 'Chưa trả lời' }}
                </span>
              </p>
              <p>
                Đáp án đúng: <span class="correct-answer">{{ answer.correctAnswer }}</span>
              </p>
              <p v-if="answer.maxScore > 0" class="score-info">
                Điểm: <strong>{{ answer.score.toFixed(1) }}</strong> / {{ answer.maxScore }}
              </p>
            </div>
            <div v-if="answer.userAnswer !== answer.correctAnswer && answer.explanation" class="explanation">
              <strong>Giải thích:</strong> {{ answer.explanation }}
            </div>
          </div>

          <div v-if="totalPages > 1" class="pagination-controls">
            <button class="btn-page" :disabled="currentPage === 1" @click="prevPage">‹ Trang trước</button>
            <span class="page-info">Trang {{ currentPage }} / {{ totalPages }}</span>
            <button class="btn-page" :disabled="currentPage === totalPages" @click="nextPage">Trang sau ›</button>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { examService } from '@/services/exam.service'
import { showToast } from '@/utils/toast'
import { useAuthStore } from '@/store/auth.store'
import { useThemeStore } from '@/store/theme.store'

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const showReview = ref(false)
const userAnswers = ref<any[]>([])
const loading = ref(true)
const route = useRoute()
const auth = useAuthStore()
const canShowAnswers = ref(true)
const showAnswersSetting = ref('always')
const userKey = computed(() => {
  const u = auth.user
  return String(u?.id ?? u?.email ?? u?.name ?? 'guest')
})

const currentPage = ref(1)
const itemsPerPage = 10

const attemptData = ref<any>(null)
const totalScore = ref(0)
const maxScore = ref(0)

const mockUserAnswers = [
  { questionText: 'Có lỗi xảy ra, không nhận được dữ liệu bài làm.', userAnswer: '', correctAnswer: '', explanation: 'Vui lòng quay lại và thử nộp bài lần nữa.' },
]

function formatAnswerForDisplay(answer: any, question: any): string {
  if (answer === null || answer === undefined) return 'Chưa trả lời'
  const qtype = question.type || 'single'
  if (qtype === 'single' || qtype === 'mcq') {
    let selectedId: string | null = null
    if (typeof answer === 'string') selectedId = answer
    else if (typeof answer === 'object' && answer !== null) {
      selectedId = answer.selected_choice_id || answer.choice_id || answer.id || null
      if (!selectedId && Array.isArray(answer)) selectedId = answer[0] || null
    }
    if (!selectedId) return 'Chưa trả lời'
    const choice = question.choices?.find((c: any) => {
      const cid = String(c.id || c.choice_id || '')
      const sid = String(selectedId || '')
      return cid === sid || cid.toLowerCase() === sid.toLowerCase()
    })
    return choice?.text || choice?.label || String(selectedId)
  }
  if (qtype === 'multi') {
    let selectedIds: string[] = []
    if (Array.isArray(answer)) selectedIds = answer.map(id => String(id))
    else if (typeof answer === 'object' && answer !== null) selectedIds = (answer.selected_choice_ids || answer.choice_ids || []).map((id: any) => String(id))
    else if (typeof answer === 'string') selectedIds = [answer]
    if (!selectedIds.length) return 'Chưa trả lời'
    const choices = question.choices?.filter((c: any) => {
      const cid = String(c.id || c.choice_id || '')
      return selectedIds.some(sid => cid === sid || cid.includes(sid) || sid.includes(cid))
    }) || []
    return choices.length > 0 ? choices.map((c: any) => c.text || c.label).join(', ') : selectedIds.join(', ')
  }
  if (qtype === 'boolean') {
    const val = typeof answer === 'object' && answer.value !== undefined ? answer.value : answer
    if (val === true || val === 'true' || val === 'True') return 'Đúng'
    if (val === false || val === 'false' || val === 'False') return 'Sai'
    return String(val)
  }
  if (qtype === 'fill' || qtype === 'short_answer') {
    const val = typeof answer === 'object' && answer.value !== undefined ? answer.value : (Array.isArray(answer) ? answer.join(', ') : answer)
    return String(val || 'Chưa trả lời')
  }
  if (qtype === 'match') {
    if (typeof answer === 'object' && answer.pairs) return answer.pairs.map((p: any) => `${p.left} → ${p.right}`).join(', ')
    return String(answer || 'Chưa trả lời')
  }
  if (qtype === 'order') {
    if (Array.isArray(answer)) return answer.map((item: any, idx: number) => `${idx + 1}. ${item}`).join(', ')
    return String(answer || 'Chưa trả lời')
  }
  return String(answer || 'Chưa trả lời')
}

function getCorrectAnswer(question: any): string {
  if (question.correct_answer) return question.correct_answer
  const qtype = question.type || 'single'
  if (qtype === 'single' || qtype === 'mcq') {
    const correctChoice = question.choices?.find((c: any) => c.is_correct === true)
    return correctChoice?.text || 'N/A'
  }
  if (qtype === 'multi') {
    const correctChoices = question.choices?.filter((c: any) => c.is_correct === true) || []
    return correctChoices.map((c: any) => c.text).join(', ') || 'N/A'
  }
  if (qtype === 'boolean') {
    const correct = question.meta?.correct_answer
    if (correct === true || correct === 'true') return 'Đúng'
    if (correct === false || correct === 'false') return 'Sai'
    return String(correct || 'N/A')
  }
  if (qtype === 'fill' || qtype === 'short_answer') return question.meta?.correct_answer || question.meta?.answer || 'N/A'
  if (qtype === 'match') {
    const pairs = question.pairs || question.meta?.pairs || []
    return pairs.map((p: any) => `${p.left} → ${p.right}`).join(', ') || 'N/A'
  }
  if (qtype === 'order') {
    const items = question.items || question.meta?.items || []
    return items.map((item: any, idx: number) => `${idx + 1}. ${item}`).join(', ') || 'N/A'
  }
  return 'N/A'
}

async function loadAttemptData() {
  let attemptId = route.query.attemptId as string
  if (!attemptId) {
    const examId = route.params.id as string
    if (examId && userKey.value) {
      try {
        const savedAttemptId = localStorage.getItem(`exam_done_${examId}_${userKey.value}`)
        if (savedAttemptId) attemptId = savedAttemptId
      } catch (e) {}
    }
  }
  if (!attemptId) {
    showToast('Không tìm thấy thông tin bài làm. Vui lòng làm bài lại.', 'error')
    userAnswers.value = mockUserAnswers
    loading.value = false
    return
  }
  try {
    loading.value = true
    const data = await examService.getAttemptSummary(attemptId)
    attemptData.value = data
    totalScore.value = data.totalScore || 0
    maxScore.value = data.maxScore || data.totalCount || 0
    canShowAnswers.value = data.can_show_answers !== false
    showAnswersSetting.value = data.show_answers || 'always'
    const questions = data.questions || []
    userAnswers.value = questions.map((q: any, index: number) => {
      const userAnswer = q.answer || null
      const correctAnswer = getCorrectAnswer(q)
      return {
        originalIndex: index,
        questionText: q.prompt || q.text || `Câu hỏi ${index + 1}`,
        userAnswer: formatAnswerForDisplay(userAnswer, q),
        correctAnswer: canShowAnswers.value ? correctAnswer : '***',
        correct: q.correct || false,
        score: q.answer_score || q.score || 0,
        maxScore: q.points || q.maxScore || 0,
        explanation: q.explanation || null,
        question: q,
      }
    })
    if (userAnswers.value.length === 0) userAnswers.value = mockUserAnswers
  } catch (error: any) {
    const errorMsg = error.response?.data?.detail || error.message || 'Lỗi không xác định'
    if (error.response?.status === 404) showToast('Không tìm thấy bài làm.', 'error')
    else if (error.response?.status === 403) showToast('Bạn không có quyền xem bài làm này.', 'error')
    else showToast('Không thể tải dữ liệu bài làm: ' + errorMsg, 'error')
    userAnswers.value = mockUserAnswers
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  const attemptId = route.query.attemptId as string | undefined
  const examId = route.params.id as string | undefined
  if (examId && attemptId) {
    try { localStorage.setItem(`exam_done_${examId}_${userKey.value}`, attemptId) } catch (e) {}
  }
  loadAttemptData()
})

function isAnswerCorrect(answer: any) { return answer.correct === true }

const total = computed(() => {
  if (attemptData.value && maxScore.value > 0) return maxScore.value
  return userAnswers.value.length
})

const score = computed(() => {
  if (attemptData.value && totalScore.value > 0) return totalScore.value
  return userAnswers.value.filter((a) => isAnswerCorrect(a)).length
})

const percentage = computed(() => {
  if (total.value === 0 || userAnswers.value === mockUserAnswers) return 0
  if (attemptData.value && maxScore.value > 0 && totalScore.value >= 0) {
    const pct = (totalScore.value / maxScore.value) * 100
    return Math.min(100, Math.max(0, Math.round(pct)))
  }
  const correctCount = userAnswers.value.filter((a) => isAnswerCorrect(a)).length
  const pct = (correctCount / userAnswers.value.length) * 100
  return Math.min(100, Math.max(0, Math.round(pct)))
})

function formatScore(val: number): string {
  if (typeof val !== 'number') return String(val)
  if (Number.isInteger(val)) return String(val)
  return val.toFixed(1)
}

const resultStatus = computed(() => {
  if (userAnswers.value === mockUserAnswers) return { tone: 'danger', message: 'Không thể tính toán kết quả.', color: '#ef4444' }
  if (percentage.value >= 80) return { tone: 'success', message: 'Xuất sắc! Bạn đã làm rất tốt! 🎉', color: '#16a34a' }
  else if (percentage.value >= 50) return { tone: 'warning', message: 'Khá tốt! Cùng cố gắng hơn ở lần sau nhé. 👍', color: '#f59e0b' }
  return { tone: 'danger', message: 'Đừng nản lòng, hãy xem lại và thử lại nhé! 💪', color: '#ef4444' }
})

const toneClass = computed(() => {
  switch (resultStatus.value.tone) {
    case 'success': return 'tone-success'
    case 'warning': return 'tone-warning'
    case 'danger': return 'tone-danger'
    default: return ''
  }
})

const totalPages = computed(() => Math.ceil(userAnswers.value.length / itemsPerPage))
const paginatedAnswers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return userAnswers.value.slice(start, end).map((answer, index) => ({ ...answer, originalIndex: start + index }))
})

function nextPage() { if (currentPage.value < totalPages.value) { currentPage.value++; scrollToReviewTop() } }
function prevPage() { if (currentPage.value > 1) { currentPage.value--; scrollToReviewTop() } }
function toggleReview() { showReview.value = !showReview.value; if (showReview.value) currentPage.value = 1 }
function scrollToReviewTop() { const el = document.querySelector('.review-section'); if (el) el.scrollIntoView({ behavior: 'smooth' }) }
</script>

<style scoped>
.page-wrapper { min-height: 100vh; position: relative; transition: background-color 0.3s ease; }
.page-wrapper.dark-mode { background: #020617; }
.page-wrapper.light-mode { background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%); }

.bg-elements { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.glow { position: absolute; border-radius: 50%; filter: blur(100px); }
.glow-1 { top: 10%; left: -5%; width: 300px; height: 300px; background: rgba(6, 182, 212, 0.1); }
.glow-2 { bottom: 10%; right: -5%; width: 250px; height: 250px; background: rgba(139, 92, 246, 0.1); }

.page-content { position: relative; z-index: 10; max-width: 960px; margin: 0 auto; padding: 32px 16px; display: flex; flex-direction: column; gap: 28px; align-items: center; }

.result-card { width: 100%; border-radius: 32px; padding: 40px 32px; text-align: center; }
.dark-mode .result-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .result-card { background: white; border: 1px solid #e2e8f0; box-shadow: 0 35px 80px rgba(79, 70, 229, 0.12); }

.result-card.tone-success { }
.dark-mode .result-card.tone-success { border-color: rgba(6,182,212,0.3); background: rgba(6,182,212,0.05); }
.light-mode .result-card.tone-success { border-color: #a7f3d0; background: rgba(240, 253, 244, 0.8); }
.result-card.tone-warning { }
.dark-mode .result-card.tone-warning { border-color: rgba(251,191,36,0.3); background: rgba(251,191,36,0.05); }
.light-mode .result-card.tone-warning { border-color: #fde68a; background: rgba(254, 243, 199, 0.8); }
.result-card.tone-danger { }
.dark-mode .result-card.tone-danger { border-color: rgba(239,68,68,0.3); background: rgba(239,68,68,0.05); }
.light-mode .result-card.tone-danger { border-color: #fecaca; background: rgba(254, 242, 242, 0.8); }

.result-card h1 { font-size: clamp(1.5rem, 4vw, 2.3rem); font-weight: 800; margin-bottom: 8px; }
.dark-mode .result-card h1 { color: white; }
.light-mode .result-card h1 { color: #0f172a; }

.result-card .lead { font-size: 16px; margin-bottom: 24px; }
.dark-mode .result-card .lead { color: #94a3b8; }
.light-mode .result-card .lead { color: #475569; }

.loading-state { padding: 32px; text-align: center; }
.dark-mode .loading-state p { color: #64748b; }
.light-mode .loading-state p { color: #64748b; }

.score-display { display: flex; justify-content: center; align-items: baseline; gap: 8px; }
.score-value { font-size: clamp(3rem, 10vw, 4.5rem); font-weight: 900; }
.dark-mode .score-value { color: white; }
.light-mode .score-value { color: #111827; }
.score-total { font-size: 20px; font-weight: 600; }
.dark-mode .score-total { color: #64748b; }
.light-mode .score-total { color: #94a3b8; }

.percentage { margin-top: 4px; font-size: 24px; font-weight: 700; }
.message { margin-top: 8px; font-size: 16px; }
.dark-mode .message { color: #94a3b8; }
.light-mode .message { color: #475569; }

.actions { margin-top: 28px; display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; }
.hint-text { font-size: 14px; }
.dark-mode .hint-text { color: #64748b; }
.light-mode .hint-text { color: #64748b; }

.btn { min-width: 180px; border-radius: 999px; padding: 14px 28px; font-weight: 700; font-size: 15px; border: 1px solid transparent; cursor: pointer; transition: transform 0.15s ease, box-shadow 0.15s ease; text-decoration: none; display: inline-flex; align-items: center; justify-content: center; }
.btn:hover { transform: translateY(-1px); box-shadow: 0 12px 25px rgba(15, 23, 42, 0.08); }
.btn.primary { background: linear-gradient(135deg, #f97316, #facc15); color: #111827; border: none; }
.btn.ghost { }
.dark-mode .btn.ghost { border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; background: transparent; }
.light-mode .btn.ghost { border: 1px solid #cbd5e1; color: #475569; background: white; }

.review-section { width: 100%; border-radius: 30px; padding: 32px; }
.dark-mode .review-section { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .review-section { background: white; border: 1px solid #e2e8f0; box-shadow: 0 25px 70px rgba(15, 23, 42, 0.08); }

.review-header { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 16px; align-items: center; border-bottom: 1px solid; padding-bottom: 16px; margin-bottom: 24px; }
.dark-mode .review-header { border-color: rgba(255,255,255,0.08); }
.light-mode .review-header { border-color: #e2e8f0; }
.review-header h2 { font-size: 22px; font-weight: 800; }
.dark-mode .review-header h2 { color: white; }
.light-mode .review-header h2 { color: #0f172a; }
.review-header p { font-size: 15px; }
.dark-mode .review-header p { color: #64748b; }
.light-mode .review-header p { color: #64748b; }

.question-review { border-radius: 24px; padding: 24px; margin-bottom: 20px; transition: border-color 0.2s ease, background 0.2s ease; }
.dark-mode .question-review { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .question-review { background: #f8fafc; border: 1px solid #e2e8f0; }
.question-review.correct { }
.dark-mode .question-review.correct { border-color: rgba(74, 222, 128, 0.3); background: rgba(74, 222, 128, 0.05); }
.light-mode .question-review.correct { border-color: rgba(74, 222, 128, 0.5); background: rgba(240, 253, 244, 0.8); }
.question-review.incorrect { }
.dark-mode .question-review.incorrect { border-color: rgba(248, 113, 113, 0.3); background: rgba(248, 113, 113, 0.05); }
.light-mode .question-review.incorrect { border-color: rgba(248, 113, 113, 0.5); background: rgba(254, 242, 242, 0.9); }

.question-header { font-weight: 700; margin-bottom: 12px; display: flex; flex-direction: column; gap: 4px; }
.dark-mode .question-header { color: white; }
.light-mode .question-header { color: #0f172a; }
.q-text :deep(p) { margin: 0; }

.answer-details p { margin: 4px 0; font-size: 15px; }
.dark-mode .answer-details p { color: #94a3b8; }
.light-mode .answer-details p { color: #475569; }
.user-answer { font-weight: 700; }
.dark-mode .user-answer { color: #cbd5e1; }
.light-mode .user-answer { color: #334155; }
.text-red { color: #ef4444 !important; }
.text-green { color: #22c55e !important; }
.correct-answer { font-weight: 800; color: #16a34a; }

.explanation { margin-top: 12px; padding: 14px 16px; border-radius: 18px; font-size: 14px; }
.dark-mode .explanation { background: rgba(59, 130, 246, 0.1); color: #60a5fa; }
.light-mode .explanation { background: rgba(59, 130, 246, 0.08); color: #1d4ed8; }

.score-info { margin-top: 8px; font-size: 14px; }
.dark-mode .score-info { color: #64748b; }
.light-mode .score-info { color: #64748b; }
.score-info strong { }
.dark-mode .score-info strong { color: white; }
.light-mode .score-info strong { color: #0f172a; }

.pagination-controls { display: flex; justify-content: center; align-items: center; gap: 16px; margin-top: 24px; }
.btn-page { min-width: 150px; border-radius: 999px; padding: 10px 22px; font-weight: 600; cursor: pointer; transition: background 0.15s ease, color 0.15s ease; }
.dark-mode .btn-page { border: 1px solid rgba(255,255,255,0.1); background: transparent; color: #94a3b8; }
.light-mode .btn-page { border: 1px solid #cbd5e1; background: white; color: #475569; }
.btn-page:disabled { cursor: not-allowed; opacity: 0.5; }
.btn-page:not(:disabled):hover { }
.dark-mode .btn-page:not(:disabled):hover { background: rgba(255,255,255,0.05); color: white; }
.light-mode .btn-page:not(:disabled):hover { background: #eef2ff; color: #312e81; }
.page-info { font-weight: 600; }
.dark-mode .page-info { color: white; }
.light-mode .page-info { color: #0f172a; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 768px) {
  .result-card, .review-section { border-radius: 24px; padding: 24px; }
  .actions { flex-direction: column; width: 100%; }
  .btn { width: 100%; }
  .review-header { flex-direction: column; align-items: flex-start; }
}
</style>
