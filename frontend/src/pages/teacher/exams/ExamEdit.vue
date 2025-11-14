<!-- src/pages/teacher/exams/ExamEdit.vue -->
<template>
  <div class="min-h-screen w-full overflow-x-hidden bg-slate-50">
    <main class="w-full mx-auto max-w-screen-2xl px-4 py-6 sm:px-6 md:px-10 md:py-8">
      <!-- Header -->
      <div class="mb-5 flex items-center justify-between">
        <h1 class="text-2xl font-semibold">Sửa bài kiểm tra</h1>
        <button
          class="rounded-xl border px-4 py-2 text-sm hover:bg-slate-50"
          @click="router.back()"
        >
          Hủy
        </button>
      </div>

      <div v-if="loading" class="py-16 text-center text-slate-500">Đang tải...</div>

      <form v-else @submit.prevent="submit" class="space-y-6">
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
              <label class="mb-1 block text-sm font-medium">Khối lớp</label>
              <select
                v-model="form.level"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none focus:border-sky-400 focus:ring-2 focus:ring-sky-500/30"
              >
                <option value="Khối 1–2">Khối 1–2</option>
                <option value="Khối 3–5">Khối 3–5</option>
              </select>
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
              <label class="mb-1 block text-sm font-medium">Trạng thái</label>
              <select
                v-model="form.status"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none focus:border-sky-400 focus:ring-2 focus:ring-sky-500/30"
              >
                <option value="draft">Nháp</option>
                <option value="published">Đã phát hành</option>
              </select>
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

            <div class="md:col-span-2 flex gap-4">
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
          </div>
        </div>

        <!-- Danh sách câu hỏi -->
        <div class="rounded-2xl border border-slate-200 bg-white p-6">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-lg font-semibold">Câu hỏi ({{ form.questions?.length || 0 }})</h2>
            <button
              type="button"
              class="rounded-xl bg-sky-600 px-4 py-2 text-sm font-semibold text-white hover:bg-sky-700"
              @click="showAddQuestion = true"
            >
              + Thêm câu hỏi
            </button>
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
            {{ submitting ? 'Đang lưu...' : 'Lưu thay đổi' }}
          </button>
        </div>
      </form>

      <!-- Modal thêm/sửa câu hỏi (giống ExamCreate) -->
      <div
        v-if="showAddQuestion || editingQuestionIndex !== null"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
        @click.self="closeQuestionModal"
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
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { examService, type ExamDetail, type Question, type QType, type Level, type ExamStatus } from '@/services/exam.service'

const router = useRouter()
const route = useRoute()
const examId = computed(() => Number(route.params.id))

const loading = ref(true)
const submitting = ref(false)
const showAddQuestion = ref(false)
const editingQuestionIndex = ref<number | null>(null)

const form = reactive<Partial<ExamDetail>>({
  title: '',
  level: 'Khối 1–2' as Level,
  durationSec: 1800,
  passScore: 12,
  status: 'draft' as ExamStatus,
  description: '',
  shuffleQuestions: true,
  shuffleChoices: true,
  questions: [],
})

const durationMin = computed({
  get: () => Math.round((form.durationSec || 0) / 60),
  set: (val) => { form.durationSec = val * 60 }
})

const canSubmit = computed(() => {
  return form.title && form.questions && form.questions.length > 0
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

function saveQuestion() {
  if (!currentQuestion.text || !currentQuestion.type) return

  let question: Question

  if (currentQuestion.type === 'single' || currentQuestion.type === 'multi') {
    if (!currentQuestion.choices || currentQuestion.choices.length < 2) {
      alert('Cần ít nhất 2 đáp án')
      return
    }
    if (!Array.isArray(currentQuestion.answer) || currentQuestion.answer.length === 0) {
      alert('Vui lòng chọn ít nhất một đáp án đúng')
      return
    }
    if (currentQuestion.type === 'single' && currentQuestion.answer.length > 1) {
      alert('Câu hỏi trắc nghiệm 1 đáp án chỉ được chọn 1 đáp án đúng')
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
      alert(`Cần ít nhất ${blanks} đáp án`)
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
      alert('Cần ít nhất 2 cặp')
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
      alert('Cần ít nhất 2 mục để sắp xếp')
      return
    }
    question = {
      id: currentQuestion.id || makeId('q'),
      type: 'order',
      text: currentQuestion.text,
      score: currentQuestion.score || 1,
      items,
      answer: items.slice(),
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

function removeQuestion(index: number) {
  if (form.questions && confirm('Bạn có chắc muốn xóa câu hỏi này?')) {
    form.questions.splice(index, 1)
  }
}

function closeQuestionModal() {
  showAddQuestion.value = false
  editingQuestionIndex.value = null
  resetQuestion()
}

async function loadExam() {
  loading.value = true
  try {
    const exam = await examService.detail(examId.value)
    form.title = exam.title
    form.level = exam.level
    form.durationSec = exam.durationSec
    form.passScore = exam.passScore
    form.status = exam.status
    form.description = exam.description
    form.shuffleQuestions = exam.shuffleQuestions ?? true
    form.shuffleChoices = exam.shuffleChoices ?? true
    form.questions = exam.questions ? [...exam.questions] : []
  } catch (e: any) {
    alert(e?.message || 'Không tải được đề thi')
    router.back()
  } finally {
    loading.value = false
  }
}

async function submit() {
  if (!canSubmit.value) {
    alert('Vui lòng điền đầy đủ thông tin và thêm ít nhất một câu hỏi')
    return
  }

  submitting.value = true
  try {
    await examService.update(examId.value, form)
    router.push({ path: `/teacher/exams/${examId.value}` })
  } catch (e: any) {
    alert(e?.message || 'Cập nhật đề thi thất bại')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadExam()
})
</script>

<style scoped>
:host, .min-h-screen { overflow-x: hidden; }
</style>

