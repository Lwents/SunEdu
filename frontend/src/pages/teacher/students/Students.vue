<template>
  <div class="students-page min-h-screen w-full overflow-x-hidden" :class="pageClass">
    <main class="w-full mx-auto max-w-screen-2xl px-4 py-6 sm:px-6 md:px-10">
      <!-- Header -->
      <div class="mb-4 sm:mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <h1 :class="titleClass" class="text-xl font-semibold sm:text-2xl">Học viên của tôi</h1>
      </div>

      <!-- Tools -->
      <div :class="filterPanelClass" class="mb-5 rounded-3xl border p-4 sm:p-5">
        <div class="grid grid-cols-1 gap-2 sm:gap-3 md:grid-cols-4">
        <!-- Search -->
        <div class="md:col-span-2">
          <label class="sr-only">Tìm kiếm</label>
          <div :class="controlShellClass" class="search-shell flex items-center gap-2 rounded-2xl border px-3 py-2.5">
            <svg
              viewBox="0 0 24 24"
              class="h-5 w-5 shrink-0"
              :class="iconClass"
              fill="none"
              stroke="currentColor"
              aria-hidden="true"
            >
              <circle cx="11" cy="11" r="8" stroke-width="2" />
              <path d="M21 21l-4.3-4.3" stroke-width="2" />
            </svg>
            <input
              v-model.trim="q"
              type="text"
              placeholder="Tìm tên, username, email…"
              :class="['search-input', controlInputClass]"
              @input="onChanged(true)"
            />
          </div>
        </div>

        <!-- Course Filter -->
        <div class="select-wrap">
          <select v-model="selectedCourseId" :class="selectClass" @change="onChanged(true)">
            <option value="">Tất cả khóa học</option>
            <option v-for="course in courses" :key="course.id" :value="course.id">
              {{ course.title }}
            </option>
          </select>
          <span class="select-chevron" :class="iconClass" aria-hidden="true">
            <svg viewBox="0 0 20 20" fill="currentColor" class="h-4 w-4">
              <path
                fill-rule="evenodd"
                d="M5.23 7.21a.75.75 0 011.06.02L10 10.17l3.71-2.94a.75.75 0 111.04 1.08l-4.24 3.36a.75.75 0 01-.94 0L5.21 8.31a.75.75 0 01.02-1.1z"
                clip-rule="evenodd"
              />
            </svg>
          </span>
        </div>

        <!-- Sort -->
        <div class="select-wrap">
          <select v-model="sortBy" :class="selectClass" @change="onChanged(true)">
            <option value="name">Tên (A→Z)</option>
            <option value="courses">Số khóa học</option>
          </select>
          <span class="select-chevron" :class="iconClass" aria-hidden="true">
            <svg viewBox="0 0 20 20" fill="currentColor" class="h-4 w-4">
              <path
                fill-rule="evenodd"
                d="M5.23 7.21a.75.75 0 011.06.02L10 10.17l3.71-2.94a.75.75 0 111.04 1.08l-4.24 3.36a.75.75 0 01-.94 0L5.21 8.31a.75.75 0 01.02-1.1z"
                clip-rule="evenodd"
              />
            </svg>
          </span>
        </div>
      </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="py-16 text-center" :class="subtleTextClass">Đang tải…</div>

      <!-- List -->
      <div v-else class="grid grid-cols-1 gap-3">
        <article
          v-for="student in filteredList"
          :key="student.id"
          :class="listCardClass"
          class="flex flex-wrap items-center gap-3 sm:gap-4 rounded-2xl border p-3 sm:p-4 transition"
        >
          <img
            :src="getStudentAvatar(student)"
            :alt="student.name"
            class="h-12 w-12 rounded-full object-cover border-2"
            :class="avatarClass"
          />

          <div class="min-w-0 flex-1">
            <div class="flex flex-wrap items-center gap-x-2 gap-y-1">
              <h3 class="truncate font-semibold" :class="titleClass">{{ student.name }}</h3>
              <span class="truncate text-xs" :class="subtleTextClass">@{{ student.username }}</span>
              <span
                v-if="student.courses.length > 0"
                :class="badgeClass"
                class="rounded-full border px-2 py-0.5 text-xs font-semibold"
              >
                {{ student.courses.length }} khóa học
              </span>
            </div>

            <div class="mt-1 truncate text-xs sm:text-sm" :class="subtleTextClass">
              {{ student.email }}
            </div>
          </div>

          <div class="flex w-full sm:w-auto shrink-0 gap-2">
            <button
              class="flex-1 sm:flex-none rounded-xl border px-4 py-2 text-sm font-semibold transition"
              :class="actionBtnClass"
              @click="openFeedback(student.id)"
            >
              Phản hồi
            </button>
          </div>
        </article>

        <div v-if="!filteredList.length && !loading" class="mt-10 text-center">
          <div class="mx-auto max-w-md">
            <div :class="emptyIconClass" class="mx-auto mb-4 h-20 w-20 rounded-full flex items-center justify-center">
              <svg class="h-10 w-10" :class="emptyIconColorClass" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
            <h3 class="text-lg font-bold" :class="titleClass">Không có học viên</h3>
            <p class="mt-2 text-sm" :class="subtleTextClass">
              {{ error || 'Hiện tại chưa có học viên nào tham gia các khóa học của bạn.' }}
            </p>
            <p v-if="!error" class="mt-1 text-xs" :class="subtleTextClass">
              Học viên sẽ xuất hiện ở đây sau khi họ đăng ký vào các khóa học của bạn.
            </p>
          </div>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="error && !loading" :class="errorCardClass" class="mt-4 rounded-2xl border p-5 shadow-lg">
        <div class="flex items-start gap-3">
          <svg class="h-5 w-5 shrink-0 mt-0.5" :class="errorIconClass" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
          </svg>
          <div class="flex-1">
            <p class="font-semibold" :class="errorTextClass">{{ error }}</p>
            <button
              class="mt-2 text-sm underline"
              :class="errorLinkClass"
              @click="fetchList"
            >
              Thử lại
            </button>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div class="mt-6">
        <!-- Compact on mobile -->
        <div
          v-if="isCompact"
          class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2"
        >
          <div class="text-sm" :class="subtleTextClass">
            Tổng {{ total }} • Trang {{ page }} / {{ totalPages || 1 }}
          </div>
          <div class="flex items-center gap-2">
            <button
              class="rounded-xl border px-3 py-2 text-sm disabled:opacity-50"
              :class="pagerBtnClass"
              :disabled="page <= 1"
              @click="go(page - 1)"
            >
              Trước
            </button>
            <span class="text-sm" :class="subtleTextClass">Trang {{ page }} / {{ totalPages || 1 }}</span>
            <button
              class="rounded-xl border px-3 py-2 text-sm disabled:opacity-50"
              :class="pagerBtnClass"
              :disabled="page >= totalPages"
              @click="go(page + 1)"
            >
              Sau
            </button>

            <div class="select-wrap ml-1">
              <select v-model.number="pageSize" :class="pagerSelectClass" @change="onChanged(true)">
                <option :value="10">10 / trang</option>
                <option :value="20">20 / trang</option>
                <option :value="50">50 / trang</option>
              </select>
              <span class="select-chevron" :class="iconClass" aria-hidden="true">
                <svg viewBox="0 0 20 20" fill="currentColor" class="h-4 w-4">
                  <path
                    fill-rule="evenodd"
                    d="M5.23 7.21a.75.75 0 011.06.02L10 10.17l3.71-2.94a.75.75 0 111.04 1.08l-4.24 3.36a.75.75 0 01-.94 0L5.21 8.31a.75.75 0 01.02-1.1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </span>
            </div>
          </div>
        </div>

        <!-- Full on ≥ md -->
        <div v-else class="flex items-center justify-between">
          <div class="text-sm" :class="subtleTextClass">
            Tổng {{ total }} • Trang {{ page }} / {{ totalPages || 1 }}
          </div>
          <div class="flex items-center gap-2">
            <button
              class="rounded-xl border px-3 py-2 text-sm disabled:opacity-50"
              :class="pagerBtnClass"
              :disabled="page <= 1"
              @click="go(page - 1)"
            >
              Trước
            </button>

            <div class="select-wrap">
              <select v-model.number="page" :class="[pagerSelectClass, 'h-10 w-[92px]']" @change="go(page)">
                <option v-for="p in Math.max(totalPages, 1)" :key="p" :value="p">{{ p }}</option>
              </select>
              <span class="select-chevron" :class="iconClass" aria-hidden="true">
                <svg viewBox="0 0 20 20" fill="currentColor" class="h-4 w-4">
                  <path
                    fill-rule="evenodd"
                    d="M5.23 7.21a.75.75 0 011.06.02L10 10.17l3.71-2.94a.75.75 0 111.04 1.08l-4.24 3.36a.75.75 0 01-.94 0L5.21 8.31a.75.75 0 01.02-1.1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </span>
            </div>

            <button
              class="rounded-xl border px-3 py-2 text-sm disabled:opacity-50"
              :class="pagerBtnClass"
              :disabled="page >= totalPages"
              @click="go(page + 1)"
            >
              Sau
            </button>

            <div class="select-wrap ml-1">
              <select v-model.number="pageSize" :class="[pagerSelectClass, 'h-10']" @change="onChanged(true)">
                <option :value="10">10 / trang</option>
                <option :value="20">20 / trang</option>
                <option :value="50">50 / trang</option>
              </select>
              <span class="select-chevron" :class="iconClass" aria-hidden="true">
                <svg viewBox="0 0 20 20" fill="currentColor" class="h-4 w-4">
                  <path
                    fill-rule="evenodd"
                    d="M5.23 7.21a.75.75 0 011.06.02L10 10.17l3.71-2.94a.75.75 0 111.04 1.08l-4.24 3.36a.75.75 0 01-.94 0L5.21 8.31a.75.75 0 01.02-1.1z"
                    clip-rule="evenodd"
                  />
                </svg>
              </span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { teacherService, type TeacherStudent } from '@/services/teacher.service'
import { courseService } from '@/services/course.service'
import { getAvatarSrc } from '@/utils/avatar'
import { useThemeStore } from '@/store/theme.store'

const router = useRouter()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const loading = ref(false)
const list = ref<TeacherStudent[]>([])
const total = ref(0)
const courses = ref<Array<{ id: string; title: string }>>([])

// Filters
const q = ref('')
const selectedCourseId = ref('')
const sortBy = ref<'name' | 'courses'>('name')

// Pagination
const page = ref(1)
const pageSize = ref(20)
const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

// Responsive flag
const isCompact = ref(false)
function updateCompact() {
  isCompact.value = window.innerWidth < 640
}

// Fetch courses for filter
async function fetchCourses() {
  try {
    const { items } = await courseService.list({ page: 1, pageSize: 100 })
    courses.value = items.map(c => ({ id: String(c.id), title: c.title }))
  } catch (e) {
    console.error('Error fetching courses:', e)
  }
}

// Fetch students
const error = ref('')
async function fetchList() {
  loading.value = true
  error.value = ''
  try {
    const params = {
      q: q.value || undefined,
      courseId: selectedCourseId.value || undefined,
      page: page.value,
      pageSize: pageSize.value
    }
    const response = await teacherService.getStudents(params)
    list.value = response.items || []
    total.value = response.total || 0
  } catch (e: any) {
    console.error('Error fetching students:', e)
    error.value = e?.message || 'Không thể tải danh sách học viên'
    list.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// Filtered and sorted list
const filteredList = computed(() => {
  const arr = list.value.slice()
  
  // Sort
  if (sortBy.value === 'courses') {
    arr.sort((a, b) => (b.courses?.length || 0) - (a.courses?.length || 0))
  } else {
    arr.sort((a, b) => (a.name || '').localeCompare(b.name || ''))
  }
  
  return arr
})

const pageClass = computed(() => isDark.value ? 'bg-slate-950 text-slate-100' : 'bg-slate-50 text-slate-900')
const titleClass = computed(() => isDark.value ? 'text-white' : 'text-slate-900')
const subtleTextClass = computed(() => isDark.value ? 'text-slate-400' : 'text-slate-600')
const iconClass = computed(() => isDark.value ? 'text-slate-500' : 'text-slate-400')
const filterPanelClass = computed(() => isDark.value
  ? 'border-slate-800/80 bg-slate-900/60 shadow-[0_10px_30px_rgba(6,10,20,0.35)]'
  : 'border-slate-200 bg-white shadow-sm'
)
const controlShellClass = computed(() => isDark.value ? 'border-slate-800/80 bg-slate-950/60' : 'border-slate-200 bg-white')
const controlInputClass = computed(() => [
  'w-full bg-transparent outline-none text-sm sm:text-base',
  isDark.value ? 'text-slate-100 placeholder-slate-500' : 'text-slate-700 placeholder-slate-400'
])
const selectClass = computed(() => [
  'select-base transition-colors focus:ring-2',
  isDark.value
    ? 'border-slate-800/80 bg-slate-950/60 text-slate-100 focus:border-cyan-400 focus:ring-cyan-500/20'
    : 'border-slate-200 bg-white text-slate-700 focus:border-slate-400 focus:ring-slate-200'
])
const listCardClass = computed(() => isDark.value
  ? 'border-slate-800/80 bg-slate-900/50 hover:border-slate-700/80 hover:shadow-[0_12px_28px_rgba(8,15,30,0.35)]'
  : 'border-slate-200 bg-white hover:shadow-sm'
)
const avatarClass = computed(() => isDark.value ? 'border-slate-700' : 'border-slate-200')
const badgeClass = computed(() => isDark.value
  ? 'border-cyan-500/30 bg-cyan-500/10 text-cyan-200'
  : 'border-cyan-200 bg-cyan-50 text-cyan-700'
)
const actionBtnClass = computed(() => isDark.value
  ? 'border-slate-700 bg-slate-900/70 text-slate-200 hover:bg-slate-800'
  : 'border-slate-300 bg-white text-gray-700 hover:bg-slate-50'
)
const emptyIconClass = computed(() => isDark.value
  ? 'bg-slate-900/70 border border-slate-800/80'
  : 'bg-gradient-to-br from-slate-100 to-slate-200'
)
const emptyIconColorClass = computed(() => isDark.value ? 'text-slate-500' : 'text-slate-400')
const errorCardClass = computed(() => isDark.value
  ? 'border-rose-500/30 bg-rose-500/10'
  : 'border-rose-200 bg-gradient-to-r from-rose-50 to-pink-50'
)
const errorIconClass = computed(() => isDark.value ? 'text-rose-300' : 'text-rose-600')
const errorTextClass = computed(() => isDark.value ? 'text-rose-100' : 'text-rose-900')
const errorLinkClass = computed(() => isDark.value ? 'text-rose-200 hover:text-rose-100' : 'text-rose-700 hover:text-rose-900')
const pagerBtnClass = computed(() => isDark.value
  ? 'border-slate-700 bg-slate-900/70 text-slate-200 hover:bg-slate-800'
  : 'border-slate-300 bg-white text-slate-700 hover:bg-slate-50'
)
const pagerSelectClass = computed(() => [
  'select-base transition-colors focus:ring-2',
  isDark.value
    ? 'border-slate-700 bg-slate-900/70 text-slate-200 focus:border-cyan-400 focus:ring-cyan-500/20'
    : 'border-slate-300 bg-white text-slate-700 focus:border-slate-400 focus:ring-slate-200'
])

function onChanged(resetPage = false) {
  if (resetPage) page.value = 1
  debouncedFetch()
}

function go(p: number) {
  page.value = p
  fetchList()
}

function openFeedback(id: string | number) {
  router.push({ path: '/teacher/students/feedback', query: { id: String(id) } })
}

function getStudentAvatar(student: TeacherStudent): string {
  return getAvatarSrc(
    student.avatar,
    student.gender as 'male' | 'female' | 'other' | null | undefined,
    'student'
  )
}

// Debounce fetch
let t: number | undefined
function debouncedFetch(delay = 300) {
  if (t) window.clearTimeout(t)
  t = window.setTimeout(() => fetchList(), delay)
}

// Auto fetch
watch([q, selectedCourseId, pageSize], () => onChanged(true))
onMounted(() => {
  updateCompact()
  window.addEventListener('resize', updateCompact, { passive: true })
  fetchCourses()
  fetchList()
})
</script>

<style scoped>
:host,
.min-h-screen {
  overflow-x: hidden;
}

/* ===== Custom select (cross-browser, stable size) ===== */
.select-wrap {
  position: relative;
}
.select-chevron {
  pointer-events: none;
  position: absolute;
  right: 10px;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  color: #94a3b8; /* slate-400 */
}
.select-base {
  width: 100%;
  border-radius: 1rem; /* rounded-2xl */
  border: 1px solid transparent;
  background: transparent;
  padding: 0 2.5rem 0 0.75rem; /* pr-10 + pl-3 */
  height: 40px; /* h-10 */
  font-size: 0.875rem; /* text-sm */
  line-height: 1.25rem;
  background-clip: padding-box; /* fix Safari radius */
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}
.select-base::-ms-expand {
  display: none;
} /* old Edge/IE */
.select-base:focus {
  outline: none;
}
</style>
