<!-- src/pages/teacher/dashboard/dashboard.vue -->
<template>
  <div class="min-h-screen w-full overflow-x-hidden bg-slate-50">
    <main class="w-full mx-auto max-w-screen-2xl px-4 py-6 sm:px-6 md:px-10 md:py-8">
      <h1 class="mb-4 text-xl sm:text-2xl font-semibold">Bảng điều khiển</h1>

      <div class="grid grid-cols-1 gap-4 sm:gap-6 xl:grid-cols-3">
        <div class="space-y-4 sm:space-y-6 xl:col-span-2">
          <!-- Thao tác nhanh -->
          <Card>
            <CardHeader title="Thao tác nhanh" />
            <div class="grid grid-cols-2 gap-2 p-3 sm:grid-cols-4 sm:gap-3 sm:p-4">
              <QuickAction label="Tạo khoá học" :onClick="goCreateCourse"><IconPlus /></QuickAction>
              <QuickAction label="Xem bài kiểm tra" :onClick="goGradeAssignments"><IconClipboard /></QuickAction>
              <QuickAction label="Tạo bài kiểm tra" :onClick="goCreateExam"><IconFile /></QuickAction>
              <QuickAction label="Xem báo cáo" :onClick="goReports"><IconChart /></QuickAction>
            </div>
          </Card>

          <!-- Khoá học của tôi -->
          <Card>
            <CardHeader title="Khoá học của tôi" />
            <div class="space-y-2 p-3 sm:space-y-3 sm:p-4">
              <template v-if="loading">
                <div class="rounded-2xl border border-slate-200 bg-white p-6 text-center text-sm text-slate-500">
                  Đang tải dữ liệu...
                </div>
              </template>

              <template v-else-if="myCourses.length">
                <CourseItem
                  v-for="c in myCourses"
                  :key="String(c.id)"
                  :title="c.title"
                  :students="c.enrolled"
                  :status="statusLabel(c.status)"
                  :data="sparkFor(c.id, c.enrolled)"
                  :onClick="() => openCourse(c.id)"
                />
              </template>

              <div v-else class="rounded-2xl border border-slate-200 bg-white p-6 text-center text-sm text-slate-500">
                Chưa có khoá học nào.
              </div>
            </div>
          </Card>
        </div>

        <!-- Cột phải -->
        <div class="space-y-4 sm:space-y-6">
          <Card>
            <div class="flex items-center justify-between border-b p-3 pb-2 sm:p-4 sm:pb-2">
              <h2 class="text-sm font-semibold sm:text-base">Sự kiện sắp tới</h2>
              <button
                type="button"
                class="rounded-lg bg-slate-900 px-2 py-1 text-xs font-medium text-white hover:bg-slate-800"
                @click="showEventModal = true"
              >
                + Thêm
              </button>
            </div>
            <div class="p-3 sm:p-4">
              <div class="max-h-60 space-y-1.5 overflow-y-auto pr-1">
                <template v-if="loadingEvents">
                  <div class="py-4 text-center text-sm text-slate-500">Đang tải...</div>
                </template>
                <template v-else-if="upcomingEvents.length">
                  <UpcomingItem
                    v-for="e in upcomingEvents"
                    :key="e.id"
                    :title="e.name"
                    :time="e.time || formatTime(e.start_date)"
                    :type="e.type"
                  />
                </template>
                <div v-else class="py-4 text-center text-sm text-slate-500">
                  Chưa có sự kiện nào
                </div>
              </div>
            </div>
          </Card>

          <Card>
            <CardHeader title="Thống kê" />
            <div class="grid grid-cols-3 gap-2 p-3 text-center sm:gap-3 sm:p-4">
              <Stat k="Khoá học" :v="stats.courses" />
              <Stat k="Học sinh" :v="stats.students" />
              <Stat k="Bài học" :v="stats.assignments" />
            </div>
          </Card>
        </div>
      </div>
    </main>

    <!-- Event Modal -->
    <Teleport to="body">
      <div 
        v-if="showEventModal" 
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
        @click.self="showEventModal = false"
      >
        <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
          <h3 class="mb-4 text-lg font-bold">Tạo sự kiện mới</h3>
          
          <div class="space-y-4">
            <div>
              <label class="mb-1 block text-sm font-medium">Tên sự kiện *</label>
              <input
                v-model="eventForm.name"
                type="text"
                class="w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
                placeholder="VD: Kiểm tra giữa kỳ"
              />
            </div>
            
            <div>
              <label class="mb-1 block text-sm font-medium">Mô tả</label>
              <textarea
                v-model="eventForm.description"
                rows="2"
                class="w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
                placeholder="Mô tả ngắn về sự kiện..."
              ></textarea>
            </div>
            
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="mb-1 block text-sm font-medium">Ngày *</label>
                <input
                  v-model="eventForm.start_date"
                  type="date"
                  class="w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
                />
              </div>
              <div>
                <label class="mb-1 block text-sm font-medium">Giờ</label>
                <input
                  v-model="eventForm.start_time"
                  type="time"
                  class="w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-blue-500 focus:outline-none"
                />
              </div>
            </div>
            
            <!-- Loại sự kiện: bỏ chọn, mặc định 'other' -->
            <input type="hidden" v-model="eventForm.type" />
          </div>
          
          <div class="mt-6 flex justify-end gap-3">
            <button
              type="button"
              class="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium hover:bg-slate-50"
              @click="showEventModal = false"
            >
              Hủy
            </button>
            <button
              type="button"
              class="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:opacity-50"
              :disabled="savingEvent"
              @click="createEvent"
            >
              {{ savingEvent ? 'Đang tạo...' : 'Tạo sự kiện' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="tsx">
import { computed, defineComponent, type PropType, ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { courseService, type CourseStatus, type CourseSummary } from '@/services/course.service'
import { eventService, type EventItem } from '@/services/event.service'
import { showToast } from '@/utils/toast'

type Status = CourseStatus
type TeacherCourse = {
  id: string | number
  title: string
  enrolled: number
  lessons: number
  status: Status
  numericId?: number // For sparkline calculation
}

const loading = ref(true)
const source = ref<TeacherCourse[]>([])
const totals = ref({ courses: 0, students: 0, assignments: 0 })

// Events state
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

async function loadEvents() {
  try {
    loadingEvents.value = true
    upcomingEvents.value = await eventService.getUpcoming()
  } catch (e) {
    console.error('Error loading events:', e)
  } finally {
    loadingEvents.value = false
  }
}

function formatTime(dateStr: string): string {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
}

async function createEvent() {
  if (!eventForm.name.trim()) {
    showToast('Vui lòng nhập tên sự kiện', 'error')
    return
  }
  if (!eventForm.start_date) {
    showToast('Vui lòng chọn ngày bắt đầu', 'error')
    return
  }
  
  savingEvent.value = true
  try {
    const startDateTime = eventForm.start_time 
      ? `${eventForm.start_date}T${eventForm.start_time}:00`
      : `${eventForm.start_date}T09:00:00`
    
    await eventService.create({
      name: eventForm.name,
      description: eventForm.description,
      start_date: startDateTime,
      type: eventForm.type,
    })
    
    showToast('Tạo sự kiện thành công!', 'success')
    showEventModal.value = false
    resetEventForm()
    await loadEvents()
  } catch (e: any) {
    showToast(e?.response?.data?.detail || 'Không thể tạo sự kiện', 'error')
  } finally {
    savingEvent.value = false
  }
}

function resetEventForm() {
  eventForm.name = ''
  eventForm.description = ''
  eventForm.start_date = ''
  eventForm.start_time = ''
  eventForm.type = 'other'
}

async function loadCourses() {
  try {
    const { items } = await courseService.list({ page: 1, pageSize: 8 })
    source.value = (items as CourseSummary[]).map((c) => {
      // Keep id as string (UUID) to avoid NaN issues
      const courseId = String(c.id)
      // For sparkline, use a numeric hash of the UUID
      const numericId = courseId.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
      return {
        id: courseId as any, // Store as string but type as any for compatibility
      title: c.title,
        enrolled: Number(c.enrollments) || 0,
        lessons: c.lessonsCount || 0,
        status: c.status as Status,
        numericId // For sparkline calculation
      }
    })
  } catch (e) {
    console.error('Error loading courses:', e)
    source.value = Array.from({ length: 5 }, (_, i) => ({
      id: String(i + 1),
      title: `Khoá học #${i + 1}`,
      enrolled: 20 + i * 7,
      lessons: 8 + i * 3,
      status: (i % 2 === 0 ? 'published' : 'draft') as Status,
      numericId: i + 1
    }))
  } finally {
    loading.value = false
  }
}

async function computeTotals() {
  const pageSize = 50
  let page = 1
  let total = 0
  let sumStudents = 0
  let sumLessons = 0
  let knownTotal = false

  while (true) {
    const res = await courseService.list({ page, pageSize })
    if (!knownTotal) {
      total = res.total || res.items.length
      knownTotal = true
    }

    const producedSoFar = (page - 1) * pageSize
    const remaining = Math.max(0, total - producedSoFar)
    const take = Math.min(remaining, res.items.length)

    const chunk = (res.items as CourseSummary[]).slice(0, take)
    for (const c of chunk) {
      sumStudents += c.enrollments || 0
      sumLessons += c.lessonsCount || 0
    }

    if (page * pageSize >= total || take <= 0) break
    page++
    if (page > 50) break
  }

  totals.value = { courses: total, students: sumStudents, assignments: sumLessons }
}

onMounted(async () => {
  await Promise.all([loadCourses(), computeTotals(), loadEvents()])
})

type Pt = { x: number; y: number }
function sparkFor(id: number | string, enrolled: number): Pt[] {
  const n = 6
  // Convert string UUID to numeric for sparkline
  const numericId = typeof id === 'string' 
    ? id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0)
    : id
  return Array.from({ length: n }, (_, i) => {
    const y = 6 + ((numericId * (i + 3) + enrolled) % 13)
    return { x: i + 1, y }
  })
}

const myCourses = computed<TeacherCourse[]>(() => source.value.slice())
const stats = computed(() => totals.value)

const Card = defineComponent({
  name: 'Card',
  setup(_, { slots }) {
    return () => (
      <div class="overflow-hidden rounded-xl sm:rounded-2xl border border-slate-200 bg-white shadow-sm">
        {slots.default?.()}
      </div>
    )
  }
})

const CardHeader = defineComponent({
  name: 'CardHeader',
  props: { title: { type: String, required: true } },
  setup(p) {
    return () => (
      <div class="border-b p-3 pb-2 sm:p-4 sm:pb-2">
        <h2 class="text-sm font-semibold sm:text-base">{p.title}</h2>
      </div>
    )
  }
})

const QuickAction = defineComponent({
  name: 'QuickAction',
  props: {
    label: String,
    onClick: Function as PropType<() => void>
  },
  setup(props, { slots }) {
    return () => (
      <button
        type="button"
        class="w-full rounded-xl sm:rounded-2xl border border-slate-200 bg-white p-3 sm:p-4 text-left transition hover:shadow-lg focus:outline-none active:scale-95"
        onClick={props.onClick as any}
      >
        <div class="flex flex-col items-center gap-2 sm:flex-row sm:items-center sm:gap-3">
          <div class="rounded-xl sm:rounded-2xl bg-slate-100 p-2.5 sm:p-3">
            <div class="h-4 w-4 sm:h-5 sm:w-5">{slots.default?.()}</div>
          </div>
          <div class="text-xs font-medium text-center sm:text-left sm:text-sm">{props.label}</div>
        </div>
      </button>
    )
  }
})

const BarChart = defineComponent({
  name: 'BarChart',
  props: { data: { type: Array as PropType<Pt[]>, required: true } },
  setup(props) {
    const animatedHeights = ref<number[]>([])
    const isAnimating = ref(false)
    
    onMounted(() => {
      // Start animation when component mounts
      isAnimating.value = true
      const pts = props.data
      const ys = pts.map((p) => p.y)
      const minY = Math.min(...ys)
      const maxY = Math.max(...ys)
      const range = maxY - minY || 1
      
      // Initialize heights to 0
      animatedHeights.value = new Array(pts.length).fill(0)
      
      // Animate each bar
      const duration = 800
      const startTime = Date.now()
      
      const animate = () => {
        const elapsed = Date.now() - startTime
        const progress = Math.min(elapsed / duration, 1)
        
        // Easing function (ease-out)
        const easeOut = 1 - Math.pow(1 - progress, 3)
        
        animatedHeights.value = pts.map((p) => {
          const normalized = (p.y - minY) / range
          return normalized * easeOut
        })
        
        if (progress < 1) {
          requestAnimationFrame(animate)
        } else {
          isAnimating.value = false
        }
      }
      
      requestAnimationFrame(animate)
    })
    
    const d = computed(() => {
      const pts = props.data
      const w = 120
      const h = 40
      const barWidth = (w - 8) / pts.length - 2
      const maxBarHeight = h - 8
      
      return pts.map((p, i) => {
        const x = 4 + i * (barWidth + 2)
        const height = (animatedHeights.value[i] || 0) * maxBarHeight
        const y = h - 4 - height
        return { x, y, width: barWidth, height: Math.max(height, 2) }
      })
    })
    
    return () => (
      <svg viewBox="0 0 120 40" class="block h-8 w-24 leading-none sm:h-10 sm:w-32">
        <defs>
          <linearGradient id="bar-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style={{ stopColor: 'rgb(14, 165, 233)', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: 'rgb(56, 189, 248)', stopOpacity: 0.8 }} />
          </linearGradient>
        </defs>
        {d.value.map((bar, i) => (
          <rect
            key={i}
            x={bar.x}
            y={bar.y}
            width={bar.width}
            height={bar.height}
            fill="url(#bar-gradient)"
            rx="2"
            style={{ transition: 'all 0.3s ease' }}
          />
        ))}
      </svg>
    )
  }
})

const CourseItem = defineComponent({
  name: 'CourseItem',
  props: {
    title: String,
    students: Number,
    status: String,
    data: { type: Array as PropType<Pt[]>, required: true },
    onClick: Function as PropType<() => void>
  },
  setup(p) {
    return () => (
      <div
        class="flex items-center gap-2 sm:gap-4 rounded-xl sm:rounded-2xl border border-slate-200 bg-white p-3 sm:p-4 hover:bg-slate-50 cursor-pointer transition active:scale-[0.98]"
        onClick={p.onClick as any}
      >
        <div class="min-w-0 flex-1">
          <div class="text-xs font-medium sm:text-sm truncate">{p.title}</div>
          <div class="text-[10px] text-slate-500 sm:text-xs">{p.students} học viên</div>
        </div>
        <div class="ml-auto shrink-0 flex items-center justify-end">
          <BarChart data={p.data as Pt[]} />
        </div>
        <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
          {p.status ? (
            <span class="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] sm:text-xs whitespace-nowrap">{p.status}</span>
          ) : null}
          <IconChevron class="text-slate-400 h-4 w-4 sm:h-5 sm:w-5" />
        </div>
      </div>
    )
  }
})

const UpcomingItem = defineComponent({
  name: 'UpcomingItem',
  props: { title: String, time: String },
  setup(p) {
    return () => (
      <div class="flex items-center justify-between rounded-lg sm:rounded-xl p-2.5 sm:p-3 hover:bg-slate-50 transition">
        <div class="flex items-center gap-2 sm:gap-3">
          <div class="rounded-lg sm:rounded-xl bg-slate-100 p-1.5 sm:p-2">
            <IconClock class="h-3.5 w-3.5 sm:h-4 sm:w-4" />
          </div>
          <div class="text-xs sm:text-sm truncate">{p.title}</div>
        </div>
        <div class="text-[10px] text-slate-500 sm:text-xs whitespace-nowrap ml-2">{p.time}</div>
      </div>
    )
  }
})

const Stat = defineComponent({
  name: 'Stat',
  props: {
    k: { type: String, required: true },
    v: { type: Number, default: 0 }
  },
  setup(p) {
    const fmt = (n: number) => new Intl.NumberFormat('vi-VN').format(n)
    return () => (
      <div class="rounded-xl sm:rounded-2xl bg-slate-100 p-3 sm:p-4">
        <div class="text-lg font-semibold sm:text-2xl">{fmt(Number(p.v ?? 0))}</div>
        <div class="text-[10px] text-slate-500 sm:text-xs">{p.k}</div>
      </div>
    )
  }
})

const IconPlus = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-full w-full">
    <path d="M12 5v14M5 12h14" style={{ strokeWidth: 2 }} />
  </svg>
)
const IconClipboard = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-full w-full">
    <rect x="8" y="2" width="8" height="4" rx="1" style={{ strokeWidth: 2 }} />
    <path d="M9 4H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-2" style={{ strokeWidth: 2 }} />
  </svg>
)
const IconFile = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-full w-full">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12V8z" style={{ strokeWidth: 2 }} />
    <path d="M14 2v6h6" style={{ strokeWidth: 2 }} />
  </svg>
)
const IconChart = () => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" class="h-full w-full">
    <path d="M3 3v18h18" style={{ strokeWidth: 2 }} />
    <path d="M7 13l3 3 7-7" style={{ strokeWidth: 2 }} />
  </svg>
)
const IconClock = (p: any) => (
  <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor">
    <circle cx="12" cy="12" r="10" style={{ strokeWidth: 2 }} />
    <path d="M12 6v6l4 2" style={{ strokeWidth: 2 }} />
  </svg>
)
const IconChevron = (p: any) => (
  <svg {...p} viewBox="0 0 24 24" fill="none" stroke="currentColor">
    <path d="M9 18l6-6-6-6" style={{ strokeWidth: 2 }} />
  </svg>
)

function statusLabel(s: Status) {
  return s === 'published'
    ? 'Đang dạy'
    : s === 'draft'
    ? 'Nháp'
    : s === 'archived'
    ? 'Lưu trữ'
    : s === 'pending_review'
    ? 'Chờ duyệt'
    : s === 'rejected'
    ? 'Bị từ chối'
    : s
}

const router = useRouter()
function openCourse(id: number | string) {
  // Ensure id is a string (UUID) not NaN
  const courseId = String(id)
  if (courseId === 'NaN' || !courseId) {
    console.error('Invalid course ID:', id)
    return
  }
  router.push({ path: `/teacher/courses/${courseId}` })
}
const has = (name: string) => router.getRoutes().some((r) => r.name === (name as any))
const go = (name: string, path: string) => (has(name) ? router.push({ name }) : router.push({ path }))
function goCreateCourse() {
  go('teacher-course-new', '/teacher/courses/new')
}
function goGradeAssignments() {
  go('teacher-exams', '/teacher/exams')
}
function goCreateExam() {
  has('teacher-exam-new') ? router.push({ name: 'teacher-exam-new' }) : router.push({ path: '/teacher/exams' })
}
function goReports() {
  go('teacher-reports', '/teacher/reports')
}
</script>

<style scoped>
:host,
.min-h-screen {
  overflow-x: hidden;
}
</style>
