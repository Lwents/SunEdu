<!-- src/pages/teacher/students/Feedback.vue -->
<template>
  <div class="min-h-screen w-full overflow-x-hidden bg-slate-50">
    <main class="w-full mx-auto max-w-screen-2xl px-4 py-6 sm:px-6 md:px-10">
      <!-- Header -->
      <div class="mb-4 sm:mb-5 flex flex-wrap items-center justify-between gap-2 sm:gap-3">
        <h1 class="text-xl font-semibold sm:text-2xl text-slate-900">Phản hồi học sinh</h1>

        <button
          class="shrink-0 rounded-lg border border-slate-300 px-2.5 py-1.5 text-xs sm:rounded-lg sm:px-4 sm:py-2 sm:text-sm text-slate-700 hover:bg-slate-50 transition"
          @click="goBack"
          aria-label="Quay lại danh sách học sinh"
        >
          ← <span class="ml-1">Quay lại danh sách</span>
        </button>
      </div>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
        <!-- Left: student list -->
        <section class="lg:col-span-1 rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <div class="mb-3 flex items-center gap-2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2">
            <svg
              viewBox="0 0 24 24"
              class="h-5 w-5 text-slate-400"
              fill="none"
              stroke="currentColor"
              aria-hidden="true"
            >
              <circle cx="11" cy="11" r="8" stroke-width="2" />
              <path d="M21 21l-4.3-4.3" stroke-width="2" />
            </svg>
            <input
              v-model.trim="q"
              placeholder="Tìm học sinh…"
              class="w-full bg-transparent outline-none text-sm"
              @input="debouncedFilter"
            />
          </div>

          <div v-if="loading" class="space-y-2">
            <div
              v-for="i in 6"
              :key="'sk-' + i"
              class="flex items-center gap-3 rounded-lg px-2 py-2"
            >
              <div class="h-9 w-9 rounded-full bg-slate-200 animate-pulse"></div>
              <div class="flex-1">
                <div class="h-3 w-2/3 rounded bg-slate-200 animate-pulse mb-2"></div>
                <div class="h-3 w-1/2 rounded bg-slate-100 animate-pulse"></div>
              </div>
            </div>
          </div>

          <ul v-else-if="students.length" class="max-h-[560px] space-y-2 overflow-auto pr-1">
            <li v-for="s in students" :key="s.id">
              <button
                class="flex w-full items-center gap-3 rounded-lg px-2 py-2 text-left hover:bg-slate-50 transition"
                :class="selectedId === s.id ? 'bg-slate-100' : ''"
                @click="select(s.id)"
              >
                <img :src="s.avatar" :alt="s.name" class="h-9 w-9 rounded-full object-cover border border-slate-200" />
                <div class="min-w-0 flex-1">
                  <div class="truncate text-sm font-medium text-slate-900">{{ s.name }}</div>
                  <div class="truncate text-xs text-slate-500">
                    {{ s.classCode }} · {{ s.course }}
                  </div>
                </div>
              </button>
            </li>
          </ul>
          <div v-else class="py-10 text-center text-sm text-slate-500">
            Không có học sinh phù hợp.
          </div>
        </section>

        <!-- Right: composer -->
        <section class="lg:col-span-2 rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
          <div v-if="!current" class="p-6 text-center text-slate-500">
            Chọn một học sinh ở danh sách bên trái để viết phản hồi.
          </div>

          <div v-else class="space-y-4">
            <div class="flex items-center gap-3">
              <img
                :src="current.avatar"
                :alt="current.name"
                class="h-12 w-12 rounded-full object-cover border border-slate-200"
              />
              <div>
                <div class="font-semibold text-slate-900">{{ current.name }}</div>
                <div class="text-xs text-slate-500">
                  {{ current.classCode }} · {{ current.course }}
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 gap-3 sm:grid-cols-3">
              <div class="rounded-lg bg-slate-50 p-3 text-sm">
                Tiến độ: <span class="font-medium text-slate-900">{{ current.progress }}%</span>
              </div>
              <div class="rounded-lg bg-slate-50 p-3 text-sm">
                Điểm TB: <span class="font-medium text-slate-900">{{ current.avgScore.toFixed(1) }}/10</span>
              </div>
              <div class="rounded-lg bg-slate-50 p-3 text-sm">
                Hoạt động: <span class="font-medium text-slate-900">{{ current.lastActive }}</span>
              </div>
            </div>

            <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
              <div class="space-y-2 md:col-span-2">
                <label class="text-sm font-medium text-slate-700">Nội dung phản hồi</label>
                <textarea
                  v-model="message"
                  rows="7"
                  class="w-full rounded-lg border border-slate-300 p-3 text-sm outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
                  placeholder="Viết nhận xét, gợi ý ôn tập, điểm cần cải thiện…"
                ></textarea>

                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="(t, i) in chipTexts"
                    :key="'chip-' + i"
                    type="button"
                    class="rounded-full border border-slate-300 px-2 py-1 text-xs hover:bg-slate-50 transition"
                    @click="append(t)"
                  >
                    {{ t }}
                  </button>
                </div>
              </div>

              <div class="space-y-3">
                <div>
                  <label class="mb-1 block text-sm font-medium text-slate-700">Mức độ hoàn thành</label>
                  <input
                    type="range"
                    min="0"
                    max="10"
                    step="0.5"
                    v-model.number="rating"
                    class="w-full"
                  />
                  <div class="mt-1 text-sm text-slate-600">
                    <span class="font-medium">{{ rating.toFixed(1) }}</span> / 10
                  </div>
                </div>

                <div>
                  <label class="mb-1 block text-sm font-medium text-slate-700">Mẫu phản hồi</label>
                  <select
                    v-model="template"
                    class="w-full rounded-lg border border-slate-300 p-2 text-sm focus:outline-none focus:ring-2 focus:ring-slate-200"
                  >
                    <option value="">— Chọn mẫu —</option>
                    <option value="praise">Khen ngợi</option>
                    <option value="improve">Cần cải thiện</option>
                    <option value="suggest">Gợi ý ôn tập</option>
                  </select>
                </div>

                <button
                  class="w-full rounded-lg bg-slate-900 px-3 py-2 font-semibold text-white hover:bg-slate-800 transition disabled:opacity-50 disabled:cursor-not-allowed"
                  :disabled="!canSend || sending"
                  @click="send"
                >
                  {{ sending ? 'Đang gửi...' : 'Gửi phản hồi' }}
                </button>
                <p v-if="sent" class="text-center text-sm text-green-600">Đã gửi phản hồi 🎉</p>
                <p v-if="error" class="text-center text-sm text-red-600">{{ error }}</p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { teacherService } from '@/services/teacher.service'
import { showToast } from '@/utils/toast'

type StudentRow = {
  id: number
  name: string
  avatar: string
  classCode: string
  course: string
  progress: number
  avgScore: number
  lastActive: string
}

const route = useRoute()
const router = useRouter()

const q = ref('')
const selectedId = ref<number | null>(route.query.id ? Number(route.query.id) : null)
const message = ref('')
const rating = ref(7.5)
type Tpl = '' | 'praise' | 'improve' | 'suggest'
const template = ref<Tpl>('')
const sent = ref(false)
const sending = ref(false)
const error = ref('')

const loading = ref(true)
const allStudents = ref<StudentRow[]>([])

let t: number | null = null
const debouncedFilter = () => {
  if (t) clearTimeout(t)
  t = window.setTimeout(() => {}, 250) as unknown as number
}

const chipTexts = ref<string[]>([
  'Em làm tốt phần lý thuyết.',
  'Cần luyện thêm bài tập vận dụng.',
  'Cố gắng đọc kỹ câu hỏi trước khi trả lời.',
  'Rất tích cực phát biểu.',
  'Ôn lại từ vựng chương này nhé.',
])

async function fetchStudents() {
  loading.value = true
  error.value = ''
  try {
    const response = await teacherService.getStudents({ pageSize: 100 })
    const now = Date.now()
    
    allStudents.value = response.items.map((s, i) => {
      const id = Number(s.id)
      // Get first course for display
      const firstCourse = s.courses && s.courses.length > 0 ? s.courses[0] : null
      const cls = firstCourse ? `L${(id % 5) + 1}0${(id % 3) + 1}` : `L${(id % 5) + 1}0${(id % 3) + 1}`
      const course = firstCourse ? firstCourse.title : `Khoá ${(id % 6) + 1}`
      const progress = firstCourse ? firstCourse.progress : (40 + ((id + i) % 50))
      
      // Calculate average score from courses
      let totalScore = 0
      let scoreCount = 0
      if (s.courses && s.courses.length > 0) {
        // Placeholder: use progress as score estimate
        s.courses.forEach(c => {
          totalScore += c.progress / 10 // Convert progress to score
          scoreCount++
        })
      }
      const avgScore = scoreCount > 0 ? totalScore / scoreCount : (6 + ((id + i) % 40) / 10)
      
      // Get avatar URL - handle both relative and absolute URLs
      let avatarUrl = s.avatar || null
      if (avatarUrl && !avatarUrl.startsWith('http://') && !avatarUrl.startsWith('https://')) {
        // If relative URL, construct full URL
        const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const baseUrl = apiUrl.replace(/\/+$/, '')
        avatarUrl = avatarUrl.startsWith('/') ? `${baseUrl}${avatarUrl}` : `${baseUrl}/${avatarUrl}`
      }
      // Fallback to dicebear if no avatar
      if (!avatarUrl) {
        avatarUrl = `https://api.dicebear.com/7.x/thumbs/svg?seed=${encodeURIComponent(s.username || s.name || String(id))}&backgroundType=gradientLinear`
      }
      
      return {
        id,
        name: s.name || s.username || `Học sinh ${id}`,
        avatar: avatarUrl,
        classCode: cls,
        course,
        progress,
        avgScore: Math.min(10, Math.max(0, avgScore)),
        lastActive: firstCourse && firstCourse.enrolledAt 
          ? new Date(firstCourse.enrolledAt).toLocaleString('vi-VN')
          : new Date(now - (i + 1) * 36e5).toLocaleString('vi-VN'),
      }
    })
  } catch (e: any) {
    console.error('Error fetching students:', e)
    error.value = e?.message || 'Không thể tải danh sách học sinh'
    showToast('Không thể tải danh sách học sinh', 'error')
  } finally {
    loading.value = false
  }
}

const students = computed(() => {
  const key = q.value.trim().toLowerCase()
  return allStudents.value.filter(
    (s) =>
      !key ||
      s.name.toLowerCase().includes(key) ||
      s.classCode.toLowerCase().includes(key) ||
      s.course.toLowerCase().includes(key),
  )
})

const current = computed<StudentRow | null>(
  () => students.value.find((s) => s.id === selectedId.value) ?? null,
)

const canSend = computed(() => !!current.value && message.value.trim().length > 0)

function select(id: number) {
  if (selectedId.value === id) return
  selectedId.value = id
  sent.value = false
  error.value = ''
  message.value = ''
  rating.value = 7.5
  template.value = ''
}

watch(selectedId, (val) => {
  const q = { ...route.query }
  if (val) q.id = String(val)
  else delete q.id
  router.replace({ query: q })
})

watch(template, (t) => {
  if (!t) return
  if (t === 'praise')
    message.value = 'Cô/Thầy đánh giá cao sự nỗ lực của em. Tiếp tục phát huy nhé!'
  if (t === 'improve')
    message.value = 'Em cần chú ý hơn ở các bài tập vận dụng và luyện thêm ví dụ tương tự.'
  if (t === 'suggest')
    message.value = 'Gợi ý: Ôn lại các mục trọng tâm và làm bài luyện tập ở cuối chương.'
})

function append(t: string) {
  message.value = message.value ? `${message.value} ${t}` : t
}

async function send() {
  if (!canSend.value || !current.value || sending.value) return
  
  sending.value = true
  error.value = ''
  sent.value = false
  
  try {
    // Get first course ID if available
    const studentData = allStudents.value.find(s => s.id === current.value!.id)
    const studentFromService = allStudents.value.find(s => s.id === current.value!.id)
    
    // Find course ID from service response
    const response = await teacherService.getStudents({ pageSize: 100 })
    const fullStudent = response.items.find(s => Number(s.id) === current.value!.id)
    const courseId = fullStudent?.courses && fullStudent.courses.length > 0 
      ? fullStudent.courses[0].id 
      : undefined
    
    await teacherService.sendFeedback({
      studentId: current.value.id,
      courseId: courseId,
      message: message.value.trim(),
      rating: rating.value
    })
    
    sent.value = true
    showToast('Đã gửi phản hồi thành công! Học sinh sẽ nhận được thông báo.', 'success')
    
    // Reset form after a delay
    setTimeout(() => {
      message.value = ''
      rating.value = 7.5
      template.value = ''
      sent.value = false
    }, 2000)
    
  } catch (e: any) {
    console.error('Error sending feedback:', e)
    error.value = e?.response?.data?.error || e?.message || 'Không thể gửi phản hồi'
    showToast(error.value, 'error')
  } finally {
    sending.value = false
  }
}

function goBack() {
  router.push({ path: '/teacher/students' })
}

onMounted(async () => {
  await fetchStudents()
  if (selectedId.value && !allStudents.value.some((s) => s.id === selectedId.value)) {
    selectedId.value = null
  }
})
</script>

<style scoped>
:host,
.min-h-screen {
  overflow-x: hidden;
}
</style>
