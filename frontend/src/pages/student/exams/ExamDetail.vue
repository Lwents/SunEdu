<template>
  <div class="student-shell">
    <div class="student-container max-w-6xl">
      <header
        class="flex flex-col gap-4 rounded-3xl border border-slate-200 bg-white/95 px-5 py-5 shadow-sm shadow-slate-100 sm:flex-row sm:items-center sm:justify-between"
      >
        <div>
          <p class="student-section-title">Đề luyện tập</p>
          <h1 class="text-2xl font-black text-gray-900 dark:text-gray-100">{{ exam?.title || 'Đề luyện tập' }}</h1>
          <p class="mt-1 flex flex-wrap gap-3 text-sm text-gray-600 dark:text-gray-400">
            <span>{{ labelLevel(exam?.level) }}</span>
            <span>• {{ Math.round((exam?.durationSec || 0) / 60) }} phút</span>
            <span>• {{ questions.length }} câu</span>
            <span>• Đạt ≥ {{ exam?.passCount || Math.ceil(questions.length * 0.6) }} câu</span>
          </p>
        </div>
        <div class="flex items-center gap-3">
          <div
            class="inline-flex items-center gap-2 rounded-2xl border px-4 py-2 text-sm font-bold transition-all duration-300"
            :class="
              timeLeft <= 300
                ? 'border-rose-300 bg-rose-100 text-rose-700 animate-pulse'
                : 'border-slate-200 bg-white text-gray-900 dark:text-gray-100'
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
            class="rounded-2xl border border-slate-200 px-4 py-2 text-sm font-semibold text-gray-600 dark:text-gray-400 transition hover:bg-slate-50"
            @click="goBack"
          >
            Thoát
          </button>
        </div>
      </header>

      <div v-if="loading" class="student-card mt-6 space-y-3">
        <div class="h-4 w-2/3 animate-pulse rounded bg-slate-200/70"></div>
        <div class="h-32 animate-pulse rounded-3xl bg-slate-100"></div>
        <div class="h-4 w-3/4 animate-pulse rounded bg-slate-200/70"></div>
      </div>

      <main v-else class="mt-6 grid gap-6 lg:grid-cols-[minmax(260px,320px)_minmax(0,1fr)]">
        <section
          class="rounded-3xl border border-slate-200 bg-white/95 p-5 shadow-sm shadow-slate-100"
        >
          <h3 class="text-base font-bold text-gray-900 dark:text-gray-100">Danh sách câu hỏi</h3>
          <div class="mt-4 grid grid-cols-5 gap-2 sm:grid-cols-6">
            <button
              v-for="(ans, i) in answers"
              :key="i"
              class="flex h-10 items-center justify-center rounded-2xl border text-sm font-semibold transition"
              :class="[
                i === idx
                  ? 'border-cyan-500 dark:border-cyan-600 bg-cyan-50 dark:bg-cyan-900/20 text-cyan-700 dark:text-cyan-300'
                  : 'border-slate-200 bg-white text-gray-900 dark:text-gray-100',
                isAnswered(ans) && i !== idx ? 'border-cyan-200 dark:border-cyan-700 bg-cyan-50 dark:bg-cyan-900/20 text-cyan-600 dark:text-cyan-400' : '',
              ]"
              @click="go(i)"
            >
              {{ i + 1 }}
            </button>
          </div>
        </section>

        <section class="space-y-4">
          <div
            class="rounded-3xl border border-slate-200 bg-white/95 p-5 shadow-sm shadow-slate-100"
          >
            <div class="flex items-center justify-between text-sm font-semibold text-gray-600 dark:text-gray-400">
              <span class="inline-flex items-center gap-2 text-gray-900 dark:text-gray-100">
                <span class="student-pill !text-xs">Câu {{ idx + 1 }}</span>
              </span>
              <span
                class="rounded-full border border-slate-200 px-3 py-1 text-xs uppercase tracking-[0.3em]"
              >
                {{ q?.type }}
              </span>
            </div>
            <div class="mt-4 space-y-4">
              <div class="prose prose-sm max-w-none text-gray-900 dark:text-gray-100" v-html="q?.text"></div>

              <template v-if="q?.type === 'mcq'">
                <ul class="space-y-3">
                  <li
                    v-for="opt in q.options"
                    :key="opt.key"
                    class="rounded-2xl border transition cursor-pointer"
                    :class="answers[idx] === opt.key 
                      ? 'border-cyan-500 dark:border-cyan-600 bg-cyan-50 dark:bg-cyan-900/20 ring-2 ring-cyan-200 dark:ring-cyan-800' 
                      : 'border-slate-200 bg-white hover:border-cyan-300 dark:hover:border-cyan-700 hover:bg-cyan-50/50'"
                  >
                    <label
                      class="flex items-center gap-3 px-4 py-3 text-sm font-semibold cursor-pointer"
                      :class="answers[idx] === opt.key ? 'text-cyan-700 dark:text-cyan-300' : 'text-gray-900 dark:text-gray-100'"
                    >
                      <input
                        type="radio"
                        class="h-4 w-4 text-cyan-600 dark:text-cyan-400 focus:ring-cyan-500/30"
                        :name="'q_' + idx"
                        :value="opt.key"
                        :checked="answers[idx] === opt.key"
                        @change="setAnswer(idx, opt.key)"
                      />
                      <span
                        class="inline-flex h-7 w-7 items-center justify-center rounded-full text-sm font-bold"
                        :class="answers[idx] === opt.key ? 'bg-cyan-500 text-white' : 'bg-slate-100 text-gray-700'"
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
                    class="flex items-center justify-center rounded-2xl border px-4 py-3 text-sm font-semibold transition cursor-pointer"
                    :class="answers[idx] === 'T'
                      ? 'border-cyan-500 dark:border-cyan-600 bg-cyan-50 dark:bg-cyan-900/20 text-cyan-700 dark:text-cyan-300 ring-2 ring-cyan-200 dark:ring-cyan-800'
                      : 'border-slate-200 bg-white text-gray-900 dark:text-gray-100 hover:border-cyan-300 dark:hover:border-cyan-700 hover:bg-cyan-50/50'"
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
                    class="flex items-center justify-center rounded-2xl border px-4 py-3 text-sm font-semibold transition cursor-pointer"
                    :class="answers[idx] === 'F'
                      ? 'border-cyan-500 dark:border-cyan-600 bg-cyan-50 dark:bg-cyan-900/20 text-cyan-700 dark:text-cyan-300 ring-2 ring-cyan-200 dark:ring-cyan-800'
                      : 'border-slate-200 bg-white text-gray-900 dark:text-gray-100 hover:border-cyan-300 dark:hover:border-cyan-700 hover:bg-cyan-50/50'"
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
                  class="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm text-gray-900 dark:text-gray-100 shadow-sm shadow-slate-100 focus:border-cyan-500 dark:border-cyan-600 focus:outline-none focus:ring-4 focus:ring-cyan-500/30"
                  :value="answers[idx] ?? ''"
                  @input="setAnswer(idx, ($event.target as HTMLInputElement).value)"
                  placeholder="Nhập câu trả lời của bạn..."
                />
              </template>
            </div>
          </div>

          <div
            class="flex flex-col gap-3 rounded-3xl border border-slate-200 bg-white/95 px-4 py-3 shadow-sm shadow-slate-100 sm:flex-row sm:items-center sm:justify-between"
          >
            <button
              type="button"
              class="inline-flex items-center justify-center rounded-2xl border border-slate-200 px-4 py-2 text-sm font-semibold text-gray-900 dark:text-gray-100 transition hover:bg-slate-50 disabled:opacity-50"
              :disabled="idx === 0"
              @click="prev"
            >
              ‹ Câu trước
            </button>
            <div
              v-if="idx === questions.length - 1 && questions.length > 0"
              class="text-center text-sm font-semibold text-gray-600 dark:text-gray-400"
            >
              {{ answeredCount }}/{{ questions.length }} câu đã trả lời
            </div>
            <button
              v-if="idx === questions.length - 1 && questions.length > 0"
              type="button"
              class="inline-flex items-center justify-center rounded-2xl border border-transparent bg-rose-500 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-rose-200 transition hover:bg-rose-600 disabled:opacity-50"
              :disabled="submitting"
              @click="submit"
            >
              {{ submitting ? 'Đang nộp…' : 'Nộp bài' }}
            </button>
            <button
              v-else
              type="button"
              class="inline-flex items-center justify-center rounded-2xl border border-transparent bg-gradient-to-r from-cyan-500 to-cyan-600 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-cyan-500/40 transition hover:from-cyan-600 hover:to-cyan-700 hover:shadow-xl hover:-translate-y-0.5 disabled:opacity-50 disabled:hover:translate-y-0"
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
        <div
          class="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-6 shadow-2xl shadow-slate-200"
        >
          <header class="flex items-center justify-between">
            <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100">Xác nhận nộp bài</h3>
            <button
              type="button"
              class="rounded-full p-2 text-gray-600 dark:text-gray-400 hover:bg-slate-100"
              aria-label="Đóng"
              @click="showSubmitModal = false"
            >
              ×
            </button>
          </header>
          <section class="mt-4 text-sm text-gray-900 dark:text-gray-100">
            <p v-html="submitMsg"></p>
          </section>
          <footer class="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-end">
            <button
              type="button"
              class="rounded-2xl border border-slate-200 px-4 py-2 text-sm font-semibold text-gray-600 dark:text-gray-400 hover:bg-slate-50"
              :disabled="submitting"
              @click="showSubmitModal = false"
            >
              Tiếp tục làm
            </button>
            <button
              type="button"
              class="rounded-2xl border border-transparent bg-rose-500 px-4 py-2 text-sm font-semibold text-white shadow-lg shadow-rose-200 hover:bg-rose-600 disabled:opacity-50"
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
