<template>
  <div class="result-page">
    <div class="result-card" :class="toneClass">
      <h1>Hoàn thành!</h1>
      <p class="lead">Đây là kết quả bài làm của bạn:</p>

      <div class="score-display">
        <span class="score-value">{{ score }}</span>
        <span class="score-total">/ {{ total }}</span>
      </div>
      
      <p class="percentage" :style="{ color: resultStatus.color }">
        Đạt {{ percentage.toFixed(0) }}%
      </p>

      <p class="message">{{ resultStatus.message }}</p>

      <div class="actions">
        <button class="btn ghost" @click="toggleReview">
          {{ showReview ? 'Ẩn đáp án' : 'Xem lại đáp án' }}
        </button>
        <router-link
          class="btn primary"
          :to="{ name: 'student-exams-ranking' }"
          style="color: black; border: 1px;" 

        >
          Xem bảng xếp hạng
        </router-link>
      </div>
    </div>

    <Transition name="fade">
      <div v-if="showReview" class="review-section">
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
            <p>Đáp án của bạn: <span class="user-answer">{{ answer.userAnswer || 'Chưa trả lời' }}</span></p>
            <p>Đáp án đúng: <span class="correct-answer">{{ answer.correctAnswer }}</span></p>
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
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const showReview = ref(false);
const userAnswers = ref<any[]>([]);
const route = useRoute();

// --- Cấu hình Phân trang ---
const currentPage = ref(1);
const itemsPerPage = 10; // Hiển thị 10 câu mỗi trang

// Dữ liệu mẫu nếu không nhận được gì từ trang trước
const mockUserAnswers = [
  { questionText: 'Có lỗi xảy ra, không nhận được dữ liệu bài làm.', userAnswer: '', correctAnswer: '', explanation: 'Vui lòng quay lại và thử nộp bài lần nữa.' }
];

function persistAnswers(answers: any[]) {
  try {
    const key = route.params.id ? `examResult:${route.params.id}` : 'examResult:last';
    sessionStorage.setItem(
      key,
      JSON.stringify({ examId: route.params.id, answers, savedAt: Date.now() })
    );
  } catch (error) {
    console.warn('Không thể lưu tạm kết quả:', error);
  }
}

function loadStoredAnswers(): any[] | null {
  const keys: string[] = [];
  if (route.params.id) keys.push(`examResult:${route.params.id}`);
  keys.push('examResult:last');

  for (const key of keys) {
    const raw = sessionStorage.getItem(key);
    if (!raw) continue;
    try {
      const payload = JSON.parse(raw);
      if (Array.isArray(payload?.answers) && payload.answers.length) {
        sessionStorage.removeItem(key);
        return payload.answers;
      }
    } catch (error) {
      console.warn('Không đọc được kết quả đã lưu:', error);
    }
  }
  return null;
}

onMounted(() => {
  const answersFromState =
    history.state && Array.isArray(history.state.userAnswers) ? history.state.userAnswers : null;
  if (answersFromState?.length) {
    userAnswers.value = answersFromState;
    persistAnswers(answersFromState);
    return;
  }

  const stored = loadStoredAnswers();
  if (stored?.length) {
    userAnswers.value = stored;
  } else {
    console.warn('Không tìm thấy dữ liệu bài làm, đang sử dụng dữ liệu giả (mock data).');
    userAnswers.value = mockUserAnswers;
  }
});

function normalizeAnswer(val: any): string {
  if (Array.isArray(val)) {
    return val
      .map((v) => (v ?? '').toString().trim().toLowerCase())
      .filter(Boolean)
      .sort()
      .join('|');
  }
  return (val ?? '').toString().trim().toLowerCase();
}

function isAnswerCorrect(answer: { userAnswer: any; correctAnswer: any }) {
  return normalizeAnswer(answer.userAnswer) === normalizeAnswer(answer.correctAnswer);
}

const total = computed(() => userAnswers.value.length);
const score = computed(() => userAnswers.value.filter((a) => isAnswerCorrect(a)).length);
const percentage = computed(() => {
  if (total.value === 0 || userAnswers.value === mockUserAnswers) return 0;
  return (score.value / total.value) * 100;
});

const resultStatus = computed(() => {
  if (userAnswers.value === mockUserAnswers) {
    return { tone: 'danger', message: 'Không thể tính toán kết quả.', color: '#ef4444' }
  }
  if (percentage.value >= 80) {
    return { tone: 'success', message: 'Xuất sắc! Bạn đã làm rất tốt! 🎉', color: '#16a34a' }
  } else if (percentage.value >= 50) {
    return { tone: 'warning', message: 'Khá tốt! Cùng cố gắng hơn ở lần sau nhé. 👍', color: '#f59e0b' }
  }
  return { tone: 'danger', message: 'Đừng nản lòng, hãy xem lại và thử lại nhé! 💪', color: '#ef4444' }
})

const toneClass = computed(() => {
  switch (resultStatus.value.tone) {
    case 'success':
      return 'border-brand-200 bg-brand-50'
    case 'warning':
      return 'border-amber-200 bg-amber-50/80'
    case 'danger':
      return 'border-rose-200 bg-rose-50/80'
    default:
      return 'border-slate-200 bg-white'
  }
})

// --- Logic Phân trang ---
const totalPages = computed(() => Math.ceil(userAnswers.value.length / itemsPerPage));

const paginatedAnswers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  // Thêm originalIndex để giữ đúng số thứ tự câu hỏi
  return userAnswers.value.slice(start, end).map((answer, index) => ({
    ...answer,
    originalIndex: start + index
  }));
});

function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    scrollToReviewTop();
  }
}

function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
    scrollToReviewTop();
  }
}

function toggleReview() {
  showReview.value = !showReview.value;
  // Reset về trang 1 mỗi khi mở lại
  if(showReview.value) {
    currentPage.value = 1;
  }
}

function scrollToReviewTop() {
  const reviewElement = document.querySelector('.review-section');
  if (reviewElement) {
    reviewElement.scrollIntoView({ behavior: 'smooth' });
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
  transition: transform 0.15s ease, box-shadow 0.15s ease;
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
  transition: border-color 0.2s ease, background 0.2s ease;
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
  transition: background 0.15s ease, color 0.15s ease;
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
