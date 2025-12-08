<template>
  <div class="min-h-screen bg-slate-50 pb-14 pt-8">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-6">
        <h1 class="text-3xl font-bold text-slate-900">Trò chơi giáo dục</h1>
        <p class="text-sm text-slate-600">Học mà chơi, chơi mà học</p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="grid gap-6 sm:grid-cols-3">
        <div v-for="i in 3" :key="i" class="h-64 animate-pulse rounded-2xl border border-slate-200 bg-white"></div>
      </div>

      <!-- Main View: 3 Game Categories -->
      <div v-else-if="!selectedCategory">
        <div class="grid gap-6 sm:grid-cols-3">
          <!-- Trắc nghiệm nhanh -->
          <div class="flex flex-col rounded-2xl border border-slate-200 bg-white p-6">
            <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-sky-100">
              <svg class="h-6 w-6 text-sky-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 class="mb-2 text-lg font-bold text-slate-900">Trắc nghiệm nhanh</h3>
            <p class="mb-4 flex-1 text-sm text-slate-600">Thử thách kiến thức của bạn với các câu hỏi trắc nghiệm vui nhộn</p>
            <button
              class="w-full rounded-xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
              @click="openCategory('quiz')"
            >
              Chơi ngay
            </button>
          </div>

          <!-- Ghép từ -->
          <div class="flex flex-col rounded-2xl border border-slate-200 bg-white p-6">
            <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-amber-100">
              <svg class="h-6 w-6 text-amber-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <h3 class="mb-2 text-lg font-bold text-slate-900">Ghép từ</h3>
            <p class="mb-4 flex-1 text-sm text-slate-600">Luyện tập từ vựng và kiến thức qua trò chơi ghép từ</p>
            <button
              class="w-full rounded-xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
              @click="openCategory('word_match')"
            >
              Chơi ngay
            </button>
          </div>

          <!-- Đố vui -->
          <div class="flex flex-col rounded-2xl border border-slate-200 bg-white p-6">
            <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-violet-100">
              <svg class="h-6 w-6 text-violet-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="mb-2 text-lg font-bold text-slate-900">Đố vui</h3>
            <p class="mb-4 flex-1 text-sm text-slate-600">Giải đố và thử thách bản thân với các câu hỏi khó</p>
            <button
              class="w-full rounded-xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
              @click="openCategory('puzzle')"
            >
              Chơi ngay
            </button>
          </div>
        </div>

        <!-- Coming Soon -->
        <div class="mt-10 rounded-2xl border border-slate-200 bg-white p-8 text-center">
          <div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-slate-100">
            <svg class="h-6 w-6 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="mb-1 text-lg font-semibold text-slate-900">Sắp có thêm nhiều trò chơi mới</h3>
          <p class="text-sm text-slate-600">
            Chúng tôi đang phát triển thêm nhiều trò chơi giáo dục thú vị. Hãy quay lại sau nhé!
          </p>
        </div>
      </div>

      <!-- Category View: List of games -->
      <div v-else>
        <!-- Back button -->
        <button
          class="mb-6 flex items-center gap-2 text-sm font-semibold text-slate-600 hover:text-slate-900"
          @click="selectedCategory = null"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Quay lại
        </button>

        <h2 class="mb-6 text-xl font-bold text-slate-900">{{ getCategoryTitle(selectedCategory) }}</h2>

        <!-- Games Grid -->
        <div v-if="filteredGames.length" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <div
            v-for="game in filteredGames"
            :key="game.id"
            class="group cursor-pointer rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition-all hover:-translate-y-1 hover:shadow-md"
            @click="openGame(game)"
          >
            <div class="mb-4 flex items-start justify-end">
              <span
                class="rounded-full px-2 py-1 text-xs font-semibold"
                :class="getDifficultyClass(game.difficulty)"
              >
                {{ game.difficulty_display || game.difficulty }}
              </span>
            </div>
            
            <h3 class="mb-1 text-lg font-semibold text-slate-900 group-hover:text-slate-700 transition">{{ game.title }}</h3>
            <p class="mb-3 text-sm text-slate-600 line-clamp-2">{{ game.description || 'Thử thách kiến thức của bạn!' }}</p>
            
            <div class="mb-4 flex items-center justify-between text-xs text-slate-500">
              <span>{{ game.question_count }} câu hỏi</span>
              <span>{{ game.play_count }} lượt chơi</span>
            </div>
            
            <!-- User Stats -->
            <div v-if="game.user_best_score" class="mb-4 rounded-lg border border-amber-100 bg-amber-50 p-3">
              <div class="flex items-center justify-between text-sm">
                <span class="text-amber-700">Điểm cao nhất</span>
                <span class="font-bold text-amber-800">{{ game.user_best_score }}</span>
              </div>
            </div>
            
            <button
              class="w-full rounded-lg bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
            >
              Chơi ngay
            </button>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="py-16 text-center">
          <div class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-slate-100">
            <svg class="h-8 w-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M12 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h3 class="mb-2 text-lg font-semibold text-slate-900">Chưa có trò chơi nào</h3>
          <p class="text-sm text-slate-600">Thể loại này chưa có trò chơi. Hãy quay lại sau nhé!</p>
        </div>
      </div>
    </div>

    <!-- Game Modal -->
    <Teleport to="body">
      <div
        v-if="activeGame"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4"
      >
        <div class="w-full max-w-3xl overflow-y-auto rounded-2xl bg-white shadow-2xl max-h-[90vh]">
          <!-- Game Header -->
          <div class="sticky top-0 flex items-center justify-between border-b border-slate-200 bg-white p-4">
            <div class="flex items-center gap-3">
              <div>
                <h2 class="text-lg font-bold text-slate-900">{{ currentGameData?.title || 'Trò chơi' }}</h2>
                <p class="text-xs text-slate-500">{{ currentGameData?.game_type_display }}</p>
              </div>
            </div>
            <div class="flex items-center gap-4">
              <div class="text-center">
                <div class="text-2xl font-bold text-slate-900">{{ gameScore }}</div>
                <div class="text-xs text-slate-500">Điểm</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-slate-700">{{ gameTime }}s</div>
                <div class="text-xs text-slate-500">Thời gian</div>
              </div>
            </div>
            <button
              class="rounded-xl border border-slate-300 px-4 py-2 text-sm font-semibold transition hover:bg-slate-50"
              @click="stopGame"
            >
              ✕ Thoát
            </button>
          </div>

          <!-- Quiz Game -->
          <div v-if="activeGame === 'quiz' && questions.length" class="p-6">
            <div class="mb-6">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-semibold text-slate-600">Câu {{ currentQuestion + 1 }}/{{ questions.length }}</span>
                <span class="text-sm text-slate-500">{{ Math.round(((currentQuestion + 1) / questions.length) * 100) }}%</span>
              </div>
              <div class="h-3 overflow-hidden rounded-full bg-slate-100">
                <div
                  class="h-full bg-slate-900 transition-all duration-300"
                  :style="{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }"
                ></div>
              </div>
            </div>

            <div class="mb-6 rounded-2xl border border-slate-200 bg-slate-50 p-6">
              <h3 class="text-xl font-bold text-slate-900">
                {{ questions[currentQuestion].question }}
              </h3>
            </div>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <button
                v-for="(option, idx) in questions[currentQuestion].options"
                :key="idx"
                class="rounded-xl border-2 bg-white p-4 text-left font-medium transition-all hover:border-slate-300 hover:bg-slate-50 hover:shadow-sm"
                :class="selectedAnswer === idx ? 'border-slate-900 bg-slate-100' : 'border-slate-200'"
                @click="answerQuiz(idx)"
              >
                <div class="flex items-center gap-3">
                  <div class="flex h-8 w-8 items-center justify-center rounded-lg text-sm font-bold"
                    :class="selectedAnswer === idx ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-700'">
                    {{ String.fromCharCode(65 + idx) }}
                  </div>
                  <span>{{ option }}</span>
                </div>
              </button>
            </div>
          </div>

          <!-- Word Match Game -->
          <div v-else-if="activeGame === 'word-match'" class="p-6">
            <div class="mb-6">
              <div class="flex items-center justify-between mb-2">
                <span class="text-sm font-semibold text-slate-600">Đã ghép {{ Object.keys(matchedPairs).length }}/{{ wordPairs.length }}</span>
              </div>
              <div class="h-3 overflow-hidden rounded-full bg-slate-100">
                <div
                  class="h-full bg-slate-900 transition-all duration-300"
                  :style="{ width: `${(Object.keys(matchedPairs).length / wordPairs.length) * 100}%` }"
                ></div>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-6">
              <div>
                <h3 class="mb-3 font-bold text-slate-900 flex items-center gap-2">🇻🇳 Tiếng Việt</h3>
                <div class="space-y-2">
                  <button
                    v-for="pair in shuffledLeft"
                    :key="pair.left"
                    class="w-full rounded-xl border-2 p-4 text-left font-medium transition-all"
                    :class="getWordButtonClass('left', pair)"
                    :disabled="isWordMatched(pair)"
                    @click="selectWord('left', pair.left)"
                  >
                    {{ pair.left }}
                  </button>
                </div>
              </div>
              <div>
                <h3 class="mb-3 font-bold text-slate-900 flex items-center gap-2">🇬🇧 Tiếng Anh</h3>
                <div class="space-y-2">
                  <button
                    v-for="pair in shuffledRight"
                    :key="pair.right"
                    class="w-full rounded-xl border-2 p-4 text-left font-medium transition-all"
                    :class="getWordButtonClass('right', pair)"
                    :disabled="isWordMatched(pair)"
                    @click="selectWord('right', pair.right)"
                  >
                    {{ pair.right }}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Game Result -->
          <div v-else-if="activeGame === 'result'" class="p-6 text-center">
            <h2 class="mb-2 text-2xl font-bold text-slate-900">Hoàn thành!</h2>
            <p class="mb-6 text-slate-600">{{ currentGameData?.title }}</p>
            
            <div class="mb-6 rounded-2xl border border-slate-200 bg-slate-50 p-6">
              <div class="grid grid-cols-3 gap-4">
                <div>
                  <div class="text-3xl font-bold text-slate-900">{{ gameResult?.score }}</div>
                  <div class="text-sm text-slate-600">Điểm</div>
                </div>
                <div>
                  <div class="text-3xl font-bold text-slate-900">{{ gameResult?.percentage }}%</div>
                  <div class="text-sm text-slate-600">Chính xác</div>
                </div>
                <div>
                  <div class="text-3xl font-bold text-slate-900">{{ gameResult?.time_spent }}s</div>
                  <div class="text-sm text-slate-600">Thời gian</div>
                </div>
              </div>
            </div>
            
            <div v-if="gameResult?.rank" class="mb-6 rounded-xl border border-amber-100 bg-amber-50 p-4">
              <p class="text-amber-800">
                🏅 Xếp hạng <strong>#{{ gameResult.rank }}</strong> trong {{ gameResult.total_players }} người chơi
              </p>
            </div>
            
            <div class="flex gap-3">
              <button
                class="flex-1 rounded-xl border border-slate-200 px-4 py-3 font-semibold text-slate-700 transition hover:bg-slate-50"
                @click="stopGame"
              >
                Đóng
              </button>
              <button
                class="flex-1 rounded-xl bg-slate-900 px-4 py-3 font-bold text-white transition hover:bg-slate-800"
                @click="playAgain"
              >
                Chơi lại
              </button>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { gameService, type Game, type GameResult } from '@/services/game.service'
import { showToast } from '@/utils/toast'

const loading = ref(true)
const games = ref<Game[]>([])
const activeGame = ref<string | null>(null)
const currentGameData = ref<Game | null>(null)
const sessionId = ref<string | null>(null)
const gameScore = ref(0)
const gameTime = ref(0)
const currentQuestion = ref(0)
const questions = ref<any[]>([])
const selectedAnswer = ref<number | null>(null)
const gameResult = ref<GameResult | null>(null)
const gameAnswers = ref<any[]>([])

// Word Match
const wordPairs = ref<any[]>([])
const shuffledLeft = ref<any[]>([])
const shuffledRight = ref<any[]>([])
const selectedLeft = ref<string | null>(null)
const selectedRight = ref<string | null>(null)
const matchedPairs = ref<Record<string, boolean>>({})

// Category selection
const selectedCategory = ref<string | null>(null)

const filteredGames = computed(() => {
  if (!selectedCategory.value) return games.value
  return games.value.filter(g => g.game_type === selectedCategory.value)
})

function openCategory(category: string) {
  selectedCategory.value = category
}

function getCategoryTitle(category: string) {
  const titles: Record<string, string> = {
    quiz: 'Trắc nghiệm nhanh',
    word_match: 'Ghép từ',
    puzzle: 'Đố vui',
  }
  return titles[category] || 'Trò chơi'
}

function getDifficultyClass(difficulty: string) {
  const classes: Record<string, string> = {
    easy: 'bg-green-100 text-green-700',
    medium: 'bg-amber-100 text-amber-700',
    hard: 'bg-red-100 text-red-700',
  }
  return classes[difficulty] || 'bg-slate-100 text-slate-700'
}

async function loadGames() {
  loading.value = true
  try {
    const data = await gameService.list()
    games.value = data.games || []
  } catch (e) {
    console.error('Load games error:', e)
    // Fallback to demo games
    games.value = [
      {
        id: 'demo-quiz',
        title: 'Trắc nghiệm Toán lớp 1',
        description: 'Thử thách kiến thức toán học cơ bản',
        game_type: 'quiz',
        game_type_display: 'Trắc nghiệm nhanh',
        difficulty: 'easy',
        difficulty_display: 'Dễ',
        subject: 'math',
        grade_level: 1,
        question_count: 5,
        play_count: 120,
        questions: [
          { id: 1, question: '2 + 2 = ?', options: ['3', '4', '5', '6'], correct: 1 },
          { id: 2, question: '5 - 3 = ?', options: ['1', '2', '3', '4'], correct: 1 },
          { id: 3, question: '3 + 4 = ?', options: ['6', '7', '8', '9'], correct: 1 },
          { id: 4, question: '10 - 5 = ?', options: ['4', '5', '6', '7'], correct: 1 },
          { id: 5, question: '1 + 1 = ?', options: ['1', '2', '3', '4'], correct: 1 },
        ],
      },
      {
        id: 'demo-word',
        title: 'Ghép từ Tiếng Anh',
        description: 'Luyện từ vựng tiếng Anh cơ bản',
        game_type: 'word_match',
        game_type_display: 'Ghép từ',
        difficulty: 'easy',
        difficulty_display: 'Dễ',
        subject: 'english',
        grade_level: 1,
        question_count: 5,
        play_count: 85,
        questions: [
          { id: 101, question: '', options: [], correct: 0, left: 'Mèo', right: 'Cat' },
          { id: 102, question: '', options: [], correct: 0, left: 'Chó', right: 'Dog' },
          { id: 103, question: '', options: [], correct: 0, left: 'Nhà', right: 'House' },
          { id: 104, question: '', options: [], correct: 0, left: 'Trường', right: 'School' },
          { id: 105, question: '', options: [], correct: 0, left: 'Sách', right: 'Book' },
        ],
      },
      {
        id: 'demo-puzzle',
        title: 'Đố vui Tiếng Việt',
        description: 'Câu đố vui về tiếng Việt',
        game_type: 'puzzle',
        game_type_display: 'Đố vui',
        difficulty: 'medium',
        difficulty_display: 'Trung bình',
        subject: 'vietnamese',
        grade_level: 2,
        question_count: 5,
        play_count: 65,
        questions: [
          { id: 1, question: 'Thủ đô của Việt Nam là?', options: ['Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Huế'], correct: 0 },
          { id: 2, question: 'Từ nào viết đúng chính tả?', options: ['giải thưởng', 'dải thưởng', 'rải thưởng', 'gải thưởng'], correct: 0 },
          { id: 3, question: 'Việt Nam có bao nhiêu tỉnh thành?', options: ['61', '62', '63', '64'], correct: 2 },
        ],
      },
    ]
  } finally {
    loading.value = false
  }
}

async function openGame(game: Game) {
  currentGameData.value = game
  gameScore.value = 0
  gameTime.value = 0
  currentQuestion.value = 0
  selectedAnswer.value = null
  gameResult.value = null
  gameAnswers.value = []
  matchedPairs.value = {}
  selectedLeft.value = null
  selectedRight.value = null
  
  // Load game questions
  if (game.questions) {
    questions.value = [...game.questions]
    
    if (game.game_type === 'word_match') {
      wordPairs.value = [...game.questions]
      shuffledLeft.value = [...game.questions].sort(() => Math.random() - 0.5)
      shuffledRight.value = [...game.questions].sort(() => Math.random() - 0.5)
    }
  }
  
  // Try to start session from API
  try {
    if (!game.id.startsWith('demo-')) {
      const session = await gameService.start(game.id)
      sessionId.value = session.session_id
      if (session.questions) {
        questions.value = session.questions
      }
    }
  } catch (e) {
    console.error('Start session error:', e)
  }
  
  // Set game type
  if (game.game_type === 'word_match') {
    activeGame.value = 'word-match'
  } else {
    activeGame.value = game.game_type || 'quiz'
  }
  
  // Start timer
  const timer = setInterval(() => {
    gameTime.value++
  }, 1000)
  ;(window as any).gameTimer = timer
}

function stopGame() {
  activeGame.value = null
  currentGameData.value = null
  sessionId.value = null
  if ((window as any).gameTimer) {
    clearInterval((window as any).gameTimer)
  }
}

function answerQuiz(optionIndex: number) {
  selectedAnswer.value = optionIndex
  const q = questions.value[currentQuestion.value]
  const isCorrect = optionIndex === q.correct
  
  if (isCorrect) {
    gameScore.value += 10
  }
  
  gameAnswers.value.push({
    question_id: q.id,
    selected: optionIndex,
    correct: q.correct,
    is_correct: isCorrect,
  })
  
  setTimeout(() => {
    selectedAnswer.value = null
    if (currentQuestion.value < questions.value.length - 1) {
      currentQuestion.value++
    } else {
      finishGame()
    }
  }, 300)
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

function isWordMatched(pair: any) {
  return !!matchedPairs.value[`${pair.left}-${pair.right}`]
}

function getWordButtonClass(side: 'left' | 'right', pair: any) {
  const key = `${pair.left}-${pair.right}`
  if (matchedPairs.value[key]) {
    return 'border-emerald-500 bg-emerald-50 text-emerald-800 opacity-70'
  }
  if (side === 'left' && selectedLeft.value === pair.left) {
    return 'border-slate-900 bg-slate-100'
  }
  if (side === 'right' && selectedRight.value === pair.right) {
    return 'border-slate-900 bg-slate-100'
  }
  return 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50'
}

async function finishGame() {
  if ((window as any).gameTimer) {
    clearInterval((window as any).gameTimer)
  }
  
  const maxScore = questions.value.length * 10
  const percentage = Math.round((gameScore.value / maxScore) * 100)
  
  // Submit to API
  try {
    if (currentGameData.value && !currentGameData.value.id.startsWith('demo-')) {
      const result = await gameService.submit(currentGameData.value.id, {
        session_id: sessionId.value || undefined,
        score: gameScore.value,
        time_spent: gameTime.value,
        answers: gameAnswers.value,
      })
      gameResult.value = result
    } else {
      gameResult.value = {
        session_id: 'demo',
        score: gameScore.value,
        max_score: maxScore,
        time_spent: gameTime.value,
        percentage,
        rank: 1,
        total_players: 1,
      }
    }
  } catch (e) {
    console.error('Submit error:', e)
    gameResult.value = {
      session_id: 'local',
      score: gameScore.value,
      max_score: maxScore,
      time_spent: gameTime.value,
      percentage,
      rank: 0,
      total_players: 0,
    }
  }
  
  activeGame.value = 'result'
  showToast(`Chúc mừng! Bạn đạt ${gameScore.value} điểm!`, 'success')
}

function playAgain() {
  if (currentGameData.value) {
    openGame(currentGameData.value)
  }
}

onMounted(() => {
  loadGames()
})
</script>
