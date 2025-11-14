<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
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
    alert(`Chúc mừng! Bạn đạt ${gameScore.value} điểm trong ${gameTime.value} giây!`)
    stopGame()
  }, 500)
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-cyan-50/30 to-slate-50">
    <!-- Game Modal -->
    <div
      v-if="activeGame"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4"
    >
      <div class="w-full max-w-4xl rounded-3xl bg-white p-6">
        <!-- Quiz Game -->
        <div v-if="activeGame === 'quiz' && questions.length">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-2xl font-bold">Trắc nghiệm nhanh</h2>
            <div class="flex items-center gap-4">
              <div class="text-sm">
                <span class="font-semibold">Điểm:</span> {{ gameScore }}
              </div>
              <div class="text-sm">
                <span class="font-semibold">Thời gian:</span> {{ gameTime }}s
              </div>
              <button
                class="rounded-lg border px-3 py-1 text-sm hover:bg-slate-50"
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
                class="h-full bg-cyan-500 transition-all"
                :style="{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }"
              ></div>
            </div>
          </div>

          <div class="space-y-4">
            <h3 class="text-xl font-semibold">
              {{ questions[currentQuestion].question }}
            </h3>
            <div class="grid grid-cols-2 gap-3">
              <button
                v-for="(option, idx) in questions[currentQuestion].options"
                :key="idx"
                class="rounded-xl border-2 border-slate-200 bg-white p-4 text-left font-semibold transition hover:border-cyan-500 hover:bg-cyan-50"
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
            <h2 class="text-2xl font-bold">Ghép từ</h2>
            <div class="flex items-center gap-4">
              <div class="text-sm">
                <span class="font-semibold">Điểm:</span> {{ gameScore }}
              </div>
              <div class="text-sm">
                <span class="font-semibold">Đã ghép:</span> {{ Object.keys(matchedPairs).length }}/{{ wordPairs.length }}
              </div>
              <button
                class="rounded-lg border px-3 py-1 text-sm hover:bg-slate-50"
                @click="stopGame"
              >
                Thoát
              </button>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-6">
            <div>
              <h3 class="mb-3 font-semibold">Tiếng Việt</h3>
              <div class="space-y-2">
                <button
                  v-for="pair in wordPairs"
                  :key="pair.left"
                  class="w-full rounded-xl border-2 p-3 text-left font-semibold transition"
                  :class="
                    matchedPairs[`${pair.left}-${pair.right}`]
                      ? 'border-emerald-500 bg-emerald-50 opacity-50'
                      : selectedLeft === pair.left
                        ? 'border-cyan-500 bg-cyan-50'
                        : 'border-slate-200 bg-white hover:border-slate-300'
                  "
                  :disabled="!!matchedPairs[`${pair.left}-${pair.right}`]"
                  @click="selectWord('left', pair.left)"
                >
                  {{ pair.left }}
                </button>
              </div>
            </div>
            <div>
              <h3 class="mb-3 font-semibold">Tiếng Anh</h3>
              <div class="space-y-2">
                <button
                  v-for="pair in wordPairs"
                  :key="pair.right"
                  class="w-full rounded-xl border-2 p-3 text-left font-semibold transition"
                  :class="
                    matchedPairs[`${pair.left}-${pair.right}`]
                      ? 'border-emerald-500 bg-emerald-50 opacity-50'
                      : selectedRight === pair.right
                        ? 'border-cyan-500 bg-cyan-50'
                        : 'border-slate-200 bg-white hover:border-slate-300'
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
            <h2 class="text-2xl font-bold">Đố vui</h2>
            <button
              class="rounded-lg border px-3 py-1 text-sm hover:bg-slate-50"
              @click="stopGame"
            >
              Thoát
            </button>
          </div>
          <div class="text-center">
            <p class="text-slate-600">Trò chơi đang được phát triển...</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 pb-20">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center gap-3 mb-3">
          <div
            class="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-500 to-cyan-600 shadow-lg shadow-cyan-500/30"
          >
            <svg class="h-7 w-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <div>
            <h1 class="text-3xl font-black text-slate-900 sm:text-4xl">Trò chơi giáo dục</h1>
            <p class="mt-1 text-sm text-slate-600">Học mà chơi, chơi mà học</p>
          </div>
        </div>
      </div>

      <!-- Game Grid -->
      <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <!-- Game Card 1 -->
        <div
          class="group relative overflow-hidden rounded-3xl border border-slate-200/80 bg-white/95 p-6 shadow-xl shadow-slate-100 transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl hover:shadow-cyan-500/20"
        >
          <div
            class="absolute -right-8 -top-8 h-32 w-32 rounded-full bg-gradient-to-br from-cyan-400/20 to-sky-400/20 blur-2xl transition-all duration-500 group-hover:scale-150"
          ></div>
          <div class="relative">
            <div
              class="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-cyan-500 to-cyan-600 shadow-lg shadow-cyan-500/30"
            >
              <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900">Trắc nghiệm nhanh</h3>
            <p class="mt-2 text-sm text-slate-600">
              Thử thách kiến thức của bạn với các câu hỏi trắc nghiệm vui nhộn
            </p>
            <button
              class="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-2xl border border-transparent bg-gradient-to-r from-cyan-500 to-cyan-600 px-4 py-3 text-sm font-bold text-white shadow-lg shadow-cyan-500/30 transition-all duration-300 hover:shadow-xl hover:shadow-cyan-500/40"
              @click="startGame('quiz')"
            >
              <span>Chơi ngay</span>
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M14 5l7 7m0 0l-7 7m7-7H3"
                />
              </svg>
            </button>
          </div>
        </div>

        <!-- Game Card 2 -->
        <div
          class="group relative overflow-hidden rounded-3xl border border-slate-200/80 bg-white/95 p-6 shadow-xl shadow-slate-100 transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl hover:shadow-sky-500/20"
        >
          <div
            class="absolute -right-8 -top-8 h-32 w-32 rounded-full bg-gradient-to-br from-sky-400/20 to-blue-400/20 blur-2xl transition-all duration-500 group-hover:scale-150"
          ></div>
          <div class="relative">
            <div
              class="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-sky-500 to-sky-600 shadow-lg shadow-sky-500/30"
            >
              <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900">Ghép từ</h3>
            <p class="mt-2 text-sm text-slate-600">
              Luyện tập từ vựng và kiến thức qua trò chơi ghép từ
            </p>
            <button
              class="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-2xl border border-transparent bg-gradient-to-r from-sky-500 to-sky-600 px-4 py-3 text-sm font-bold text-white shadow-lg shadow-sky-500/30 transition-all duration-300 hover:shadow-xl hover:shadow-sky-500/40"
              @click="startGame('word-match')"
            >
              <span>Chơi ngay</span>
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M14 5l7 7m0 0l-7 7m7-7H3"
                />
              </svg>
            </button>
          </div>
        </div>

        <!-- Game Card 3 -->
        <div
          class="group relative overflow-hidden rounded-3xl border border-slate-200/80 bg-white/95 p-6 shadow-xl shadow-slate-100 transition-all duration-300 hover:scale-[1.02] hover:shadow-2xl hover:shadow-blue-500/20"
        >
          <div
            class="absolute -right-8 -top-8 h-32 w-32 rounded-full bg-gradient-to-br from-blue-400/20 to-indigo-400/20 blur-2xl transition-all duration-500 group-hover:scale-150"
          ></div>
          <div class="relative">
            <div
              class="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-blue-600 shadow-lg shadow-blue-500/30"
            >
              <svg class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <h3 class="text-xl font-bold text-slate-900">Đố vui</h3>
            <p class="mt-2 text-sm text-slate-600">
              Giải đố và thử thách bản thân với các câu hỏi khó
            </p>
            <button
              class="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-2xl border border-transparent bg-gradient-to-r from-blue-500 to-blue-600 px-4 py-3 text-sm font-bold text-white shadow-lg shadow-blue-500/30 transition-all duration-300 hover:shadow-xl hover:shadow-blue-500/40"
              @click="startGame('puzzle')"
            >
              <span>Chơi ngay</span>
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M14 5l7 7m0 0l-7 7m7-7H3"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Coming Soon Section -->
      <div class="mt-12">
        <div
          class="rounded-3xl border border-slate-200/80 bg-white/95 p-8 text-center shadow-xl shadow-slate-100"
        >
          <div class="mx-auto mb-4 flex h-20 w-20 items-center justify-center">
            <svg
              class="h-20 w-20 text-slate-300"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <h3 class="text-2xl font-bold text-slate-900">Sắp có thêm nhiều trò chơi mới</h3>
          <p class="mt-2 text-slate-600">
            Chúng tôi đang phát triển thêm nhiều trò chơi giáo dục thú vị. Hãy quay lại sau nhé!
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
