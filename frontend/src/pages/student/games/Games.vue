<template>
  <div class="page-wrapper" :class="isDark ? 'dark-mode' : 'light-mode'">
    <div v-if="isDark" class="bg-elements">
      <div class="glow glow-1"></div>
      <div class="glow glow-2"></div>
    </div>

    <div class="page-content">
      <!-- Header -->
      <div class="page-header">
        <h1>Trò chơi giáo dục</h1>
        <p>Học mà chơi, chơi mà học</p>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="games-grid">
        <div v-for="i in 3" :key="i" class="skeleton-card"></div>
      </div>

      <!-- Main View: 3 Game Categories -->
      <div v-else-if="!selectedCategory">
        <div class="games-grid">
          <!-- Trắc nghiệm nhanh -->
          <div class="game-category-card">
            <div class="category-icon blue">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3>Trắc nghiệm nhanh</h3>
            <p>Thử thách kiến thức của bạn với các câu hỏi trắc nghiệm vui nhộn</p>
            <button class="play-btn" @click="openCategory('quiz')">Chơi ngay</button>
          </div>

          <!-- Ghép từ -->
          <div class="game-category-card">
            <div class="category-icon amber">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <h3>Ghép từ</h3>
            <p>Luyện tập từ vựng và kiến thức qua trò chơi ghép từ</p>
            <button class="play-btn" @click="openCategory('word_match')">Chơi ngay</button>
          </div>

          <!-- Đố vui -->
          <div class="game-category-card">
            <div class="category-icon violet">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3>Đố vui</h3>
            <p>Giải đố và thử thách bản thân với các câu hỏi khó</p>
            <button class="play-btn" @click="openCategory('puzzle')">Chơi ngay</button>
          </div>
        </div>

        <!-- Coming Soon -->
        <div class="coming-soon">
          <div class="coming-icon">⏰</div>
          <h3>Sắp có thêm nhiều trò chơi mới</h3>
          <p>Chúng tôi đang phát triển thêm nhiều trò chơi giáo dục thú vị. Hãy quay lại sau nhé!</p>
        </div>
      </div>

      <!-- Category View -->
      <div v-else>
        <button class="back-btn" @click="selectedCategory = null">
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
          Quay lại
        </button>

        <h2 class="category-title">{{ getCategoryTitle(selectedCategory) }}</h2>

        <div v-if="filteredGames.length" class="games-list">
          <div v-for="game in filteredGames" :key="game.id" class="game-card" @click="openGame(game)">
            <div class="game-header">
              <span class="difficulty-badge" :class="game.difficulty">{{ game.difficulty_display || game.difficulty }}</span>
            </div>
            <h3>{{ game.title }}</h3>
            <p>{{ game.description || 'Thử thách kiến thức của bạn!' }}</p>
            <div class="game-stats">
              <span>{{ game.question_count }} câu hỏi</span>
              <span>{{ game.play_count }} lượt chơi</span>
            </div>
            <div v-if="game.user_best_score" class="best-score">
              <span>Điểm cao nhất</span>
              <strong>{{ game.user_best_score }}</strong>
            </div>
            <button class="play-btn">Chơi ngay</button>
          </div>
        </div>

        <div v-else class="empty-state">
          <div class="empty-icon">🎮</div>
          <h3>Chưa có trò chơi nào</h3>
          <p>Thể loại này chưa có trò chơi. Hãy quay lại sau nhé!</p>
        </div>
      </div>
    </div>

    <!-- Game Modal -->
    <Teleport to="body">
      <div v-if="activeGame" class="game-modal-overlay" @click.self="stopGame">
        <div class="game-modal" :class="isDark ? 'dark-mode' : 'light-mode'">
          <div class="modal-header">
            <div>
              <h2>{{ currentGameData?.title || 'Trò chơi' }}</h2>
              <p>{{ currentGameData?.game_type_display }}</p>
            </div>
            <div class="modal-stats">
              <div class="stat-item"><div class="stat-value">{{ gameScore }}</div><div class="stat-label">Điểm</div></div>
              <div class="stat-item"><div class="stat-value">{{ gameTime }}s</div><div class="stat-label">Thời gian</div></div>
            </div>
            <button class="close-btn" @click="stopGame">✕ Thoát</button>
          </div>

          <!-- Quiz Game -->
          <div v-if="activeGame === 'quiz' && questions.length" class="modal-body">
            <div class="progress-section">
              <span>Câu {{ currentQuestion + 1 }}/{{ questions.length }}</span>
              <div class="progress-bar"><div class="progress-fill" :style="{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }"></div></div>
            </div>
            <div class="question-box"><h3>{{ questions[currentQuestion].question }}</h3></div>
            <div class="options-grid">
              <button v-for="(option, idx) in questions[currentQuestion].options" :key="idx"
                class="option-btn" :class="{ selected: selectedAnswer === idx }" @click="answerQuiz(Number(idx))">
                <div class="option-letter">{{ String.fromCharCode(65 + Number(idx)) }}</div>
                <span>{{ option }}</span>
              </button>
            </div>
          </div>

          <!-- Word Match Game -->
          <div v-else-if="activeGame === 'word-match'" class="modal-body">
            <div class="progress-section">
              <span>Đã ghép {{ Object.keys(matchedPairs).length }}/{{ wordPairs.length }}</span>
              <div class="progress-bar"><div class="progress-fill" :style="{ width: `${(Object.keys(matchedPairs).length / wordPairs.length) * 100}%` }"></div></div>
            </div>
            <div class="word-match-grid">
              <div class="word-column">
                <h4>🇻🇳 Tiếng Việt</h4>
                <button v-for="pair in shuffledLeft" :key="pair.left" class="word-btn" :class="getWordButtonClass('left', pair)"
                  :disabled="isWordMatched(pair)" @click="selectWord('left', pair.left)">{{ pair.left }}</button>
              </div>
              <div class="word-column">
                <h4>🇬🇧 Tiếng Anh</h4>
                <button v-for="pair in shuffledRight" :key="pair.right" class="word-btn" :class="getWordButtonClass('right', pair)"
                  :disabled="isWordMatched(pair)" @click="selectWord('right', pair.right)">{{ pair.right }}</button>
              </div>
            </div>
          </div>

          <!-- Game Result -->
          <div v-else-if="activeGame === 'result'" class="modal-body result-view">
            <h2>Hoàn thành!</h2>
            <p>{{ currentGameData?.title }}</p>
            <div class="result-stats">
              <div><div class="big-num">{{ gameResult?.score }}</div><div>Điểm</div></div>
              <div><div class="big-num">{{ gameResult?.percentage }}%</div><div>Chính xác</div></div>
              <div><div class="big-num">{{ gameResult?.time_spent }}s</div><div>Thời gian</div></div>
            </div>
            <div v-if="gameResult?.rank" class="rank-info">🏅 Xếp hạng <strong>#{{ gameResult.rank }}</strong> trong {{ gameResult.total_players }} người chơi</div>
            <div class="result-actions">
              <button class="btn-outline" @click="stopGame">Đóng</button>
              <button class="btn-primary" @click="playAgain">Chơi lại</button>
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
import { useThemeStore } from '@/store/theme.store'

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

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

const wordPairs = ref<any[]>([])
const shuffledLeft = ref<any[]>([])
const shuffledRight = ref<any[]>([])
const selectedLeft = ref<string | null>(null)
const selectedRight = ref<string | null>(null)
const matchedPairs = ref<Record<string, boolean>>({})

const selectedCategory = ref<string | null>(null)
const filteredGames = computed(() => selectedCategory.value ? games.value.filter(g => g.game_type === selectedCategory.value) : games.value)

function openCategory(category: string) { selectedCategory.value = category }
function getCategoryTitle(category: string) { return { quiz: 'Trắc nghiệm nhanh', word_match: 'Ghép từ', puzzle: 'Đố vui' }[category] || 'Trò chơi' }

async function loadGames() {
  loading.value = true
  try {
    const data = await gameService.list()
    games.value = data.games || []
  } catch {
    games.value = [
      { id: 'demo-quiz', title: 'Trắc nghiệm Toán lớp 1', description: 'Thử thách kiến thức toán học cơ bản', game_type: 'quiz', game_type_display: 'Trắc nghiệm nhanh', difficulty: 'easy', difficulty_display: 'Dễ', subject: 'math', grade_level: 1, question_count: 5, play_count: 120,
        questions: [{ id: 1, question: '2 + 2 = ?', options: ['3', '4', '5', '6'], correct: 1 }, { id: 2, question: '5 - 3 = ?', options: ['1', '2', '3', '4'], correct: 1 }, { id: 3, question: '3 + 4 = ?', options: ['6', '7', '8', '9'], correct: 1 }] },
      { id: 'demo-word', title: 'Ghép từ Tiếng Anh', description: 'Luyện từ vựng tiếng Anh cơ bản', game_type: 'word_match', game_type_display: 'Ghép từ', difficulty: 'easy', difficulty_display: 'Dễ', subject: 'english', grade_level: 1, question_count: 5, play_count: 85,
        questions: [{ id: 101, question: '', options: [], correct: 0, left: 'Mèo', right: 'Cat' }, { id: 102, question: '', options: [], correct: 0, left: 'Chó', right: 'Dog' }, { id: 103, question: '', options: [], correct: 0, left: 'Nhà', right: 'House' }] },
      { id: 'demo-puzzle', title: 'Đố vui Tiếng Việt', description: 'Câu đố vui về tiếng Việt', game_type: 'puzzle', game_type_display: 'Đố vui', difficulty: 'medium', difficulty_display: 'Trung bình', subject: 'vietnamese', grade_level: 2, question_count: 3, play_count: 65,
        questions: [{ id: 1, question: 'Thủ đô của Việt Nam là?', options: ['Hà Nội', 'TP.HCM', 'Đà Nẵng', 'Huế'], correct: 0 }] }
    ]
  } finally { loading.value = false }
}

async function openGame(game: Game) {
  currentGameData.value = game; gameScore.value = 0; gameTime.value = 0; currentQuestion.value = 0
  selectedAnswer.value = null; gameResult.value = null; gameAnswers.value = []; matchedPairs.value = {}
  selectedLeft.value = null; selectedRight.value = null
  if (game.questions) {
    questions.value = [...game.questions]
    if (game.game_type === 'word_match') {
      wordPairs.value = [...game.questions]
      shuffledLeft.value = [...game.questions].sort(() => Math.random() - 0.5)
      shuffledRight.value = [...game.questions].sort(() => Math.random() - 0.5)
    }
  }
  try { if (!game.id.startsWith('demo-')) { const session = await gameService.start(game.id); sessionId.value = session.session_id; if (session.questions) questions.value = session.questions } } catch {}
  activeGame.value = game.game_type === 'word_match' ? 'word-match' : (game.game_type || 'quiz')
  const timer = setInterval(() => { gameTime.value++ }, 1000); (window as any).gameTimer = timer
}

function stopGame() { activeGame.value = null; currentGameData.value = null; sessionId.value = null; if ((window as any).gameTimer) clearInterval((window as any).gameTimer) }

function answerQuiz(optionIndex: number) {
  selectedAnswer.value = optionIndex
  const q = questions.value[currentQuestion.value]
  const isCorrect = optionIndex === q.correct
  if (isCorrect) gameScore.value += 10
  gameAnswers.value.push({ question_id: q.id, selected: optionIndex, correct: q.correct, is_correct: isCorrect })
  setTimeout(() => { selectedAnswer.value = null; if (currentQuestion.value < questions.value.length - 1) currentQuestion.value++; else finishGame() }, 300)
}

function selectWord(side: 'left' | 'right', word: string) {
  if (side === 'left') selectedLeft.value = word; else selectedRight.value = word
  if (selectedLeft.value && selectedRight.value) {
    const pair = wordPairs.value.find(p => p.left === selectedLeft.value && p.right === selectedRight.value)
    if (pair) { matchedPairs.value[`${pair.left}-${pair.right}`] = true; gameScore.value += 20; selectedLeft.value = null; selectedRight.value = null
      if (Object.keys(matchedPairs.value).length === wordPairs.value.length) finishGame()
    } else { setTimeout(() => { selectedLeft.value = null; selectedRight.value = null }, 500) }
  }
}

function isWordMatched(pair: any) { return !!matchedPairs.value[`${pair.left}-${pair.right}`] }
function getWordButtonClass(side: 'left' | 'right', pair: any) {
  if (matchedPairs.value[`${pair.left}-${pair.right}`]) return 'matched'
  if (side === 'left' && selectedLeft.value === pair.left) return 'selected'
  if (side === 'right' && selectedRight.value === pair.right) return 'selected'
  return ''
}

async function finishGame() {
  if ((window as any).gameTimer) clearInterval((window as any).gameTimer)
  const maxScore = questions.value.length * 10, percentage = Math.round((gameScore.value / maxScore) * 100)
  try {
    if (currentGameData.value && !currentGameData.value.id.startsWith('demo-')) {
      gameResult.value = await gameService.submit(currentGameData.value.id, { session_id: sessionId.value || undefined, score: gameScore.value, time_spent: gameTime.value, answers: gameAnswers.value })
    } else { gameResult.value = { session_id: 'demo', score: gameScore.value, max_score: maxScore, time_spent: gameTime.value, percentage, rank: 1, total_players: 1 } }
  } catch { gameResult.value = { session_id: 'local', score: gameScore.value, max_score: maxScore, time_spent: gameTime.value, percentage, rank: 0, total_players: 0 } }
  activeGame.value = 'result'; showToast(`Chúc mừng! Bạn đạt ${gameScore.value} điểm!`, 'success')
}

function playAgain() { if (currentGameData.value) openGame(currentGameData.value) }
onMounted(() => { loadGames() })
</script>

<style scoped>
.page-wrapper { min-height: 100vh; position: relative; transition: background-color 0.3s ease; padding-bottom: 60px; }
.page-wrapper.dark-mode { background: #020617; }
.page-wrapper.light-mode { background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%); }

.bg-elements { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.glow { position: absolute; border-radius: 50%; filter: blur(100px); }
.glow-1 { top: 10%; left: -5%; width: 300px; height: 300px; background: rgba(6, 182, 212, 0.1); }
.glow-2 { bottom: 10%; right: -5%; width: 250px; height: 250px; background: rgba(139, 92, 246, 0.1); }

.page-content { position: relative; z-index: 10; max-width: 1200px; margin: 0 auto; padding: 32px 24px; }

.page-header { margin-bottom: 24px; }
.page-header h1 { font-size: 28px; font-weight: 800; margin: 0 0 8px; }
.dark-mode .page-header h1 { color: white; }
.light-mode .page-header h1 { color: #1e293b; }
.page-header p { font-size: 14px; margin: 0; }
.dark-mode .page-header p { color: #64748b; }
.light-mode .page-header p { color: #64748b; }

.games-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
@media (max-width: 1024px) { .games-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .games-grid { grid-template-columns: 1fr; } }

.skeleton-card { height: 240px; border-radius: 20px; animation: pulse 1.5s infinite; }
.dark-mode .skeleton-card { background: rgba(255,255,255,0.03); }
.light-mode .skeleton-card { background: white; border: 1px solid #e2e8f0; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

.game-category-card { border-radius: 20px; padding: 24px; display: flex; flex-direction: column; transition: all 0.3s; }
.dark-mode .game-category-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .game-category-card { background: white; border: 1px solid #e2e8f0; }
.game-category-card:hover { transform: translateY(-4px); }
.dark-mode .game-category-card:hover { border-color: rgba(6,182,212,0.3); }
.light-mode .game-category-card:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.1); }

.category-icon { width: 48px; height: 48px; border-radius: 16px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; }
.category-icon.blue { background: rgba(14,165,233,0.1); color: #0ea5e9; }
.category-icon.amber { background: rgba(245,158,11,0.1); color: #f59e0b; }
.category-icon.violet { background: rgba(139,92,246,0.1); color: #8b5cf6; }

.game-category-card h3 { font-size: 18px; font-weight: 700; margin: 0 0 8px; }
.dark-mode .game-category-card h3 { color: white; }
.light-mode .game-category-card h3 { color: #1e293b; }
.game-category-card p { font-size: 14px; margin: 0 0 16px; flex: 1; }
.dark-mode .game-category-card p { color: #64748b; }
.light-mode .game-category-card p { color: #64748b; }

.play-btn { width: 100%; padding: 12px; border-radius: 12px; font-size: 14px; font-weight: 600; border: none; cursor: pointer; transition: all 0.3s; }
.dark-mode .play-btn { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; }
.light-mode .play-btn { background: #1e293b; color: white; }
.play-btn:hover { transform: translateY(-2px); }

.coming-soon { text-align: center; padding: 40px 20px; border-radius: 20px; margin-top: 40px; }
.dark-mode .coming-soon { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .coming-soon { background: white; border: 1px solid #e2e8f0; }
.coming-icon { font-size: 40px; margin-bottom: 12px; }
.coming-soon h3 { font-size: 18px; font-weight: 600; margin: 0 0 8px; }
.dark-mode .coming-soon h3 { color: white; }
.light-mode .coming-soon h3 { color: #1e293b; }
.coming-soon p { font-size: 14px; margin: 0; }
.dark-mode .coming-soon p { color: #64748b; }
.light-mode .coming-soon p { color: #64748b; }

.back-btn { display: flex; align-items: center; gap: 8px; padding: 8px 0; font-size: 14px; font-weight: 600; background: none; border: none; cursor: pointer; margin-bottom: 16px; }
.dark-mode .back-btn { color: #64748b; }
.light-mode .back-btn { color: #64748b; }
.back-btn:hover { opacity: 0.8; }
.dark-mode .back-btn:hover { color: white; }
.light-mode .back-btn:hover { color: #1e293b; }

.category-title { font-size: 20px; font-weight: 700; margin: 0 0 20px; }
.dark-mode .category-title { color: white; }
.light-mode .category-title { color: #1e293b; }

.games-list { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
@media (max-width: 1024px) { .games-list { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 640px) { .games-list { grid-template-columns: 1fr; } }

.game-card { border-radius: 16px; padding: 20px; cursor: pointer; transition: all 0.3s; }
.dark-mode .game-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .game-card { background: white; border: 1px solid #e2e8f0; }
.game-card:hover { transform: translateY(-4px); }
.dark-mode .game-card:hover { border-color: rgba(6,182,212,0.3); }
.light-mode .game-card:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.1); }

.game-header { display: flex; justify-content: flex-end; margin-bottom: 12px; }
.difficulty-badge { padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.difficulty-badge.easy { background: rgba(34,197,94,0.1); color: #22c55e; }
.difficulty-badge.medium { background: rgba(245,158,11,0.1); color: #f59e0b; }
.difficulty-badge.hard { background: rgba(239,68,68,0.1); color: #ef4444; }

.game-card h3 { font-size: 16px; font-weight: 600; margin: 0 0 8px; }
.dark-mode .game-card h3 { color: white; }
.light-mode .game-card h3 { color: #1e293b; }
.game-card > p { font-size: 13px; margin: 0 0 12px; display: -webkit-box; -webkit-line-clamp: 2; line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.dark-mode .game-card > p { color: #64748b; }
.light-mode .game-card > p { color: #64748b; }

.game-stats { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 12px; }
.dark-mode .game-stats { color: #475569; }
.light-mode .game-stats { color: #94a3b8; }

.best-score { display: flex; justify-content: space-between; padding: 10px 12px; border-radius: 10px; font-size: 13px; margin-bottom: 12px; }
.dark-mode .best-score { background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.2); color: #fbbf24; }
.light-mode .best-score { background: #fef3c7; border: 1px solid #fde68a; color: #92400e; }

.empty-state { text-align: center; padding: 60px 20px; }
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-state h3 { font-size: 18px; font-weight: 600; margin: 0 0 8px; }
.dark-mode .empty-state h3 { color: white; }
.light-mode .empty-state h3 { color: #1e293b; }
.empty-state p { font-size: 14px; margin: 0; }
.dark-mode .empty-state p { color: #64748b; }
.light-mode .empty-state p { color: #64748b; }

/* Modal Styles */
.game-modal-overlay { position: fixed; inset: 0; z-index: 9999; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.8); backdrop-filter: blur(4px); padding: 16px; }
.game-modal { width: 100%; max-width: 720px; max-height: 90vh; overflow-y: auto; border-radius: 20px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); }
.game-modal.dark-mode { background: #0f172a; }
.game-modal.light-mode { background: white; }

.modal-header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; border-bottom: 1px solid; position: sticky; top: 0; z-index: 10; }
.dark-mode .modal-header { background: #0f172a; border-color: rgba(255,255,255,0.1); }
.light-mode .modal-header { background: white; border-color: #e2e8f0; }
.game-modal.dark-mode .modal-header { background: #0f172a; border-color: rgba(255,255,255,0.1); }
.game-modal.light-mode .modal-header { background: white; border-color: #e2e8f0; }
.modal-header h2 { font-size: 18px; font-weight: 700; margin: 0; }
.game-modal.dark-mode .modal-header h2 { color: white; }
.game-modal.light-mode .modal-header h2 { color: #1e293b; }
.dark-mode .modal-header h2 { color: white; }
.light-mode .modal-header h2 { color: #1e293b; }
.modal-header > div:first-child p { font-size: 12px; margin: 4px 0 0; }
.game-modal.dark-mode .modal-header > div:first-child p { color: #64748b; }
.game-modal.light-mode .modal-header > div:first-child p { color: #64748b; }
.dark-mode .modal-header > div:first-child p { color: #64748b; }
.light-mode .modal-header > div:first-child p { color: #64748b; }

.modal-stats { display: flex; gap: 24px; }
.stat-item { text-align: center; }
.stat-value { font-size: 24px; font-weight: 800; }
.game-modal.dark-mode .stat-value { color: white; }
.game-modal.light-mode .stat-value { color: #1e293b; }
.dark-mode .stat-value { color: white; }
.light-mode .stat-value { color: #1e293b; }
.stat-label { font-size: 11px; }
.game-modal.dark-mode .stat-label { color: #64748b; }
.game-modal.light-mode .stat-label { color: #64748b; }
.dark-mode .stat-label { color: #64748b; }
.light-mode .stat-label { color: #64748b; }

.close-btn { padding: 10px 16px; border-radius: 12px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.game-modal.dark-mode .close-btn { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.game-modal.light-mode .close-btn { background: #f1f5f9; border: 1px solid #e2e8f0; color: #64748b; }
.dark-mode .close-btn { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .close-btn { background: #f1f5f9; border: 1px solid #e2e8f0; color: #64748b; }
.close-btn:hover { transform: scale(1.02); }
.game-modal.dark-mode .close-btn:hover { background: rgba(255,255,255,0.1); }
.game-modal.light-mode .close-btn:hover { background: #e2e8f0; }
.dark-mode .close-btn:hover { background: rgba(255,255,255,0.1); }
.light-mode .close-btn:hover { background: #e2e8f0; }

.modal-body { padding: 24px; }

.progress-section { margin-bottom: 24px; }
.progress-section > span { font-size: 14px; font-weight: 600; display: block; margin-bottom: 8px; }
.game-modal.dark-mode .progress-section > span { color: #94a3b8; }
.game-modal.light-mode .progress-section > span { color: #64748b; }
.dark-mode .progress-section > span { color: #94a3b8; }
.light-mode .progress-section > span { color: #64748b; }
.progress-bar { height: 8px; border-radius: 4px; overflow: hidden; }
.game-modal.dark-mode .progress-bar { background: rgba(255,255,255,0.1); }
.game-modal.light-mode .progress-bar { background: #e2e8f0; }
.dark-mode .progress-bar { background: rgba(255,255,255,0.1); }
.light-mode .progress-bar { background: #e2e8f0; }
.progress-fill { height: 100%; transition: width 0.3s; }
.game-modal.dark-mode .progress-fill { background: linear-gradient(90deg, #06b6d4, #8b5cf6); }
.game-modal.light-mode .progress-fill { background: #1e293b; }
.dark-mode .progress-fill { background: linear-gradient(90deg, #06b6d4, #8b5cf6); }
.light-mode .progress-fill { background: #1e293b; }

.question-box { padding: 24px; border-radius: 16px; margin-bottom: 24px; }
.game-modal.dark-mode .question-box { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.game-modal.light-mode .question-box { background: #f8fafc; border: 1px solid #e2e8f0; }
.dark-mode .question-box { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .question-box { background: #f8fafc; border: 1px solid #e2e8f0; }
.question-box h3 { font-size: 20px; font-weight: 700; margin: 0; }
.game-modal.dark-mode .question-box h3 { color: white; }
.game-modal.light-mode .question-box h3 { color: #1e293b; }
.dark-mode .question-box h3 { color: white; }
.light-mode .question-box h3 { color: #1e293b; }

.options-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
@media (max-width: 640px) { .options-grid { grid-template-columns: 1fr; } }

.option-btn { display: flex; align-items: center; gap: 12px; padding: 16px; border-radius: 12px; text-align: left; cursor: pointer; transition: all 0.3s; }
.game-modal.dark-mode .option-btn { background: rgba(255,255,255,0.03); border: 2px solid rgba(255,255,255,0.08); }
.game-modal.light-mode .option-btn { background: white; border: 2px solid #e2e8f0; }
.dark-mode .option-btn { background: rgba(255,255,255,0.03); border: 2px solid rgba(255,255,255,0.08); }
.light-mode .option-btn { background: white; border: 2px solid #e2e8f0; }
.option-btn:hover { transform: scale(1.01); }
.game-modal.dark-mode .option-btn:hover { border-color: rgba(255,255,255,0.2); }
.game-modal.light-mode .option-btn:hover { border-color: #cbd5e1; }
.dark-mode .option-btn:hover { border-color: rgba(255,255,255,0.2); }
.light-mode .option-btn:hover { border-color: #cbd5e1; }
.option-btn.selected { transform: scale(1.01); }
.game-modal.dark-mode .option-btn.selected { border-color: #06b6d4; background: rgba(6,182,212,0.1); }
.game-modal.light-mode .option-btn.selected { border-color: #1e293b; background: #f1f5f9; }
.dark-mode .option-btn.selected { border-color: #06b6d4; background: rgba(6,182,212,0.1); }
.light-mode .option-btn.selected { border-color: #1e293b; background: #f1f5f9; }

.option-letter { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 700; }
.game-modal.dark-mode .option-letter { background: rgba(255,255,255,0.1); color: #94a3b8; }
.game-modal.light-mode .option-letter { background: #f1f5f9; color: #64748b; }
.dark-mode .option-letter { background: rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .option-letter { background: #f1f5f9; color: #64748b; }
.option-btn.selected .option-letter { transform: scale(1.05); }
.game-modal.dark-mode .option-btn.selected .option-letter { background: #06b6d4; color: white; }
.game-modal.light-mode .option-btn.selected .option-letter { background: #1e293b; color: white; }
.dark-mode .option-btn.selected .option-letter { background: #06b6d4; color: white; }
.light-mode .option-btn.selected .option-letter { background: #1e293b; color: white; }
.option-btn span { font-size: 14px; font-weight: 500; }
.game-modal.dark-mode .option-btn span { color: white; }
.game-modal.light-mode .option-btn span { color: #1e293b; }
.dark-mode .option-btn span { color: white; }
.light-mode .option-btn span { color: #1e293b; }

.word-match-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }
.word-column h4 { font-size: 14px; font-weight: 700; margin: 0 0 12px; }
.game-modal.dark-mode .word-column h4 { color: white; }
.game-modal.light-mode .word-column h4 { color: #1e293b; }
.dark-mode .word-column h4 { color: white; }
.light-mode .word-column h4 { color: #1e293b; }
.word-btn { width: 100%; padding: 14px; border-radius: 12px; font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.3s; margin-bottom: 8px; }
.game-modal.dark-mode .word-btn { background: rgba(255,255,255,0.03); border: 2px solid rgba(255,255,255,0.08); color: white; }
.game-modal.light-mode .word-btn { background: white; border: 2px solid #e2e8f0; color: #1e293b; }
.dark-mode .word-btn { background: rgba(255,255,255,0.03); border: 2px solid rgba(255,255,255,0.08); color: white; }
.light-mode .word-btn { background: white; border: 2px solid #e2e8f0; color: #1e293b; }
.word-btn:hover:not(:disabled) { transform: scale(1.02); }
.game-modal.dark-mode .word-btn:hover:not(:disabled) { border-color: rgba(255,255,255,0.2); }
.game-modal.light-mode .word-btn:hover:not(:disabled) { border-color: #cbd5e1; }
.dark-mode .word-btn:hover:not(:disabled) { border-color: rgba(255,255,255,0.2); }
.light-mode .word-btn:hover:not(:disabled) { border-color: #cbd5e1; }
.word-btn.selected { transform: scale(1.02); }
.game-modal.dark-mode .word-btn.selected { border-color: #06b6d4; background: rgba(6,182,212,0.1); }
.game-modal.light-mode .word-btn.selected { border-color: #1e293b; background: #f1f5f9; }
.dark-mode .word-btn.selected { border-color: #06b6d4; background: rgba(6,182,212,0.1); }
.light-mode .word-btn.selected { border-color: #1e293b; background: #f1f5f9; }
.word-btn.matched { opacity: 0.5; }
.game-modal.dark-mode .word-btn.matched { border-color: #22c55e; background: rgba(34,197,94,0.1); color: #22c55e; }
.game-modal.light-mode .word-btn.matched { border-color: #22c55e; background: #dcfce7; color: #16a34a; }
.dark-mode .word-btn.matched { border-color: #22c55e; background: rgba(34,197,94,0.1); color: #22c55e; }
.light-mode .word-btn.matched { border-color: #22c55e; background: #dcfce7; color: #16a34a; }

.result-view { text-align: center; }
.result-view h2 { font-size: 24px; font-weight: 800; margin: 0 0 8px; }
.game-modal.dark-mode .result-view h2 { color: white; }
.game-modal.light-mode .result-view h2 { color: #1e293b; }
.dark-mode .result-view h2 { color: white; }
.light-mode .result-view h2 { color: #1e293b; }
.result-view > p { font-size: 14px; margin: 0 0 24px; }
.game-modal.dark-mode .result-view > p { color: #64748b; }
.game-modal.light-mode .result-view > p { color: #64748b; }
.dark-mode .result-view > p { color: #64748b; }
.light-mode .result-view > p { color: #64748b; }

.result-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; padding: 24px; border-radius: 16px; margin-bottom: 24px; }
.game-modal.dark-mode .result-stats { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.game-modal.light-mode .result-stats { background: #f8fafc; border: 1px solid #e2e8f0; }
.dark-mode .result-stats { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .result-stats { background: #f8fafc; border: 1px solid #e2e8f0; }
.big-num { font-size: 32px; font-weight: 900; }
.game-modal.dark-mode .big-num { color: white; }
.game-modal.light-mode .big-num { color: #1e293b; }
.dark-mode .big-num { color: white; }
.light-mode .big-num { color: #1e293b; }
.result-stats > div > div:last-child { font-size: 13px; }
.game-modal.dark-mode .result-stats > div > div:last-child { color: #64748b; }
.game-modal.light-mode .result-stats > div > div:last-child { color: #64748b; }
.dark-mode .result-stats > div > div:last-child { color: #64748b; }
.light-mode .result-stats > div > div:last-child { color: #64748b; }

.rank-info { padding: 16px; border-radius: 12px; margin-bottom: 24px; font-size: 14px; }
.game-modal.dark-mode .rank-info { background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.2); color: #fbbf24; }
.game-modal.light-mode .rank-info { background: #fef3c7; border: 1px solid #fde68a; color: #92400e; }
.dark-mode .rank-info { background: rgba(251,191,36,0.1); border: 1px solid rgba(251,191,36,0.2); color: #fbbf24; }
.light-mode .rank-info { background: #fef3c7; border: 1px solid #fde68a; color: #92400e; }

.result-actions { display: flex; gap: 12px; }
.btn-outline, .btn-primary { flex: 1; padding: 14px; border-radius: 12px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.btn-outline { background: transparent; }
.game-modal.dark-mode .btn-outline { border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.game-modal.light-mode .btn-outline { border: 1px solid #e2e8f0; color: #64748b; }
.dark-mode .btn-outline { border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .btn-outline { border: 1px solid #e2e8f0; color: #64748b; }
.btn-primary { border: none; }
.game-modal.dark-mode .btn-primary { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; }
.game-modal.light-mode .btn-primary { background: #1e293b; color: white; }
.dark-mode .btn-primary { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; }
.light-mode .btn-primary { background: #1e293b; color: white; }

@media (max-width: 640px) { .page-content { padding: 24px 16px; } .modal-header { flex-wrap: wrap; gap: 12px; } .modal-stats { width: 100%; justify-content: center; } }
</style>
