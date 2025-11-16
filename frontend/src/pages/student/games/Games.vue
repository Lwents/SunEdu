<template>
  <div class="min-h-screen bg-slate-50 pb-16 pt-10">
    <div class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">Trò chơi giáo dục</h1>
        <p class="text-slate-600">Học mà chơi, chơi mà học</p>
      </div>

      <!-- Game Grid -->
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <!-- Quiz Game -->
        <div class="rounded-lg border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition">
          <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-slate-900 mb-2">Trắc nghiệm nhanh</h3>
          <p class="text-sm text-slate-600 mb-4">
            Thử thách kiến thức của bạn với các câu hỏi trắc nghiệm vui nhộn
          </p>
          <button
            class="w-full rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white hover:bg-slate-800 transition"
            @click="startGame('quiz')"
          >
            Chơi ngay
          </button>
        </div>

        <!-- Word Match Game -->
        <div class="rounded-lg border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition">
          <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-slate-900 mb-2">Ghép từ</h3>
          <p class="text-sm text-slate-600 mb-4">
            Luyện tập từ vựng và kiến thức qua trò chơi ghép từ
          </p>
          <button
            class="w-full rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white hover:bg-slate-800 transition"
            @click="startGame('word-match')"
          >
            Chơi ngay
          </button>
        </div>

        <!-- Puzzle Game -->
        <div class="rounded-lg border border-slate-200 bg-white p-6 shadow-sm hover:shadow-md transition">
          <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
            <svg class="w-6 h-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold text-slate-900 mb-2">Đố vui</h3>
          <p class="text-sm text-slate-600 mb-4">
            Giải đố và thử thách bản thân với các câu hỏi khó
          </p>
          <button
            class="w-full rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white hover:bg-slate-800 transition"
            @click="startGame('puzzle')"
          >
            Chơi ngay
          </button>
        </div>
      </div>

      <!-- Coming Soon -->
      <div class="mt-12 rounded-lg border border-slate-200 bg-white p-8 text-center">
        <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-slate-900 mb-2">Sắp có thêm nhiều trò chơi mới</h3>
        <p class="text-sm text-slate-600">
          Chúng tôi đang phát triển thêm nhiều trò chơi giáo dục thú vị. Hãy quay lại sau nhé!
        </p>
      </div>
    </div>

    <!-- Game Modal -->
    <div
      v-if="activeGame"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
    >
      <div class="w-full max-w-3xl rounded-lg bg-white p-6 shadow-lg">
        <!-- Quiz Game -->
        <div v-if="activeGame === 'quiz' && questions.length">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-semibold text-slate-900">Trắc nghiệm nhanh</h2>
            <div class="flex items-center gap-4">
              <div class="text-sm text-slate-600">
                <span class="font-semibold">Điểm:</span> {{ gameScore }}
              </div>
              <div class="text-sm text-slate-600">
                <span class="font-semibold">Thời gian:</span> {{ gameTime }}s
              </div>
              <button
                class="rounded-lg border border-slate-300 px-3 py-1.5 text-sm hover:bg-slate-50 transition"
                @click="stopGame"
              >
                Thoát
              </button>
            </div>
          </div>

          <div class="mb-4">
            <div class="mb-2 text-sm text-slate-600">
              Câu {{ currentQuestion + 1 }}/{{ questions.length }}
            </div>
            <div class="h-2 overflow-hidden rounded-full bg-slate-200">
              <div
                class="h-full bg-blue-600 transition-all"
                :style="{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }"
              ></div>
            </div>
          </div>

          <div class="space-y-4">
            <h3 class="text-lg font-semibold text-slate-900">
              {{ questions[currentQuestion].question }}
            </h3>
            <div class="grid grid-cols-2 gap-3">
              <button
                v-for="(option, idx) in questions[currentQuestion].options"
                :key="idx"
                class="rounded-lg border border-slate-300 bg-white p-4 text-left font-medium transition hover:border-blue-500 hover:bg-blue-50"
                @click="answerQuiz(idx)"
              >
                {{ option }}
              </button>
            </div>
          </div>
        </div>

        <!-- Word Match Game -->
        <div v-else-if="activeGame === 'word-match'">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-semibold text-slate-900">Ghép từ</h2>
            <div class="flex items-center gap-4">
              <div class="text-sm text-slate-600">
                <span class="font-semibold">Điểm:</span> {{ gameScore }}
              </div>
              <div class="text-sm text-slate-600">
                <span class="font-semibold">Đã ghép:</span> {{ Object.keys(matchedPairs).length }}/{{ wordPairs.length }}
              </div>
              <button
                class="rounded-lg border border-slate-300 px-3 py-1.5 text-sm hover:bg-slate-50 transition"
                @click="stopGame"
              >
                Thoát
              </button>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-6">
            <div>
              <h3 class="mb-3 font-semibold text-slate-900">Tiếng Việt</h3>
              <div class="space-y-2">
                <button
                  v-for="pair in wordPairs"
                  :key="pair.left"
                  class="w-full rounded-lg border-2 p-3 text-left font-medium transition"
                  :class="
                    matchedPairs[`${pair.left}-${pair.right}`]
                      ? 'border-green-500 bg-green-50 opacity-50'
                      : selectedLeft === pair.left
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-slate-300 bg-white hover:border-slate-400'
                  "
                  :disabled="!!matchedPairs[`${pair.left}-${pair.right}`]"
                  @click="selectWord('left', pair.left)"
                >
                  {{ pair.left }}
                </button>
              </div>
            </div>
            <div>
              <h3 class="mb-3 font-semibold text-slate-900">Tiếng Anh</h3>
              <div class="space-y-2">
                <button
                  v-for="pair in wordPairs"
                  :key="pair.right"
                  class="w-full rounded-lg border-2 p-3 text-left font-medium transition"
                  :class="
                    matchedPairs[`${pair.left}-${pair.right}`]
                      ? 'border-green-500 bg-green-50 opacity-50'
                      : selectedRight === pair.right
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-slate-300 bg-white hover:border-slate-400'
                  "
                  :disabled="!!matchedPairs[`${pair.left}-${pair.right}`]"
                  @click="selectWord('right', pair.right)"
                >
                  {{ pair.right }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Puzzle Game -->
        <div v-else-if="activeGame === 'puzzle'">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-xl font-semibold text-slate-900">Đố vui</h2>
            <button
              class="rounded-lg border border-slate-300 px-3 py-1.5 text-sm hover:bg-slate-50 transition"
              @click="stopGame"
            >
              Thoát
            </button>
          </div>
          <div class="text-center py-8">
            <p class="text-slate-600">Trò chơi đang được phát triển...</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { showToast } from '@/utils/toast'

const activeGame = ref<string | null>(null)
const gameScore = ref(0)
const gameTime = ref(0)
const currentQuestion = ref(0)
const questions = ref<any[]>([])

// Quiz Game
const quizQuestions = ref([
  {
    id: 1,
    question: '2 + 2 = ?',
    options: ['3', '4', '5', '6'],
    correct: 1,
  },
  {
    id: 2,
    question: 'Thủ đô của Việt Nam là?',
    options: ['Hà Nội', 'Hồ Chí Minh', 'Đà Nẵng', 'Huế'],
    correct: 0,
  },
  {
    id: 3,
    question: 'Từ nào viết đúng chính tả?',
    options: ['giải thưởng', 'dải thưởng', 'rải thưởng', 'gải thưởng'],
    correct: 0,
  },
])

// Word Match Game
const wordPairs = ref([
  { left: 'Mèo', right: 'Cat' },
  { left: 'Chó', right: 'Dog' },
  { left: 'Nhà', right: 'House' },
  { left: 'Trường', right: 'School' },
])

const selectedLeft = ref<string | null>(null)
const selectedRight = ref<string | null>(null)
const matchedPairs = ref<Record<string, boolean>>({})

function startGame(type: string) {
  activeGame.value = type
  gameScore.value = 0
  gameTime.value = 0
  currentQuestion.value = 0
  matchedPairs.value = {}
  selectedLeft.value = null
  selectedRight.value = null

  if (type === 'quiz') {
    questions.value = [...quizQuestions.value]
  }

  // Start timer
  const timer = setInterval(() => {
    gameTime.value++
  }, 1000)

  // Store timer to clear later
  ;(window as any).gameTimer = timer
}

function stopGame() {
  activeGame.value = null
  if ((window as any).gameTimer) {
    clearInterval((window as any).gameTimer)
  }
}

function answerQuiz(optionIndex: number) {
  const q = questions.value[currentQuestion.value]
  if (optionIndex === q.correct) {
    gameScore.value += 10
  }
  if (currentQuestion.value < questions.value.length - 1) {
    currentQuestion.value++
  } else {
    finishGame()
  }
}

function selectWord(side: 'left' | 'right', word: string) {
  if (side === 'left') {
    selectedLeft.value = word
  } else {
    selectedRight.value = word
  }

  if (selectedLeft.value && selectedRight.value) {
    const pair = wordPairs.value.find(
      (p) => p.left === selectedLeft.value && p.right === selectedRight.value,
    )
    if (pair) {
      const key = `${pair.left}-${pair.right}`
      matchedPairs.value[key] = true
      gameScore.value += 20
      selectedLeft.value = null
      selectedRight.value = null

      if (Object.keys(matchedPairs.value).length === wordPairs.value.length) {
        finishGame()
      }
    } else {
      setTimeout(() => {
        selectedLeft.value = null
        selectedRight.value = null
      }, 500)
    }
  }
}

function finishGame() {
  setTimeout(() => {
    showToast(`Chúc mừng! Bạn đạt ${gameScore.value} điểm trong ${gameTime.value} giây!`, 'success')
    stopGame()
  }, 500)
}
</script>
