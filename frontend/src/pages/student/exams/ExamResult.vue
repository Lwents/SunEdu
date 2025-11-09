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
          :class="{ correct: answer.userAnswer === answer.correctAnswer, incorrect: answer.userAnswer !== answer.correctAnswer }"
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

const showReview = ref(false);
const userAnswers = ref<any[]>([]);

// --- Cấu hình Phân trang ---
const currentPage = ref(1);
const itemsPerPage = 10; // Hiển thị 10 câu mỗi trang

// Dữ liệu mẫu nếu không nhận được gì từ trang trước
const mockUserAnswers = [
  { questionText: 'Có lỗi xảy ra, không nhận được dữ liệu bài làm.', userAnswer: '', correctAnswer: '', explanation: 'Vui lòng quay lại và thử nộp bài lần nữa.' }
];

onMounted(() => {
  if (history.state && history.state.userAnswers) {
    userAnswers.value = history.state.userAnswers;
  } else {
    console.warn("Không tìm thấy dữ liệu bài làm, đang sử dụng dữ liệu giả (mock data).");
    userAnswers.value = mockUserAnswers;
  }
});

const total = computed(() => userAnswers.value.length);
const score = computed(() => userAnswers.value.filter(a => a.userAnswer === a.correctAnswer).length);
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
