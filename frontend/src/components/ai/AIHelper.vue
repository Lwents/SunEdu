<template>
  <!-- Nhân vật Mặt Trời - góc phải màn hình -->
  <div class="ai-helper-container">
    <!-- Mascot -->
    <div 
      class="mascot-wrapper"
      :class="{ 'mascot-talking': isTalking, 'mascot-celebrating': isCelebrating }"
      @click="toggleHelper"
    >
      <div class="mascot">
        <span class="mascot-face">🌟</span>
      </div>
      
      <!-- Speech Bubble -->
      <Transition name="bubble">
        <div v-if="showBubble && currentMessage" class="speech-bubble">
          <div class="bubble-content">
            <p class="bubble-text">{{ currentMessage }}</p>
            
            <!-- Action buttons trong bubble -->
            <div v-if="showActions" class="bubble-actions">
              <button 
                v-if="canGetHint"
                @click.stop="getHint"
                class="action-btn hint-btn"
                :disabled="loadingHint"
              >
                <span v-if="loadingHint">⏳</span>
                <span v-else>💡 Gợi ý</span>
              </button>
              
              <button 
                @click.stop="closeBubble"
                class="action-btn close-btn"
              >
                ✓ Hiểu rồi
              </button>
            </div>
          </div>
          
          <!-- Bubble arrow -->
          <div class="bubble-arrow"></div>
        </div>
      </Transition>
    </div>

    <!-- Quick Help Button (khi bubble đóng) -->
    <Transition name="fade">
      <button 
        v-if="!showBubble && canGetHint"
        @click="getHint"
        class="quick-help-btn"
        :disabled="loadingHint"
      >
        {{ loadingHint ? '⏳' : '❓ Giúp con!' }}
      </button>
    </Transition>

    <!-- Celebration Overlay -->
    <Transition name="celebrate">
      <div v-if="showCelebration" class="celebration-overlay" @click="closeCelebration">
        <div class="celebration-content">
          <div class="celebration-emoji">{{ celebrationEmoji }}</div>
          <p class="celebration-text">{{ celebrationText }}</p>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { aiTutorService } from '@/services/ai-tutor.service'

const props = defineProps<{
  // Context cho AI
  questionText?: string
  questionChoices?: string[]
  correctAnswer?: string
  studentAnswer?: string
  subject?: string
  lessonTitle?: string
  
  // Triggers
  showWelcome?: boolean
  showCorrectFeedback?: boolean
  showWrongFeedback?: boolean
  score?: number
}>()

const emit = defineEmits<{
  (e: 'hint-received', hint: string): void
  (e: 'help-requested'): void
}>()

// State
const showBubble = ref(false)
const currentMessage = ref('')
const showActions = ref(true)
const isTalking = ref(false)
const isCelebrating = ref(false)
const loadingHint = ref(false)
const hintLevel = ref(0)
const canGetHint = ref(false)

// Celebration
const showCelebration = ref(false)
const celebrationEmoji = ref('🎉')
const celebrationText = ref('')

// Messages
const welcomeMessages = [
  'Chào con! Mặt Trời sẽ giúp con học bài nhé! 🌟',
  'Xin chào! Cần gì cứ gọi Mặt Trời nhé! ☀️',
  'Chào con yêu! Học vui vẻ nha! 🌈',
]

const correctMessages = [
  'Giỏi quá! Con làm đúng rồi! 🎉',
  'Tuyệt vời! Đúng rồi đó! ⭐',
  'Xuất sắc! Con thật thông minh! 🏆',
  'Wow! Chính xác luôn! 🌟',
]

const wrongMessages = [
  'Ồ, chưa đúng rồi! Thử lại nhé! 💪',
  'Gần đúng rồi! Cố lên con! 🌟',
  'Không sao, sai là để học mà! 📚',
]

const encourageMessages = [
  'Con đang làm tốt lắm! Tiếp tục nhé! 💪',
  'Mặt Trời tin con làm được! ☀️',
  'Cố gắng lên nào! 🌟',
]

// Methods
function toggleHelper() {
  if (showBubble.value) {
    closeBubble()
  } else {
    showRandomEncouragement()
  }
}

function showMessage(message: string, withActions = true) {
  currentMessage.value = message
  showActions.value = withActions
  showBubble.value = true
  isTalking.value = true
  
  setTimeout(() => {
    isTalking.value = false
  }, 500)
}

function closeBubble() {
  showBubble.value = false
  currentMessage.value = ''
}

function showRandomEncouragement() {
  const msg = encourageMessages[Math.floor(Math.random() * encourageMessages.length)]
  showMessage(msg, true)
}

function showWelcomeMessage() {
  const msg = welcomeMessages[Math.floor(Math.random() * welcomeMessages.length)]
  showMessage(msg, false)
  
  // Auto close after 3s
  setTimeout(() => {
    if (showBubble.value && !showActions.value) {
      closeBubble()
    }
  }, 3000)
}

function showCorrect() {
  const msg = correctMessages[Math.floor(Math.random() * correctMessages.length)]
  showMessage(msg, false)
  
  // Show celebration
  celebrationEmoji.value = ['🎉', '⭐', '🏆', '🌟'][Math.floor(Math.random() * 4)]
  celebrationText.value = 'Đúng rồi!'
  showCelebration.value = true
  isCelebrating.value = true
  
  setTimeout(() => {
    showCelebration.value = false
    isCelebrating.value = false
    closeBubble()
  }, 2000)
}

function showWrong() {
  const msg = wrongMessages[Math.floor(Math.random() * wrongMessages.length)]
  showMessage(msg, true)
  canGetHint.value = true
  hintLevel.value = 0
}

async function getHint() {
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
      showMessage(response.hint, true)
      emit('hint-received', response.hint)
      
      // Disable hint if max level
      if (!response.can_get_more_hints) {
        canGetHint.value = false
      }
    }
  } catch (error) {
    showMessage('Mặt Trời đang nghĩ... Thử lại sau nhé! 🤔', true)
  } finally {
    loadingHint.value = false
  }
}

function closeCelebration() {
  showCelebration.value = false
  isCelebrating.value = false
}

// Watchers
watch(() => props.showWelcome, (val) => {
  if (val) showWelcomeMessage()
})

watch(() => props.showCorrectFeedback, (val) => {
  if (val) showCorrect()
})

watch(() => props.showWrongFeedback, (val) => {
  if (val) showWrong()
})

watch(() => props.questionText, () => {
  // Reset hint level when question changes
  hintLevel.value = 0
  canGetHint.value = !!props.questionText
})

// Lifecycle
onMounted(() => {
  if (props.showWelcome) {
    setTimeout(showWelcomeMessage, 500)
  }
  canGetHint.value = !!props.questionText
})

onBeforeUnmount(() => {
  // cleanup if needed
})

// Expose methods for parent
defineExpose({
  showMessage,
  showCorrect,
  showWrong,
  getHint,
  closeBubble,
})
</script>

<style scoped>
.ai-helper-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

/* Mascot */
.mascot-wrapper {
  position: relative;
  cursor: pointer;
}

.mascot {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(251, 191, 36, 0.4);
  transition: transform 0.3s, box-shadow 0.3s;
}

.mascot:hover {
  transform: scale(1.1);
  box-shadow: 0 6px 25px rgba(251, 191, 36, 0.5);
}

.mascot-face {
  font-size: 40px;
  animation: float 3s ease-in-out infinite;
}

.mascot-talking .mascot {
  animation: talk 0.3s ease-in-out 2;
}

.mascot-celebrating .mascot {
  animation: celebrate 0.5s ease-in-out 3;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

@keyframes talk {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

@keyframes celebrate {
  0%, 100% { transform: scale(1) rotate(0deg); }
  25% { transform: scale(1.2) rotate(-10deg); }
  75% { transform: scale(1.2) rotate(10deg); }
}

/* Speech Bubble */
.speech-bubble {
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 280px;
  background: white;
  border-radius: 20px;
  padding: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.bubble-arrow {
  position: absolute;
  bottom: -10px;
  right: 25px;
  width: 0;
  height: 0;
  border-left: 10px solid transparent;
  border-right: 10px solid transparent;
  border-top: 10px solid white;
}

.bubble-text {
  font-size: 15px;
  line-height: 1.5;
  color: #374151;
  margin-bottom: 12px;
}

.bubble-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.action-btn {
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.hint-btn {
  background: linear-gradient(135deg, #a855f7, #7c3aed);
  color: white;
}

.hint-btn:hover:not(:disabled) {
  transform: scale(1.05);
}

.read-btn {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
}

.read-btn:hover:not(:disabled) {
  transform: scale(1.05);
}

.close-btn {
  background: #f3f4f6;
  color: #6b7280;
}

.close-btn:hover {
  background: #e5e7eb;
}

/* Quick Help Button */
.quick-help-btn {
  position: absolute;
  bottom: 80px;
  right: 0;
  padding: 10px 18px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
  transition: all 0.3s;
  animation: pulse 2s infinite;
}

.quick-help-btn:hover:not(:disabled) {
  transform: scale(1.05);
}

.quick-help-btn:disabled {
  opacity: 0.7;
  animation: none;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4); }
  50% { box-shadow: 0 4px 25px rgba(239, 68, 68, 0.6); }
}

/* Celebration Overlay */
.celebration-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.celebration-content {
  text-align: center;
  animation: pop-in 0.3s ease-out;
}

.celebration-emoji {
  font-size: 80px;
  animation: bounce 0.5s ease-in-out infinite;
}

.celebration-text {
  font-size: 28px;
  font-weight: 700;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  margin-top: 10px;
}

@keyframes pop-in {
  0% { transform: scale(0); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

/* Transitions */
.bubble-enter-active,
.bubble-leave-active {
  transition: all 0.3s ease;
}

.bubble-enter-from,
.bubble-leave-to {
  opacity: 0;
  transform: translateY(10px) scale(0.9);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
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
