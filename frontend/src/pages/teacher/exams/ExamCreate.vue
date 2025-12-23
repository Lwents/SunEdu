<!-- src/pages/teacher/exams/ExamCreate.vue -->
<template>
  <div class="min-h-screen w-full overflow-x-hidden bg-slate-50">
    <main class="w-full mx-auto max-w-screen-2xl px-4 py-6 sm:px-6 md:px-10 md:py-8">
      <!-- Header -->
      <div class="mb-5 flex items-center justify-between">
        <h1 class="text-2xl font-semibold">Tạo bài kiểm tra mới</h1>
        <button
          class="rounded-xl border px-4 py-2 text-sm hover:bg-slate-50"
          @click="router.back()"
        >
          Hủy
        </button>
      </div>

      <form @submit.prevent="submit" class="space-y-6">
        <!-- Thông tin cơ bản -->
        <div class="rounded-2xl border border-slate-200 bg-white p-6">
          <h2 class="mb-4 text-lg font-semibold">Thông tin cơ bản</h2>
          <div class="grid grid-cols-1 gap-4 md:grid-cols-2">
            <div class="md:col-span-2">
              <label class="mb-1 block text-sm font-medium">Tên đề thi <span class="text-rose-600">*</span></label>
              <input
                v-model.trim="form.title"
                type="text"
                required
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none focus:border-sky-400 focus:ring-2 focus:ring-sky-500/30"
                placeholder="Ví dụ: Kiểm tra giữa kỳ môn Toán lớp 3"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Khóa học áp dụng <span class="text-rose-600">*</span></label>
              <select
                v-model="form.courseId"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none focus:border-sky-400 focus:ring-2 focus:ring-sky-500/30"
                :disabled="loadingCourses"
              >
                <option value="" disabled>Chọn khóa học</option>
                <option v-for="c in courses" :key="c.id" :value="String(c.id)">
                  {{ c.title }} (Lớp {{ c.grade }})
                </option>
              </select>
              <p class="mt-1 text-xs text-slate-500">Chỉ học sinh đã ghi danh khóa này mới thấy đề thi.</p>
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Thời gian (phút)</label>
              <input
                v-model.number="durationMin"
                type="number"
                min="1"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none focus:border-sky-400 focus:ring-2 focus:ring-sky-500/30"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Điểm đạt tối thiểu</label>
              <input
                v-model.number="form.passScore"
                type="number"
                min="0"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none focus:border-sky-400 focus:ring-2 focus:ring-sky-500/30"
              />
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Số lần làm tối đa</label>
              <input
                v-model.number="form.maxAttempts"
                type="number"
                min="1"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none focus:border-sky-400 focus:ring-2 focus:ring-sky-500/30"
                placeholder="Ví dụ: 1"
              />
              <p class="mt-1 text-xs text-slate-500">0 nghĩa là không giới hạn; mặc định 1 lần.</p>
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Trạng thái</label>
              <select
                v-model="form.status"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none focus:border-sky-400 focus:ring-2 focus:ring-sky-500/30"
                @change="onStatusChange"
              >
                <option value="draft">Nháp</option>
                <option value="scheduled">Đã lên lịch</option>
                <option value="published">Đã phát hành</option>
              </select>
            </div>

            <div v-if="form.status === 'scheduled'" class="md:col-span-2 space-y-4">
              <div>
                <label class="mb-1 block text-sm font-medium">Thời gian phát hành <span class="text-rose-600">*</span></label>
                <input
                  v-model="scheduledAtLocal"
                  type="datetime-local"
                  required
                  :min="minDateTime"
                  class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none focus:border-sky-400 focus:ring-2 focus:ring-sky-500/30"
                />
                <p class="mt-1 text-xs text-slate-500">Đề thi sẽ tự động phát hành vào thời gian đã chọn</p>
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium">Thời gian kết thúc <span class="text-rose-600">*</span></label>
                <input
                  v-model="endAtLocal"
                  type="datetime-local"
                  required
                  :min="scheduledAtLocal || minDateTime"
                  class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none focus:border-sky-400 focus:ring-2 focus:ring-sky-500/30"
                />
                <p class="mt-1 text-xs text-slate-500">Sau thời gian này, học sinh sẽ không thể làm bài thi nữa</p>
              </div>
            </div>

            <div class="md:col-span-2">
              <label class="mb-1 block text-sm font-medium">Mô tả</label>
              <textarea
                v-model.trim="form.description"
                rows="3"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none focus:border-sky-400 focus:ring-2 focus:ring-sky-500/30"
                placeholder="Mô tả về bài kiểm tra..."
              ></textarea>
            </div>

            <div class="md:col-span-2 flex flex-wrap gap-4">
              <label class="flex items-center gap-2">
                <input
                  v-model="form.shuffleQuestions"
                  type="checkbox"
                  class="rounded border-slate-300"
                />
                <span class="text-sm">Xáo trộn thứ tự câu hỏi</span>
              </label>
              <label class="flex items-center gap-2">
                <input
                  v-model="form.shuffleChoices"
                  type="checkbox"
                  class="rounded border-slate-300"
                />
                <span class="text-sm">Xáo trộn thứ tự đáp án</span>
              </label>
            </div>
            
            <div class="md:col-span-2">
              <label class="mb-1 block text-sm font-medium">Hiển thị đáp án</label>
              <select
                v-model="form.showAnswers"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none focus:border-sky-400 focus:ring-2 focus:ring-sky-500/30"
              >
                <option value="always">Luôn hiển thị sau khi nộp bài</option>
                <option value="after_duration">Chỉ hiển thị sau khi hết thời gian làm bài</option>
                <option value="after_end">Chỉ hiển thị sau khi hết hạn bài thi</option>
                <option value="never">Không hiển thị đáp án</option>
              </select>
              <p class="mt-1 text-xs text-slate-500">
                {{ form.showAnswers === 'after_duration' 
                  ? `Học sinh sẽ xem được đáp án sau ${durationMin} phút kể từ khi bắt đầu làm bài`
                  : form.showAnswers === 'after_end'
                  ? 'Học sinh sẽ xem được đáp án sau thời gian kết thúc bài thi'
                  : form.showAnswers === 'never'
                  ? 'Học sinh sẽ không bao giờ xem được đáp án'
                  : 'Học sinh sẽ xem được đáp án ngay sau khi nộp bài' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Danh sách câu hỏi -->
        <div class="rounded-2xl border border-slate-200 bg-white p-6">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-lg font-semibold">Câu hỏi ({{ form.questions?.length || 0 }})</h2>
            <div class="flex items-center gap-2">
              <button
                type="button"
                class="rounded-xl bg-sky-600 px-4 py-2 text-sm font-semibold text-white hover:bg-sky-700"
                @click="showAddQuestion = true"
              >
                + Thêm câu hỏi
              </button>
            </div>
          </div>

          <div v-if="!form.questions || form.questions.length === 0" class="py-8 text-center text-slate-500">
            Chưa có câu hỏi nào. Nhấn "Thêm câu hỏi" để bắt đầu.
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="(q, idx) in form.questions"
              :key="q.id"
              class="rounded-xl border border-slate-200 p-4"
            >
              <div class="mb-3 flex items-start justify-between">
                <div class="flex-1">
                  <div class="mb-2 flex items-center gap-2">
                    <span class="font-semibold">Câu {{ idx + 1 }}</span>
                    <span class="rounded-full bg-slate-100 px-2 py-0.5 text-xs">{{ q.type.toUpperCase() }}</span>
                    <span class="text-sm text-slate-500">{{ q.score }} điểm</span>
                  </div>
                  <p class="text-sm">{{ q.text }}</p>
                </div>
                <div class="flex gap-2">
                  <button
                    type="button"
                    class="rounded-lg border px-2 py-1 text-xs hover:bg-slate-50"
                    @click="editQuestion(idx)"
                  >
                    Sửa
                  </button>
                  <button
                    type="button"
                    class="rounded-lg border px-2 py-1 text-xs text-rose-600 hover:bg-rose-50"
                    @click="removeQuestion(idx)"
                  >
                    Xóa
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-3">
          <button
            type="button"
            class="rounded-xl border px-6 py-2.5 text-sm font-medium hover:bg-slate-50"
            @click="router.back()"
          >
            Hủy
          </button>
          <button
            type="submit"
            :disabled="submitting || !canSubmit"
            class="rounded-xl bg-sky-600 px-6 py-2.5 text-sm font-semibold text-white hover:bg-sky-700 disabled:opacity-50"
          >
            {{ submitting ? 'Đang lưu...' : 'Lưu đề thi' }}
          </button>
        </div>
      </form>

      <!-- Modal thêm/sửa câu hỏi -->
      <div
        v-if="showAddQuestion || editingQuestionIndex !== null"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      >
        <div class="w-full max-w-2xl rounded-2xl bg-white p-6 max-h-[90vh] overflow-y-auto">
          <h3 class="mb-4 text-lg font-semibold">
            {{ editingQuestionIndex !== null ? 'Sửa câu hỏi' : 'Thêm câu hỏi' }}
          </h3>

          <div class="space-y-4">
            <div>
              <label class="mb-1 block text-sm font-medium">Loại câu hỏi</label>
              <select
                v-model="currentQuestion.type"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none"
              >
                <option value="single">Trắc nghiệm (1 đáp án)</option>
                <option value="multi">Trắc nghiệm (nhiều đáp án)</option>
                <option value="boolean">Đúng/Sai</option>
                <option value="fill">Điền từ</option>
                <option value="match">Nối cặp</option>
                <option value="order">Sắp xếp</option>
              </select>
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Nội dung câu hỏi <span class="text-rose-600">*</span></label>
              <textarea
                v-model.trim="currentQuestion.text"
                rows="3"
                required
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none"
                placeholder="Nhập nội dung câu hỏi..."
              ></textarea>
            </div>

            <div>
              <label class="mb-1 block text-sm font-medium">Điểm số</label>
              <input
                v-model.number="currentQuestion.score"
                type="number"
                min="0.5"
                step="0.5"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none"
              />
            </div>

            <!-- Choices cho single/multi -->
            <div v-if="currentQuestion.type === 'single' || currentQuestion.type === 'multi'">
              <label class="mb-2 block text-sm font-medium">Đáp án</label>
              <div class="space-y-2">
                <div
                  v-for="(choice, i) in currentQuestion.choices"
                  :key="i"
                  class="flex items-center gap-2"
                >
                  <input
                    v-model="choice.text"
                    type="text"
                    class="flex-1 rounded-lg border border-slate-200 px-3 py-1.5 text-sm outline-none"
                    :placeholder="`Đáp án ${i + 1}`"
                  />
                  <label class="flex items-center gap-1">
                    <input
                      v-model="currentQuestion.answer"
                      type="checkbox"
                      :value="choice.id"
                      :class="currentQuestion.type === 'single' ? 'rounded-full' : 'rounded'"
                    />
                    <span class="text-xs">Đúng</span>
                  </label>
                  <button
                    v-if="currentQuestion.choices && currentQuestion.choices.length > 2"
                    type="button"
                    class="rounded-lg border px-2 py-1 text-xs text-rose-600 hover:bg-rose-50"
                    @click="removeChoice(i)"
                  >
                    Xóa
                  </button>
                </div>
                <button
                  type="button"
                  class="rounded-lg border px-3 py-1.5 text-sm hover:bg-slate-50"
                  @click="addChoice"
                >
                  + Thêm đáp án
                </button>
              </div>
            </div>

            <!-- Boolean -->
            <div v-if="currentQuestion.type === 'boolean'">
              <label class="mb-1 block text-sm font-medium">Đáp án đúng</label>
              <select
                v-model="currentQuestion.answer"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none"
              >
                <option :value="true">Đúng</option>
                <option :value="false">Sai</option>
              </select>
            </div>

            <!-- Fill -->
            <div v-if="currentQuestion.type === 'fill'">
              <label class="mb-1 block text-sm font-medium">Số chỗ trống</label>
              <input
                v-model.number="currentQuestion.blanks"
                type="number"
                min="1"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none"
              />
              <label class="mt-2 block text-sm font-medium">Đáp án (mỗi đáp án một dòng)</label>
              <textarea
                v-model="fillAnswersText"
                rows="3"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none"
                placeholder="Đáp án 1&#10;Đáp án 2"
              ></textarea>
            </div>

            <!-- Match -->
            <div v-if="currentQuestion.type === 'match'">
              <label class="mb-2 block text-sm font-medium">Các cặp nối</label>
              <div class="space-y-2">
                <div
                  v-for="(pair, i) in currentQuestion.pairs"
                  :key="i"
                  class="flex items-center gap-2"
                >
                  <input
                    v-model="pair.left"
                    type="text"
                    class="flex-1 rounded-lg border border-slate-200 px-3 py-1.5 text-sm outline-none"
                    placeholder="Bên trái"
                  />
                  <span>→</span>
                  <input
                    v-model="pair.right"
                    type="text"
                    class="flex-1 rounded-lg border border-slate-200 px-3 py-1.5 text-sm outline-none"
                    placeholder="Bên phải"
                  />
                  <button
                    v-if="currentQuestion.pairs && currentQuestion.pairs.length > 2"
                    type="button"
                    class="rounded-lg border px-2 py-1 text-xs text-rose-600 hover:bg-rose-50"
                    @click="removePair(i)"
                  >
                    Xóa
                  </button>
                </div>
                <button
                  type="button"
                  class="rounded-lg border px-3 py-1.5 text-sm hover:bg-slate-50"
                  @click="addPair"
                >
                  + Thêm cặp
                </button>
              </div>
            </div>

            <!-- Order -->
            <div v-if="currentQuestion.type === 'order'">
              <label class="mb-2 block text-sm font-medium">Các mục cần sắp xếp (mỗi mục một dòng)</label>
              <textarea
                v-model="orderItemsText"
                rows="4"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none"
                placeholder="Mục 1&#10;Mục 2&#10;Mục 3"
              ></textarea>
            </div>
          </div>

          <div class="mt-6 flex justify-end gap-3">
            <button
              type="button"
          class="rounded-xl border px-4 py-2 text-sm hover:bg-slate-50"
          @click="closeQuestionModal"
        >
          Hủy
        </button>
        <button
          type="button"
          class="rounded-xl border px-4 py-2 text-sm text-sky-700 hover:bg-sky-50"
          @click="openAiFromModal"
        >
          Tạo bằng AI
        </button>
        <button
          type="button"
          class="rounded-xl bg-sky-600 px-4 py-2 text-sm font-semibold text-white hover:bg-sky-700"
          @click="saveQuestion"
        >
              Lưu
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>

  <!-- Modal cấu hình AI -->
  <transition name="fade">
    <div
      v-if="aiDialogOpen"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
    >
      <div class="w-full max-w-lg rounded-2xl bg-white p-6">
        <div class="mb-4 flex items-center justify-between">
          <h3 class="text-lg font-semibold">Tạo câu hỏi bằng AI</h3>
          <button class="text-sm text-slate-500 hover:text-slate-700" @click="aiDialogOpen = false">Đóng</button>
        </div>

        <div class="space-y-4">
          <div>
            <label class="mb-1 block text-sm font-medium">Số câu cần tạo</label>
            <input
              v-model.number="aiCount"
              type="number"
              min="1"
              max="10"
              class="w-28 rounded-lg border border-slate-200 px-3 py-2 text-sm outline-none"
            />
            <p class="mt-1 text-xs text-slate-500">Tối đa 10 câu/lần.</p>
          </div>

          <div>
            <label class="mb-1 block text-sm font-medium">Mô tả mong muốn (tùy chọn)</label>
            <textarea
              v-model.trim="aiHint"
              rows="3"
              class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm outline-none"
              placeholder="Ví dụ: tập trung kiến thức phép cộng, độ khó vừa phải..."
            ></textarea>
          </div>

          <div>
            <label class="mb-1 block text-sm font-medium">Loại câu hỏi</label>
            <select
              v-model="aiType"
              class="w-full rounded-lg border border-slate-200 px-3 py-2 text-sm outline-none"
            >
              <option value="single">Trắc nghiệm 1 đáp án</option>
              <option value="multi">Trắc nghiệm nhiều đáp án</option>
              <option value="boolean">Đúng/Sai</option>
              <option value="fill">Điền từ</option>
              <option value="match">Nối cặp</option>
              <option value="order">Sắp xếp</option>
              <option value="auto">Tự chọn (AI quyết định)</option>
            </select>
            <p class="mt-1 text-xs text-slate-500">AI hỗ trợ trắc nghiệm, đúng/sai, điền từ, nối cặp, sắp xếp.</p>
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-2">
          <button
            type="button"
            class="rounded-lg border px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
            @click="aiDialogOpen = false"
          >
            Hủy
          </button>
          <button
            type="button"
            class="rounded-lg bg-sky-600 px-4 py-2 text-sm font-semibold text-white hover:bg-sky-700 disabled:opacity-60"
            :disabled="aiGenerating"
            @click="generateQuestionsWithAI"
          >
            {{ aiGenerating ? 'Đang tạo...' : 'Tạo câu hỏi' }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { examService, type ExamDetail, type Question, type QType, type Level, type ExamStatus } from '@/services/exam.service'
import { courseService, type CourseSummary } from '@/services/course.service'
import { useAuthStore } from '@/store/auth.store'
import { showToast } from '@/utils/toast'
import { showConfirm } from '@/utils/confirm'
import http from '@/config/axios'

const router = useRouter()

const loadingCourses = ref(false)
const submitting = ref(false)
const showAddQuestion = ref(false)
const editingQuestionIndex = ref<number | null>(null)
const aiGenerating = ref(false)
const aiCount = ref(5)
const aiType = ref<QType | 'auto'>('single') // Loại câu hỏi AI sinh
const aiDialogOpen = ref(false)
const aiHint = ref('')

function openAiFromModal() {
  closeQuestionModal()
  // Nếu đang ở modal câu hỏi, ưu tiên loại hiện tại (chỉ áp dụng với loại AI hỗ trợ)
  if (['single', 'multi', 'boolean'].includes(currentQuestion.type as string)) {
    aiType.value = currentQuestion.type as QType
  } else {
    aiType.value = 'single'
  }
  aiDialogOpen.value = true
}

const form = reactive<Partial<ExamDetail> & { showAnswers?: string }>({
  title: '',
  level: 'Khối 1' as Level,
  courseId: '',
  durationSec: 1800,
  passScore: 10,
  maxAttempts: 1,
  status: 'draft' as ExamStatus,
  description: '',
  shuffleQuestions: true,
  shuffleChoices: true,
  showAnswers: 'always',
  questions: [],
  scheduledAt: undefined,
  endAt: undefined,
})

const durationMin = computed({
  get: () => Math.round((form.durationSec || 0) / 60),
  set: (val) => { form.durationSec = val * 60 }
})

const authStore = useAuthStore()
const courses = ref<CourseSummary[]>([])

// Scheduled datetime handling
const scheduledAtLocal = ref('')
const endAtLocal = ref('')
const minDateTime = computed(() => {
  const now = new Date()
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
  return now.toISOString().slice(0, 16)
})

async function loadCourses() {
  loadingCourses.value = true
  try {
    const teacherId = authStore.user?.id
    const { items } = await courseService.list({ teacherId, pageSize: 200 })
    // Coerce id to string so select v-model matches option values consistently
    courses.value = (items || []).map((c) => ({ ...c, id: String(c.id) })) as CourseSummary[]
  } catch (e: any) {
    console.error('Load courses error:', e)
    showToast('Không tải được danh sách khóa học', 'error')
  } finally {
    loadingCourses.value = false
  }
}

watch(() => form.courseId, (val) => {
  const found = courses.value.find(c => String(c.id) === String(val))
  if (found?.grade) {
    form.level = (`Khối ${found.grade}`) as Level
  }
})

function onStatusChange() {
  if (form.status === 'scheduled' && !scheduledAtLocal.value) {
    // Set default to 1 hour from now
    const future = new Date()
    future.setHours(future.getHours() + 1)
    scheduledAtLocal.value = future.toISOString().slice(0, 16)
    
    // Set default end time to 1 day after start time
    const endTime = new Date(future)
    endTime.setDate(endTime.getDate() + 1)
    endAtLocal.value = endTime.toISOString().slice(0, 16)
  } else if (form.status !== 'scheduled') {
    scheduledAtLocal.value = ''
    endAtLocal.value = ''
    form.scheduledAt = undefined
    form.endAt = undefined
  }
}

watch(scheduledAtLocal, (val) => {
  if (val && form.status === 'scheduled') {
    // Convert local datetime to ISO string
    const date = new Date(val)
    form.scheduledAt = date.toISOString()
    
    // Ensure end time is after start time
    if (endAtLocal.value && new Date(endAtLocal.value) <= date) {
      const endTime = new Date(date)
      endTime.setDate(endTime.getDate() + 1)
      endAtLocal.value = endTime.toISOString().slice(0, 16)
    }
  } else {
    form.scheduledAt = undefined
  }
})

watch(endAtLocal, (val) => {
  if (val && form.status === 'scheduled') {
    // Convert local datetime to ISO string
    const date = new Date(val)
    form.endAt = date.toISOString()
    
    // Validate that end time is after start time
    if (scheduledAtLocal.value && date <= new Date(scheduledAtLocal.value)) {
      showToast('Thời gian kết thúc phải sau thời gian phát hành', 'warning')
      const startTime = new Date(scheduledAtLocal.value)
      startTime.setDate(startTime.getDate() + 1)
      endAtLocal.value = startTime.toISOString().slice(0, 16)
      form.endAt = startTime.toISOString()
    }
  } else {
    form.endAt = undefined
  }
})

const canSubmit = computed(() => {
  return form.title && form.courseId && form.questions && form.questions.length > 0
})

function makeId(prefix: string) {
  return `${prefix}_${Date.now()}_${Math.random().toString(36).slice(2, 7)}`
}

const currentQuestion = reactive<Partial<Question> & { 
  choices?: Array<{ id: string; text: string }>; 
  pairs?: Array<{ left: string; right: string }>;
  answer?: string[] | boolean;
  items?: string[];
  blanks?: number;
}>({
  id: '',
  type: 'single',
  text: '',
  score: 1,
  answer: [],
  choices: [{ id: 'c1', text: '' }, { id: 'c2', text: '' }],
})

const fillAnswersText = ref('')
const orderItemsText = ref('')

function resetQuestion() {
  currentQuestion.id = makeId('q')
  currentQuestion.type = 'single'
  currentQuestion.text = ''
  currentQuestion.score = 1
  currentQuestion.answer = []
  currentQuestion.choices = [{ id: 'c1', text: '' }, { id: 'c2', text: '' }]
  currentQuestion.pairs = [{ left: '', right: '' }, { left: '', right: '' }]
  currentQuestion.items = []
  currentQuestion.blanks = 2
  fillAnswersText.value = ''
  orderItemsText.value = ''
}

onMounted(() => {
  resetQuestion()
  currentQuestion.id = makeId('q')
  loadCourses()
})

watch(() => currentQuestion.type, (newType) => {
  if (newType === 'single' || newType === 'multi') {
    if (!currentQuestion.choices || currentQuestion.choices.length < 2) {
      currentQuestion.choices = [{ id: 'c1', text: '' }, { id: 'c2', text: '' }]
    }
    if (newType === 'single') {
      currentQuestion.answer = []
    }
  } else if (newType === 'fill') {
    currentQuestion.blanks = 2
    fillAnswersText.value = ''
  } else if (newType === 'match') {
    if (!currentQuestion.pairs || currentQuestion.pairs.length < 2) {
      currentQuestion.pairs = [{ left: '', right: '' }, { left: '', right: '' }]
    }
  } else if (newType === 'order') {
    orderItemsText.value = ''
  }
})

function addChoice() {
  if (!currentQuestion.choices) currentQuestion.choices = []
  currentQuestion.choices.push({ id: `c${currentQuestion.choices.length + 1}`, text: '' })
}

function removeChoice(index: number) {
  if (currentQuestion.choices && currentQuestion.choices.length > 2) {
    currentQuestion.choices.splice(index, 1)
  }
}

function addPair() {
  if (!currentQuestion.pairs) currentQuestion.pairs = []
  currentQuestion.pairs.push({ left: '', right: '' })
}

function removePair(index: number) {
  if (currentQuestion.pairs && currentQuestion.pairs.length > 2) {
    currentQuestion.pairs.splice(index, 1)
  }
}

async function generateQuestionsWithAI() {
  if (!form.title || !form.title.trim()) {
    showToast('Vui lòng nhập tên đề thi trước khi tạo câu hỏi bằng AI', 'warning')
    return
  }
  const count = Math.max(1, Math.min(aiCount.value || 5, 10))
  aiGenerating.value = true
  try {
    const { data } = await http.post('/activities/ai/generate-questions/', {
      title: form.title,
      level: form.level,
      description: form.description,
      count,
      hint: aiHint.value,
      question_type: aiType.value === 'auto' ? undefined : aiType.value,
      model: import.meta.env.VITE_GEMINI_MODEL,
    })
    const text = data?.text || ''
    const parsed = parseAIResponse(text)
    // Nếu chọn loại cụ thể, lọc kết quả theo loại đó
    const filtered = (aiType.value === 'auto')
      ? parsed
      : parsed.filter(q => q.type === aiType.value)

    let finalQuestions = filtered
    // Fallback: nếu AI không trả về câu hỏi hợp lệ, tự tạo mẫu cho loại đã chọn
    if (!finalQuestions.length && aiType.value !== 'auto') {
      finalQuestions = buildFallbackQuestions(count, aiType.value as QType)
    }

    if (!finalQuestions.length) {
      showToast('AI không trả về câu hỏi hợp lệ', 'warning')
      return
    }
    if (!form.questions) form.questions = []
    finalQuestions.forEach((q) => form.questions!.push(q))
    showToast(`Đã thêm ${finalQuestions.length} câu hỏi từ AI`, 'success')
  } catch (e: any) {
    console.error('AI generate error:', e)
    const message = e?.response?.data?.detail || e?.message || 'Không thể tạo câu hỏi bằng AI'
    showToast(message, 'error')
  } finally {
    aiGenerating.value = false
  }
}

function parseAIResponse(raw: string): Question[] {
  if (!raw) return []
  let jsonText = raw.trim()
  // Nếu có code block, lấy nội dung bên trong
  const match = jsonText.match(/```(?:json)?\\s*([\\s\\S]*?)\\s*```/)
  if (match && match[1]) {
    jsonText = match[1]
  }
  try {
    const obj = JSON.parse(jsonText)
    const list = Array.isArray(obj) ? obj : obj.questions
    if (!Array.isArray(list)) return []
    return list.map((item: any, idx: number) => normalizeAIQuestion(item, idx))
      .filter(Boolean) as Question[]
  } catch (err) {
    console.warn('Cannot parse AI JSON, raw text:', raw)
    return []
  }
}

function normalizeAIQuestion(item: any, idx: number): Question | null {
  const id = makeId(`aiq${idx}`)
  const type = (item.type || 'single') as QType
  const score = Number(item.score) || 1
  const text = String(item.text || '').trim()
  if (!text) return null

  if (type === 'single' || type === 'multi') {
    const choices = (item.choices || []).map((c: any, i: number) => ({ id: `c${i + 1}`, text: String(c || '') }))
    const correctIdx = Array.isArray(item.correct_indices) ? item.correct_indices : [item.correct_index ?? 0]
    const answer = correctIdx.filter((n: any) => Number.isInteger(n) && choices[n]) .map((n: number) => choices[n].id)
    if (choices.length < 2 || answer.length === 0) return null
    return { id, type, text, score, choices, answer } as Question
  }

  if (type === 'boolean') {
    // Hỗ trợ cả correct_answer và answers
    let ans = item.correct_answer
    if (ans === undefined) {
      ans = Array.isArray(item.answers) ? item.answers[0] : item.answers
    }
    const val = ans === true || ans === 'true' || ans === 'True'
    return { id, type: 'boolean', text, score, answer: val } as Question
  }

  if (type === 'fill') {
    const blanks = Number(item.blanks) || 2
    const answers = Array.isArray(item.answers) ? item.answers.filter((x: any) => String(x || '').trim()) : []
    if (answers.length < blanks) return null
    return { id, type: 'fill', text, score, blanks, answer: answers.slice(0, blanks) } as Question
  }

  if (type === 'match') {
    const pairs = Array.isArray(item.pairs) ? item.pairs.map((p: any) => ({ left: String(p.left || ''), right: String(p.right || '') })) : []
    if (pairs.length < 2) return null
    return { id, type: 'match', text, score, pairs } as Question
  }

  if (type === 'order') {
    const items = Array.isArray(item.items) ? item.items.map((t: any) => String(t || '')) : []
    if (items.length < 2) return null
    return { id, type: 'order', text, score, items, answer: items.slice() } as Question
  }

  return null
}

function buildFallbackQuestions(count: number, type: QType): Question[] {
  const list: Question[] = []
  for (let i = 0; i < count; i++) {
    const id = makeId(`fallback_${type}`)
    const score = 1
    if (type === 'single') {
      const choices = [
        { id: 'c1', text: 'Đáp án 1' },
        { id: 'c2', text: 'Đáp án 2' },
        { id: 'c3', text: 'Đáp án 3' },
        { id: 'c4', text: 'Đáp án 4' },
      ]
      list.push({ id, type, text: `Câu hỏi trắc nghiệm #${i + 1}`, score, choices, answer: ['c1'] })
    } else if (type === 'multi') {
      const choices = [
        { id: 'c1', text: 'Đáp án 1' },
        { id: 'c2', text: 'Đáp án 2' },
        { id: 'c3', text: 'Đáp án 3' },
        { id: 'c4', text: 'Đáp án 4' },
      ]
      list.push({ id, type, text: `Câu hỏi nhiều đáp án #${i + 1}`, score, choices, answer: ['c1', 'c2'] })
    } else if (type === 'boolean') {
      list.push({ id, type: 'boolean', text: `Câu hỏi Đúng/Sai #${i + 1}`, score, answer: i % 2 === 0 })
    } else if (type === 'fill') {
      list.push({ id, type: 'fill', text: `Điền từ #${i + 1}`, score, blanks: 2, answer: ['Đáp án 1', 'Đáp án 2'] })
    } else if (type === 'match') {
      list.push({
        id,
        type: 'match',
        text: `Nối cặp #${i + 1}`,
        score,
        pairs: [
          { left: 'A1', right: 'B1' },
          { left: 'A2', right: 'B2' },
          { left: 'A3', right: 'B3' },
        ],
      })
    } else if (type === 'order') {
      const items = ['Bước 1', 'Bước 2', 'Bước 3']
      list.push({ id, type: 'order', text: `Sắp xếp #${i + 1}`, score, items, answer: items.slice() })
    }
  }
  return list
}

function saveQuestion() {
  if (!currentQuestion.text || !currentQuestion.type) return

  let question: Question

  if (currentQuestion.type === 'single' || currentQuestion.type === 'multi') {
    if (!currentQuestion.choices || currentQuestion.choices.length < 2) {
      showToast('Cần ít nhất 2 đáp án', 'warning')
      return
    }
    const answer = currentQuestion.answer
    if (!Array.isArray(answer) || answer.length === 0) {
      showToast('Vui lòng chọn ít nhất một đáp án đúng', 'warning')
      return
    }
    if (currentQuestion.type === 'single' && answer.length > 1) {
      showToast('Câu hỏi trắc nghiệm 1 đáp án chỉ được chọn 1 đáp án đúng', 'warning')
      return
    }
    question = {
      id: currentQuestion.id || makeId('q'),
      type: currentQuestion.type,
      text: currentQuestion.text,
      score: currentQuestion.score || 1,
      choices: currentQuestion.choices,
      answer: (Array.isArray(currentQuestion.answer) ? currentQuestion.answer : []) as string[],
    } as Question
  } else if (currentQuestion.type === 'boolean') {
    question = {
      id: currentQuestion.id || makeId('q'),
      type: 'boolean',
      text: currentQuestion.text,
      score: currentQuestion.score || 1,
      answer: (typeof currentQuestion.answer === 'boolean' ? currentQuestion.answer : false) as boolean,
    } as Question
  } else if (currentQuestion.type === 'fill') {
    const answers = fillAnswersText.value.split('\n').filter(s => s.trim())
    const blanks = currentQuestion.blanks || 2
    if (answers.length < blanks) {
      showToast(`Cần ít nhất ${blanks} đáp án`, 'warning')
      return
    }
    question = {
      id: currentQuestion.id || makeId('q'),
      type: 'fill',
      text: currentQuestion.text,
      score: currentQuestion.score || 1,
      blanks: blanks,
      answer: answers.slice(0, blanks),
    } as Question
  } else if (currentQuestion.type === 'match') {
    if (!currentQuestion.pairs || currentQuestion.pairs.length < 2) {
      showToast('Cần ít nhất 2 cặp', 'warning')
      return
    }
    question = {
      id: currentQuestion.id || makeId('q'),
      type: 'match',
      text: currentQuestion.text,
      score: currentQuestion.score || 1,
      pairs: currentQuestion.pairs,
    } as Question
  } else if (currentQuestion.type === 'order') {
    const items = orderItemsText.value.split('\n').filter(s => s.trim())
    if (items.length < 2) {
      showToast('Cần ít nhất 2 mục để sắp xếp', 'warning')
      return
    }
    question = {
      id: currentQuestion.id || makeId('q'),
      type: 'order',
      text: currentQuestion.text,
      score: currentQuestion.score || 1,
      items,
      answer: items.slice(), // đúng thứ tự ban đầu
    } as Question
  } else {
    return
  }

  if (editingQuestionIndex.value !== null) {
    if (form.questions) {
      form.questions[editingQuestionIndex.value] = question
    }
    editingQuestionIndex.value = null
  } else {
    if (!form.questions) form.questions = []
    form.questions.push(question)
  }

  closeQuestionModal()
}

function editQuestion(index: number) {
  if (!form.questions) return
  const q = form.questions[index]
  editingQuestionIndex.value = index
  
  currentQuestion.id = q.id
  currentQuestion.type = q.type
  currentQuestion.text = q.text
  currentQuestion.score = q.score

  if (q.type === 'single' || q.type === 'multi') {
    currentQuestion.choices = q.choices?.map(c => ({ ...c })) || []
    currentQuestion.answer = Array.isArray(q.answer) ? [...q.answer] : []
  } else if (q.type === 'boolean') {
    currentQuestion.answer = q.answer as boolean
  } else if (q.type === 'fill') {
    currentQuestion.blanks = q.blanks
    fillAnswersText.value = Array.isArray(q.answer) ? q.answer.join('\n') : ''
  } else if (q.type === 'match') {
    currentQuestion.pairs = q.pairs?.map(p => ({ ...p })) || []
  } else if (q.type === 'order') {
    orderItemsText.value = q.items?.join('\n') || ''
  }

  showAddQuestion.value = true
}

async function removeQuestion(index: number) {
  if (!form.questions) return
  const confirmed = await showConfirm({
    message: 'Bạn có chắc muốn xóa câu hỏi này?',
    title: 'Xác nhận xóa câu hỏi',
    type: 'danger',
    confirmText: 'Xóa',
    cancelText: 'Hủy'
  })
  if (confirmed) {
    form.questions.splice(index, 1)
  }
}

function closeQuestionModal() {
  showAddQuestion.value = false
  editingQuestionIndex.value = null
  resetQuestion()
}

async function submit() {
  if (!canSubmit.value) {
    showToast('Vui lòng điền đầy đủ thông tin và thêm ít nhất một câu hỏi', 'warning')
    return
  }

  // Double check title is not empty
  if (!form.title || !form.title.trim()) {
    showToast('Vui lòng nhập tên đề thi', 'warning')
    return
  }
  if (!form.courseId) {
    showToast('Vui lòng chọn khóa học áp dụng', 'warning')
    return
  }

  submitting.value = true
  try {
    console.log('Submitting form:', { title: form.title, questionsCount: form.questions?.length })
    await examService.create(form)
    showToast('Đã tạo đề thi thành công!', 'success')
    router.push({ path: '/teacher/exams' })
  } catch (e: any) {
    console.error('Submit error:', e)
    showToast(e?.message || 'Tạo đề thi thất bại', 'error')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
:host, .min-h-screen { overflow-x: hidden; }
</style>
