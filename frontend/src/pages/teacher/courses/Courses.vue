<!-- src/pages/teacher/courses/Courses.vue -->
<template>
  <div class="min-h-screen w-full overflow-x-hidden" :class="isDark ? 'bg-slate-950' : 'bg-slate-50'">
    <main class="w-full mx-auto max-w-screen-2xl px-4 py-6 sm:px-6 md:px-10 md:py-8">
      <!-- Header -->
      <div class="mb-6 flex flex-col items-stretch justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h1 :class="isDark ? 'text-white' : 'text-gray-900'" class="text-2xl font-bold sm:text-3xl">Khoá học của tôi</h1>
          <p :class="isDark ? 'text-gray-400' : 'text-gray-600'" class="mt-1 text-sm">Quản lý và tổ chức các khóa học của bạn</p>
        </div>
        <button :class="primaryBtnClass" @click="createCourse">
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Tạo khoá học mới
        </button>
      </div>

      <!-- Tools -->
      <div class="mb-5 grid grid-cols-1 gap-3 md:grid-cols-3">
        <div class="md:col-span-2">
          <div :class="searchBoxClass" class="search-box flex items-center gap-2 rounded-2xl px-3 py-2">
            <svg viewBox="0 0 24 24" :class="isDark ? 'text-gray-500' : 'text-slate-400'" class="h-5 w-5" fill="none" stroke="currentColor">
              <circle cx="11" cy="11" r="8" stroke-width="2" />
              <path d="M21 21l-4.3-4.3" stroke-width="2" />
            </svg>
            <input v-model.trim="q" type="text" placeholder="Tìm khoá học…" :class="searchInputClass" @input="debouncedFetch()" />
          </div>
        </div>
        <div class="grid grid-cols-1 gap-2 sm:grid-cols-2">
          <select v-model="status" @change="fetch()" :class="selectClass">
            <option value="all">Tất cả trạng thái</option>
            <option value="published">Đã xuất bản</option>
            <option value="draft">Nháp</option>
            <option value="archived">Lưu trữ</option>
          </select>
          <select v-model="sort" @change="fetch()" :class="selectClass">
            <option value="updated,descending">Mới cập nhật</option>
            <option value="title,ascending">A → Z</option>
            <option value="enrollments,descending">Học sinh nhiều</option>
          </select>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div :class="statCardClass" class="rounded-2xl p-4">
          <div class="flex items-center justify-between">
            <div>
              <p :class="isDark ? 'text-gray-400' : 'text-gray-600'" class="text-sm font-medium">Tổng khóa học</p>
              <p :class="isDark ? 'text-white' : 'text-gray-900'" class="mt-1 text-2xl font-bold">{{ total }}</p>
            </div>
            <div :class="isDark ? 'bg-cyan-500/20' : 'bg-cyan-100'" class="rounded-full p-3">
              <svg :class="isDark ? 'text-cyan-400' : 'text-cyan-600'" class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
          </div>
        </div>
        <div :class="statCardClass" class="rounded-2xl p-4">
          <div class="flex items-center justify-between">
            <div>
              <p :class="isDark ? 'text-gray-400' : 'text-gray-600'" class="text-sm font-medium">Đã xuất bản</p>
              <p :class="isDark ? 'text-white' : 'text-gray-900'" class="mt-1 text-2xl font-bold">{{ publishedCount }}</p>
            </div>
            <div :class="isDark ? 'bg-emerald-500/20' : 'bg-emerald-100'" class="rounded-full p-3">
              <svg :class="isDark ? 'text-emerald-400' : 'text-emerald-600'" class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>
        <div :class="statCardClass" class="rounded-2xl p-4">
          <div class="flex items-center justify-between">
            <div>
              <p :class="isDark ? 'text-gray-400' : 'text-gray-600'" class="text-sm font-medium">Tổng học sinh</p>
              <p :class="isDark ? 'text-white' : 'text-gray-900'" class="mt-1 text-2xl font-bold">{{ totalEnrollments }}</p>
            </div>
            <div :class="isDark ? 'bg-amber-500/20' : 'bg-amber-100'" class="rounded-full p-3">
              <svg :class="isDark ? 'text-amber-400' : 'text-amber-600'" class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <div v-for="i in pageSize" :key="i" :class="cardClass" class="rounded-2xl overflow-hidden animate-pulse">
          <div class="h-48" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'" />
          <div class="p-4 space-y-3">
            <div class="h-4 w-3/4 rounded" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'" />
            <div class="h-3 w-1/2 rounded" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'" />
            <div class="h-8 w-full rounded" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'" />
          </div>
        </div>
      </div>

      <!-- Course List -->
      <div v-else-if="items.length" class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <article v-for="c in items" :key="String(c.id)" :class="cardClass" class="group relative flex flex-col rounded-2xl transition-all hover:shadow-lg hover:-translate-y-1 overflow-hidden">
          <!-- Thumbnail -->
          <div class="relative h-48 w-full" :class="[isDark ? 'bg-slate-800' : 'bg-slate-100', openMenuId === c.id ? 'overflow-visible' : 'overflow-hidden']">
            <img v-if="getImageUrl(c.thumbnail)" :src="getImageUrl(c.thumbnail)" :alt="c.title" class="h-full w-full object-cover transition-transform group-hover:scale-105" :class="isDark ? 'opacity-60 brightness-75' : ''" @error="handleImageError" />
            <div v-if="getImageUrl(c.thumbnail) && isDark" class="absolute inset-0 bg-slate-900/50 pointer-events-none"></div>
            <div v-if="!getImageUrl(c.thumbnail)" class="flex h-full items-center justify-center">
              <svg :class="isDark ? 'text-slate-600' : 'text-slate-300'" class="h-16 w-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <!-- Status Badge -->
            <div class="absolute top-3 right-3">
              <span class="rounded-full border px-3 py-1 text-xs font-semibold shadow-sm" :class="badgeClass(c.status)">{{ statusText(c.status) }}</span>
            </div>
            <!-- Actions Menu -->
            <div class="absolute top-3 left-3">
              <div class="relative">
                <button @click.stop="toggleMenu(c.id)" :class="isDark ? 'bg-slate-800/90 hover:bg-slate-700' : 'bg-white/90 hover:bg-white'" class="rounded-full p-1.5 shadow-sm transition">
                  <svg :class="isDark ? 'text-gray-300' : 'text-gray-700'" class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                  </svg>
                </button>
                <!-- Dropdown Menu -->
                <div v-if="openMenuId === c.id" :class="menuClass" class="absolute left-0 top-full mt-2 min-w-[200px] w-auto rounded-xl shadow-xl z-50" @click.stop>
                  <button :class="menuItemClass" @click="viewDetail(c.id); closeMenu()">
                    <svg class="h-4 w-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                    Xem chi tiết
                  </button>
                  <button :class="menuItemClass" @click="openLibrary(c.id); closeMenu()">
                    <svg class="h-4 w-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                    Thư viện nội dung
                  </button>
                  <div :class="isDark ? 'border-white/5' : 'border-slate-100'" class="border-t" />
                  <button v-if="c.status !== 'published'" class="w-full px-4 py-2.5 text-left text-sm text-emerald-500 hover:bg-emerald-500/10 transition flex items-center gap-2" @click="publishCourse(c); closeMenu()">
                    <svg class="h-4 w-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    Xuất bản
                  </button>
                  <button v-else class="w-full px-4 py-2.5 text-left text-sm text-amber-500 hover:bg-amber-500/10 transition flex items-center gap-2" @click="unpublishCourse(c); closeMenu()">
                    <svg class="h-4 w-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    Gỡ xuất bản
                  </button>
                  <button v-if="c.status !== 'archived'" :class="menuItemClass" @click="archiveCourse(c); closeMenu()">
                    <svg class="h-4 w-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" /></svg>
                    Lưu trữ
                  </button>
                  <button v-else class="w-full px-4 py-2.5 text-left text-sm text-blue-500 hover:bg-blue-500/10 transition flex items-center gap-2" @click="restoreCourse(c); closeMenu()">
                    <svg class="h-4 w-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
                    Khôi phục
                  </button>
                  <div :class="isDark ? 'border-white/5' : 'border-slate-100'" class="border-t" />
                  <button class="w-full px-4 py-2.5 text-left text-sm text-rose-500 hover:bg-rose-500/10 transition flex items-center gap-2" @click="confirmDelete(c); closeMenu()">
                    <svg class="h-4 w-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                    Xóa khóa học
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Content -->
          <div class="flex flex-1 flex-col p-5">
            <h3 :class="isDark ? 'text-white hover:text-cyan-400' : 'text-gray-900 hover:text-cyan-600'" class="mb-2 line-clamp-2 text-lg font-bold cursor-pointer transition" @click="viewDetail(c.id)" :title="c.title">{{ c.title }}</h3>
            <div :class="isDark ? 'text-gray-400' : 'text-gray-600'" class="mb-4 flex flex-wrap items-center gap-3 text-sm">
              <span class="flex items-center gap-1">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
                {{ c.lessonsCount }} bài học
              </span>
              <span class="flex items-center gap-1">
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
                {{ c.enrollments }} học sinh
              </span>
            </div>
            <div :class="isDark ? 'border-white/5' : 'border-slate-100'" class="mt-auto flex items-center justify-between border-t pt-4">
              <span :class="isDark ? 'text-gray-500' : 'text-gray-500'" class="text-xs">Cập nhật {{ fmtDate(c.updatedAt) }}</span>
              <button :class="editBtnClass" @click="editCourse(c.id)">Chỉnh sửa</button>
            </div>
          </div>
        </article>
      </div>

      <!-- Empty State -->
      <div v-else :class="isDark ? 'border-slate-700 bg-slate-900/50' : 'border-slate-300 bg-white'" class="mt-16 flex flex-col items-center justify-center rounded-3xl border-2 border-dashed px-6 py-16 text-center">
        <svg :class="isDark ? 'text-slate-600' : 'text-slate-400'" class="h-16 w-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
        <h3 :class="isDark ? 'text-white' : 'text-gray-900'" class="mt-4 text-lg font-semibold">Chưa có khóa học nào</h3>
        <p :class="isDark ? 'text-gray-400' : 'text-gray-500'" class="mt-2 max-w-sm text-sm">Bắt đầu tạo khóa học đầu tiên của bạn để chia sẻ kiến thức với học sinh.</p>
        <button :class="primaryBtnClass" class="mt-6" @click="createCourse">
          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
          Tạo khóa học đầu tiên
        </button>
      </div>

      <!-- Pager -->
      <div v-if="total > pageSize" class="mt-8 flex flex-wrap items-center justify-center gap-2">
        <button :class="pagerBtnClass" :disabled="page <= 1" @click="go(page - 1)">‹</button>
        <button v-for="p in pagesToShow" :key="p.key" :disabled="p.sep" @click="!p.sep && go(p.num!)"
          class="inline-flex h-10 min-w-[40px] items-center justify-center rounded-xl border text-sm font-semibold transition"
          :class="p.sep ? 'border-transparent bg-transparent text-slate-400' : p.num === page ? (isDark ? 'border-cyan-500 bg-cyan-600 text-white' : 'border-slate-900 bg-slate-900 text-white') : pagerBtnClass">
          {{ p.text }}
        </button>
        <button :class="pagerBtnClass" :disabled="page >= totalPages" @click="go(page + 1)">›</button>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { courseService, type CourseSummary, type CourseStatus } from '@/services/course.service'
import { showToast } from '@/utils/toast'
import { showConfirm } from '@/utils/confirm'
import { resolveMediaUrl } from '@/utils/media'
import { useThemeStore } from '@/store/theme.store'

const router = useRouter()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

// ============ Styles ============
const primaryBtnClass = computed(() => [
  'inline-flex items-center justify-center gap-2 rounded-lg px-6 py-3 font-semibold text-white transition',
  isDark.value ? 'bg-cyan-600 hover:bg-cyan-500' : 'bg-slate-900 hover:bg-slate-800'
])
const searchBoxClass = computed(() => isDark.value ? 'bg-white/5 border border-white/10' : 'border border-slate-200 bg-white')
const searchInputClass = computed(() => ['search-input w-full bg-transparent outline-none', isDark.value ? 'text-white placeholder-gray-500' : 'placeholder-slate-400'])
const selectClass = computed(() => [
  'rounded-2xl border px-3 py-2 text-sm outline-none',
  isDark.value ? 'bg-slate-900/50 border-slate-700 text-white' : 'border-slate-200 bg-white'
])
const statCardClass = computed(() => isDark.value ? 'bg-slate-900/50' : 'border border-slate-200 bg-white shadow-sm')
const cardClass = computed(() => isDark.value ? 'bg-slate-900/50' : 'border border-slate-200 bg-white shadow-sm')
const menuClass = computed(() => isDark.value ? 'bg-slate-900 border border-slate-700' : 'border border-slate-200 bg-white')
const menuItemClass = computed(() => [
  'w-full px-4 py-2.5 text-left text-sm transition flex items-center gap-2',
  isDark.value ? 'text-gray-300 hover:bg-white/5' : 'text-gray-700 hover:bg-slate-50'
])
const editBtnClass = computed(() => [
  'rounded-lg px-4 py-2 text-sm font-semibold transition',
  isDark.value ? 'bg-cyan-600 text-white hover:bg-cyan-500' : 'bg-slate-900 text-white hover:bg-slate-800'
])
const pagerBtnClass = computed(() => [
  'inline-flex h-10 w-10 items-center justify-center rounded-lg border text-sm font-bold transition disabled:cursor-not-allowed disabled:opacity-40',
  isDark.value ? 'border-slate-700 bg-slate-900/50 text-gray-300 hover:bg-slate-800' : 'border-slate-200 bg-white text-slate-700 hover:bg-slate-50'
])

// ============ State ============
const q = ref('')
const status = ref<'all' | CourseStatus>('all')
const sort = ref<'updated,descending' | 'title,ascending' | 'enrollments,descending'>('updated,descending')
const items = ref<CourseSummary[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(8)
const loading = ref(true)
const openMenuId = ref<string | number | null>(null)
const deleting = ref(false)

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))
const publishedCount = computed(() => items.value.filter(c => c.status === 'published').length)
const totalEnrollments = computed(() => items.value.reduce((sum, c) => sum + (Number(c.enrollments) || 0), 0))

const pagesToShow = computed(() => {
  const max = totalPages.value, cur = page.value, windowSize = 5
  const arr: { key: string; num?: number; text: string; sep?: boolean }[] = []
  const push = (n: number) => arr.push({ key: 'p' + n, num: n, text: String(n) })
  const sep = (k: string) => arr.push({ key: k, text: '…', sep: true })
  if (max <= windowSize + 2) { for (let i = 1; i <= max; i++) push(i) }
  else {
    push(1)
    const start = Math.max(2, cur - 1), end = Math.min(max - 1, cur + 1)
    if (start > 2) sep('s')
    for (let i = start; i <= end; i++) push(i)
    if (end < max - 1) sep('e')
    push(max)
  }
  return arr
})

// ============ Fetch ============
async function fetch(p = page.value) {
  loading.value = true; page.value = p
  try {
    const [sortBy, sortDir] = (sort.value as string).split(',') as any
    const res = await courseService.list({ q: q.value || undefined, status: status.value === 'all' ? undefined : status.value, sortBy, sortDir, page: page.value, pageSize: pageSize.value })
    items.value = res.items; total.value = res.total
  } catch { items.value = []; total.value = 0 }
  finally { loading.value = false }
}

let t: number | null = null
function debouncedFetch() { if (t) clearTimeout(t); t = window.setTimeout(() => fetch(1), 300) as unknown as number }

// ============ Helpers ============
function badgeClass(s: CourseStatus) {
  if (isDark.value) {
    return s === 'published' ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
      : s === 'draft' ? 'bg-amber-500/20 text-amber-400 border-amber-500/30'
      : s === 'archived' ? 'bg-slate-500/20 text-slate-400 border-slate-500/30'
      : s === 'pending_review' ? 'bg-sky-500/20 text-sky-400 border-sky-500/30'
      : 'bg-rose-500/20 text-rose-400 border-rose-500/30'
  }
  return s === 'published' ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
    : s === 'draft' ? 'bg-amber-50 text-amber-700 border-amber-200'
    : s === 'archived' ? 'bg-slate-100 text-slate-700 border-slate-200'
    : s === 'pending_review' ? 'bg-sky-50 text-sky-700 border-sky-200'
    : 'bg-rose-50 text-rose-700 border-rose-200'
}
function statusText(s: CourseStatus) { return s === 'published' ? 'Đã xuất bản' : s === 'pending_review' ? 'Chờ duyệt' : s === 'draft' ? 'Nháp' : s === 'rejected' ? 'Từ chối' : 'Lưu trữ' }
function fmtDate(iso?: string) { if (!iso) return ''; try { return new Date(iso).toLocaleString() } catch { return iso } }
function getImageUrl(thumbnail: string | undefined): string { return resolveMediaUrl(thumbnail) }
function handleImageError(event: Event) { const img = event.target as HTMLImageElement; img.onerror = null; img.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="320" height="180" viewBox="0 0 320 180"><rect width="320" height="180" fill="%23f3f4f6"/></svg>' }
function go(p: number) { fetch(p) }
function toggleMenu(id: string | number) { openMenuId.value = openMenuId.value === id ? null : id }
function closeMenu() { openMenuId.value = null }

// ============ Actions ============
function createCourse() { router.push({ path: '/teacher/courses/new' }) }
function viewDetail(id: string | number) { router.push({ path: `/teacher/courses/${id}` }) }
function openLibrary(id: string | number) { router.push({ path: '/teacher/courses/content-library', query: { courseId: String(id) } }) }
function editCourse(id: string | number) { router.push({ path: `/teacher/courses/${id}/edit` }) }

async function confirmDelete(course: CourseSummary) {
  if (!await showConfirm({ message: `Bạn chắc chắn muốn xóa khóa học "${course.title}"?`, title: 'Xác nhận xóa', type: 'danger', confirmText: 'Xóa', cancelText: 'Hủy' })) return
  deleting.value = true
  try { await courseService.delete(course.id); showToast('Đã xóa khóa học', 'success'); await fetch(page.value) }
  catch (e: any) { showToast(e?.response?.data?.detail || e?.message || 'Không thể xóa', 'error') }
  finally { deleting.value = false }
}
async function publishCourse(course: CourseSummary) {
  try { await courseService.publishCourse(course.id); showToast('Đã xuất bản', 'success'); await fetch(page.value) }
  catch (e: any) { showToast(e?.response?.data?.detail || e?.message || 'Không thể xuất bản', 'error') }
}
async function unpublishCourse(course: CourseSummary) {
  try { await courseService.unpublishCourse(course.id); showToast('Đã gỡ xuất bản', 'success'); await fetch(page.value) }
  catch (e: any) { showToast(e?.message || 'Không thể gỡ xuất bản', 'error') }
}
async function archiveCourse(course: CourseSummary) {
  try { await courseService.archiveCourse(course.id); showToast('Đã lưu trữ', 'success'); await fetch(page.value) }
  catch (e: any) { showToast(e?.message || 'Không thể lưu trữ', 'error') }
}
async function restoreCourse(course: CourseSummary) {
  try { await courseService.restoreCourse(course.id); showToast('Đã khôi phục', 'success'); await fetch(page.value) }
  catch (e: any) { showToast(e?.message || 'Không thể khôi phục', 'error') }
}

onMounted(() => { fetch(); document.addEventListener('click', closeMenu) })
onBeforeUnmount(() => { document.removeEventListener('click', closeMenu); if (t) clearTimeout(t) })
</script>

<style scoped>
.search-box .search-input {
  background-color: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
}

.search-box .search-input:focus {
  border-color: transparent !important;
  box-shadow: none !important;
}
</style>

<style scoped>
h3 { word-break: break-word; }
</style>
