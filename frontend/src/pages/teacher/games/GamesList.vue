<template>
  <div class="min-h-screen bg-slate-50 pb-16 pt-10">
    <div class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8 flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-slate-900">Quản lý trò chơi</h1>
          <p class="mt-1 text-slate-600">Tạo và quản lý các trò chơi giáo dục cho học sinh</p>
        </div>
        <button
          class="flex items-center gap-2 rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800"
          @click="openCreateModal"
        >
          Tạo trò chơi mới
        </button>
      </div>

      <!-- Stats -->
      <div class="mb-8 grid gap-4 sm:grid-cols-4">
        <div class="rounded-xl border border-slate-200 bg-white p-4">
          <div class="text-sm font-semibold text-slate-600">Tổng trò chơi</div>
          <div class="mt-2 text-2xl font-bold text-slate-900">{{ games.length }}</div>
        </div>
        <div class="rounded-xl border border-slate-200 bg-white p-4">
          <div class="text-sm font-semibold text-slate-600">Đã xuất bản</div>
          <div class="mt-2 text-2xl font-bold text-slate-900">{{ publishedCount }}</div>
        </div>
        <div class="rounded-xl border border-slate-200 bg-white p-4">
          <div class="text-sm font-semibold text-slate-600">Lượt chơi</div>
          <div class="mt-2 text-2xl font-bold text-slate-900">{{ totalPlays }}</div>
        </div>
        <div class="rounded-xl border border-slate-200 bg-white p-4">
          <div class="text-sm font-semibold text-slate-600">Điểm TB</div>
          <div class="mt-2 text-2xl font-bold text-slate-900">{{ avgScore }}%</div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="space-y-4">
        <div v-for="i in 3" :key="i" class="h-24 animate-pulse rounded-xl bg-white border border-slate-200"></div>
      </div>

      <!-- Games List -->
      <div v-else-if="games.length" class="space-y-4">
        <div
          v-for="game in games"
          :key="game.id"
          class="rounded-xl bg-white border border-slate-200 p-5 hover:shadow-md transition"
        >
          <div class="flex items-start justify-between">
            <div class="flex flex-col gap-1">
              <div class="flex items-center gap-2">
                <h3 class="text-lg font-bold text-slate-900">{{ game.title }}</h3>
                <span 
                  class="rounded-full px-2 py-0.5 text-xs font-semibold"
                  :class="game.is_published ? 'bg-green-100 text-green-700' : 'bg-slate-100 text-slate-600'"
                >
                  {{ game.is_published ? 'Đã xuất bản' : 'Bản nháp' }}
                </span>
              </div>
              <p class="text-sm text-slate-600">{{ game.description || 'Chưa có mô tả' }}</p>
              <div class="flex flex-wrap items-center gap-4 text-xs text-slate-500">
                <span>{{ game.game_type_display }}</span>
                <span>•</span>
                <span>{{ game.question_count }} câu hỏi</span>
                <span>•</span>
                <span>{{ game.play_count }} lượt chơi</span>
                <span>•</span>
                <span>Điểm TB: {{ Math.round(game.avg_score || 0) }}</span>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <button
                class="rounded-lg border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
                @click="editGame(game)"
              >
                Sửa
              </button>
              <button
                class="rounded-lg border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
                @click="viewStats(game)"
              >
                Thống kê
              </button>
              <button
                class="rounded-lg border border-red-200 px-3 py-2 text-sm font-semibold text-red-600 transition hover:bg-red-50"
                @click="confirmDelete(game)"
              >
                Xóa
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-16 bg-white rounded-xl border border-slate-200">
        <h3 class="mb-2 text-xl font-bold text-slate-900">Chưa có trò chơi nào</h3>
        <p class="mb-6 text-slate-600">Tạo trò chơi đầu tiên để học sinh có thể học tập vui vẻ!</p>
        <button
          class="rounded-xl bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
          @click="openCreateModal"
        >
          Tạo trò chơi mới
        </button>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
        <div class="w-full max-w-3xl rounded-2xl bg-white shadow-2xl max-h-[90vh] overflow-y-auto">
          <div class="sticky top-0 bg-white border-b border-slate-200 p-5 flex items-center justify-between">
            <h2 class="text-xl font-bold text-slate-900">
              {{ editingGame ? 'Chỉnh sửa trò chơi' : 'Tạo trò chơi mới' }}
            </h2>
            <button class="text-slate-400 hover:text-slate-600" @click="closeModal">✕</button>
          </div>
          
          <div class="p-5 space-y-6">
            <div v-if="modalLoading" class="py-10 text-center text-sm text-slate-500">Đang tải chi tiết trò chơi...</div>
            <div v-else>
            <!-- Basic Info -->
            <div class="space-y-4 rounded-xl border border-slate-200 bg-slate-50 p-4">
              <div class="grid gap-4 md:grid-cols-2">
                <div class="space-y-1">
                  <label class="block text-sm font-semibold text-slate-700">Tên trò chơi *</label>
                  <input
                    v-model="form.title"
                    type="text"
                    class="w-full rounded-xl border border-slate-300 px-4 py-3 focus:border-slate-900 focus:ring-slate-900"
                    placeholder="VD: Trắc nghiệm Toán lớp 1"
                  />
                </div>
                <div class="space-y-1">
                  <label class="block text-sm font-semibold text-slate-700">Loại trò chơi *</label>
                  <select
                    v-model="form.game_type"
                    class="w-full rounded-xl border border-slate-300 px-4 py-3 focus:border-slate-900 focus:ring-slate-900"
                  >
                    <option value="quiz">Trắc nghiệm nhanh</option>
                    <option value="word_match">Ghép từ</option>
                    <option value="puzzle">Đố vui</option>
                  </select>
                </div>
              </div>
              
              <div class="space-y-1">
                <label class="block text-sm font-semibold text-slate-700">Mô tả</label>
                <textarea
                  v-model="form.description"
                  rows="2"
                  class="w-full rounded-xl border border-slate-300 px-4 py-3 focus:border-slate-900 focus:ring-slate-900"
                  placeholder="Mô tả ngắn về trò chơi..."
                ></textarea>
              </div>
              
              <div class="grid gap-4 md:grid-cols-3">
                <div class="space-y-1">
                  <label class="block text-sm font-semibold text-slate-700">Độ khó</label>
                  <select
                    v-model="form.difficulty"
                    class="w-full rounded-xl border border-slate-300 px-4 py-3 focus:border-slate-900 focus:ring-slate-900"
                  >
                    <option value="easy">Dễ</option>
                    <option value="medium">Trung bình</option>
                    <option value="hard">Khó</option>
                  </select>
                </div>
                <div class="space-y-1">
                  <label class="block text-sm font-semibold text-slate-700">Môn học</label>
                  <select v-model="form.subject" class="w-full rounded-xl border border-slate-300 px-4 py-3">
                    <option value="">-- Chọn môn --</option>
                    <option value="math">Toán</option>
                    <option value="vietnamese">Tiếng Việt</option>
                    <option value="english">Tiếng Anh</option>
                    <option value="science">Khoa học</option>
                  </select>
                </div>
                <div class="space-y-1">
                  <label class="block text-sm font-semibold text-slate-700">Lớp</label>
                  <select v-model="form.grade_level" class="w-full rounded-xl border border-slate-300 px-4 py-3">
                    <option :value="null">-- Chọn lớp --</option>
                    <option v-for="g in 5" :key="g" :value="g">Lớp {{ g }}</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Questions -->
            <div class="rounded-xl border border-slate-200 p-4">
              <div class="mb-4 space-y-2 md:flex md:items-center md:justify-between md:space-y-0">
                <label class="text-sm font-semibold text-slate-700 block">
                  {{ form.game_type === 'word_match' ? 'Cặp từ ghép' : 'Câu hỏi' }} ({{ form.questions.length }})
                </label>
                <div class="flex flex-wrap items-center gap-2 md:justify-end">
                  <button
                    class="rounded-lg border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-60"
                    :disabled="aiGenerating"
                    @click="openAIDialog"
                  >
                    {{ aiGenerating ? 'Đang tạo...' : 'Tạo bằng AI' }}
                  </button>
                  <button
                    class="rounded-lg bg-slate-900 px-3 py-2 text-sm font-semibold text-white hover:bg-slate-800"
                    @click="addQuestion"
                  >
                    Thêm {{ form.game_type === 'word_match' ? 'cặp từ' : 'câu hỏi' }}
                  </button>
                </div>
              </div>
              
              <div class="space-y-3 max-h-64 overflow-y-auto pr-1">
                <!-- Quiz/Puzzle Questions -->
                <div
                  v-if="form.game_type !== 'word_match'"
                  v-for="(q, idx) in form.questions"
                  :key="idx"
                  class="rounded-xl border border-slate-200 bg-slate-50 p-4"
                >
                  <div class="flex items-start justify-between mb-3">
                    <span class="text-sm font-semibold text-slate-500">Câu {{ idx + 1 }}</span>
                    <button class="text-sm font-semibold text-red-600 hover:text-red-500" @click="removeQuestion(idx)">Xóa</button>
                  </div>
                  <input
                    v-model="q.question"
                    type="text"
                    class="w-full rounded-lg border border-slate-300 px-3 py-2 mb-3 text-sm"
                    placeholder="Nhập câu hỏi..."
                  />
                  <div class="grid grid-cols-2 gap-2">
                    <div v-for="(opt, oidx) in q.options" :key="oidx" class="flex items-center gap-2">
                      <input
                        type="radio"
                        :name="`correct-${idx}`"
                        :checked="q.correct === oidx"
                        @change="q.correct = oidx"
                        class="text-slate-900 focus:ring-slate-900"
                      />
                      <input
                        v-model="q.options[oidx]"
                        type="text"
                        class="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm"
                        :placeholder="`Đáp án ${oidx + 1}`"
                      />
                    </div>
                  </div>
                </div>
                
                <!-- Word Match Pairs -->
                <div
                  v-if="form.game_type === 'word_match'"
                  v-for="(q, idx) in form.questions"
                  :key="idx"
                  class="rounded-xl border border-slate-200 bg-slate-50 p-4"
                >
                  <div class="flex items-center justify-between mb-3">
                    <span class="text-sm font-semibold text-slate-500">Cặp {{ idx + 1 }}</span>
                    <button class="text-sm font-semibold text-red-600 hover:text-red-500" @click="removeQuestion(idx)">Xóa</button>
                  </div>
                  <div class="grid grid-cols-2 gap-3">
                    <input
                      v-model="q.left"
                      type="text"
                      class="rounded-lg border border-slate-300 px-3 py-2 text-sm"
                      placeholder="Tiếng Việt"
                    />
                    <input
                      v-model="q.right"
                      type="text"
                      class="rounded-lg border border-slate-300 px-3 py-2 text-sm"
                      placeholder="Tiếng Anh"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Publish Toggle -->
            <div class="flex items-center gap-3 rounded-xl bg-slate-50 p-4 border border-slate-200">
              <input
                type="checkbox"
                v-model="form.is_published"
                id="publish"
                class="h-5 w-5 rounded text-slate-900 focus:ring-slate-900"
              />
              <label for="publish" class="text-sm font-semibold text-slate-700">
                Xuất bản ngay (học sinh có thể chơi)
              </label>
            </div>
          </div>
          <!-- end of p-5 content -->
          </div>
          
          <div class="sticky bottom-0 bg-white border-t border-slate-200 p-5 flex justify-end gap-3">
            <button
              class="rounded-xl border border-slate-200 px-5 py-3 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              @click="closeModal"
            >
              Hủy
            </button>
            <button
              class="rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
              :disabled="saving"
              @click="saveGame"
            >
              {{ saving ? 'Đang lưu...' : (editingGame ? 'Cập nhật' : 'Tạo trò chơi') }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- AI Dialog -->
    <Teleport to="body">
      <div v-if="showAIDialog" class="fixed inset-0 z-[60] flex items-center justify-center bg-black/50 p-4">
        <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-bold text-slate-900">Tạo câu hỏi bằng AI</h3>
            <button class="text-slate-400 hover:text-slate-600" @click="showAIDialog = false">✕</button>
          </div>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1">Số câu cần tạo</label>
              <input
                v-model.number="aiCount"
                type="number"
                min="1"
                max="15"
                class="w-full rounded-xl border border-slate-300 px-4 py-3"
              />
              <p class="mt-1 text-xs text-slate-500">Tối đa 15 câu/lần</p>
            </div>
            
            <div>
              <label class="block text-sm font-semibold text-slate-700 mb-1">Mô tả mong muốn (tùy chọn)</label>
              <textarea
                v-model="aiHint"
                rows="3"
                class="w-full rounded-xl border border-slate-300 px-4 py-3"
                placeholder="VD: tập trung kiến thức phép cộng, độ khó vừa phải..."
              ></textarea>
            </div>
          </div>
          
          <div class="mt-6 flex justify-end gap-3">
            <button
              class="rounded-xl border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              @click="showAIDialog = false"
            >
              Hủy
            </button>
            <button
              class="rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
              @click="generateWithAI"
            >
              Tạo câu hỏi
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Stats Modal -->
    <Teleport to="body">
      <div v-if="showStatsModal" class="fixed inset-0 z-[60] flex items-center justify-center bg-black/50 p-4">
        <div class="w-full max-w-2xl rounded-2xl bg-white shadow-2xl max-h-[90vh] overflow-y-auto">
          <div class="sticky top-0 bg-white border-b border-slate-200 p-5 flex items-center justify-between">
            <h2 class="text-xl font-bold text-slate-900">Thống kê trò chơi</h2>
            <button class="text-slate-400 hover:text-slate-600" @click="showStatsModal = false">✕</button>
          </div>
          
          <!-- Loading -->
          <div v-if="statsLoading" class="p-8 text-center">
            <div class="animate-spin w-8 h-8 border-4 border-slate-200 border-t-slate-900 rounded-full mx-auto"></div>
            <p class="mt-3 text-slate-600">Đang tải thống kê...</p>
          </div>
          
          <!-- Stats Content -->
          <div v-else-if="statsData" class="p-5 space-y-6">
            <h3 class="text-lg font-semibold text-slate-900">{{ statsData.game_title }}</h3>
            
            <!-- Overview -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div class="rounded-xl border border-slate-200 p-4 text-center">
                <div class="text-2xl font-bold text-slate-900">{{ statsData.total_plays }}</div>
                <div class="text-sm text-slate-600">Lượt chơi</div>
              </div>
              <div class="rounded-xl border border-slate-200 p-4 text-center">
                <div class="text-2xl font-bold text-slate-900">{{ statsData.unique_players }}</div>
                <div class="text-sm text-slate-600">Người chơi</div>
              </div>
              <div class="rounded-xl border border-slate-200 p-4 text-center">
                <div class="text-2xl font-bold text-slate-900">{{ Math.round(statsData.avg_score || 0) }}</div>
                <div class="text-sm text-slate-600">Điểm TB</div>
              </div>
              <div class="rounded-xl border border-slate-200 p-4 text-center">
                <div class="text-2xl font-bold text-slate-900">{{ Math.round(statsData.avg_time || 0) }}s</div>
                <div class="text-sm text-slate-600">Thời gian TB</div>
              </div>
            </div>
            
            <!-- Score Distribution -->
            <div v-if="statsData.score_distribution">
              <h4 class="text-sm font-semibold text-slate-700 mb-3">Phân bố điểm số</h4>
              <div class="space-y-2">
                <div v-for="(count, range) in statsData.score_distribution" :key="range" class="flex items-center gap-3">
                  <span class="text-sm text-slate-600 w-16">{{ range }}%</span>
                  <div class="flex-1 h-6 bg-slate-100 rounded-full overflow-hidden">
                    <div 
                      class="h-full bg-slate-900 rounded-full transition-all"
                      :style="{ width: `${statsData.total_plays ? (count / statsData.total_plays * 100) : 0}%` }"
                    ></div>
                  </div>
                  <span class="text-sm font-semibold text-slate-900 w-8">{{ count }}</span>
                </div>
              </div>
            </div>
            
            <!-- Recent Plays -->
            <div v-if="statsData.recent_plays?.length">
              <h4 class="text-sm font-semibold text-slate-700 mb-3">Lượt chơi gần đây</h4>
              <div class="space-y-2">
                <div 
                  v-for="(play, idx) in statsData.recent_plays" 
                  :key="idx"
                  class="flex items-center justify-between p-3 rounded-xl border border-slate-200"
                >
                  <div>
                    <div class="font-semibold text-slate-900">{{ play.player_name }}</div>
                    <div class="text-xs text-slate-500">{{ play.time_spent }}s</div>
                  </div>
                  <div class="text-right">
                    <div class="font-bold text-slate-900">{{ play.score }}/{{ play.max_score }}</div>
                    <div class="text-xs text-slate-500">{{ Math.round(play.max_score ? play.score / play.max_score * 100 : 0) }}%</div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Empty State -->
            <div v-if="!statsData.total_plays" class="text-center py-8">
              <p class="text-slate-600">Chưa có ai chơi trò chơi này</p>
            </div>
          </div>
          
          <div class="sticky bottom-0 bg-white border-t border-slate-200 p-4 flex justify-end">
            <button
              class="rounded-xl border border-slate-200 px-5 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              @click="showStatsModal = false"
            >
              Đóng
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { teacherGameService } from '@/services/game.service'
import { showToast } from '@/utils/toast'

const loading = ref(true)
const saving = ref(false)
const modalLoading = ref(false)
const aiGenerating = ref(false)
const showAIDialog = ref(false)
const showStatsModal = ref(false)
const statsLoading = ref(false)
const statsData = ref<any>(null)
const aiCount = ref(5)
const aiHint = ref('')
const games = ref<any[]>([])
const showModal = ref(false)
const editingGame = ref<any>(null)

const form = ref({
  title: '',
  description: '',
  game_type: 'quiz',
  difficulty: 'easy',
  subject: '',
  grade_level: null as number | null,
  questions: [] as any[],
  is_published: false,
})

const publishedCount = computed(() => games.value.filter(g => g.is_published).length)
const totalPlays = computed(() => games.value.reduce((sum, g) => sum + (g.play_count || 0), 0))
const avgScore = computed(() => {
  const scores = games.value.filter(g => g.avg_score).map(g => g.avg_score)
  return scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 0
})

async function loadGames() {
  loading.value = true
  try {
    const data = await teacherGameService.list()
    games.value = data.games || []
  } catch (e) {
    console.error('Load games error:', e)
    showToast('Không thể tải danh sách trò chơi', 'error')
  } finally {
    loading.value = false
  }
}

function openCreateModal() {
  editingGame.value = null
  form.value = {
    title: '',
    description: '',
    game_type: 'quiz',
    difficulty: 'easy',
    subject: '',
    grade_level: null,
    questions: [],
    is_published: false,
  }
  // Không tự thêm câu hỏi rỗng - để giáo viên tự thêm hoặc dùng AI
  showModal.value = true
}

function normalizeQuestions(raw: any[], gameType: string) {
  if (!Array.isArray(raw)) return []

  return raw.map((q, idx) => {
    if (gameType === 'word_match') {
      const left = q.left || q.word_left || q.term || q.question || q.prompt || ''
      const right = q.right || q.word_right || q.answer || q.definition || q.response || ''
      return { left, right }
    }

    const question = q.question || q.prompt || q.text || ''
    const choices = Array.isArray(q.options)
      ? [...q.options]
      : Array.isArray(q.choices)
      ? q.choices.map((c: any) => c?.text ?? c?.option ?? c?.answer ?? '')
      : []

    const correctIndex =
      typeof q.correct === 'number'
        ? q.correct
        : Array.isArray(q.choices)
        ? q.choices.findIndex((c: any) => c?.is_correct || c?.correct === true)
        : typeof q.answer_index === 'number'
        ? q.answer_index
        : typeof q.answer === 'number'
        ? q.answer
        : -1

    const options = choices.length ? choices : ['', '', '', '']
    while (options.length < 4) options.push('')

    return {
      id: q.id ?? Date.now() + idx,
      question,
      options,
      correct: correctIndex >= 0 ? correctIndex : 0,
    }
  }).filter((q: any) => (gameType === 'word_match' ? q.left || q.right : q.question))
}

async function editGame(game: any) {
  editingGame.value = game
  showModal.value = true
  modalLoading.value = true
  try {
    const detail = await teacherGameService.detail(game.id)
    form.value = {
      title: detail.title,
      description: detail.description || '',
      game_type: detail.game_type,
      difficulty: detail.difficulty,
      subject: detail.subject || '',
      grade_level: detail.grade_level,
      questions: normalizeQuestions(detail.questions || [], detail.game_type),
      is_published: detail.is_published,
    }
  } catch (e) {
    console.error('Load game detail error:', e)
    showToast('Không tải được chi tiết trò chơi', 'error')
    showModal.value = false
    editingGame.value = null
  } finally {
    modalLoading.value = false
  }
}

function closeModal() {
  showModal.value = false
  editingGame.value = null
}

function addQuestion() {
  if (form.value.game_type === 'word_match') {
    form.value.questions.push({ left: '', right: '' })
  } else {
    form.value.questions.push({
      id: Date.now(),
      question: '',
      options: ['', '', '', ''],
      correct: 0,
    })
  }
}

function removeQuestion(idx: number) {
  form.value.questions.splice(idx, 1)
}

async function saveGame() {
  if (!form.value.title.trim()) {
    showToast('Vui lòng nhập tên trò chơi', 'error')
    return
  }
  if (form.value.questions.length === 0) {
    showToast('Vui lòng thêm ít nhất 1 câu hỏi', 'error')
    return
  }
  
  saving.value = true
  try {
    const payload = {
      ...form.value,
      grade_level: form.value.grade_level || undefined,
    }

    if (editingGame.value) {
      await teacherGameService.update(editingGame.value.id, payload)
      showToast('Đã cập nhật trò chơi!', 'success')
    } else {
      await teacherGameService.create(payload)
      showToast('Đã tạo trò chơi mới!', 'success')
    }
    closeModal()
    loadGames()
  } catch (e) {
    console.error('Save game error:', e)
    showToast('Không thể lưu trò chơi', 'error')
  } finally {
    saving.value = false
  }
}

async function confirmDelete(game: any) {
  if (!confirm(`Bạn có chắc muốn xóa "${game.title}"?`)) return
  
  try {
    await teacherGameService.delete(game.id)
    showToast('Đã xóa trò chơi!', 'success')
    loadGames()
  } catch (e) {
    console.error('Delete game error:', e)
    showToast('Không thể xóa trò chơi', 'error')
  }
}

async function viewStats(game: any) {
  showStatsModal.value = true
  statsLoading.value = true
  statsData.value = null
  
  try {
    const data = await teacherGameService.stats(game.id)
    statsData.value = data
  } catch (e) {
    console.error('Load stats error:', e)
    showToast('Không thể tải thống kê', 'error')
    showStatsModal.value = false
  } finally {
    statsLoading.value = false
  }
}

function openAIDialog() {
  aiCount.value = 5
  aiHint.value = ''
  showAIDialog.value = true
}

async function generateWithAI() {
  if (!form.value.title.trim()) {
    showToast('Vui lòng nhập tên trò chơi trước', 'warning')
    return
  }
  
  aiGenerating.value = true
  showAIDialog.value = false
  
  try {
    const result = await teacherGameService.generateWithAI({
      game_type: form.value.game_type,
      title: form.value.title,
      subject: form.value.subject,
      grade_level: form.value.grade_level || 1,
      count: aiCount.value,
      hint: aiHint.value,
    })
    
    const text = result?.text || ''
    const parsed = parseAIResponse(text)
    
    if (!parsed.length) {
      showToast('AI không trả về kết quả hợp lệ', 'warning')
      return
    }
    
    // Add parsed questions to form
    parsed.forEach(q => form.value.questions.push(q))
    showToast(`Đã thêm ${parsed.length} câu hỏi từ AI`, 'success')
  } catch (e: any) {
    console.error('AI generate error:', e)
    showToast(e?.message || 'Không thể tạo câu hỏi bằng AI', 'error')
  } finally {
    aiGenerating.value = false
  }
}

function parseAIResponse(raw: string): any[] {
  if (!raw) return []
  let jsonText = raw.trim()
  
  // Remove markdown code block if present
  const match = jsonText.match(/```(?:json)?\s*([\s\S]*?)\s*```/)
  if (match && match[1]) {
    jsonText = match[1]
  }
  
  try {
    const obj = JSON.parse(jsonText)
    const list = Array.isArray(obj) ? obj : obj.questions
    if (!Array.isArray(list)) return []
    
    return list.map((item: any, idx: number) => {
      if (form.value.game_type === 'word_match') {
        return { left: item.left || '', right: item.right || '' }
      }
      return {
        id: Date.now() + idx,
        question: item.question || '',
        options: item.options || ['', '', '', ''],
        correct: item.correct ?? 0,
      }
    }).filter((q: any) => {
      if (form.value.game_type === 'word_match') {
        return q.left && q.right
      }
      return q.question
    })
  } catch (err) {
    console.warn('Cannot parse AI JSON:', raw)
    return []
  }
}

onMounted(() => {
  loadGames()
})
</script>
