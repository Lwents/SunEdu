<template>
  <div class="my-courses" :class="isDark ? 'dark' : 'light'">
    <div v-if="isDark" class="bg-glow">
      <div class="glow g1"></div>
      <div class="glow g2"></div>
    </div>

    <div class="wrapper">
      <!-- Header -->
      <div class="header-card">
        <div class="header-left">
          <h1>🎓 Khóa học của tôi</h1>
          <p>Tiếp tục hành trình học tập của bạn</p>
        </div>
        <router-link class="ai-btn" :to="{ name: 'student-learning-path' }">
          🧭 Lộ trình AI →
        </router-link>
      </div>

      <!-- Stats Row -->
      <div class="stats-row">
        <div class="stat-box">
          <span class="stat-num">{{ mainCoursesCount }}</span>
          <span class="stat-txt">Tổng khóa học</span>
        </div>
        <div class="stat-box">
          <span class="stat-num completed">{{ enrolled.filter(c => c.done).length }}</span>
          <span class="stat-txt">Đã hoàn thành</span>
        </div>
        <div class="stat-box">
          <span class="stat-num learning">{{ enrolled.filter(c => !c.done).length }}</span>
          <span class="stat-txt">Đang học</span>
        </div>
      </div>

      <!-- Tabs -->
      <div class="tabs-bar">
        <button :class="['tab-btn', { active: activeTab === 'main' }]" @click="activeTab = 'main'">
          📖 Khóa học của tôi <span class="tab-count">{{ mainCoursesCount }}</span>
        </button>
        <button :class="['tab-btn', { active: activeTab === 'supp' }]" @click="activeTab = 'supp'">
          🔍 Khám phá thêm <span class="tab-count">{{ suppList.length }}</span>
        </button>
      </div>

      <!-- Grade Filter -->
      <div class="grade-bar">
        <span class="filter-label">Lọc theo lớp:</span>
        <div class="grade-btns">
          <button 
            :class="['grade-btn', { active: selectedGrade === null }]"
            @click="selectedGrade = null; gradeFilter = null"
          >Tất cả</button>
          <button 
            v-for="g in [1,2,3,4,5]" 
            :key="g" 
            :class="['grade-btn', { active: selectedGrade === g }]"
            @click="toggleGrade(g)"
          >Lớp {{ g }}</button>
        </div>
      </div>

      <!-- My Courses -->
      <template v-if="activeTab === 'main'">
        <div v-if="filteredMain.length" class="courses-grid">
          <div v-for="c in filteredMain" :key="c.id" class="course-item" @click="openDetail(c.id)">
            <div class="course-thumb">
              <img v-if="c.thumbnail && !imageErrors[String(c.id)]" :src="getThumbnailUrl(c.thumbnail)" @error="handleImageError(c.id)" />
              <div v-else class="thumb-placeholder">📘</div>
              <div class="progress-badge">{{ Math.round(animatedProgress[String(c.id)] || 0) }}%</div>
              <button class="play-btn" @click.stop="playFirst(c.id)">▶</button>
            </div>
            <div class="course-info">
              <span class="grade-tag">Lớp {{ c.grade }}</span>
              <h3>{{ c.title }}</h3>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: (animatedProgress[String(c.id)] || 0) + '%' }"></div>
              </div>
              <span :class="['status-tag', c.done ? 'done' : 'learning']">
                {{ c.done ? '✅ Hoàn thành' : '📝 Đang học' }}
              </span>
            </div>
          </div>
        </div>
        <div v-else class="empty-box">
          <span class="empty-icon">📚</span>
          <h3>Chưa có khóa học</h3>
          <p>Hãy khám phá và đăng ký khóa học mới!</p>
          <button class="explore-btn" @click="router.push({ name: 'student-catalog' })">🚀 Khám phá ngay</button>
        </div>
      </template>

      <!-- Explore -->
      <template v-else>
        <div v-if="suppList.length" class="courses-grid">
          <div v-for="s in suppList" :key="s.id" class="course-item supp">
            <div class="course-thumb">
              <img v-if="s.thumbnail" :src="getThumbnailUrl(s.thumbnail)" />
              <div v-else class="thumb-placeholder">📗</div>
              <span class="price-tag" :class="(Number(s.price)||0) === 0 ? 'free' : ''">
                {{ (Number(s.price)||0) === 0 ? 'Miễn phí' : formatPrice(s.price) }}
              </span>
            </div>
            <div class="course-info">
              <span class="grade-tag">Lớp {{ s.grade }}</span>
              <h3>{{ s.title }}</h3>
              <div class="action-btns">
                <button class="btn-outline" @click="openDetail(s.id)">Chi tiết</button>
                <button class="btn-primary" @click="enroll(s.id)">Đăng ký</button>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="empty-box">
          <span class="empty-icon">🔎</span>
          <h3>Không có khóa học phù hợp</h3>
          <p>Thử thay đổi bộ lọc</p>
        </div>
      </template>

      <div v-if="err" class="error-msg">⚠️ {{ err }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, nextTick, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { courseService, type CourseSummary, type CourseDetail, type StudentMyCourse, type ID } from '@/services/course.service'
import { resolveMediaUrl } from '@/utils/media'
import { useThemeStore } from '@/store/theme.store'

const router = useRouter()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)
const imageErrors = reactive<Record<string, boolean>>({})

const activeTab = ref<'main'|'supp'>('main')
const gradeFilter = ref<number | null>(null)
const selectedGrade = ref<number | null>(null)
const err = ref('')

function toggleGrade(g: number) {
  if (selectedGrade.value === g) { selectedGrade.value = null; gradeFilter.value = null }
  else { selectedGrade.value = g; gradeFilter.value = g }
}

const animatedProgress = ref<Record<string, number>>({})

function animateProgress(id: string, target: number) {
  const start = Date.now()
  const update = () => {
    const p = Math.min((Date.now() - start) / 800, 1)
    animatedProgress.value[id] = target * (1 - Math.pow(1 - p, 3))
    if (p < 1) requestAnimationFrame(update)
    else animatedProgress.value[id] = target
  }
  requestAnimationFrame(update)
}

type EnrolledItem = { id: ID; title: string; grade: number; thumbnail?: string; progress: number; done: boolean }
type SuggestionItem = CourseSummary & { tag?: string }

const enrolled = ref<EnrolledItem[]>([])
const suggestions = ref<SuggestionItem[]>([])
const detailsMap = ref(new Map<string, CourseDetail>())

function clamp(v?: number | null) { return typeof v === 'number' && !isNaN(v) ? Math.max(0, Math.min(100, Math.round(v))) : 0 }
function toGrade(v: any): number { const n = Number(v); return !isNaN(n) && n >= 1 && n <= 5 ? n : 1 }

function normalize(c: StudentMyCourse): EnrolledItem {
  const progress = clamp(c.progress)
  return { id: c.id as ID, title: c.title || 'Khóa học', grade: toGrade(c.grade), thumbnail: c.thumbnail, progress, done: c.done ?? progress >= 100 }
}

async function load() {
  try {
    err.value = ''
    const [my, cat] = await Promise.all([courseService.myCourses(), courseService.list({ page: 1, pageSize: 20, status: 'published' })])
    enrolled.value = (my.all || []).map(normalize)
    suggestions.value = (cat.items || []).map(i => ({ ...i, price: Number((i as any).price) || 0 }))
    await nextTick()
    enrolled.value.forEach(c => animateProgress(String(c.id), c.progress))
  } catch (e: any) { err.value = e?.message || String(e) }
}

const filteredMain = computed(() => {
  let arr = enrolled.value.slice()
  if (gradeFilter.value) arr = arr.filter(x => x.grade === gradeFilter.value)
  return arr
})

const mainCoursesCount = computed(() => filteredMain.value.length)
const enrolledIds = computed(() => new Set(enrolled.value.map(c => String(c.id))))

const suppList = computed(() => {
  let arr = suggestions.value.filter(c => !enrolledIds.value.has(String(c.id)))
  if (gradeFilter.value) arr = arr.filter(s => s.grade === gradeFilter.value)
  return arr
})

function openDetail(id: number | string) { router.push({ name: 'student-course-detail', params: { id } }) }

async function playFirst(id: number | string) {
  let d = detailsMap.value.get(String(id))
  if (!d) { d = await courseService.detail(id); detailsMap.value.set(String(id), d) }
  const first = d.sections?.[0]?.lessons?.[0]?.id
  if (first) router.push({ name: 'student-course-player', params: { id, lessonId: first } })
  else openDetail(id)
}

async function enroll(id: number | string) {
  try {
    const c = await courseService.detail(id)
    if ((Number(c.price) || 0) === 0) { await courseService.enroll(id); await load(); playFirst(id) }
    else router.push({ name: 'student-payments-cart', query: { add: String(id) } })
  } catch (e: any) { alert(e?.message || 'Lỗi') }
}

const getThumbnailUrl = (t?: string) => resolveMediaUrl(t)
function handleImageError(id: string | number) { imageErrors[String(id)] = true }
function formatPrice(p?: number | string): string {
  if (!p) return 'Miễn phí'
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(Number(p))
}

onMounted(load)
</script>

<style scoped>
.my-courses { min-height: 100vh; position: relative; }
.my-courses.dark { background: #0f172a; }
.my-courses.light { background: #f1f5f9; }

.bg-glow { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.glow { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.3; }
.g1 { top: -50px; left: -50px; width: 300px; height: 300px; background: #06b6d4; }
.g2 { bottom: -50px; right: -50px; width: 250px; height: 250px; background: #8b5cf6; }

.wrapper { position: relative; z-index: 1; max-width: 1000px; margin: 0 auto; padding: 20px 16px; }

/* Header */
.header-card { display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 20px; border-radius: 16px; margin-bottom: 16px; }
.dark .header-card { background: rgba(30,41,59,0.7); border: 1px solid rgba(255,255,255,0.1); }
.light .header-card { background: #fff; border: 1px solid #e2e8f0; }

.header-left h1 { font-size: 20px; font-weight: 700; margin: 0 0 4px; }
.dark .header-left h1 { color: #fff; }
.light .header-left h1 { color: #1e293b; }
.header-left p { font-size: 13px; margin: 0; }
.dark .header-left p { color: #94a3b8; }
.light .header-left p { color: #64748b; }

.ai-btn { padding: 10px 16px; border-radius: 10px; font-size: 13px; font-weight: 600; text-decoration: none; transition: all 0.2s; white-space: nowrap; }
.dark .ai-btn { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: #fff; }
.light .ai-btn { background: #1e293b; color: #fff; }
.ai-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.2); }

/* Stats */
.stats-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 16px; }
.stat-box { padding: 16px; border-radius: 12px; text-align: center; }
.dark .stat-box { background: rgba(30,41,59,0.6); border: 1px solid rgba(255,255,255,0.08); }
.light .stat-box { background: #fff; border: 1px solid #e2e8f0; }

.stat-num { display: block; font-size: 24px; font-weight: 800; margin-bottom: 4px; }
.dark .stat-num { color: #22d3ee; }
.light .stat-num { color: #6366f1; }
.stat-num.completed { color: #22c55e; }
.stat-num.learning { color: #f59e0b; }
.stat-txt { font-size: 11px; font-weight: 500; }
.dark .stat-txt { color: #94a3b8; }
.light .stat-txt { color: #64748b; }

/* Control Bar - Tabs & Filter Combined */
.control-bar { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 10px; border-radius: 14px; margin-bottom: 16px; }
.dark .control-bar { background: rgba(30,41,59,0.6); border: 1px solid rgba(255,255,255,0.08); }
.light .control-bar { background: #fff; border: 1px solid #e2e8f0; }

/* Tabs Bar */
.tabs-bar { display: flex; gap: 8px; margin-bottom: 12px; }
.tab-btn { flex: 1; display: flex; align-items: center; justify-content: center; gap: 8px; padding: 14px 20px; border-radius: 12px; font-size: 14px; font-weight: 600; border: none; cursor: pointer; transition: all 0.2s; }
.dark .tab-btn { background: rgba(30,41,59,0.6); color: #64748b; border: 1px solid rgba(255,255,255,0.08); }
.light .tab-btn { background: #fff; color: #64748b; border: 1px solid #e2e8f0; }
.tab-btn:hover { }
.dark .tab-btn:hover { color: #e2e8f0; border-color: rgba(255,255,255,0.15); }
.light .tab-btn:hover { color: #1e293b; border-color: #cbd5e1; }
.tab-btn.active { }
.dark .tab-btn.active { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: #fff; border-color: transparent; }
.light .tab-btn.active { background: #1e293b; color: #fff; border-color: #1e293b; }
.tab-count { padding: 3px 8px; border-radius: 6px; font-size: 12px; font-weight: 700; }
.dark .tab-count { background: rgba(255,255,255,0.15); }
.light .tab-count { background: rgba(0,0,0,0.08); }
.tab-btn.active .tab-count { background: rgba(255,255,255,0.25); }

/* Grade Bar */
.grade-bar { display: flex; align-items: center; gap: 12px; padding: 10px 14px; border-radius: 12px; margin-bottom: 16px; flex-wrap: wrap; }
.dark .grade-bar { background: rgba(30,41,59,0.5); border: 1px solid rgba(255,255,255,0.06); }
.light .grade-bar { background: #fff; border: 1px solid #e2e8f0; }

.filter-label { font-size: 13px; font-weight: 600; white-space: nowrap; }
.dark .filter-label { color: #94a3b8; }
.light .filter-label { color: #64748b; }

.grade-btns { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }

.grade-btn { padding: 8px 14px; border-radius: 8px; font-size: 12px; font-weight: 600; border: none; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.dark .grade-btn { background: rgba(255,255,255,0.05); color: #94a3b8; }
.light .grade-btn { background: #f1f5f9; color: #64748b; }
.grade-btn:hover { transform: translateY(-1px); }
.dark .grade-btn:hover { color: #22d3ee; background: rgba(6,182,212,0.15); }
.light .grade-btn:hover { color: #6366f1; background: #e0e7ff; }
.grade-btn.active { }
.dark .grade-btn.active { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: #fff; }
.light .grade-btn.active { background: #1e293b; color: #fff; }

/* Filter - unused */
.filter-section { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; padding: 12px 16px; border-radius: 12px; }
.dark .filter-section { background: rgba(30,41,59,0.5); }
.light .filter-section { background: #fff; border: 1px solid #e2e8f0; }

.filter-label { font-size: 12px; font-weight: 600; }
.dark .filter-label { color: #94a3b8; }
.light .filter-label { color: #64748b; }

.filter-btns { display: flex; gap: 6px; flex-wrap: wrap; }
.filter-btn { padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 500; border: none; cursor: pointer; transition: all 0.2s; }
.dark .filter-btn { background: rgba(255,255,255,0.05); color: #94a3b8; }
.light .filter-btn { background: #f1f5f9; color: #64748b; }
.filter-btn:hover { transform: translateY(-1px); }
.dark .filter-btn:hover { background: rgba(6,182,212,0.2); color: #22d3ee; }
.light .filter-btn:hover { background: #e0e7ff; color: #6366f1; }
.filter-btn.active { }
.dark .filter-btn.active { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: #fff; }
.light .filter-btn.active { background: #1e293b; color: #fff; }

/* Tabs */
.tabs-row { display: flex; gap: 8px; margin-bottom: 16px; }
.tab-btn { flex: 1; padding: 12px; border-radius: 10px; font-size: 13px; font-weight: 600; border: none; cursor: pointer; transition: all 0.2s; }
.dark .tab-btn { background: rgba(30,41,59,0.5); color: #64748b; }
.light .tab-btn { background: #fff; color: #64748b; border: 1px solid #e2e8f0; }
.tab-btn:hover { }
.dark .tab-btn:hover { color: #e2e8f0; }
.light .tab-btn:hover { color: #1e293b; }
.tab-btn.active { }
.dark .tab-btn.active { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: #fff; }
.light .tab-btn.active { background: #1e293b; color: #fff; border-color: #1e293b; }

/* Courses Grid */
.courses-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }

.course-item { border-radius: 14px; overflow: hidden; cursor: pointer; transition: all 0.2s; }
.dark .course-item { background: rgba(30,41,59,0.7); border: 1px solid rgba(255,255,255,0.08); }
.light .course-item { background: #fff; border: 1px solid #e2e8f0; }
.course-item:hover { transform: translateY(-4px); }
.dark .course-item:hover { border-color: rgba(6,182,212,0.3); box-shadow: 0 8px 24px rgba(6,182,212,0.1); }
.light .course-item:hover { box-shadow: 0 8px 20px rgba(0,0,0,0.08); }

.course-thumb { position: relative; height: 120px; overflow: hidden; }
.dark .course-thumb { background: rgba(255,255,255,0.05); }
.light .course-thumb { background: #f1f5f9; }
.course-thumb img { width: 100%; height: 100%; object-fit: cover; }
.thumb-placeholder { display: flex; align-items: center; justify-content: center; height: 100%; font-size: 32px; opacity: 0.4; }

.progress-badge { position: absolute; bottom: 8px; left: 8px; padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: 700; }
.dark .progress-badge { background: rgba(0,0,0,0.7); color: #22d3ee; }
.light .progress-badge { background: rgba(255,255,255,0.95); color: #6366f1; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }

.play-btn { position: absolute; bottom: 8px; right: 8px; width: 32px; height: 32px; border-radius: 50%; border: none; cursor: pointer; font-size: 12px; transition: all 0.2s; }
.dark .play-btn { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: #fff; }
.light .play-btn { background: #1e293b; color: #fff; }
.play-btn:hover { transform: scale(1.1); }

.price-tag { position: absolute; top: 8px; right: 8px; padding: 4px 8px; border-radius: 6px; font-size: 10px; font-weight: 700; background: #f59e0b; color: #fff; }
.price-tag.free { background: #22c55e; }

.course-info { padding: 12px; }
.grade-tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: 600; margin-bottom: 6px; }
.dark .grade-tag { background: rgba(6,182,212,0.15); color: #22d3ee; }
.light .grade-tag { background: #dbeafe; color: #2563eb; }

.course-info h3 { font-size: 13px; font-weight: 600; margin: 0 0 8px; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.dark .course-info h3 { color: #fff; }
.light .course-info h3 { color: #1e293b; }

.progress-bar { height: 4px; border-radius: 2px; overflow: hidden; margin-bottom: 8px; }
.dark .progress-bar { background: rgba(255,255,255,0.1); }
.light .progress-bar { background: #e2e8f0; }
.progress-fill { height: 100%; border-radius: 2px; transition: width 0.8s ease; }
.dark .progress-fill { background: linear-gradient(90deg, #06b6d4, #8b5cf6); }
.light .progress-fill { background: linear-gradient(90deg, #6366f1, #8b5cf6); }

.status-tag { font-size: 11px; font-weight: 600; }
.status-tag.done { color: #22c55e; }
.status-tag.learning { color: #f59e0b; }

.action-btns { display: flex; gap: 6px; margin-top: 8px; }
.btn-outline, .btn-primary { flex: 1; padding: 8px; border-radius: 8px; font-size: 11px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-outline { }
.dark .btn-outline { background: transparent; border: 1px solid rgba(255,255,255,0.15); color: #94a3b8; }
.light .btn-outline { background: transparent; border: 1px solid #e2e8f0; color: #64748b; }
.btn-outline:hover { }
.dark .btn-outline:hover { border-color: #22d3ee; color: #22d3ee; }
.light .btn-outline:hover { border-color: #6366f1; color: #6366f1; }
.btn-primary { border: none; }
.dark .btn-primary { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: #fff; }
.light .btn-primary { background: #1e293b; color: #fff; }

/* Empty */
.empty-box { text-align: center; padding: 40px 20px; border-radius: 16px; }
.dark .empty-box { background: rgba(30,41,59,0.4); border: 2px dashed rgba(255,255,255,0.1); }
.light .empty-box { background: #fff; border: 2px dashed #e2e8f0; }
.empty-icon { font-size: 40px; display: block; margin-bottom: 12px; }
.empty-box h3 { font-size: 16px; font-weight: 700; margin: 0 0 4px; }
.dark .empty-box h3 { color: #fff; }
.light .empty-box h3 { color: #1e293b; }
.empty-box p { font-size: 13px; margin: 0 0 16px; }
.dark .empty-box p { color: #64748b; }
.light .empty-box p { color: #64748b; }
.explore-btn { padding: 10px 20px; border-radius: 10px; font-size: 13px; font-weight: 600; border: none; cursor: pointer; }
.dark .explore-btn { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: #fff; }
.light .explore-btn { background: #1e293b; color: #fff; }

.error-msg { padding: 12px; border-radius: 10px; font-size: 13px; margin-top: 16px; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); color: #f87171; }

@media (max-width: 640px) {
  .wrapper { padding: 16px 12px; }
  .header-card { flex-direction: column; text-align: center; }
  .ai-btn { width: 100%; text-align: center; }
  .stats-row { grid-template-columns: repeat(3, 1fr); gap: 8px; }
  .stat-num { font-size: 20px; }
  .filter-section { flex-direction: column; align-items: flex-start; }
  .tabs-row { flex-direction: column; }
  .courses-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
}
@media (max-width: 400px) {
  .courses-grid { grid-template-columns: 1fr; }
}
</style>
