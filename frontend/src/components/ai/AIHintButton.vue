<template>
  <div class="ai-hint-wrapper">
    <!-- Hint Button - Đơn giản, màu cyan -->
    <button
      @click="requestHint"
      :disabled="loading || hintsRemaining <= 0"
      class="flex items-center gap-1 px-3 py-1 rounded-lg text-sm font-medium transition-all"
      :class="hintsRemaining > 0 
        ? 'bg-cyan-100 text-cyan-700 hover:bg-cyan-200' 
        : 'bg-gray-100 text-gray-400 cursor-not-allowed'"
    >
      <span>{{ loading ? '⏳' : '💡' }}</span>
      <span>{{ loading ? '...' : `Gợi ý (${hintsRemaining})` }}</span>
    </button>

    <!-- Hint Modal - Đơn giản -->
    <Teleport to="body">
      <Transition name="hint-fade">
        <div
          v-if="showHint"
          class="fixed inset-0 z-[100] flex items-center justify-center bg-black/50 p-4"
          @click.self="closeHint"
        >
          <div class="w-full max-w-md rounded-2xl bg-white shadow-xl overflow-hidden">
            <!-- Header -->
            <div class="bg-cyan-600 px-5 py-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <span class="text-xl">💡</span>
                  <h3 class="font-semibold text-white">Gợi ý</h3>
                </div>
                <span class="text-cyan-200 text-xs">{{ currentHintLevel }}/3</span>
              </div>
            </div>

            <!-- Hint Content -->
            <div class="p-5">
              <div class="bg-cyan-50 rounded-xl p-4 mb-4">
                <p class="text-slate-700 whitespace-pre-wrap leading-relaxed text-sm">
                  {{ currentHint }}
                </p>
              </div>

              <!-- Actions -->
              <div class="flex gap-2">
                <button
                  v-if="canGetMoreHints"
                  @click="requestMoreHint"
                  :disabled="loading"
                  class="flex-1 rounded-lg border border-cyan-300 px-3 py-2 text-sm font-medium text-cyan-700 hover:bg-cyan-50"
                >
                  {{ loading ? '⏳...' : 'Gợi ý thêm' }}
                </button>
                <button
                  @click="closeHint"
                  class="flex-1 rounded-lg bg-cyan-600 px-3 py-2 text-sm font-medium text-white hover:bg-cyan-700"
                >
                  Đã hiểu
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { aiTutorService } from '@/services/ai-tutor.service'

// Props
const props = defineProps<{
  questionText: string
  questionType?: 'multiple_choice' | 'fill_blank' | 'true_false' | 'short_answer'
  choices?: string[]
  correctAnswer?: string
  questionId?: string | number
  maxHints?: number
}>()

// Emits
const emit = defineEmits<{
  (e: 'hint-used', level: number): void
}>()

// State
const loading = ref(false)
const showHint = ref(false)
const currentHint = ref('')
const currentHintLevel = ref(0)
const hintsRemaining = ref(props.maxHints || 3)
const canGetMoreHints = ref(true)

// Methods
async function requestHint(studentAnswer?: string) {
  if (loading.value || hintsRemaining.value <= 0) return

  loading.value = true

  try {
    const response = await aiTutorService.getHint({
      question_text: props.questionText,
      question_type: props.questionType,
      choices: props.choices,
      student_answer: studentAnswer,
      correct_answer: props.correctAnswer,
      hint_level: currentHintLevel.value + 1,
      question_id: props.questionId,
    })

    if (response.success) {
      currentHint.value = response.hint
      currentHintLevel.value = response.hint_level
      hintsRemaining.value = response.hints_remaining
      canGetMoreHints.value = response.can_get_more_hints
      showHint.value = true
      
      emit('hint-used', response.hint_level)
    }
  } catch (error) {
    console.error('Hint error:', error)
    currentHint.value = '💡 Gợi ý: Con đọc lại đề bài thật kỹ nhé! Mặt Trời tin con làm được! 🌟'
    showHint.value = true
  } finally {
    loading.value = false
  }
}

async function requestMoreHint() {
  if (!canGetMoreHints.value) return
  await requestHint()
}

function closeHint() {
  showHint.value = false
}

// Expose method for parent component
defineExpose({
  requestHint,
  hintsRemaining,
})
</script>

<style scoped>
.hint-fade-enter-active,
.hint-fade-leave-active {
  transition: all 0.3s ease;
}

.hint-fade-enter-from,
.hint-fade-leave-to {
  opacity: 0;
}

.hint-fade-enter-from .animate-bounce-in,
.hint-fade-leave-to .animate-bounce-in {
  transform: scale(0.9) translateY(20px);
}

@keyframes bounce-in {
  0% {
    transform: scale(0.9) translateY(20px);
    opacity: 0;
  }
  50% {
    transform: scale(1.02);
  }
  100% {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

.animate-bounce-in {
  animation: bounce-in 0.4s ease-out;
}
</style>
