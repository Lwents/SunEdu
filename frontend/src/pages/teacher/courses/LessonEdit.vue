<!-- src/pages/teacher/courses/LessonEdit.vue -->
<template>
  <div class="mx-auto max-w-4xl p-6">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Chỉnh sửa bài học</h1>
        <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">{{ lessonTitle }}</p>
      </div>
      <button
        class="rounded-xl bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700"
        @click="saveLesson"
        :disabled="saving"
      >
        {{ saving ? 'Đang lưu...' : 'Lưu thay đổi' }}
      </button>
    </div>

    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="h-32 rounded-2xl bg-slate-200 animate-pulse" />
    </div>

    <div v-else-if="error" class="rounded-xl border border-rose-200 bg-rose-50 p-4 text-rose-700">
      {{ error }}
    </div>

    <div v-else class="space-y-6">
      <!-- Thông tin cơ bản -->
      <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">Thông tin cơ bản</h2>
        <div class="space-y-4">
          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">Tên bài học</label>
            <input
              v-model="form.title"
              type="text"
              class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
              placeholder="Tên bài học"
            />
          </div>
          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">Giới thiệu bài học</label>
            <textarea
              v-model="form.introduction"
              rows="4"
              class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
              placeholder="Giới thiệu ngắn gọn về bài học (hiển thị trước video)"
            ></textarea>
            <p class="mt-1 text-xs text-gray-500">Nội dung này sẽ hiển thị trước khi học sinh xem video</p>
          </div>
        </div>
      </div>

      <!-- Loại nội dung -->
      <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">Nội dung bài học</h2>
        <div class="mb-4 grid grid-cols-2 gap-2">
          <button
            v-for="opt in contentTypeOptions"
            :key="opt.value"
            type="button"
            :class="[
              'flex items-center gap-2 rounded-lg border px-3 py-2 text-sm font-medium transition',
              form.content_type === opt.value ? 'border-cyan-500 bg-cyan-50 text-cyan-700' : 'border-slate-300 bg-white text-gray-700 hover:bg-slate-50'
            ]"
            @click="form.content_type = opt.value"
          >
            <span>{{ opt.icon }}</span>
            <span>{{ opt.label }}</span>
          </button>
        </div>

        <!-- Video -->
        <div v-if="isVideoContent" class="space-y-4">
          <h3 class="text-sm font-semibold text-gray-800">Video bài học</h3>
          <div class="mb-3 flex gap-4">
            <label class="flex items-center gap-2">
              <input type="radio" v-model="videoInputType" value="url" class="h-4 w-4" />
              <span class="text-sm">Link URL</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="radio" v-model="videoInputType" value="file" class="h-4 w-4" />
              <span class="text-sm">Upload file</span>
            </label>
          </div>
          <input
            v-if="videoInputType === 'url'"
            v-model="form.video_url"
            type="url"
            class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
            placeholder="https://www.youtube.com/watch?v=..."
          />
          <div v-else class="flex items-center gap-4">
            <input
              ref="videoInput"
              type="file"
              accept="video/*"
              class="hidden"
              @change="onPickVideo"
            />
            <button
              type="button"
              class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
              @click="videoInput?.click()"
            >
              Chọn video
            </button>
            <span v-if="videoFile" class="text-sm text-gray-600">{{ videoFile.name }}</span>
          </div>
        </div>

        <!-- Văn bản -->
        <div v-if="form.content_type === 'text'" class="mt-4 space-y-2">
          <h3 class="text-sm font-semibold text-gray-800">Nội dung văn bản</h3>
          <textarea
            v-model="form.text_content"
            rows="6"
            class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
            placeholder="Nhập nội dung văn bản..."
          ></textarea>
        </div>

        <!-- PDF/Word -->
        <div v-if="form.content_type === 'pdf' || form.content_type === 'document'" class="mt-4 space-y-2">
          <h3 class="text-sm font-semibold text-gray-800">Tài liệu</h3>
          <input
            ref="docInput"
            type="file"
            :accept="form.content_type === 'pdf' ? 'application/pdf' : '.doc,.docx,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document'"
            class="hidden"
            @change="onPickDocument"
          />
          <button
            type="button"
            class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            @click="docInput?.click()"
          >
            Chọn tài liệu
          </button>
          <p v-if="docFile" class="text-sm text-gray-600">{{ docFile.name }}</p>
          <p v-else-if="existingDocumentName" class="text-sm text-gray-600">Đã có: {{ existingDocumentName }}</p>
          <p class="text-xs text-gray-500">PDF/Word ≤ 50MB</p>
        </div>

        <!-- Bài tập -->
        <div v-if="form.content_type === 'exercise'" class="mt-4 space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-semibold text-gray-800">Danh sách câu hỏi</h3>
            <div class="flex gap-2">
              <button
                type="button"
                class="rounded-lg border border-cyan-500 px-3 py-1.5 text-sm font-medium text-cyan-600 hover:bg-cyan-50"
                @click="showAIGenerateModal = true"
              >
                🤖 AI tạo đề
              </button>
              <button
                type="button"
                class="rounded-lg bg-cyan-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-cyan-700"
                @click="addQuestion"
              >
                + Thêm câu hỏi
              </button>
            </div>
          </div>

          <!-- Danh sách câu hỏi -->
          <div v-if="exerciseQuestions.length === 0" class="rounded-xl border-2 border-dashed border-gray-300 bg-gray-50 p-6 text-center">
            <p class="text-gray-500">Chưa có câu hỏi nào. Nhấn "+ Thêm câu hỏi" hoặc "AI tạo đề" để bắt đầu.</p>
          </div>

          <div v-else class="max-h-[500px] overflow-y-auto space-y-4 pr-2">
            <div
              v-for="(question, qIdx) in exerciseQuestions"
              :key="qIdx"
              class="rounded-xl border border-gray-200 bg-gray-50 p-4"
            >
              <div class="mb-3 flex items-start justify-between">
                <span class="rounded bg-cyan-100 px-2 py-0.5 text-xs font-medium text-cyan-700">
                  Câu {{ qIdx + 1 }}
                </span>
                <button
                  type="button"
                  class="text-xs text-rose-600 hover:underline"
                  @click="removeQuestion(qIdx)"
                >
                  Xóa
                </button>
              </div>

              <!-- Loại câu hỏi -->
              <div class="mb-3">
                <label class="mb-1 block text-xs font-medium text-gray-600">Loại câu hỏi</label>
                <select
                  v-model="question.type"
                  class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
                >
                  <option value="mcq">Trắc nghiệm</option>
                  <option value="short_answer">Tự luận ngắn</option>
                  <option value="matching">Nối cặp</option>
                </select>
              </div>

              <!-- Nội dung câu hỏi -->
              <div class="mb-3">
                <label class="mb-1 block text-xs font-medium text-gray-600">Nội dung câu hỏi</label>
                <textarea
                  v-model="question.prompt"
                  rows="2"
                  class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
                  placeholder="Nhập nội dung câu hỏi..."
                ></textarea>
              </div>

              <!-- Đáp án trắc nghiệm -->
              <div v-if="question.type === 'mcq'" class="space-y-2">
                <div class="flex items-center justify-between">
                  <label class="text-xs font-medium text-gray-600">Đáp án (chọn đáp án đúng)</label>
                  <button
                    type="button"
                    class="text-xs text-cyan-600 hover:underline"
                    @click="addChoice(qIdx)"
                  >
                    + Thêm đáp án
                  </button>
                </div>
                <div v-for="(choice, cIdx) in question.choices" :key="cIdx" class="flex items-center gap-2">
                  <input
                    type="radio"
                    :name="'q-' + qIdx + '-correct'"
                    :checked="choice.is_correct"
                    class="h-4 w-4 text-cyan-600"
                    @change="setCorrectChoice(qIdx, cIdx)"
                  />
                  <input
                    v-model="choice.text"
                    type="text"
                    class="flex-1 rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
                    :placeholder="'Đáp án ' + (cIdx + 1)"
                  />
                  <button
                    v-if="question.choices.length > 2"
                    type="button"
                    class="text-xs text-rose-500 hover:underline"
                    @click="removeChoice(qIdx, cIdx)"
                  >
                    Xóa
                  </button>
                </div>
              </div>

              <!-- Đáp án tự luận -->
              <div v-if="question.type === 'short_answer'" class="space-y-2">
                <label class="text-xs font-medium text-gray-600">Đáp án chấp nhận (cách nhau bởi dấu phẩy)</label>
                <input
                  v-model="question.accepted_answers"
                  type="text"
                  class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
                  placeholder="Ví dụ: đáp án 1, đáp án 2, đáp án 3"
                />
                <p class="text-xs text-gray-500">Hệ thống sẽ chấp nhận các đáp án khớp gần đúng</p>
              </div>

              <!-- Nối cặp -->
              <div v-if="question.type === 'matching'" class="space-y-2">
                <div class="flex items-center justify-between">
                  <label class="text-xs font-medium text-gray-600">Các cặp nối</label>
                  <button
                    type="button"
                    class="text-xs text-cyan-600 hover:underline"
                    @click="addMatchingPair(qIdx)"
                  >
                    + Thêm cặp
                  </button>
                </div>
                <div v-for="(pair, pIdx) in question.matching_pairs" :key="pIdx" class="grid grid-cols-2 gap-2">
                  <input
                    v-model="pair.left"
                    type="text"
                    class="rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
                    :placeholder="'Vế trái ' + (pIdx + 1)"
                  />
                  <div class="flex gap-2">
                    <input
                      v-model="pair.right"
                      type="text"
                      class="flex-1 rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
                      :placeholder="'Vế phải ' + (pIdx + 1)"
                    />
                    <button
                      v-if="question.matching_pairs.length > 2"
                      type="button"
                      class="text-xs text-rose-500 hover:underline"
                      @click="removeMatchingPair(qIdx, pIdx)"
                    >
                      Xóa
                    </button>
                  </div>
                </div>
              </div>

              <!-- Điểm -->
              <div class="mt-3">
                <label class="mb-1 block text-xs font-medium text-gray-600">Điểm</label>
                <input
                  v-model.number="question.points"
                  type="number"
                  min="1"
                  class="w-24 rounded-lg border border-gray-300 px-3 py-1.5 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
                />
              </div>
            </div>
          </div>

          <!-- Cài đặt bài tập -->
          <div class="rounded-xl border border-gray-200 bg-white p-4">
            <h4 class="mb-3 text-sm font-semibold text-gray-800">Cài đặt bài tập</h4>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="mb-1 block text-xs font-medium text-gray-600">Thời gian làm bài (phút)</label>
                <input
                  v-model.number="exerciseSettings.duration_minutes"
                  type="number"
                  min="1"
                  class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
                  placeholder="Không giới hạn"
                />
              </div>
              <div>
                <label class="mb-1 block text-xs font-medium text-gray-600">Điểm đạt (%)</label>
                <input
                  v-model.number="exerciseSettings.pass_score"
                  type="number"
                  min="0"
                  max="100"
                  class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
                />
              </div>
              <div>
                <label class="mb-1 block text-xs font-medium text-gray-600">Số lần làm tối đa</label>
                <input
                  v-model.number="exerciseSettings.max_attempts"
                  type="number"
                  min="1"
                  class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
                  placeholder="Không giới hạn"
                />
              </div>
              <div class="flex items-center gap-4">
                <label class="flex items-center gap-2">
                  <input
                    v-model="exerciseSettings.shuffle_questions"
                    type="checkbox"
                    class="h-4 w-4 rounded border-gray-300"
                  />
                  <span class="text-xs text-gray-700">Xáo trộn câu hỏi</span>
                </label>
                <label class="flex items-center gap-2">
                  <input
                    v-model="exerciseSettings.shuffle_choices"
                    type="checkbox"
                    class="h-4 w-4 rounded border-gray-300"
                  />
                  <span class="text-xs text-gray-700">Xáo trộn đáp án</span>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- AI Generate Modal -->
  <div v-if="showAIGenerateModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
    <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
      <div class="mb-4 flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">🤖 AI Tạo đề tự động</h3>
        <button
          type="button"
          class="rounded-lg p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600"
          @click="showAIGenerateModal = false"
        >
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="space-y-4">
        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Chủ đề / Nội dung *</label>
          <textarea
            v-model="aiTopic"
            rows="3"
            class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
            placeholder="Ví dụ: Phép cộng trong phạm vi 100, Bảng cửu chương..."
          ></textarea>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Số câu hỏi</label>
            <select
              v-model="aiQuestionCount"
              class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
            >
              <option :value="3">3 câu</option>
              <option :value="5">5 câu</option>
              <option :value="10">10 câu</option>
            </select>
          </div>
          <div>
            <label class="mb-1 block text-sm font-medium text-gray-700">Độ khó</label>
            <select
              v-model="aiDifficulty"
              class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
            >
              <option value="easy">Dễ</option>
              <option value="medium">Trung bình</option>
              <option value="hard">Khó</option>
            </select>
          </div>
        </div>

        <div class="rounded-lg border border-cyan-200 bg-cyan-50 p-3">
          <p class="text-xs text-cyan-700">
            💡 AI sẽ tạo câu hỏi trắc nghiệm dựa trên chủ đề bạn nhập. 
            Bạn có thể chỉnh sửa sau khi tạo.
          </p>
        </div>
      </div>

      <div class="mt-6 flex justify-end gap-3">
        <button
          type="button"
          class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          @click="showAIGenerateModal = false"
        >
          Hủy
        </button>
        <button
          type="button"
          class="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-medium text-white hover:bg-cyan-700 disabled:opacity-50"
          :disabled="!aiTopic.trim() || aiGenerating"
          @click="generateQuestionsWithAI"
        >
          {{ aiGenerating ? '⏳ Đang tạo...' : '✨ Tạo câu hỏi' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { contentService } from '@/services/content.service'
import http from '@/config/axios'
import { showToast } from '@/utils/toast'

const route = useRoute()
const router = useRouter()

const lessonIdParam = route.params.id as string
const lessonUuid = ref<string>(lessonIdParam) // UUID thực sự từ API
const lessonTitle = ref('')
const loading = ref(true)
const error = ref('')
const saving = ref(false)

const form = ref({
  title: '',
  introduction: '',
  content_type: 'video',
  video_url: '',
  video_file: null as File | null,
  document_file: null as File | null,
  text_content: '',
  requires_exercise_completion: false
})

const contentTypeOptions = [
  { value: 'video', label: 'Video bài giảng', icon: '🎬' },
  { value: 'pdf', label: 'Tài liệu PDF', icon: '📄' },
  { value: 'text', label: 'Văn bản', icon: '📝' },
  { value: 'exercise', label: 'Bài tập', icon: '✏️' },
  { value: 'document', label: 'Tài liệu Word', icon: '📑' },
]

const videoInputType = ref<'url' | 'file'>('url')
const videoInput = ref<HTMLInputElement | null>(null)
const docInput = ref<HTMLInputElement | null>(null)
const videoFile = ref<File | null>(null)
const docFile = ref<File | null>(null)
const existingDocumentName = ref<string>('')

const isVideoContent = computed(() => form.value.content_type === 'video' || form.value.content_type === 'lesson')

// Exercise types
interface ExerciseChoice {
  text: string
  is_correct: boolean
}

interface MatchingPair {
  left: string
  right: string
}

interface ExerciseQuestion {
  type: 'mcq' | 'short_answer' | 'matching'
  prompt: string
  points: number
  choices: ExerciseChoice[]
  accepted_answers: string
  matching_pairs: MatchingPair[]
}

// Exercise state
const exerciseQuestions = ref<ExerciseQuestion[]>([])
const exerciseSettings = ref({
  duration_minutes: null as number | null,
  pass_score: 50,
  max_attempts: null as number | null,
  shuffle_questions: true,
  shuffle_choices: true
})
const existingExerciseId = ref<string | null>(null)

// AI Generate Modal
const showAIGenerateModal = ref(false)
const aiGenerating = ref(false)
const aiTopic = ref('')
const aiQuestionCount = ref(5)
const aiDifficulty = ref<'easy' | 'medium' | 'hard'>('medium')

async function generateQuestionsWithAI() {
  if (!aiTopic.value.trim()) {
    showToast('Vui lòng nhập chủ đề', 'warning')
    return
  }
  
  aiGenerating.value = true
  try {
    const { data } = await http.post('/activities/ai/generate-questions/', {
      title: aiTopic.value,
      description: aiTopic.value,
      count: aiQuestionCount.value,
      level: `Lớp ${form.value.title}`,
      hint: `Độ khó: ${aiDifficulty.value === 'easy' ? 'Dễ' : aiDifficulty.value === 'medium' ? 'Trung bình' : 'Khó'}`
    })
    
    // Parse text response từ AI
    let questions: any[] = []
    if (data.text) {
      try {
        let jsonText = data.text.trim()
        if (jsonText.startsWith('```json')) {
          jsonText = jsonText.replace(/^```json\s*/, '').replace(/\s*```$/, '')
        } else if (jsonText.startsWith('```')) {
          jsonText = jsonText.replace(/^```\s*/, '').replace(/\s*```$/, '')
        }
        const parsed = JSON.parse(jsonText)
        questions = parsed.questions || []
      } catch (parseErr) {
        console.error('Parse AI response error:', parseErr, data.text)
      }
    } else if (data.questions) {
      questions = data.questions
    }
    
    // Map AI response to our format
    const generatedQuestions: ExerciseQuestion[] = questions.map((q: any) => {
      let correctIdx = 0
      if (q.correct_indices && q.correct_indices.length > 0) {
        correctIdx = q.correct_indices[0]
      } else if (typeof q.correct_index === 'number') {
        correctIdx = q.correct_index
      }
      
      return {
        type: 'mcq' as const,
        prompt: q.text || q.prompt || '',
        points: q.score || 1,
        choices: (q.choices || q.options || []).map((c: any, idx: number) => ({
          text: typeof c === 'string' ? c : c.text,
          is_correct: idx === correctIdx
        })),
        accepted_answers: '',
        matching_pairs: []
      }
    })
    
    if (generatedQuestions.length > 0) {
      // Nếu câu hỏi đầu tiên trống thì thay thế, không thì thêm mới
      if (exerciseQuestions.value.length === 1 && !exerciseQuestions.value[0].prompt.trim()) {
        exerciseQuestions.value = generatedQuestions
      } else {
        // Lọc bỏ các câu hỏi trống trước khi thêm
        exerciseQuestions.value = exerciseQuestions.value.filter(q => q.prompt.trim())
        exerciseQuestions.value.push(...generatedQuestions)
      }
      showAIGenerateModal.value = false
      aiTopic.value = ''
      showToast(`Đã tạo ${generatedQuestions.length} câu hỏi!`, 'success')
    } else {
      showToast('AI không tạo được câu hỏi. Vui lòng thử lại.', 'warning')
    }
  } catch (e: any) {
    console.error('AI generate error:', e)
    showToast('Không thể tạo câu hỏi: ' + (e.response?.data?.detail || e.message), 'error')
  } finally {
    aiGenerating.value = false
  }
}

// Exercise helper functions
function createDefaultQuestion(): ExerciseQuestion {
  return {
    type: 'mcq',
    prompt: '',
    points: 1,
    choices: [
      { text: '', is_correct: true },
      { text: '', is_correct: false },
      { text: '', is_correct: false },
      { text: '', is_correct: false }
    ],
    accepted_answers: '',
    matching_pairs: [
      { left: '', right: '' },
      { left: '', right: '' }
    ]
  }
}

function addQuestion() {
  exerciseQuestions.value.push(createDefaultQuestion())
}

function removeQuestion(idx: number) {
  exerciseQuestions.value.splice(idx, 1)
}

function addChoice(qIdx: number) {
  exerciseQuestions.value[qIdx].choices.push({ text: '', is_correct: false })
}

function removeChoice(qIdx: number, cIdx: number) {
  exerciseQuestions.value[qIdx].choices.splice(cIdx, 1)
}

function setCorrectChoice(qIdx: number, cIdx: number) {
  exerciseQuestions.value[qIdx].choices = exerciseQuestions.value[qIdx].choices.map((c, i) => ({
    ...c,
    is_correct: i === cIdx
  }))
}

function addMatchingPair(qIdx: number) {
  exerciseQuestions.value[qIdx].matching_pairs.push({ left: '', right: '' })
}

function removeMatchingPair(qIdx: number, pIdx: number) {
  exerciseQuestions.value[qIdx].matching_pairs.splice(pIdx, 1)
}

async function loadLesson() {
  try {
    const { data } = await http.get(`/content/lessons/${lessonIdParam}/`)
    // Ưu tiên lessonIdParam từ URL vì nó luôn là UUID hợp lệ
    // data.id có thể không phải UUID trong một số trường hợp
    const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i
    if (data.id && uuidPattern.test(String(data.id))) {
      lessonUuid.value = String(data.id)
    } else {
      lessonUuid.value = lessonIdParam
    }
    lessonTitle.value = data.title
    form.value = {
      title: data.title || '',
      introduction: data.introduction || '',
      content_type: data.content_type || 'video',
      video_url: data.video_url || '',
      video_file: null,
      document_file: null,
      text_content: data.text_content || '',
      requires_exercise_completion: data.requires_exercise_completion || false
    }
    videoInputType.value = data.video_url ? 'url' : 'file'
    existingDocumentName.value = data.document_file || ''
    // Transcript được tạo tự động, không cần load vào UI

    // Load exercises if content_type is exercise
    if (data.content_type === 'exercise') {
      try {
        const { data: exData } = await http.get(`/activities/exercises/?lesson_id=${lessonIdParam}`)
        const exercises = Array.isArray(exData) ? exData : exData.results || []
        if (exercises.length > 0) {
          const exercise = exercises[0]
          existingExerciseId.value = exercise.id
          
          // Load settings
          if (exercise.settings) {
            exerciseSettings.value = {
              duration_minutes: exercise.settings.duration_seconds ? Math.floor(exercise.settings.duration_seconds / 60) : null,
              pass_score: exercise.settings.pass_score || 50,
              max_attempts: exercise.settings.max_attempts || null,
              shuffle_questions: exercise.settings.shuffle_questions ?? true,
              shuffle_choices: exercise.settings.shuffle_choices ?? true
            }
          }
          
          // Load questions
          if (exercise.questions && exercise.questions.length > 0) {
            exerciseQuestions.value = exercise.questions.map((q: any) => {
              const qType = q.meta?.type || 'mcq'
              return {
                type: qType,
                prompt: q.prompt || '',
                points: q.meta?.points || q.meta?.score || 1,
                choices: qType === 'mcq' ? (q.choices || []).map((c: any) => ({
                  text: c.text || '',
                  is_correct: c.is_correct || false
                })) : [
                  { text: '', is_correct: true },
                  { text: '', is_correct: false }
                ],
                accepted_answers: qType === 'short_answer' ? (q.meta?.accepted_answers || []).join(', ') : '',
                matching_pairs: qType === 'matching'
                  ? (() => {
                    // Prefer the original text pairs if backend returned them
                    if (Array.isArray(q.meta?.pairs) && q.meta.pairs.length > 0) {
                      return q.meta.pairs.map((p: any) => ({
                        left: p.left || '',
                        right: p.right || ''
                      }))
                    }
                    // Fallback: map correct_pairs keys (L1/R1) to keep some value
                    return Object.entries(q.meta?.correct_pairs || {}).map(([left, right]) => ({
                      left,
                      right: String(right)
                    }))
                  })()
                  : [{ left: '', right: '' }, { left: '', right: '' }]
              }
            })
          }
        }
      } catch (e) {
        console.error('Error loading exercises:', e)
      }
    }
  } catch (e: any) {
    error.value = e?.message || 'Không thể tải thông tin bài học'
  } finally {
    loading.value = false
  }
}

function onPickVideo(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  if (!file.type.startsWith('video/')) {
    showToast('Vui lòng chọn file video', 'warning')
    return
  }
  videoFile.value = file
  form.value.video_file = file
}

function onPickDocument(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  // 500MB max
  if (file.size > 500 * 1024 * 1024) {
    showToast('File quá lớn (tối đa 500MB)', 'warning')
    return
  }
  docFile.value = file
  form.value.document_file = file
}

async function saveLesson() {
  // Ngăn gửi request nhiều lần
  if (saving.value) return
  saving.value = true
  try {
    const fd = new FormData()
    fd.append('title', form.value.title)
    fd.append('content_type', form.value.content_type)
    if (form.value.introduction) {
      fd.append('introduction', form.value.introduction)
    }
    if (form.value.content_type === 'video' || form.value.content_type === 'lesson') {
      if (videoInputType.value === 'url' && form.value.video_url) {
        fd.append('video_url', form.value.video_url)
      } else if (videoFile.value) {
        fd.append('video_file', videoFile.value)
      }
    }
    if (form.value.content_type === 'pdf' || form.value.content_type === 'document') {
      if (docFile.value) {
        fd.append('document_file', docFile.value)
      }
    }
    if (form.value.content_type === 'text' && form.value.text_content) {
      fd.append('text_content', form.value.text_content)
    }
    // Transcript được tạo tự động ở backend, không cần gửi từ frontend
    fd.append('requires_exercise_completion', String(form.value.requires_exercise_completion))
    
    // Save lesson (backend sẽ tự động tạo transcript nếu cần)
    await http.patch(`/content/lessons/${lessonIdParam}/`, fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    // Save exercise if content_type is exercise
    if (form.value.content_type === 'exercise' && exerciseQuestions.value.length > 0) {
      // Validate questions before saving
      for (let i = 0; i < exerciseQuestions.value.length; i++) {
        const q = exerciseQuestions.value[i]
        if (!q.prompt.trim()) {
          showToast(`Câu hỏi ${i + 1}: Vui lòng nhập nội dung câu hỏi`, 'warning')
          saving.value = false
          return
        }
        if (q.type === 'mcq') {
          const validChoices = q.choices.filter(c => c.text.trim())
          if (validChoices.length < 2) {
            showToast(`Câu hỏi ${i + 1}: Cần ít nhất 2 đáp án`, 'warning')
            saving.value = false
            return
          }
          if (!validChoices.some(c => c.is_correct)) {
            showToast(`Câu hỏi ${i + 1}: Vui lòng chọn đáp án đúng`, 'warning')
            saving.value = false
            return
          }
        }
        if (q.type === 'matching') {
          const validPairs = q.matching_pairs.filter(p => p.left.trim() && p.right.trim())
          if (validPairs.length < 1) {
            showToast(`Câu hỏi ${i + 1}: Cần ít nhất 1 cặp nối`, 'warning')
            saving.value = false
            return
          }
        }
      }

      // Determine exercise type based on first question
      const firstQuestionType = exerciseQuestions.value[0]?.type || 'mcq'
      // Sử dụng UUID thực sự từ API, không phải từ URL param
      // Validate UUID format
      const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i
      let validLessonId = lessonUuid.value
      if (!uuidPattern.test(validLessonId)) {
        validLessonId = lessonIdParam
      }
      if (!uuidPattern.test(validLessonId)) {
        showToast('Không tìm thấy ID bài học hợp lệ, vui lòng tải lại trang', 'error')
        saving.value = false
        return
      }
      console.log('Saving exercise with lesson ID:', validLessonId, 'lessonUuid:', lessonUuid.value, 'lessonIdParam:', lessonIdParam)
      const exercisePayload: any = {
        title: form.value.title || 'Bài tập',
        type: firstQuestionType,
        lesson: validLessonId,
        published: true,
        settings: {
          duration_seconds: exerciseSettings.value.duration_minutes ? exerciseSettings.value.duration_minutes * 60 : null,
          pass_score: exerciseSettings.value.pass_score || 50,
          max_attempts: exerciseSettings.value.max_attempts || null,
          shuffle_questions: exerciseSettings.value.shuffle_questions,
          shuffle_choices: exerciseSettings.value.shuffle_choices
        },
        questions: exerciseQuestions.value.map((q) => {
          const questionPayload: any = {
            prompt: q.prompt,
            meta: {
              type: q.type,
              points: q.points
            }
          }

          if (q.type === 'mcq') {
            questionPayload.choices = q.choices
              .filter(c => c.text.trim())
              .map((c, idx) => ({
                text: c.text.trim(),
                is_correct: c.is_correct,
                position: idx
              }))
          } else if (q.type === 'short_answer') {
            questionPayload.meta.accepted_answers = q.accepted_answers
              .split(',')
              .map(s => s.trim())
              .filter(Boolean)
            questionPayload.meta.similarity_threshold = 0.85
            // Short answer không cần choices
            questionPayload.choices = []
          } else if (q.type === 'matching') {
            const validPairs = q.matching_pairs.filter(p => p.left.trim() && p.right.trim())
            const correct_pairs: Record<string, string> = {}
            // Tạo choices từ các cặp nối (lưu cả left và right)
            const choices: any[] = []
            validPairs.forEach((p, idx) => {
              const leftId = `L${idx + 1}`
              const rightId = `R${idx + 1}`
              correct_pairs[leftId] = rightId
              // Thêm vế trái
              choices.push({
                text: p.left.trim(),
                is_correct: false,
                position: idx * 2
              })
              // Thêm vế phải
              choices.push({
                text: p.right.trim(),
                is_correct: false,
                position: idx * 2 + 1
              })
            })
            questionPayload.meta.correct_pairs = correct_pairs
            questionPayload.meta.pairs = validPairs.map(p => ({
              left: p.left.trim(),
              right: p.right.trim()
            }))
            questionPayload.choices = choices
          }

          return questionPayload
        })
      }

      try {
        console.log('Exercise payload:', JSON.stringify(exercisePayload, null, 2))
        if (existingExerciseId.value) {
          // Update existing exercise
          await http.patch(`/activities/exercises/${existingExerciseId.value}/`, exercisePayload)
        } else {
          // Create new exercise
          await http.post('/activities/exercises/', exercisePayload)
        }
      } catch (e: any) {
        console.error('Error saving exercise:', e)
        console.error('Error response:', e?.response?.data)
        const errorMsg = e?.response?.data?.detail || e?.response?.data?.message || JSON.stringify(e?.response?.data) || 'Lỗi không xác định'
        showToast(`Lỗi lưu bài tập: ${errorMsg}`, 'error')
        saving.value = false
        return
      }
    }
    
    showToast('Đã lưu thay đổi thành công!', 'success')
    router.back()
  } catch (e: any) {
    showToast(e?.message || 'Không thể lưu thay đổi', 'error')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadLesson()
})
</script>
