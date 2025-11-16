<template>
  <div class="min-h-screen bg-slate-50 py-8">
    <div class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
      <header class="mb-6 rounded-lg border border-slate-200 bg-white px-5 py-4 shadow-sm">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 class="text-2xl font-bold text-slate-900">{{ exam?.title || 'Đề luyện tập' }}</h1>
            <p class="mt-1 flex flex-wrap gap-3 text-sm text-slate-600">
              <span>{{ labelLevel(exam?.level) }}</span>
              <span>• {{ Math.round((exam?.durationSec || 0) / 60) }} phút</span>
              <span>• {{ questions.length }} câu</span>
              <span>• Đạt ≥ {{ exam?.passCount || Math.ceil(questions.length * 0.6) }} câu</span>
            </p>
          </div>
          <div class="flex items-center gap-3">
            <div
              class="inline-flex items-center gap-2 rounded-lg border px-4 py-2 text-sm font-semibold"
              :class="
                timeLeft <= 300
                  ? 'border-red-300 bg-red-50 text-red-700'
                  : 'border-slate-200 bg-white text-slate-900'
              "
            >
              <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
                <path
                  fill-rule="evenodd"
                  d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zM12.75 6a.75.75 0 00-1.5 0v6c0 .414.336.75.75.75h4.5a.75.75 0 000-1.5h-3.75V6z"
                  clip-rule="evenodd"
                />
              </svg>
              <span>{{ fmtTime(timeLeft) }}</span>
            </div>
            <button
              type="button"
              class="rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition"
              @click="goBack"
            >
              Thoát
            </button>
          </div>
        </div>
      </header>

      <div v-if="loading" class="space-y-3">
        <div class="h-4 w-2/3 animate-pulse rounded bg-slate-200"></div>
        <div class="h-32 animate-pulse rounded-lg bg-slate-100"></div>
        <div class="h-4 w-3/4 animate-pulse rounded bg-slate-200"></div>
      </div>

      <main v-else class="grid gap-6 lg:grid-cols-[minmax(260px,320px)_minmax(0,1fr)]">
        <section class="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <h3 class="text-base font-semibold text-slate-900 mb-4">Danh sách câu hỏi</h3>
          <div class="grid grid-cols-5 gap-2 sm:grid-cols-6">
            <button
              v-for="(ans, i) in answers"
              :key="i"
              class="flex h-10 items-center justify-center rounded-lg border text-sm font-semibold transition"
              :class="[
                i === idx
                  ? 'border-slate-900 bg-slate-900 text-white'
                  : 'border-slate-200 bg-white text-slate-900',
                isAnswered(ans) && i !== idx ? 'border-blue-500 bg-blue-50 text-blue-700' : '',
              ]"
              @click="go(i)"
            >
              {{ i + 1 }}
            </button>
          </div>
        </section>

        <section class="space-y-4">
          <div class="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
            <div class="flex items-center justify-between text-sm font-semibold text-slate-600 mb-4">
              <span class="text-slate-900">Câu {{ idx + 1 }}</span>
              <span class="rounded-full border border-slate-200 px-3 py-1 text-xs uppercase">
                {{ q?.type }}
              </span>
            </div>
            <div class="space-y-4">
              <div class="prose prose-sm max-w-none text-slate-900" v-html="q?.text"></div>

              <template v-if="q?.type === 'mcq'">
                <ul class="space-y-3">
                  <li
                    v-for="opt in q.options"
                    :key="opt.key"
                    class="rounded-lg border transition cursor-pointer"
                    :class="answers[idx] === opt.key 
                      ? 'border-slate-900 bg-slate-50 ring-2 ring-slate-200' 
                      : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50'"
                  >
                    <label
                      class="flex items-center gap-3 px-4 py-3 text-sm font-semibold cursor-pointer"
                      :class="answers[idx] === opt.key ? 'text-slate-900' : 'text-slate-700'"
                    >
                      <input
                        type="radio"
                        class="h-4 w-4 text-slate-900 focus:ring-slate-200"
                        :name="'q_' + idx"
                        :value="opt.key"
                        :checked="answers[idx] === opt.key"
                        @change="setAnswer(idx, opt.key)"
                      />
                      <span
                        class="inline-flex h-7 w-7 items-center justify-center rounded-full text-sm font-bold"
                        :class="answers[idx] === opt.key ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-700'"
                      >
                        {{ opt.key }}
                      </span>
                      <span class="flex-1" v-html="opt.text"></span>
                    </label>
                  </li>
                </ul>
              </template>

              <template v-else-if="q?.type === 'tf'">
                <div class="grid gap-3 sm:grid-cols-2">
                  <label
                    class="flex items-center justify-center rounded-lg border px-4 py-3 text-sm font-semibold transition cursor-pointer"
                    :class="answers[idx] === 'T'
                      ? 'border-slate-900 bg-slate-50 text-slate-900 ring-2 ring-slate-200'
                      : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300 hover:bg-slate-50'"
                  >
                    <input
                      type="radio"
                      class="sr-only"
                      :name="'q_' + idx"
                      value="T"
                      :checked="answers[idx] === 'T'"
                      @change="setAnswer(idx, 'T')"
                    />
                    Đúng
                  </label>
                  <label
                    class="flex items-center justify-center rounded-lg border px-4 py-3 text-sm font-semibold transition cursor-pointer"
                    :class="answers[idx] === 'F'
                      ? 'border-slate-900 bg-slate-50 text-slate-900 ring-2 ring-slate-200'
                      : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300 hover:bg-slate-50'"
                  >
                    <input
                      type="radio"
                      class="sr-only"
                      :name="'q_' + idx"
                      value="F"
                      :checked="answers[idx] === 'F'"
                      @change="setAnswer(idx, 'F')"
                    />
                    Sai
                  </label>
                </div>
              </template>

              <template v-else>
                <input
                  class="w-full rounded-lg border border-slate-300 px-4 py-3 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
                  :value="answers[idx] ?? ''"
                  @input="setAnswer(idx, ($event.target as HTMLInputElement).value)"
                  placeholder="Nhập câu trả lời của bạn..."
                />
              </template>
            </div>
          </div>

          <div class="flex flex-col gap-3 rounded-lg border border-slate-200 bg-white px-4 py-3 shadow-sm sm:flex-row sm:items-center sm:justify-between">
            <button
              type="button"
              class="inline-flex items-center justify-center rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition disabled:opacity-50"
              :disabled="idx === 0"
              @click="prev"
            >
              ‹ Câu trước
            </button>
            <div
              v-if="idx === questions.length - 1 && questions.length > 0"
              class="text-center text-sm font-semibold text-slate-600"
            >
              {{ answeredCount }}/{{ questions.length }} câu đã trả lời
            </div>
            <button
              v-if="idx === questions.length - 1 && questions.length > 0"
              type="button"
              class="inline-flex items-center justify-center rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-700 transition disabled:opacity-50"
              :disabled="submitting"
              @click="submit"
            >
              {{ submitting ? 'Đang nộp…' : 'Nộp bài' }}
            </button>
            <button
              v-else
              type="button"
              class="inline-flex items-center justify-center rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800 transition disabled:opacity-50"
              :disabled="idx === questions.length - 1"
              @click="next"
            >
              Câu tiếp ›
            </button>
          </div>
        </section>
      </main>
    </div>

    <transition
      enter-active-class="transition duration-200"
      leave-active-class="transition duration-150"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <div
        v-if="showSubmitModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 px-4"
        @click.self="showSubmitModal = false"
      >
        <div class="w-full max-w-md rounded-lg border border-slate-200 bg-white p-6 shadow-lg">
          <header class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-bold text-slate-900">Xác nhận nộp bài</h3>
            <button
              type="button"
              class="rounded-lg p-2 text-slate-600 hover:bg-slate-100"
              aria-label="Đóng"
              @click="showSubmitModal = false"
            >
              ×
            </button>
          </header>
          <section class="mb-6 text-sm text-slate-900">
            <p v-html="submitMsg"></p>
          </section>
          <footer class="flex flex-col gap-3 sm:flex-row sm:justify-end">
            <button
              type="button"
              class="rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50 transition"
              :disabled="submitting"
              @click="showSubmitModal = false"
            >
              Tiếp tục làm
            </button>
            <button
              type="button"
              class="rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white hover:bg-red-700 transition disabled:opacity-50"
              :disabled="submitting"
              @click="confirmSubmit"
            >
              {{ submitting ? 'Đang nộp…' : 'Nộp bài' }}
            </button>
          </footer>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, computed, shallowRef, ref, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from '@/utils/toast'

// --- Dữ liệu cục bộ thay thế cho Store ---
const exams = ref([
  {
    id: 1,
    title: 'Đề thi thử TOEIC Reading Part 5',
    level: 'basic' as const,
    durationSec: 25 * 60,
    passCount: 20,
  },
  {
    id: 2,
    title: 'Kiểm tra kiến thức Vue.js nâng cao',
    level: 'advanced' as const,
    durationSec: 30 * 60,
    passCount: 25,
  },
  {
    id: 3,
    title: 'Đề thi thử cuối kỳ môn Lập trình Web',
    level: 'basic' as const,
    durationSec: 60 * 60,
    passCount: 36,
  },
])

type Mcq = { type: 'mcq'; text: string; options: { key: string; text: string }[]; answer: string }
type Tf = { type: 'tf'; text: string; answer: 'T' | 'F' }
type Fill = { type: 'fill'; text: string; answer: string }
type Q = Mcq | Tf | Fill

const router = useRouter()
const route = useRoute()

const exam = computed(() => exams.value.find((x) => String(x.id) === String(route.params.id)))

const loading = ref(true)
const questions = shallowRef<Q[]>([])
const answers = shallowRef<(string | null)[]>([])
const idx = ref(0)
const submitting = ref(false)
const duration = ref(exam.value?.durationSec || 20 * 60)
const timeLeft = ref(duration.value)
let timer: number | null = null

const q = computed(() => questions.value[idx.value])
const answeredCount = computed(
  () => answers.value.filter((v) => (v ?? '').toString().trim() !== '').length,
)

function labelLevel(l?: 'basic' | 'advanced') {
  return l === 'advanced' ? 'Nâng cao' : 'Cơ bản'
}
function fmtTime(s: number) {
  const m = Math.floor(s / 60)
  const ss = s % 60
  return `${m.toString().padStart(2, '0')}:${ss.toString().padStart(2, '0')}`
}

// ===== Popup nộp bài =====
const showSubmitModal = ref(false)
const submitMsg = computed(() => {
  const unanswered = questions.value.length - answeredCount.value
  return unanswered > 0
    ? `Bạn còn <b>${unanswered}</b> câu chưa trả lời. Bạn có chắc chắn muốn nộp bài không?`
    : 'Bạn đã trả lời hết các câu hỏi. Xác nhận nộp bài?'
})

// Mở popup khi ấn nút "Nộp bài"
function submit() {
  showSubmitModal.value = true
}

// Thực sự nộp bài khi người dùng xác nhận trong popup
async function confirmSubmit() {
  if (submitting.value) return
  submitting.value = true
  stopTimer()
  await nextTick()

  const userAnswersData = questions.value.map((question, index) => {
    return {
      questionText: question.text,
      userAnswer: (answers.value[index] ?? 'Chưa trả lời').toString().trim(),
      correctAnswer: question.answer,
      explanation: `Đây là giải thích cho câu ${index + 1}.`,
    }
  })

  showSubmitModal.value = false

  const payload = {
    examId: route.params.id,
    answers: userAnswersData,
    savedAt: Date.now(),
  }
  try {
    const key = route.params.id ? `examResult:${route.params.id}` : 'examResult:last'
    sessionStorage.setItem(key, JSON.stringify(payload))
  } catch (err) {
    console.warn('Không thể lưu tạm kết quả bài làm:', err)
  }

  router.push({
    name: 'student-exam-result',
    params: { id: route.params.id },
    state: {
      userAnswers: userAnswersData,
    },
  })

  submitting.value = false
}

// ===== Các hàm sẵn có =====
function goBack() {
  // Show warning toast and go back after a short delay
  showToast('Mọi tiến trình làm bài sẽ không được lưu lại.', 'warning')
  setTimeout(() => {
    router.back()
  }, 1500)
}
function go(i: number) {
  if (i >= 0 && i < questions.value.length) idx.value = i
}
function next() {
  if (idx.value < questions.value.length - 1) idx.value++
}
function prev() {
  if (idx.value > 0) idx.value--
}
function isAnswered(v: string | null) {
  return (v ?? '').toString().trim() !== ''
}
function stopTimer() {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}

function setAnswer(i: number, val: string) {
  const next = answers.value.slice()
  next[i] = val
  answers.value = next
}

// Các hàm tạo câu hỏi mẫu
function makeMcq(i: number): Mcq {
  const letters = ['A', 'B', 'C', 'D']
  const correct = letters[i % 4]
  return {
    type: 'mcq',
    text: `Nội dung câu hỏi trắc nghiệm số <b>${i}</b>. Đâu là đáp án đúng cho phép tính: <b>${i} + ${i}</b>?`,
    options: letters.map((k) => ({
      key: k,
      text: k === correct ? String(i + i) : String(i + i + ((k.charCodeAt(0) % 3) - 1)),
    })),
    answer: correct,
  }
}
function makeTf(i: number): Tf {
  return {
    type: 'tf',
    text: `Xét tính đúng sai của mệnh đề sau: "<b>${i} là một số chẵn</b>"`,
    answer: i % 2 === 0 ? 'T' : 'F',
  }
}
function makeFill(i: number): Fill {
  return {
    type: 'fill',
    text: `Điền kết quả đúng cho phép tính sau: <b>${i} × 2</b>`,
    answer: String(i * 2),
  }
}

async function buildQuestions(total = 60, chunk = 20) {
  const buffer: Q[] = []
  questions.value = []
  answers.value = []
  for (let i = 1; i <= total; i++) {
    const t = i % 3 === 1 ? makeMcq(i) : i % 3 === 2 ? makeTf(i) : makeFill(i)
    buffer.push(t)
    if (i % chunk === 0 || i === total) {
      questions.value = questions.value.concat(buffer)
      answers.value = answers.value.concat(Array(buffer.length).fill(null))
      buffer.length = 0
      await new Promise((r) => requestAnimationFrame(() => r(null)))
    }
  }
}

onMounted(async () => {
  const numberOfQuestions = exam.value?.passCount ? exam.value.passCount + 10 : 60
  await buildQuestions(numberOfQuestions, 20)

  loading.value = false
  timeLeft.value = exam.value?.durationSec || 20 * 60

  timer = window.setInterval(() => {
    timeLeft.value--
    if (timeLeft.value <= 0) {
      clearInterval(timer!)
      // Hết giờ: tự động nộp (giữ đúng hành vi cũ, không hiện alert)
      confirmSubmit()
    }
  }, 1000) as unknown as number
})

onBeforeUnmount(() => {
  stopTimer()
})
</script>
