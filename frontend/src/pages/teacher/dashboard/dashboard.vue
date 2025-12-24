<!-- src/pages/teacher/dashboard/dashboard.vue -->
<template>
  <div class="min-h-screen w-full overflow-x-hidden" :class="isDark ? 'bg-slate-950' : 'bg-slate-50'">
    <main class="w-full mx-auto max-w-screen-2xl px-4 py-6 sm:px-6 md:px-10 md:py-8">
      <h1 class="mb-6 text-xl sm:text-2xl font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">
        Bảng điều khiển
      </h1>

      <div class="grid grid-cols-1 gap-6 xl:grid-cols-3">
        <!-- Cột trái -->
        <div class="space-y-6 xl:col-span-2">
          <!-- Thao tác nhanh -->
          <div :class="cardClass">
            <div :class="cardHeaderClass">Thao tác nhanh</div>
            <div class="grid grid-cols-2 gap-3 p-4 sm:grid-cols-4">
              <button
                v-for="action in quickActions"
                :key="action.label"
                @click="action.onClick"
                :class="quickActionClass"
              >
                <div :class="iconWrapperClass">
                  <component :is="action.icon" class="w-5 h-5" />
                </div>
                <span :class="isDark ? 'text-gray-200' : 'text-slate-700'" class="text-xs sm:text-sm font-medium">
                  {{ action.label }}
                </span>
              </button>
            </div>
          </div>

          <!-- Khoá học của tôi -->
          <div :class="cardClass">
            <div :class="cardHeaderClass">Khoá học của tôi</div>
            <div class="p-4">
              <div v-if="loading" :class="emptyStateClass">Đang tải dữ liệu...</div>
              <template v-else-if="myCourses.length">
                <div
                  v-for="(course, idx) in myCourses"
                  :key="String(course.id)"
                  @click="openCourse(course.id)"
                  :class="[courseItemClass, idx < myCourses.length - 1 ? (isDark ? 'border-b border-white/5' : 'border-b border-slate-100') : '']"
                >
                  <div class="min-w-0 flex-1">
                    <div :class="isDark ? 'text-gray-100' : 'text-slate-900'" class="text-sm font-medium truncate">
                      {{ course.title }}
                    </div>
                    <div :class="isDark ? 'text-gray-400' : 'text-slate-500'" class="text-xs">
                      {{ course.enrolled }} học viên
                    </div>
                  </div>
                  <div class="flex items-center gap-3">
                    <BarChart :data="sparkFor(course.id, course.enrolled)" />
                    <span :class="badgeClass">{{ statusLabel(course.status) }}</span>
                    <svg class="w-5 h-5" :class="isDark ? 'text-gray-500' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </template>
              <div v-else :class="emptyStateClass">Chưa có khoá học nào.</div>
            </div>
          </div>
        </div>

        <!-- Cột phải -->
        <div class="space-y-6">
          <!-- Sự kiện sắp tới -->
          <div :class="cardClass">
            <div :class="cardHeaderClass" class="flex items-center justify-between">
              <span>Sự kiện sắp tới</span>
              <button @click="showEventModal = true" :class="addButtonClass">+ Thêm</button>
            </div>
            <div class="p-4">
              <div class="max-h-60 space-y-2 overflow-y-auto">
                <div v-if="loadingEvents" :class="isDark ? 'text-gray-400' : 'text-slate-500'" class="py-4 text-center text-sm">
                  Đang tải...
                </div>
                <template v-else-if="upcomingEvents.length">
                  <div v-for="event in upcomingEvents" :key="event.id" :class="eventItemClass">
                    <div class="flex items-center gap-3">
                      <div :class="iconWrapperClass">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <circle cx="12" cy="12" r="10" stroke-width="2" />
                          <path stroke-width="2" d="M12 6v6l4 2" />
                        </svg>
                      </div>
                      <span :class="isDark ? 'text-gray-200' : 'text-slate-700'" class="text-sm truncate">
                        {{ event.name }}
                      </span>
                    </div>
                    <span :class="isDark ? 'text-gray-400' : 'text-slate-500'" class="text-xs">
                      {{ event.time || formatTime(event.start_date) }}
                    </span>
                  </div>
                </template>
                <div v-else :class="isDark ? 'text-gray-400' : 'text-slate-500'" class="py-4 text-center text-sm">
                  Chưa có sự kiện nào
                </div>
              </div>
            </div>
          </div>

          <!-- Thống kê -->
          <div :class="cardClass">
            <div :class="cardHeaderClass">Thống kê</div>
            <div class="grid grid-cols-3 gap-3 p-4">
              <div v-for="stat in statsData" :key="stat.label" :class="statClass">
                <div :class="isDark ? 'text-white' : 'text-slate-900'" class="text-xl sm:text-2xl font-semibold">
                  {{ formatNumber(stat.value) }}
                </div>
                <div :class="isDark ? 'text-gray-400' : 'text-slate-500'" class="text-xs">
                  {{ stat.label }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Event Modal -->
    <Teleport to="body">
      <div v-if="showEventModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4" @click.self="showEventModal = false">
        <div :class="modalClass">
          <h3 :class="isDark ? 'text-white' : 'text-slate-900'" class="mb-4 text-lg font-bold">Tạo sự kiện mới</h3>
          
          <div class="space-y-4">
            <div>
              <label :class="labelClass">Tên sự kiện *</label>
              <input v-model="eventForm.name" type="text" :class="inputClass" placeholder="VD: Kiểm tra giữa kỳ" />
            </div>
            <div>
              <label :class="labelClass">Mô tả</label>
              <textarea v-model="eventForm.description" rows="2" :class="inputClass" placeholder="Mô tả ngắn về sự kiện..." />
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label :class="labelClass">Ngày *</label>
                <input v-model="eventForm.start_date" type="date" :class="inputClass" />
              </div>
              <div>
                <label :class="labelClass">Giờ</label>
                <input v-model="eventForm.start_time" type="time" :class="inputClass" />
              </div>
            </div>
          </div>
          
          <div class="mt-6 flex justify-end gap-3">
            <button @click="showEventModal = false" :class="cancelButtonClass">Hủy</button>
            <button @click="createEvent" :disabled="savingEvent" :class="submitButtonClass">
              {{ savingEvent ? 'Đang tạo...' : 'Tạo sự kiện' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, reactive, h } from 'vue'
import { useRouter } from 'vue-router'
import { courseService, type CourseStatus, type CourseSummary } from '@/services/course.service'
import { eventService, type EventItem } from '@/services/event.service'
import { showToast } from '@/utils/toast'
import { useThemeStore } from '@/store/theme.store'

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)
const router = useRouter()

// ============ Styles ============
const cardClass = computed(() => [
  'rounded-2xl overflow-hidden transition-colors',
  isDark.value ? 'bg-slate-900/50' : 'bg-white shadow-sm border border-slate-200'
])

const cardHeaderClass = computed(() => [
  'px-4 py-3 text-sm font-semibold border-b',
  isDark.value ? 'text-white border-white/5' : 'text-slate-900 border-slate-100'
])

const quickActionClass = computed(() => [
  'flex flex-col items-center gap-2 p-4 rounded-xl transition-all cursor-pointer border',
  isDark.value ? 'border-white/10 hover:bg-white/5' : 'border-slate-200 hover:bg-slate-50 hover:border-slate-300'
])

const iconWrapperClass = computed(() => [
  'p-3 rounded-xl',
  isDark.value ? 'bg-slate-800/80 text-cyan-400' : 'bg-slate-100 text-slate-600'
])

const courseItemClass = computed(() => [
  'flex items-center gap-4 p-4 rounded-xl cursor-pointer transition-all',
  isDark.value ? 'hover:bg-white/5' : 'bg-slate-50 hover:bg-slate-100'
])

const badgeClass = computed(() => [
  'px-2 py-0.5 rounded-full text-xs whitespace-nowrap',
  isDark.value ? 'bg-slate-800/80 text-gray-300' : 'bg-slate-100 text-slate-600'
])

const emptyStateClass = computed(() => [
  'py-8 text-center text-sm rounded-xl',
  isDark.value ? 'text-gray-400' : 'text-slate-500'
])

const eventItemClass = computed(() => [
  'flex items-center justify-between p-3 rounded-xl transition-all',
  isDark.value ? 'hover:bg-white/5' : 'hover:bg-slate-50'
])

const statClass = computed(() => [
  'p-4 rounded-xl text-center',
  isDark.value ? 'bg-slate-800/50' : 'bg-slate-50'
])

const addButtonClass = computed(() => [
  'px-3 py-1 text-xs font-medium rounded-lg transition-colors',
  isDark.value ? 'bg-cyan-600 text-white hover:bg-cyan-500' : 'bg-slate-800 text-white hover:bg-slate-700'
])

const modalClass = computed(() => [
  'w-full max-w-md rounded-2xl p-6',
  isDark.value ? 'bg-slate-900' : 'bg-white shadow-xl'
])

const labelClass = computed(() => [
  'block mb-1 text-sm font-medium',
  isDark.value ? 'text-gray-300' : 'text-slate-700'
])

const inputClass = computed(() => [
  'w-full px-3 py-2 rounded-lg border transition-colors focus:outline-none',
  isDark.value 
    ? 'bg-slate-800 border-slate-700 text-white placeholder-gray-500 focus:border-cyan-500 dark-date-picker' 
    : 'bg-white border-slate-300 focus:border-blue-500'
])

const cancelButtonClass = computed(() => [
  'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
  isDark.value ? 'text-gray-300 hover:bg-white/5' : 'text-slate-600 hover:bg-slate-100'
])

const submitButtonClass = computed(() => [
  'px-4 py-2 text-sm font-medium text-white rounded-lg transition-colors disabled:opacity-50',
  isDark.value ? 'bg-cyan-600 hover:bg-cyan-500' : 'bg-slate-800 hover:bg-slate-700'
])

// ============ Data ============
type TeacherCourse = {
  id: string | number
  title: string
  enrolled: number
  status: CourseStatus
}

const loading = ref(true)
const source = ref<TeacherCourse[]>([])
const totals = ref({ courses: 0, students: 0, assignments: 0 })
const loadingEvents = ref(true)
const upcomingEvents = ref<EventItem[]>([])
const showEventModal = ref(false)
const savingEvent = ref(false)

const eventForm = reactive({
  name: '',
  description: '',
  start_date: '',
  start_time: '',
  type: 'other',
})

const myCourses = computed(() => source.value)
const statsData = computed(() => [
  { label: 'Khoá học', value: totals.value.courses },
  { label: 'Học sinh', value: totals.value.students },
  { label: 'Bài học', value: totals.value.assignments },
])

// ============ Icons ============
const IconPlus = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-width': 2, d: 'M12 5v14M5 12h14' })
])
const IconClipboard = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('rect', { x: 8, y: 2, width: 8, height: 4, rx: 1, 'stroke-width': 2 }),
  h('path', { 'stroke-width': 2, d: 'M9 4H7a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2h-2' })
])
const IconFile = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-width': 2, d: 'M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12V8z' }),
  h('path', { 'stroke-width': 2, d: 'M14 2v6h6' })
])
const IconChart = () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
  h('path', { 'stroke-width': 2, d: 'M3 3v18h18' }),
  h('path', { 'stroke-width': 2, d: 'M7 13l3 3 7-7' })
])

const quickActions = [
  { label: 'Tạo khoá học', icon: IconPlus, onClick: () => router.push('/teacher/courses/new') },
  { label: 'Xem bài kiểm tra', icon: IconClipboard, onClick: () => router.push('/teacher/exams') },
  { label: 'Tạo bài kiểm tra', icon: IconFile, onClick: () => router.push('/teacher/exams') },
  { label: 'Xem báo cáo', icon: IconChart, onClick: () => router.push('/teacher/reports') },
]

// ============ BarChart Component ============
const BarChart = {
  props: { data: { type: Array, required: true } },
  setup(props: { data: { x: number; y: number }[] }) {
    const bars = computed(() => {
      const ys = props.data.map(p => p.y)
      const minY = Math.min(...ys)
      const maxY = Math.max(...ys)
      const range = maxY - minY || 1
      return props.data.map((p, i) => {
        const height = ((p.y - minY) / range) * 28 + 4
        return { x: 4 + i * 18, height, y: 36 - height }
      })
    })
    return () => h('svg', { viewBox: '0 0 120 40', class: 'w-24 h-8' }, [
      h('defs', [
        h('linearGradient', { id: 'bar-grad', x1: '0%', y1: '0%', x2: '0%', y2: '100%' }, [
          h('stop', { offset: '0%', style: 'stop-color:#0ea5e9' }),
          h('stop', { offset: '100%', style: 'stop-color:#38bdf8;stop-opacity:0.8' })
        ])
      ]),
      ...bars.value.map((bar, i) => h('rect', {
        key: i, x: bar.x, y: bar.y, width: 14, height: bar.height,
        fill: 'url(#bar-grad)', rx: 2
      }))
    ])
  }
}

// ============ Functions ============
function formatNumber(n: number) {
  return new Intl.NumberFormat('vi-VN').format(n)
}

function formatTime(dateStr: string): string {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
}

function sparkFor(id: number | string, enrolled: number) {
  const numericId = typeof id === 'string' ? id.split('').reduce((a, c) => a + c.charCodeAt(0), 0) : id
  return Array.from({ length: 6 }, (_, i) => ({ x: i + 1, y: 6 + ((numericId * (i + 3) + enrolled) % 13) }))
}

function statusLabel(s: CourseStatus) {
  const labels: Record<string, string> = {
    published: 'Đang dạy', draft: 'Nháp', archived: 'Lưu trữ',
    pending_review: 'Chờ duyệt', rejected: 'Bị từ chối'
  }
  return labels[s] || s
}

function openCourse(id: number | string) {
  router.push(`/teacher/courses/${id}`)
}

async function loadCourses() {
  try {
    const { items } = await courseService.list({ page: 1, pageSize: 8 })
    source.value = (items as CourseSummary[]).map(c => ({
      id: String(c.id), title: c.title,
      enrolled: Number(c.enrollments) || 0, status: c.status as CourseStatus
    }))
  } catch { source.value = [] }
  finally { loading.value = false }
}

async function computeTotals() {
  try {
    const res = await courseService.list({ page: 1, pageSize: 100 })
    const items = res.items as CourseSummary[]
    totals.value = {
      courses: res.total || items.length,
      students: items.reduce((sum, c) => sum + (c.enrollments || 0), 0),
      assignments: items.reduce((sum, c) => sum + (c.lessonsCount || 0), 0)
    }
  } catch { /* ignore */ }
}

async function loadEvents() {
  try {
    loadingEvents.value = true
    upcomingEvents.value = await eventService.getUpcoming()
  } catch { /* ignore */ }
  finally { loadingEvents.value = false }
}

async function createEvent() {
  if (!eventForm.name.trim() || !eventForm.start_date) {
    showToast('Vui lòng nhập đầy đủ thông tin', 'error')
    return
  }
  savingEvent.value = true
  try {
    const startDateTime = eventForm.start_time 
      ? `${eventForm.start_date}T${eventForm.start_time}:00`
      : `${eventForm.start_date}T09:00:00`
    await eventService.create({ name: eventForm.name, description: eventForm.description, start_date: startDateTime, type: eventForm.type })
    showToast('Tạo sự kiện thành công!', 'success')
    showEventModal.value = false
    Object.assign(eventForm, { name: '', description: '', start_date: '', start_time: '', type: 'other' })
    await loadEvents()
  } catch (e: any) {
    showToast(e?.response?.data?.detail || 'Không thể tạo sự kiện', 'error')
  } finally { savingEvent.value = false }
}

onMounted(() => Promise.all([loadCourses(), computeTotals(), loadEvents()]))
</script>

<style scoped>
/* Dark mode date/time picker styling */
:deep(input[type="date"].dark-date-picker),
:deep(input[type="time"].dark-date-picker) {
  color-scheme: dark;
}

:deep(input[type="date"].dark-date-picker::-webkit-calendar-picker-indicator),
:deep(input[type="time"].dark-date-picker::-webkit-calendar-picker-indicator) {
  filter: invert(1);
}
</style>
