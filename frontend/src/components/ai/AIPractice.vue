<template>
  <div class="ai-practice">
    <!-- Header với phân tích -->
    <div
      v-if="analysis"
      :class="isDark ? 'bg-gradient-to-r from-slate-900/60 to-purple-900/30 border border-white/5' : 'bg-gradient-to-r from-purple-50 to-pink-50'"
      class="mb-6 rounded-xl p-4"
    >
      <div class="flex items-start gap-3">
        <div class="text-3xl">🎯</div>
        <div class="flex-1">
          <h3 :class="isDark ? 'text-purple-200' : 'text-purple-800'" class="mb-1 font-bold">AI phân tích</h3>
          <p :class="isDark ? 'text-slate-300' : 'text-gray-600'" class="text-sm">{{ analysis.encouragement }}</p>
          
          <!-- Điểm yếu cần cải thiện -->
          <div v-if="analysis.weaknesses?.length" class="mt-3">
            <p :class="isDark ? 'text-purple-300' : 'text-purple-600'" class="mb-2 text-xs font-medium">📚 Cần luyện tập thêm:</p>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="(w, i) in analysis.weaknesses.slice(0, 3)" 
                :key="i"
                class="px-2 py-1 text-xs rounded-full"
                :class="{
                  'bg-red-100 text-red-700': w.severity === 'high' && !isDark,
                  'bg-red-500/20 text-red-200': w.severity === 'high' && isDark,
                  'bg-yellow-100 text-yellow-700': w.severity === 'medium' && !isDark,
                  'bg-yellow-500/20 text-yellow-200': w.severity === 'medium' && isDark,
                  'bg-blue-100 text-blue-700': (w.severity === 'low' || !w.severity) && !isDark,
                  'bg-blue-500/20 text-blue-200': (w.severity === 'low' || !w.severity) && isDark
                }"
              >
                {{ w.topic }}
              </span>
            </div>
          </div>
          
          <!-- Điểm mạnh -->
          <div v-if="analysis.strengths?.length" class="mt-2">
            <p :class="isDark ? 'text-emerald-300' : 'text-green-600'" class="text-xs font-medium">
              ✨ Điểm mạnh: {{ analysis.strengths.join(', ') }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Nút tạo bài luyện tập -->
    <div v-if="!exercises.length && !loading" class="text-center py-8">
      <div class="text-6xl mb-4">📝</div>
      <h3 :class="isDark ? 'text-slate-100' : 'text-gray-800'" class="mb-2 text-lg font-bold">Bài luyện tập hôm nay</h3>
      <p :class="isDark ? 'text-slate-400' : 'text-gray-500'" class="mb-4 text-sm">
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
      <p :class="isDark ? 'text-slate-400' : 'text-gray-500'">Đang phân tích kết quả học tập...</p>
    </div>

    <!-- Bài tập -->
    <div v-if="exercises.length && !completed" class="space-y-4">
      <!-- Progress -->
      <div class="flex items-center justify-between mb-4">
        <span :class="isDark ? 'text-slate-300' : 'text-gray-600'" class="text-sm font-medium">
          Câu {{ currentIndex + 1 }}/{{ exercises.length }}
        </span>
        <div :class="isDark ? 'bg-slate-800' : 'bg-gray-200'" class="mx-4 h-2 flex-1 rounded-full overflow-hidden">
          <div 
            class="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-300"
            :style="{ width: `${((currentIndex) / exercises.length) * 100}%` }"
          ></div>
        </div>
        <span :class="isDark ? 'text-purple-300' : 'text-purple-600'" class="text-sm font-medium">
          {{ correctCount }}/{{ currentIndex }} đúng
        </span>
      </div>

      <!-- Current Question -->
      <div
        :class="isDark ? 'bg-slate-900/80 border-white/10 text-slate-100' : 'bg-white border-gray-100 text-gray-800'"
        class="rounded-xl border p-6 shadow-sm"
      >
        <div class="flex items-start gap-3 mb-4">
          <span 
            class="px-2 py-1 text-xs rounded-full"
            :class="{
              'bg-green-100 text-green-700': currentExercise.difficulty === 'easy' && !isDark,
              'bg-green-500/20 text-green-200': currentExercise.difficulty === 'easy' && isDark,
              'bg-yellow-100 text-yellow-700': currentExercise.difficulty === 'medium' && !isDark,
              'bg-yellow-500/20 text-yellow-200': currentExercise.difficulty === 'medium' && isDark,
              'bg-red-100 text-red-700': currentExercise.difficulty === 'hard' && !isDark,
              'bg-red-500/20 text-red-200': currentExercise.difficulty === 'hard' && isDark
            }"
          >
            {{ difficultyLabel }}
          </span>
          <span :class="isDark ? 'bg-purple-500/20 text-purple-200' : 'bg-purple-100 text-purple-700'" class="rounded-full px-2 py-1 text-xs">
            {{ currentExercise.topic }}
          </span>
        </div>

        <h3 :class="isDark ? 'text-slate-100' : 'text-gray-800'" class="mb-6 text-lg font-medium">
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
        <div
          v-if="answered"
          :class="[
            'mt-6 rounded-xl p-4',
            isCorrect
              ? (isDark ? 'bg-green-500/10' : 'bg-green-50')
              : (isDark ? 'bg-rose-500/10' : 'bg-red-50')
          ]"
        >
          <div class="flex items-start gap-3">
            <span class="text-2xl">{{ isCorrect ? '🎉' : '💡' }}</span>
            <div>
              <p
                :class="isCorrect ? (isDark ? 'text-emerald-200' : 'text-green-700') : (isDark ? 'text-rose-200' : 'text-red-700')"
                class="font-medium"
              >
                {{ isCorrect ? 'Đúng rồi! Giỏi quá!' : 'Chưa đúng rồi!' }}
              </p>
              <p :class="isDark ? 'text-slate-300' : 'text-gray-600'" class="mt-1 text-sm">
                {{ currentExercise.explanation }}
              </p>
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
      <h3 :class="isDark ? 'text-slate-100' : 'text-gray-800'" class="mb-2 text-2xl font-bold">Hoàn thành!</h3>
      <p :class="isDark ? 'text-purple-300' : 'text-purple-600'" class="mb-4 text-4xl font-bold">{{ score }}%</p>
      <p :class="isDark ? 'text-slate-300' : 'text-gray-600'" class="mb-6">
        Con đã trả lời đúng {{ correctCount }}/{{ exercises.length }} câu
      </p>
      
      <div class="flex justify-center gap-3 flex-wrap">
        <button
          @click="resetPractice"
          :class="isDark ? 'bg-slate-800 text-slate-200 hover:bg-slate-700' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
          class="rounded-full px-6 py-2 font-medium transition-colors"
        >
          🔄 Làm lại
        </button>
        <button
          @click="generateExercises"
          class="rounded-full bg-purple-500 px-6 py-2 font-medium text-white transition-colors hover:bg-purple-600"
        >
          📝 Bài mới
        </button>
        <button
          @click="exitPractice"
          :class="isDark ? 'bg-slate-900 border-white/10 text-slate-200 hover:bg-slate-800' : 'bg-white border-gray-200 text-gray-700 hover:bg-gray-50'"
          class="rounded-full border px-6 py-2 font-medium transition-colors"
        >
          ✖ Đóng
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'
import { aiTutorService, type PracticeExercise, type Weakness } from '@/services/ai-tutor.service'
import { useThemeStore } from '@/store/theme.store'

const props = defineProps<{
  autoLoad?: boolean
}>()

const emit = defineEmits<{
  (e: 'completed', score: number, dailyGoal?: any): void
  (e: 'exercise-answered', correct: boolean): void
  (e: 'exit'): void
}>()

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

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
const exerciseId = ref<string | null>(null) // ID của Exercise đã tạo trong database

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
    // Reset state UI trước khi tạo đề mới
    completed.value = false
    answered.value = false
    selectedAnswer.value = null
    exercises.value = []
    currentIndex.value = 0
    correctCount.value = 0

    // Kiểm tra xem có tiến trình đã lưu không
    if (restoreProgress()) {
      generatingExercises.value = false
      return // Đã khôi phục tiến trình, không cần tạo mới
    }
    
    const weaknesses = analysis.value?.weaknesses || []
    const response = await aiTutorService.generatePractice(weaknesses, 5)
    
    if (response.success && response.exercises?.length) {
      exercises.value = response.exercises
      exerciseId.value = response.exercise_id || null // Lưu exercise_id từ backend
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

function loadExternalExercises(external: PracticeExercise[], externalExerciseId?: string | null) {
  if (!external || !external.length) return
  exercises.value = external
  exerciseId.value = externalExerciseId || null
  currentIndex.value = 0
  correctCount.value = 0
  completed.value = false
  answered.value = false
  selectedAnswer.value = null
  answers.value = []
  startTime.value = Date.now()
  clearProgress()
  saveProgress()
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
      
      const response = await aiTutorService.submitPractice({
        exercises: exercisesData,
        score: score.value,
        time_spent: Math.floor((Date.now() - startTime.value) / 1000), // Thời gian làm bài (giây)
        exercise_id: exerciseId.value // Gửi exercise_id để sử dụng Exercise đã tạo sẵn
      })
      
      // Xóa tiến trình đã lưu sau khi submit thành công
      clearProgress()
      
      // Emit với daily_goal mới để parent component có thể cập nhật
      emit('completed', score.value, response.daily_goal)
    } catch (error) {
      console.error('Error submitting practice:', error)
      // Không block UI nếu submit lỗi
      emit('completed', score.value, null)
    }
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

function exitPractice() {
  resetPractice()
  exercises.value = []
  exerciseId.value = null
  emit('exit')
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
      exerciseId: exerciseId.value, // Lưu exercise_id
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
      exerciseId.value = progress.exerciseId || null // Khôi phục exercise_id
      
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
  const dark = isDark.value

  if (!answered.value) {
    if (selectedAnswer.value === choice) {
      return dark
        ? 'border-purple-400 bg-purple-500/10 text-slate-100'
        : 'border-purple-500 bg-purple-50'
    }
    return dark
      ? 'border-white/10 bg-slate-900/60 text-slate-100 hover:border-purple-400 hover:bg-purple-500/10'
      : 'border-gray-200 hover:border-purple-300 hover:bg-purple-50'
  }
  
  const choiceLetter = choice.charAt(0).toUpperCase()
  const correctLetter = currentExercise.value.correct_answer.charAt(0).toUpperCase()
  
  if (choiceLetter === correctLetter) {
    return dark
      ? 'border-green-400 bg-green-500/10 text-emerald-100'
      : 'border-green-500 bg-green-50'
  }
  
  if (selectedAnswer.value === choice) {
    return dark
      ? 'border-rose-400 bg-rose-500/10 text-rose-100'
      : 'border-red-500 bg-red-50'
  }
  
  return dark
    ? 'border-white/10 bg-slate-900/40 text-slate-400'
    : 'border-gray-200 opacity-50'
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
  loadExternalExercises,
})
</script>

<style scoped>
.ai-practice {
  @apply max-w-2xl mx-auto;
}
</style>
