<template>
  <div class="result-page">
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
        <button 
          v-if="canShowAnswers" 
          class="btn ghost" 
          @click="toggleReview"
        >
          {{ showReview ? 'Ẩn đáp án' : 'Xem lại đáp án' }}
        </button>
        <span 
          v-else-if="showAnswersSetting === 'after_duration'" 
          class="text-sm text-slate-500"
        >
          Đáp án sẽ được hiển thị sau khi hết thời gian làm bài
        </span>
        <span 
          v-else-if="showAnswersSetting === 'after_end'" 
          class="text-sm text-slate-500"
        >
          Đáp án sẽ được hiển thị sau khi hết hạn bài thi
        </span>
        <span 
          v-else-if="showAnswersSetting === 'never'" 
          class="text-sm text-slate-500"
        >
          Giáo viên không cho phép xem đáp án
        </span>
        <router-link
          class="btn primary"
          :to="{ name: 'student-exams-ranking', query: { examId: route.params.id } }"
          style="color: black; border: 1px"
        >
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
              <span class="user-answer" :class="{ 'text-red-600': !answer.correct, 'text-green-600': answer.correct }">
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
          <div
            v-if="answer.userAnswer !== answer.correctAnswer && answer.explanation"
            class="explanation"
          >
            <strong>Giải thích:</strong> {{ answer.explanation }}
          </div>
        </div>

        <div v-if="totalPages > 1" class="pagination-controls">
          <button class="btn-page" :disabled="currentPage === 1" @click="prevPage">
            ‹ Trang trước
          </button>
          <span class="page-info">Trang {{ currentPage }} / {{ totalPages }}</span>
          <button class="btn-page" :disabled="currentPage === totalPages" @click="nextPage">
            Trang sau ›
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { examService } from '@/services/exam.service'
import { showToast } from '@/utils/toast'
import { useAuthStore } from '@/store/auth.store'

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

// --- Cấu hình Phân trang ---
const currentPage = ref(1)
const itemsPerPage = 10 // Hiển thị 10 câu mỗi trang

// Dữ liệu từ API
const attemptData = ref<any>(null)
const totalScore = ref(0)
const maxScore = ref(0)

// Dữ liệu mẫu nếu không nhận được gì từ API
const mockUserAnswers = [
  {
    questionText: 'Có lỗi xảy ra, không nhận được dữ liệu bài làm.',
    userAnswer: '',
    correctAnswer: '',
    explanation: 'Vui lòng quay lại và thử nộp bài lần nữa.',
  },
]

// Format answer để hiển thị
function formatAnswerForDisplay(answer: any, question: any): string {
  // Kiểm tra null/undefined nhưng cho phép 0 và false
  if (answer === null || answer === undefined) return 'Chưa trả lời'
  
  const qtype = question.type || 'single'
  
  // Single/Multi choice
  if (qtype === 'single' || qtype === 'mcq') {
    // Answer có thể là: string (UUID), object với selected_choice_id, hoặc dict
    let selectedId: string | null = null
    
    if (typeof answer === 'string') {
      // Nếu là string trực tiếp (UUID)
      selectedId = answer
    } else if (typeof answer === 'object' && answer !== null) {
      // Nếu là object - kiểm tra nhiều format khác nhau
      selectedId = answer.selected_choice_id || answer.choice_id || answer.id || null
      
      // Nếu vẫn null, có thể là array với 1 phần tử
      if (!selectedId && Array.isArray(answer)) {
        selectedId = answer[0] || null
      }
    }
    
    if (!selectedId) return 'Chưa trả lời'
    
    // Tìm choice trong danh sách
    const choice = question.choices?.find((c: any) => {
      const cid = String(c.id || c.choice_id || '')
      const sid = String(selectedId || '')
      // So sánh chính xác UUID
      return cid === sid || cid.toLowerCase() === sid.toLowerCase()
    })
    
    return choice?.text || choice?.label || String(selectedId)
  }
  
  if (qtype === 'multi') {
    let selectedIds: string[] = []
    
    if (Array.isArray(answer)) {
      selectedIds = answer.map(id => String(id))
    } else if (typeof answer === 'object' && answer !== null) {
      selectedIds = (answer.selected_choice_ids || answer.choice_ids || []).map((id: any) => String(id))
    } else if (typeof answer === 'string') {
      selectedIds = [answer]
    }
    
    if (!selectedIds.length) return 'Chưa trả lời'
    
    const choices = question.choices?.filter((c: any) => {
      const cid = String(c.id || c.choice_id || '')
      return selectedIds.some(sid => cid === sid || cid.includes(sid) || sid.includes(cid))
    }) || []
    
    return choices.length > 0 
      ? choices.map((c: any) => c.text || c.label).join(', ')
      : selectedIds.join(', ')
  }
  
  // Boolean (True/False)
  if (qtype === 'boolean') {
    const val = typeof answer === 'object' && answer.value !== undefined 
      ? answer.value 
      : answer
    if (val === true || val === 'true' || val === 'True') return 'Đúng'
    if (val === false || val === 'false' || val === 'False') return 'Sai'
    return String(val)
  }
  
  // Fill/Short answer
  if (qtype === 'fill' || qtype === 'short_answer') {
    const val = typeof answer === 'object' && answer.value !== undefined
      ? answer.value
      : (Array.isArray(answer) ? answer.join(', ') : answer)
    return String(val || 'Chưa trả lời')
  }
  
  // Matching
  if (qtype === 'match') {
    if (typeof answer === 'object' && answer.pairs) {
      return answer.pairs.map((p: any) => `${p.left} → ${p.right}`).join(', ')
    }
    return String(answer || 'Chưa trả lời')
  }
  
  // Ordering
  if (qtype === 'order') {
    if (Array.isArray(answer)) {
      return answer.map((item: any, idx: number) => `${idx + 1}. ${item}`).join(', ')
    }
    return String(answer || 'Chưa trả lời')
  }
  
  return String(answer || 'Chưa trả lời')
}

// Lấy đáp án đúng từ question (backend đã trả về correct_answer)
function getCorrectAnswer(question: any): string {
  // Backend trả về correct_answer trực tiếp nếu attempt đã finished
  if (question.correct_answer) {
    return question.correct_answer
  }
  
  // Fallback nếu backend chưa trả về (cho tương thích ngược)
  const qtype = question.type || 'single'
  
  // Single/Multi choice - tìm choice có is_correct = true
  if (qtype === 'single' || qtype === 'mcq') {
    const correctChoice = question.choices?.find((c: any) => c.is_correct === true)
    return correctChoice?.text || 'N/A'
  }
  
  if (qtype === 'multi') {
    const correctChoices = question.choices?.filter((c: any) => c.is_correct === true) || []
    return correctChoices.map((c: any) => c.text).join(', ') || 'N/A'
  }
  
  // Boolean - lấy từ meta
  if (qtype === 'boolean') {
    const correct = question.meta?.correct_answer
    if (correct === true || correct === 'true') return 'Đúng'
    if (correct === false || correct === 'false') return 'Sai'
    return String(correct || 'N/A')
  }
  
  // Fill/Short answer - lấy từ meta
  if (qtype === 'fill' || qtype === 'short_answer') {
    return question.meta?.correct_answer || question.meta?.answer || 'N/A'
  }
  
  // Matching - lấy từ pairs
  if (qtype === 'match') {
    const pairs = question.pairs || question.meta?.pairs || []
    return pairs.map((p: any) => `${p.left} → ${p.right}`).join(', ') || 'N/A'
  }
  
  // Ordering - lấy từ items
  if (qtype === 'order') {
    const items = question.items || question.meta?.items || []
    return items.map((item: any, idx: number) => `${idx + 1}. ${item}`).join(', ') || 'N/A'
  }
  
  return 'N/A'
}

// Load attempt data from API
async function loadAttemptData() {
  let attemptId = route.query.attemptId as string
  
  // Fallback: Lấy attemptId từ localStorage nếu không có trong query
  if (!attemptId) {
    const examId = route.params.id as string
    if (examId && userKey.value) {
      try {
        const savedAttemptId = localStorage.getItem(`exam_done_${examId}_${userKey.value}`)
        if (savedAttemptId) {
          attemptId = savedAttemptId
          console.log('Lấy attemptId từ localStorage:', attemptId)
        }
      } catch (e) {
        console.warn('Không thể đọc localStorage:', e)
      }
    }
  }
  
  if (!attemptId) {
    console.warn('Không tìm thấy attemptId trong query string hoặc localStorage')
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
    
    // Get show_answers settings
    canShowAnswers.value = data.can_show_answers !== false
    showAnswersSetting.value = data.show_answers || 'always'
    
    // Map questions to display format
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
        question: q, // Keep full question data for reference
      }
    })
    
    if (userAnswers.value.length === 0) {
      userAnswers.value = mockUserAnswers
    }
  } catch (error: any) {
    console.error('Lỗi khi tải dữ liệu bài làm:', error)
    const errorMsg = error.response?.data?.detail || error.message || 'Lỗi không xác định'
    
    // Nếu là lỗi 404, có thể attempt không tồn tại hoặc không có quyền truy cập
    if (error.response?.status === 404) {
      showToast('Không tìm thấy bài làm. Có thể bạn chưa nộp bài hoặc bài làm đã bị xóa.', 'error')
    } else if (error.response?.status === 403) {
      showToast('Bạn không có quyền xem bài làm này.', 'error')
    } else {
      showToast('Không thể tải dữ liệu bài làm: ' + errorMsg, 'error')
    }
    
    userAnswers.value = mockUserAnswers
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  const attemptId = route.query.attemptId as string | undefined
  const examId = route.params.id as string | undefined
  if (examId && attemptId) {
    try {
      localStorage.setItem(`exam_done_${examId}_${userKey.value}`, attemptId)
    } catch (e) {
      console.warn('Cannot persist done flag', e)
    }
  }
  loadAttemptData()
})

function isAnswerCorrect(answer: any) {
  return answer.correct === true
}

const total = computed(() => {
  if (attemptData.value && maxScore.value > 0) {
    return maxScore.value
  }
  return userAnswers.value.length
})

const score = computed(() => {
  if (attemptData.value && totalScore.value > 0) {
    return totalScore.value
  }
  // Fallback: tính từ số câu đúng
  return userAnswers.value.filter((a) => isAnswerCorrect(a)).length
})

const percentage = computed(() => {
  if (total.value === 0 || userAnswers.value === mockUserAnswers) return 0
  if (attemptData.value && maxScore.value > 0 && totalScore.value >= 0) {
    const pct = (totalScore.value / maxScore.value) * 100
    return Math.min(100, Math.max(0, Math.round(pct))) // Đảm bảo trong khoảng 0-100
  }
  // Fallback: tính từ số câu đúng / tổng số câu
  const correctCount = userAnswers.value.filter((a) => isAnswerCorrect(a)).length
  const pct = (correctCount / userAnswers.value.length) * 100
  return Math.min(100, Math.max(0, Math.round(pct))) // Đảm bảo trong khoảng 0-100
})

// Format score: nếu là số nguyên thì không hiển thị .0
function formatScore(val: number): string {
  if (typeof val !== 'number') return String(val)
  if (Number.isInteger(val)) return String(val)
  return val.toFixed(1)
}

const resultStatus = computed(() => {
  if (userAnswers.value === mockUserAnswers) {
    return { tone: 'danger', message: 'Không thể tính toán kết quả.', color: '#ef4444' }
  }
  if (percentage.value >= 80) {
    return { tone: 'success', message: 'Xuất sắc! Bạn đã làm rất tốt! 🎉', color: '#16a34a' }
  } else if (percentage.value >= 50) {
    return {
      tone: 'warning',
      message: 'Khá tốt! Cùng cố gắng hơn ở lần sau nhé. 👍',
      color: '#f59e0b',
    }
  }
  return {
    tone: 'danger',
    message: 'Đừng nản lòng, hãy xem lại và thử lại nhé! 💪',
    color: '#ef4444',
  }
})

const toneClass = computed(() => {
  switch (resultStatus.value.tone) {
    case 'success':
      return 'border-cyan-200 dark:border-cyan-700 bg-cyan-50 dark:bg-cyan-900/20'
    case 'warning':
      return 'border-amber-200 bg-amber-50/80'
    case 'danger':
      return 'border-rose-200 bg-rose-50/80'
    default:
      return 'border-slate-200 bg-white'
  }
})

// --- Logic Phân trang ---
const totalPages = computed(() => Math.ceil(userAnswers.value.length / itemsPerPage))

const paginatedAnswers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  // Thêm originalIndex để giữ đúng số thứ tự câu hỏi
  return userAnswers.value.slice(start, end).map((answer, index) => ({
    ...answer,
    originalIndex: start + index,
  }))
})

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    scrollToReviewTop()
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--
    scrollToReviewTop()
  }
}

function toggleReview() {
  showReview.value = !showReview.value
  // Reset về trang 1 mỗi khi mở lại
  if (showReview.value) {
    currentPage.value = 1
  }
}

function scrollToReviewTop() {
  const reviewElement = document.querySelector('.review-section')
  if (reviewElement) {
    reviewElement.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<style scoped>
:global(body) {
  background: #f8fafc;
}

.result-page {
  min-height: calc(100vh - 120px);
  padding: 2rem 1rem 3rem;
  background: linear-gradient(180deg, rgba(229, 231, 235, 0.4), rgba(248, 250, 252, 0.9));
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
  align-items: center;
}

.result-card {
  width: min(920px, 100%);
  border-radius: 32px;
  border: 1px solid #e2e8f0;
  padding: 2.5rem 2rem;
  box-shadow: 0 35px 80px rgba(79, 70, 229, 0.12);
  background: white;
  text-align: center;
}

.result-card h1 {
  font-size: clamp(1.5rem, 4vw, 2.3rem);
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.5rem;
}

.result-card .lead {
  font-size: 1rem;
  color: #475569;
  margin-bottom: 1.6rem;
}

.score-display {
  display: flex;
  justify-content: center;
  align-items: baseline;
  gap: 0.5rem;
}

.score-value {
  font-size: clamp(3rem, 10vw, 4.5rem);
  font-weight: 900;
  color: #111827;
}

.score-total {
  font-size: 1.25rem;
  color: #94a3b8;
  font-weight: 600;
}

.percentage {
  margin-top: 0.25rem;
  font-size: 1.5rem;
  font-weight: 700;
}

.message {
  margin-top: 0.5rem;
  font-size: 1rem;
  color: #475569;
}

.actions {
  margin-top: 1.75rem;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.75rem;
}

.btn {
  min-width: 180px;
  border-radius: 999px;
  padding: 0.85rem 1.75rem;
  font-weight: 700;
  font-size: 0.95rem;
  border: 1px solid transparent;
  transition:
    transform 0.15s ease,
    box-shadow 0.15s ease;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 12px 25px rgba(15, 23, 42, 0.08);
}

.btn.primary {
  background: linear-gradient(135deg, #f97316, #facc15);
  color: #111827;
  border: none;
}

.btn.ghost {
  border: 1px solid #cbd5f5;
  color: #475569;
  background: white;
}

.review-section {
  width: min(960px, 100%);
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 30px;
  padding: 2rem;
  box-shadow: 0 25px 70px rgba(15, 23, 42, 0.08);
}

.review-header {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 1rem;
  margin-bottom: 1.5rem;
}

.review-header h2 {
  font-size: 1.35rem;
  font-weight: 800;
  color: #0f172a;
}

.review-header p {
  color: #64748b;
  font-size: 0.95rem;
}

.question-review {
  border: 1px solid #e2e8f0;
  border-radius: 24px;
  padding: 1.5rem;
  margin-bottom: 1.25rem;
  background: #f8fafc;
  transition:
    border-color 0.2s ease,
    background 0.2s ease;
}

.question-review.correct {
  border-color: rgba(74, 222, 128, 0.5);
  background: rgba(240, 253, 244, 0.8);
}

.question-review.incorrect {
  border-color: rgba(248, 113, 113, 0.5);
  background: rgba(254, 242, 242, 0.9);
}

.question-header {
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.q-text :deep(p) {
  margin: 0;
}

.answer-details p {
  margin: 0.2rem 0;
  font-size: 0.95rem;
  color: #475569;
}

.user-answer {
  font-weight: 700;
  color: #334155;
}

.correct-answer {
  font-weight: 800;
  color: #16a34a;
}

.explanation {
  margin-top: 0.8rem;
  padding: 0.9rem 1rem;
  background: rgba(59, 130, 246, 0.08);
  border-radius: 18px;
  font-size: 0.9rem;
  color: #1d4ed8;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-page {
  min-width: 150px;
  border-radius: 999px;
  border: 1px solid #cbd5f5;
  padding: 0.65rem 1.4rem;
  font-weight: 600;
  background: white;
  color: #475569;
  transition:
    background 0.15s ease,
    color 0.15s ease;
}

.btn-page:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.btn-page:not(:disabled):hover {
  background: #eef2ff;
  color: #312e81;
}

.page-info {
  font-weight: 600;
  color: #0f172a;
}

.loading-state {
  padding: 2rem;
  text-align: center;
  color: #64748b;
}

.score-info {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  color: #64748b;
}

.score-info strong {
  color: #0f172a;
}

@media (max-width: 768px) {
  .result-card,
  .review-section {
    border-radius: 24px;
    padding: 1.5rem;
  }

  .actions {
    flex-direction: column;
    width: 100%;
  }

  .btn {
    width: 100%;
  }

  .review-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
