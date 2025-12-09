<template>
  <!-- Feedback đơn giản cho học sinh tiểu học -->
  <div class="ai-feedback">
    <!-- Khi đúng -->
    <Transition name="pop">
      <div v-if="showCorrect" class="feedback-card correct">
        <div class="feedback-icon">🎉</div>
        <div class="feedback-text">
          <p class="feedback-title">Đúng rồi!</p>
          <p class="feedback-message">{{ correctMessage }}</p>
        </div>
      </div>
    </Transition>

    <!-- Khi sai -->
    <Transition name="pop">
      <div v-if="showWrong" class="feedback-card wrong">
        <div class="feedback-icon">💪</div>
        <div class="feedback-text">
          <p class="feedback-title">Thử lại nhé!</p>
          <p class="feedback-message">{{ wrongMessage }}</p>
        </div>
        
        <!-- Nút gợi ý lớn, dễ bấm -->
        <button 
          v-if="canShowHint"
          @click="requestHint"
          class="hint-button"
          :disabled="loadingHint"
        >
          <span class="hint-icon">💡</span>
          <span>{{ loadingHint ? 'Đang nghĩ...' : 'Giúp con với!' }}</span>
        </button>
      </div>
    </Transition>

    <!-- Hiển thị gợi ý -->
    <Transition name="slide">
      <div v-if="currentHint" class="hint-card">
        <div class="hint-header">
          <span class="hint-label">🌟 Gợi ý từ AI</span>
        </div>
        <p class="hint-text">{{ currentHint }}</p>
        
        <div class="hint-actions">
          <button 
            v-if="canGetMoreHints" 
            @click="requestHint" 
            class="more-hint-btn"
            :disabled="loadingHint"
          >
            Gợi ý thêm
          </button>
          <button @click="closeHint" class="got-it-btn">
            Hiểu rồi! ✓
          </button>
        </div>
      </div>
    </Transition>

    <!-- Động viên khi hoàn thành bài -->
    <Transition name="celebrate">
      <div v-if="showCompletion" class="completion-overlay" @click="closeCompletion">
        <div class="completion-card">
          <div class="completion-stars">⭐⭐⭐</div>
          <div class="completion-score">{{ score }}%</div>
          <p class="completion-message">{{ completionMessage }}</p>
          <button @click="closeCompletion" class="continue-btn">
            Tiếp tục học! 🚀
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { aiTutorService } from '@/services/ai-tutor.service'

const props = defineProps<{
  // Trạng thái
  isCorrect?: boolean
  isWrong?: boolean
  isCompleted?: boolean
  score?: number
  
  // Context cho hint
  questionText?: string
  questionChoices?: string[]
  correctAnswer?: string
  studentAnswer?: string
}>()

const emit = defineEmits<{
  (e: 'hint-received', hint: string): void
  (e: 'close'): void
}>()

// State
const showCorrect = ref(false)
const showWrong = ref(false)
const showCompletion = ref(false)
const currentHint = ref('')
const loadingHint = ref(false)
const hintLevel = ref(0)
const canGetMoreHints = ref(true)

// Messages
const correctMessages = [
  'Giỏi quá con ơi!',
  'Tuyệt vời! Đúng luôn!',
  'Xuất sắc! Con thật thông minh!',
  'Chính xác! Cố gắng tiếp nhé!',
]

const wrongMessages = [
  'Không sao, thử lại nào!',
  'Gần đúng rồi, cố lên!',
  'Sai rồi nhưng đừng bỏ cuộc nhé!',
]

const completionMessages: Record<string, string> = {
  excellent: 'Xuất sắc! Con làm tốt lắm!',
  good: 'Giỏi lắm! Tiếp tục phát huy nhé!',
  ok: 'Tốt rồi! Ôn lại một chút nhé!',
  needWork: 'Cố gắng hơn nữa nhé con!',
}

// Computed
const correctMessage = computed(() => {
  return correctMessages[Math.floor(Math.random() * correctMessages.length)]
})

const wrongMessage = computed(() => {
  return wrongMessages[Math.floor(Math.random() * wrongMessages.length)]
})

const completionMessage = computed(() => {
  const s = props.score || 0
  if (s >= 90) return completionMessages.excellent
  if (s >= 70) return completionMessages.good
  if (s >= 50) return completionMessages.ok
  return completionMessages.needWork
})

const canShowHint = computed(() => {
  return !!props.questionText && !currentHint.value
})

// Methods
async function requestHint() {
  if (!props.questionText || loadingHint.value) return
  
  loadingHint.value = true
  hintLevel.value++
  
  try {
    const response = await aiTutorService.getHint({
      question_text: props.questionText,
      choices: props.questionChoices,
      correct_answer: props.correctAnswer,
      student_answer: props.studentAnswer,
      hint_level: hintLevel.value,
    })
    
    if (response.success) {
      currentHint.value = response.hint
      canGetMoreHints.value = response.can_get_more_hints
      emit('hint-received', response.hint)
    } else {
      currentHint.value = 'AI đang bận, thử lại sau nhé! 🌟'
    }
  } catch {
    currentHint.value = 'Đọc lại đề bài thật kỹ nhé con! 📖'
  } finally {
    loadingHint.value = false
  }
}

function closeHint() {
  currentHint.value = ''
}

function closeCompletion() {
  showCompletion.value = false
  emit('close')
}

// Watchers
watch(() => props.isCorrect, (val) => {
  if (val) {
    showCorrect.value = true
    showWrong.value = false
    currentHint.value = ''
    
    setTimeout(() => {
      showCorrect.value = false
    }, 2000)
  }
})

watch(() => props.isWrong, (val) => {
  if (val) {
    showWrong.value = true
    showCorrect.value = false
    hintLevel.value = 0
    canGetMoreHints.value = true
  } else {
    showWrong.value = false
  }
})

watch(() => props.isCompleted, (val) => {
  if (val) {
    showCompletion.value = true
  }
})

watch(() => props.questionText, () => {
  // Reset khi đổi câu hỏi
  currentHint.value = ''
  hintLevel.value = 0
  canGetMoreHints.value = true
  showCorrect.value = false
  showWrong.value = false
})

// Expose
defineExpose({
  requestHint,
  closeHint,
})
</script>

<style scoped>
.ai-feedback {
  position: relative;
}

/* Feedback Cards */
.feedback-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-radius: 16px;
  margin-bottom: 16px;
}

.feedback-card.correct {
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  border: 2px solid #22c55e;
}

.feedback-card.wrong {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
  border: 2px solid #f59e0b;
  flex-wrap: wrap;
}

.feedback-icon {
  font-size: 36px;
  flex-shrink: 0;
}

.feedback-text {
  flex: 1;
}

.feedback-title {
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 4px 0;
}

.correct .feedback-title {
  color: #15803d;
}

.wrong .feedback-title {
  color: #b45309;
}

.feedback-message {
  font-size: 14px;
  margin: 0;
  color: #374151;
}

/* Hint Button */
.hint-button {
  width: 100%;
  margin-top: 12px;
  padding: 14px 20px;
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.2s;
}

.hint-button:hover:not(:disabled) {
  transform: scale(1.02);
  box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
}

.hint-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.hint-icon {
  font-size: 20px;
}

/* Hint Card */
.hint-card {
  background: linear-gradient(135deg, #ede9fe, #ddd6fe);
  border: 2px solid #8b5cf6;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 16px;
}

.hint-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.hint-label {
  font-size: 14px;
  font-weight: 600;
  color: #6d28d9;
}

.hint-text {
  font-size: 15px;
  line-height: 1.6;
  color: #374151;
  margin: 0 0 12px 0;
}

.hint-actions {
  display: flex;
  gap: 10px;
}

.more-hint-btn {
  flex: 1;
  padding: 10px;
  background: white;
  border: 2px solid #8b5cf6;
  color: #7c3aed;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.more-hint-btn:hover:not(:disabled) {
  background: #f5f3ff;
}

.more-hint-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.got-it-btn {
  flex: 1;
  padding: 10px;
  background: #8b5cf6;
  border: none;
  color: white;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.got-it-btn:hover {
  background: #7c3aed;
}

/* Completion Overlay */
.completion-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.completion-card {
  background: white;
  border-radius: 24px;
  padding: 32px;
  text-align: center;
  max-width: 320px;
  width: 100%;
  animation: pop-in 0.3s ease-out;
}

.completion-stars {
  font-size: 40px;
  margin-bottom: 10px;
}

.completion-score {
  font-size: 56px;
  font-weight: 800;
  background: linear-gradient(135deg, #f59e0b, #ef4444);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.completion-message {
  font-size: 18px;
  color: #374151;
  margin: 10px 0 20px;
}

.continue-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.continue-btn:hover {
  transform: scale(1.02);
}

/* Animations */
@keyframes pop-in {
  0% { transform: scale(0.8); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

.pop-enter-active,
.pop-leave-active {
  transition: all 0.3s ease;
}

.pop-enter-from,
.pop-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.celebrate-enter-active,
.celebrate-leave-active {
  transition: all 0.3s;
}

.celebrate-enter-from,
.celebrate-leave-to {
  opacity: 0;
}
</style>
