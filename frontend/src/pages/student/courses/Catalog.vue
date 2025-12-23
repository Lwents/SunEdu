<template>
  <div class="page-wrapper" :class="isDark ? 'dark-mode' : 'light-mode'">
    <div v-if="isDark" class="bg-elements">
      <div class="glow glow-1"></div>
      <div class="glow glow-2"></div>
    </div>

    <div class="page-content">
      <!-- Header -->
      <div class="page-header">
        <div>
          <h1>Catalog</h1>
          <p>Khám phá các khoá học đã phát hành theo khối & môn học.</p>
        </div>
        <router-link class="btn-outline" :to="{ name: 'student-learning-path' }">Lộ trình học →</router-link>
      </div>

      <!-- Filters -->
      <div class="filters-section">
        <div class="filters-row">
          <div class="search-box">
            <input v-model.trim="q" @keyup.enter="load" placeholder="Tìm khóa học…" />
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 21l-4.3-4.3"/><circle cx="11" cy="11" r="7"/>
            </svg>
          </div>
          <select v-model="grade" class="filter-select" @change="load">
            <option :value="undefined">Tất cả khối</option>
            <option v-for="g in [1,2,3,4,5]" :key="g" :value="g">Khối {{ g }}</option>
          </select>
          <select v-model="subject" class="filter-select" @change="load">
            <option :value="undefined">Tất cả môn</option>
            <option v-for="s in subjects" :key="s.value" :value="s.value">{{ s.label }}</option>
          </select>
          <select v-model="sortBy" class="filter-select" @change="load">
            <option value="updatedAt">Mới nhất</option>
            <option value="createdAt">Cũ nhất</option>
            <option value="title">Tên A-Z</option>
            <option value="enrollments">Nhiều học viên</option>
          </select>
        </div>
        <div class="filters-info">
          <span>Tìm thấy {{ total }} khóa học</span>
          <button v-if="q || grade || subject" class="clear-btn" @click="clearFilters">Xóa bộ lọc</button>
        </div>
      </div>

      <!-- Grid -->
      <div class="courses-grid">
        <template v-if="loading">
          <div v-for="i in 8" :key="i" class="skeleton-card">
            <div class="skeleton-img"></div>
            <div class="skeleton-body">
              <div class="skeleton-line w-3/4"></div>
              <div class="skeleton-line w-1/2"></div>
            </div>
          </div>
        </template>

        <article v-else v-for="c in items" :key="String(c.id)" class="course-card" @click="open(c.id)">
          <div class="course-thumbnail">
            <img v-if="c.thumbnail" :src="getThumbnailUrl(c.thumbnail)" :alt="c.title" loading="lazy" @error="handleImageError" />
            <div v-else class="thumbnail-placeholder">
              <span>Chưa có ảnh</span>
            </div>
            <span class="published-badge">PUBLISHED</span>
          </div>
          <div class="course-body">
            <h3>{{ c.title }}</h3>
            <div class="course-meta">
              <span class="grade-tag">Khối {{ c.grade }}</span>
            </div>
            <div class="course-price" :class="(c.price || 0) === 0 ? 'free' : 'paid'">
              {{ (c.price || 0) === 0 ? 'Miễn phí' : formatPrice(c.price) }}
            </div>
          </div>
        </article>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <button :disabled="page <= 1" @click="goToPage(page - 1)" class="page-btn">‹ Trước</button>
        <div class="page-numbers">
          <button v-for="p in visiblePages" :key="p" class="page-num" :class="{ active: p === page }" @click="goToPage(p)">
            {{ p }}
          </button>
        </div>
        <button :disabled="page >= totalPages" @click="goToPage(page + 1)" class="page-btn">Sau ›</button>
      </div>

      <!-- Empty -->
      <div v-if="!loading && !items.length" class="empty-state">
        <p>Không có khoá học phù hợp.</p>
      </div>

      <div v-if="err" class="error-alert">{{ err }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { courseService, type Subject } from '@/services/course.service'
import { useThemeStore } from '@/store/theme.store'

const router = useRouter()
const route = useRoute()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const items = ref<any[]>([])
const err = ref('')
const loading = ref(false)
const total = ref(0)

const q = ref('')
const grade = ref<number | undefined>()
const subject = ref<Subject | undefined>()
const sortBy = ref<'updatedAt' | 'title' | 'enrollments' | 'createdAt'>('updatedAt')
const page = ref(1)
const pageSize = 20
const subjects = courseService.subjects()

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))
const visiblePages = computed(() => {
  const max = totalPages.value, current = page.value, pages: number[] = []
  if (max <= 7) { for (let i = 1; i <= max; i++) pages.push(i) }
  else {
    if (current <= 3) { for (let i = 1; i <= 5; i++) pages.push(i) }
    else if (current >= max - 2) { for (let i = max - 4; i <= max; i++) pages.push(i) }
    else { for (let i = current - 2; i <= current + 2; i++) pages.push(i) }
  }
  return pages
})

function clearFilters() { q.value = ''; grade.value = undefined; subject.value = undefined; page.value = 1; load() }
function goToPage(p: number) { if (p >= 1 && p <= totalPages.value) { page.value = p; load() } }

async function load() {
  try {
    loading.value = true
    const res = await courseService.list({
      q: q.value || undefined, grade: grade.value as any, subject: subject.value as any,
      status: 'published', page: page.value, pageSize, sortBy: sortBy.value,
      sortDir: sortBy.value === 'title' ? 'ascending' : 'descending',
    })
    items.value = res.items
    total.value = res.total || res.items.length
    err.value = ''
  } catch(e:any) { err.value = e?.message || String(e) }
  finally { loading.value = false }
}

function open(id: number | string) { router.push({ name: 'student-course-detail', params: { id } }) }

function getThumbnailUrl(thumbnail?: string): string {
  if (!thumbnail) return ''
  if (thumbnail.startsWith('http://') || thumbnail.startsWith('https://') || thumbnail.startsWith('data:')) return thumbnail
  const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000'
  const cleanThumbnail = thumbnail.startsWith('/') ? thumbnail.slice(1) : thumbnail
  return `${apiBase}/media/${cleanThumbnail}`
}

function handleImageError(event: Event) { (event.target as HTMLImageElement).src = 'https://via.placeholder.com/400x300?text=No+Image' }
function formatPrice(price?: number | string): string {
  if (!price || price === 0 || price === '0') return 'Miễn phí'
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(numPrice)
}

onMounted(() => {
  const g = Number(route.query.grade || '')
  if (!isNaN(g) && g >= 1 && g <= 5) grade.value = g
  load()
})
</script>

<style scoped>
.page-wrapper { min-height: 100vh; position: relative; transition: background-color 0.3s ease; }
.page-wrapper.dark-mode { background: #020617; }
.page-wrapper.light-mode { background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%); }

.bg-elements { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.glow { position: absolute; border-radius: 50%; filter: blur(100px); }
.glow-1 { top: 10%; left: -5%; width: 300px; height: 300px; background: rgba(6, 182, 212, 0.1); }
.glow-2 { bottom: 10%; right: -5%; width: 250px; height: 250px; background: rgba(139, 92, 246, 0.1); }

.page-content { position: relative; z-index: 10; max-width: 1200px; margin: 0 auto; padding: 32px 24px; }

.page-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; gap: 16px; flex-wrap: wrap; }
.page-header h1 { font-size: 28px; font-weight: 800; margin: 0 0 4px; }
.dark-mode .page-header h1 { color: white; }
.light-mode .page-header h1 { color: #1e293b; }
.page-header p { font-size: 14px; margin: 0; }
.dark-mode .page-header p { color: #64748b; }
.light-mode .page-header p { color: #64748b; }

.btn-outline {
  display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px;
  border-radius: 12px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; text-decoration: none;
}
.dark-mode .btn-outline { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .btn-outline { background: white; border: 1px solid #e2e8f0; color: #64748b; }
.btn-outline:hover { transform: translateY(-2px); }
.dark-mode .btn-outline:hover { border-color: #06b6d4; color: #06b6d4; }
.light-mode .btn-outline:hover { border-color: #6366f1; color: #6366f1; }

.filters-section { margin-bottom: 24px; }
.filters-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 12px; }

.search-box { position: relative; flex: 1; min-width: 200px; }
.search-box input {
  width: 100%; padding: 12px 40px 12px 16px; border-radius: 12px; font-size: 14px; outline: none; transition: all 0.3s;
}
.dark-mode .search-box input { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; }
.light-mode .search-box input { background: white; border: 1px solid #e2e8f0; color: #1e293b; }
.search-box input:focus { }
.dark-mode .search-box input:focus { border-color: #06b6d4; box-shadow: 0 0 0 3px rgba(6,182,212,0.1); }
.light-mode .search-box input:focus { border-color: #6366f1; box-shadow: 0 0 0 3px rgba(99,102,241,0.1); }
.search-icon { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); width: 20px; height: 20px; }
.dark-mode .search-icon { stroke: #64748b; }
.light-mode .search-icon { stroke: #94a3b8; }

.filter-select { padding: 12px 16px; border-radius: 12px; font-size: 14px; cursor: pointer; transition: all 0.3s; }
.dark-mode .filter-select { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; }
.light-mode .filter-select { background: white; border: 1px solid #e2e8f0; color: #1e293b; }

.filters-info { display: flex; justify-content: space-between; align-items: center; font-size: 14px; }
.dark-mode .filters-info { color: #64748b; }
.light-mode .filters-info { color: #64748b; }
.clear-btn { background: none; border: none; cursor: pointer; font-size: 14px; }
.dark-mode .clear-btn { color: #06b6d4; }
.light-mode .clear-btn { color: #6366f1; }
.clear-btn:hover { text-decoration: underline; }

.courses-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
@media (max-width: 1024px) { .courses-grid { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 768px) { .courses-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 480px) { .courses-grid { grid-template-columns: 1fr; } }

.skeleton-card { border-radius: 16px; overflow: hidden; }
.dark-mode .skeleton-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .skeleton-card { background: white; border: 1px solid #e2e8f0; }
.skeleton-img { height: 140px; animation: pulse 1.5s infinite; }
.dark-mode .skeleton-img { background: rgba(255,255,255,0.05); }
.light-mode .skeleton-img { background: #f1f5f9; }
.skeleton-body { padding: 16px; }
.skeleton-line { height: 12px; border-radius: 4px; margin-bottom: 8px; animation: pulse 1.5s infinite; }
.dark-mode .skeleton-line { background: rgba(255,255,255,0.05); }
.light-mode .skeleton-line { background: #f1f5f9; }
.skeleton-line.w-3\/4 { width: 75%; }
.skeleton-line.w-1\/2 { width: 50%; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

.course-card { border-radius: 16px; overflow: hidden; cursor: pointer; transition: all 0.3s; }
.dark-mode .course-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .course-card { background: white; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.course-card:hover { transform: translateY(-4px); }
.dark-mode .course-card:hover { border-color: rgba(6,182,212,0.3); }
.light-mode .course-card:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.1); }

.course-thumbnail { position: relative; height: 140px; overflow: hidden; }
.dark-mode .course-thumbnail { background: rgba(255,255,255,0.05); }
.light-mode .course-thumbnail { background: #f1f5f9; }
.course-thumbnail img { width: 100%; height: 100%; object-fit: cover; }
.thumbnail-placeholder { display: flex; align-items: center; justify-content: center; height: 100%; font-size: 13px; }
.dark-mode .thumbnail-placeholder { color: #475569; }
.light-mode .thumbnail-placeholder { color: #94a3b8; }

.published-badge {
  position: absolute; right: 8px; top: 8px; padding: 4px 8px; border-radius: 6px; font-size: 10px; font-weight: 700;
}
.dark-mode .published-badge { background: rgba(255,255,255,0.9); color: #1e293b; }
.light-mode .published-badge { background: white; color: #64748b; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }

.course-body { padding: 16px; }
.course-body h3 { font-size: 14px; font-weight: 700; margin: 0 0 8px; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.dark-mode .course-body h3 { color: white; }
.light-mode .course-body h3 { color: #1e293b; }

.course-meta { margin-bottom: 8px; }
.grade-tag { display: inline-flex; padding: 4px 10px; border-radius: 20px; font-size: 12px; }
.dark-mode .grade-tag { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .grade-tag { background: #f1f5f9; border: 1px solid #e2e8f0; color: #64748b; }

.course-price { font-size: 14px; font-weight: 600; }
.course-price.free { color: #22c55e; }
.course-price.paid { color: #f59e0b; }

.pagination { display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 32px; }
.page-btn, .page-num { padding: 10px 16px; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.dark-mode .page-btn, .dark-mode .page-num { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .page-btn, .light-mode .page-num { background: white; border: 1px solid #e2e8f0; color: #64748b; }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.page-btn:not(:disabled):hover, .page-num:hover { transform: translateY(-1px); }
.dark-mode .page-btn:not(:disabled):hover, .dark-mode .page-num:hover { border-color: #06b6d4; color: #06b6d4; }
.light-mode .page-btn:not(:disabled):hover, .light-mode .page-num:hover { border-color: #6366f1; color: #6366f1; }
.page-num.active { }
.dark-mode .page-num.active { background: linear-gradient(135deg, #06b6d4, #8b5cf6); border-color: transparent; color: white; }
.light-mode .page-num.active { background: #6366f1; border-color: #6366f1; color: white; }
.page-numbers { display: flex; gap: 4px; }

.empty-state { text-align: center; padding: 60px 20px; border-radius: 20px; margin-top: 24px; }
.dark-mode .empty-state { background: rgba(255,255,255,0.02); border: 2px dashed rgba(255,255,255,0.1); }
.light-mode .empty-state { background: white; border: 2px dashed #e2e8f0; }
.empty-state p { font-size: 14px; margin: 0; }
.dark-mode .empty-state p { color: #64748b; }
.light-mode .empty-state p { color: #64748b; }

.error-alert { padding: 12px 20px; border-radius: 12px; font-size: 14px; margin-top: 20px; text-align: center;
  background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); color: #f87171; }

@media (max-width: 640px) {
  .page-content { padding: 20px 16px; }
  .page-header { flex-direction: column; }
  .filters-row { flex-direction: column; }
  .search-box { min-width: 100%; }
}
</style>
