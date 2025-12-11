<template>
  <div class="ai-practice">
    <!-- Header với phân tích -->
    <div v-if="analysis" class="mb-6 p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl">
      <div class="flex items-start gap-3">
        <div class="text-3xl">🎯</div>
        <div class="flex-1">
          <h3 class="font-bold text-purple-800 mb-1">AI phân tích</h3>
          <p class="text-sm text-gray-600">{{ analysis.encouragement }}</p>
          
          <!-- Điểm yếu cần cải thiện -->
          <div v-if="analysis.weaknesses?.length" class="mt-3">
            <p class="text-xs font-medium text-purple-600 mb-2">📚 Cần luyện tập thêm:</p>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="(w, i) in analysis.weaknesses.slice(0, 3)" 
                :key="i"
                class="px-2 py-1 text-xs rounded-full"
                :class="{
                  'bg-red-100 text-red-700': w.severity === 'high',
                  'bg-yellow-100 text-yellow-700': w.severity === 'medium',
                  'bg-blue-100 text-blue-700': w.severity === 'low' || !w.severity
                }"
              >
                {{ w.topic }}
              </span>
            </div>
          </div>
          
          <!-- Điểm mạnh -->
          <div v-if="analysis.strengths?.length" class="mt-2">
            <p class="text-xs font-medium text-green-600">✨ Điểm mạnh: {{ analysis.strengths.join(', ') }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Nút tạo bài luyện tập -->
    <div v-if="!exercises.length && !loading" class="text-center py-8">
      <div class="text-6xl mb-4">📝</div>
      <h3 class="text-lg font-bold text-gray-800 mb-2">Bài luyện tập hôm nay</h3>
      <p class="text-sm text-gray-500 mb-4">
        AI sẽ tạo bài tập phù hợp với bạn!
      </p>
      <button
        @click="generateExercises"
        :disabled="generatingExercises"
        class="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-full font-medium hover:shadow-lg transition-all disabled:opacity-50"
      >
        <span v-if="generatingExercises" class="flex items-center gap-2">
          <svg class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Đang tạo bài tập...
        </span>
        <span v-else>🚀 Bắt đầu luyện tập</span>
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-8">
      <div class="animate-bounce text-5xl mb-4">🌟</div>
      <p class="text-gray-500">Đang phân tích kết quả học tập...</p>
    </div>

    <!-- Bài tập -->
    <div v-if="exercises.length && !completed" class="space-y-4">
      <!-- Progress -->
      <div class="flex items-center justify-between mb-4">
        <span class="text-sm font-medium text-gray-600">
          Câu {{ currentIndex + 1 }}/{{ exercises.length }}
        </span>
        <div class="flex-1 mx-4 h-2 bg-gray-200 rounded-full overflow-hidden">
          <div 
            class="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-300"
            :style="{ width: `${((currentIndex) / exercises.length) * 100}%` }"
          ></div>
        </div>
        <span class="text-sm font-medium text-purple-600">
          {{ correctCount }}/{{ currentIndex }} đúng
        </span>
      </div>

      <!-- Current Question -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div class="flex items-start gap-3 mb-4">
          <span 
            class="px-2 py-1 text-xs rounded-full"
            :class="{
              'bg-green-100 text-green-700': currentExercise.difficulty === 'easy',
              'bg-yellow-100 text-yellow-700': currentExercise.difficulty === 'medium',
              'bg-red-100 text-red-700': currentExercise.difficulty === 'hard'
            }"
          >
            {{ difficultyLabel }}
          </span>
          <span class="px-2 py-1 text-xs bg-purple-100 text-purple-700 rounded-full">
            {{ currentExercise.topic }}
          </span>
        </div>

        <h3 class="text-lg font-medium text-gray-800 mb-6">
          {{ currentExercise.question }}
        </h3>

        <!-- Choices -->
        <div class="space-y-3">
          <button
            v-for="(choice, i) in currentExercise.choices"
            :key="i"
            @click="selectAnswer(choice)"
            :disabled="answered"
            class="w-full p-4 text-left rounded-xl border-2 transition-all"
            :class="getChoiceClass(choice)"
          >
            <span class="font-medium">{{ choice }}</span>
          </button>
        </div>

        <!-- Explanation (after answer) -->
        <div v-if="answered" class="mt-6 p-4 rounded-xl" :class="isCorrect ? 'bg-green-50' : 'bg-red-50'">
          <div class="flex items-start gap-3">
            <span class="text-2xl">{{ isCorrect ? '🎉' : '💡' }}</span>
            <div>
              <p class="font-medium" :class="isCorrect ? 'text-green-700' : 'text-red-700'">
                {{ isCorrect ? 'Đúng rồi! Giỏi quá!' : 'Chưa đúng rồi!' }}
              </p>
              <p class="text-sm text-gray-600 mt-1">{{ currentExercise.explanation }}</p>
            </div>
          </div>
        </div>

        <!-- Next button -->
        <div v-if="answered" class="mt-4 text-center">
          <button
            @click="nextQuestion"
            class="px-6 py-2 bg-purple-500 text-white rounded-full font-medium hover:bg-purple-600 transition-colors"
          >
            {{ currentIndex < exercises.length - 1 ? 'Câu tiếp theo →' : 'Xem kết quả 🎯' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Completed -->
    <div v-if="completed" class="text-center py-8">
      <div class="text-6xl mb-4">{{ score >= 80 ? '🏆' : score >= 50 ? '⭐' : '💪' }}</div>
      <h3 class="text-2xl font-bold text-gray-800 mb-2">Hoàn thành!</h3>
      <p class="text-4xl font-bold text-purple-600 mb-4">{{ score }}%</p>
      <p class="text-gray-600 mb-6">
        Con đã trả lời đúng {{ correctCount }}/{{ exercises.length }} câu
      </p>
      
      <div class="flex justify-center gap-4">
        <button
          @click="resetPractice"
          class="px-6 py-2 bg-gray-100 text-gray-700 rounded-full font-medium hover:bg-gray-200 transition-colors"
        >
          🔄 Làm lại
        </button>
        <button
          @click="generateExercises"
          class="px-6 py-2 bg-purple-500 text-white rounded-full font-medium hover:bg-purple-600 transition-colors"
        >
          📝 Bài mới
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'
import { aiTutorService, type PracticeExercise, type Weakness } from '@/services/ai-tutor.service'

const props = defineProps<{
  autoLoad?: boolean
}>()

const emit = defineEmits<{
  (e: 'completed', score: number): void
  (e: 'exercise-answered', correct: boolean): void
}>()

// State
const loading = ref(false)
const generatingExercises = ref(false)
const exercises = ref<PracticeExercise[]>([])
const currentIndex = ref(0)
const selectedAnswer = ref<string | null>(null)
const answered = ref(false)
const correctCount = ref(0)
const completed = ref(false)
const analysis = ref<any>(null)
const answers = ref<string[]>([]) // Lưu tất cả câu trả lời
const startTime = ref(0) // Thời gian bắt đầu làm bài

// Storage key cho localStorage
import { useAuthStore } from '@/store/auth.store'
const auth = useAuthStore()
const storageKey = computed(() => {
  const user = auth.user
  const userKey = String(user?.id ?? user?.email ?? 'guest')
  return `ai_practice_${userKey}`
})

// Computed
const currentExercise = computed(() => exercises.value[currentIndex.value])

const isCorrect = computed(() => {
  if (!selectedAnswer.value || !currentExercise.value) return false
  const selected = selectedAnswer.value.charAt(0).toUpperCase()
  const correct = currentExercise.value.correct_answer.charAt(0).toUpperCase()
  return selected === correct
})

const score = computed(() => {
  if (!exercises.value.length) return 0
  return Math.round((correctCount.value / exercises.value.length) * 100)
})

const difficultyLabel = computed(() => {
  const labels = { easy: 'Dễ', medium: 'Vừa', hard: 'Khó' }
  return labels[currentExercise.value?.difficulty] || 'Vừa'
})

// Methods
async function loadAnalysis(autoGenerate = false) {
  loading.value = true
  try {
    const response = await aiTutorService.analyzeWeaknesses()
    if (response.success) {
      analysis.value = response.analysis
    }
    // Tự động tạo bài tập nếu được yêu cầu
    if (autoGenerate) {
      await generateExercises()
    }
  } catch (error) {
    console.error('Load analysis error:', error)
  } finally {
    loading.value = false
  }
}

async function generateExercises() {
  generatingExercises.value = true
  try {
    // Kiểm tra xem có tiến trình đã lưu không
    if (restoreProgress()) {
      generatingExercises.value = false
      return // Đã khôi phục tiến trình, không cần tạo mới
    }
    
    const weaknesses = analysis.value?.weaknesses || []
    const response = await aiTutorService.generatePractice(weaknesses, 5)
    
    if (response.success && response.exercises?.length) {
      exercises.value = response.exercises
      currentIndex.value = 0
      correctCount.value = 0
      completed.value = false
      answered.value = false
      selectedAnswer.value = null
      answers.value = [] // Reset answers
      startTime.value = Date.now() // Ghi nhận thời gian bắt đầu
      
      // Lưu tiến trình mới
      saveProgress()
    }
  } catch (error) {
    console.error('Generate exercises error:', error)
  } finally {
    generatingExercises.value = false
  }
}

function selectAnswer(choice: string) {
  if (answered.value) return
  
  selectedAnswer.value = choice
  answered.value = true
  
  // Lưu câu trả lời vào mảng answers
  answers.value[currentIndex.value] = choice
  
  if (isCorrect.value) {
    correctCount.value++
  }
  
  // Lưu tiến trình vào localStorage
  saveProgress()
  
  emit('exercise-answered', isCorrect.value)
}

async function nextQuestion() {
  if (currentIndex.value < exercises.value.length - 1) {
    currentIndex.value++
    answered.value = false
    selectedAnswer.value = null
    
    // Lưu tiến trình vào localStorage
    saveProgress()
  } else {
    completed.value = true
    
    // Submit kết quả bài luyện tập để tính vào streak/daily goal
    try {
      const exercisesData = exercises.value.map((ex, idx) => ({
        question: ex.question,
        correct_answer: ex.correct_answer,
        student_answer: answers.value[idx] || '',
        is_correct: answers.value[idx] === ex.correct_answer
      }))
      
      await aiTutorService.submitPractice({
        exercises: exercisesData,
        score: score.value,
        time_spent: Math.floor((Date.now() - startTime.value) / 1000) // Thời gian làm bài (giây)
      })
      
      // Xóa tiến trình đã lưu sau khi submit thành công
      clearProgress()
    } catch (error) {
      console.error('Error submitting practice:', error)
      // Không block UI nếu submit lỗi
    }
    
    emit('completed', score.value)
  }
}

function resetPractice() {
  currentIndex.value = 0
  correctCount.value = 0
  completed.value = false
  answered.value = false
  selectedAnswer.value = null
  answers.value = []
  startTime.value = 0
  clearProgress()
}

// Lưu tiến trình vào localStorage
function saveProgress() {
  try {
    const progress = {
      exercises: exercises.value,
      currentIndex: currentIndex.value,
      answers: answers.value,
      correctCount: correctCount.value,
      startTime: startTime.value,
      completed: completed.value,
      timestamp: Date.now()
    }
    localStorage.setItem(storageKey.value, JSON.stringify(progress))
  } catch (e) {
    console.warn('Cannot save practice progress:', e)
  }
}

// Khôi phục tiến trình từ localStorage
function restoreProgress(): boolean {
  try {
    const saved = localStorage.getItem(storageKey.value)
    if (!saved) return false
    
    const progress = JSON.parse(saved)
    
    // Kiểm tra xem progress có còn hợp lệ không (không quá 24 giờ)
    const maxAge = 24 * 60 * 60 * 1000 // 24 giờ
    if (progress.timestamp && (Date.now() - progress.timestamp) > maxAge) {
      clearProgress()
      return false
    }
    
    // Khôi phục nếu chưa hoàn thành
    if (progress.exercises && progress.exercises.length > 0 && !progress.completed) {
      exercises.value = progress.exercises
      currentIndex.value = progress.currentIndex || 0
      answers.value = progress.answers || []
      correctCount.value = progress.correctCount || 0
      startTime.value = progress.startTime || Date.now()
      completed.value = false
      
      // Khôi phục trạng thái câu hỏi hiện tại
      if (currentIndex.value < exercises.value.length) {
        answered.value = !!answers.value[currentIndex.value]
        selectedAnswer.value = answers.value[currentIndex.value] || null
      }
      
      return true
    }
    
    return false
  } catch (e) {
    console.warn('Cannot restore practice progress:', e)
    return false
  }
}

// Xóa tiến trình đã lưu
function clearProgress() {
  try {
    localStorage.removeItem(storageKey.value)
  } catch (e) {
    console.warn('Cannot clear practice progress:', e)
  }
}

function getChoiceClass(choice: string) {
  if (!answered.value) {
    return selectedAnswer.value === choice
      ? 'border-purple-500 bg-purple-50'
      : 'border-gray-200 hover:border-purple-300 hover:bg-purple-50'
  }
  
  const choiceLetter = choice.charAt(0).toUpperCase()
  const correctLetter = currentExercise.value.correct_answer.charAt(0).toUpperCase()
  
  if (choiceLetter === correctLetter) {
    return 'border-green-500 bg-green-50'
  }
  
  if (selectedAnswer.value === choice) {
    return 'border-red-500 bg-red-50'
  }
  
  return 'border-gray-200 opacity-50'
}

// Lifecycle
onMounted(() => {
  // Thử khôi phục tiến trình trước
  if (restoreProgress()) {
    // Đã khôi phục tiến trình, không cần load lại
    return
  }
  
  if (props.autoLoad) {
    // Tự động load analysis VÀ generate exercises
    loadAnalysis(true)
  }
})

// Lưu tiến trình khi component unmount
onBeforeUnmount(() => {
  if (!completed.value && exercises.value.length > 0) {
    saveProgress()
  }
})

// Lưu tiến trình trước khi rời trang
onBeforeRouteLeave((to, from, next) => {
  if (!completed.value && exercises.value.length > 0) {
    saveProgress()
  }
  next()
})

// Expose methods
defineExpose({
  loadAnalysis,
  generateExercises,
  resetPractice,
})
</script>

<style scoped>
.ai-practice {
  @apply max-w-2xl mx-auto;
}
</style>
