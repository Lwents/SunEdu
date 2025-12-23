<template>
  <div class="page-wrapper" :class="isDark ? 'dark-mode' : 'light-mode'">
    <div v-if="isDark" class="bg-elements">
      <div class="glow glow-1"></div>
      <div class="glow glow-2"></div>
    </div>

    <div class="page-content">
      <!-- Header -->
      <div class="page-header">
        <h1>Bài kiểm tra</h1>
        <p>Danh sách bài kiểm tra dành cho bạn. Chọn bài và làm ngay.</p>
      </div>

      <!-- Filters -->
      <div class="filters-section">
        <div class="search-box">
          <svg class="search-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
          </svg>
          <input v-model.trim="q" @keydown.enter="applyFilters" placeholder="Tìm kiếm theo tên đề..." />
        </div>
        <div class="filter-dropdown">
          <button type="button" class="dropdown-btn" @click="open = !open">
            <span>{{ levelLabel || 'Tất cả cấp độ' }}</span>
            <svg class="dropdown-icon" :class="{ rotate: open }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <ul v-if="open" class="dropdown-menu" @mouseleave="open = false">
            <li v-for="(opt, idx) in levelOptions" :key="idx" @click="setLevel(opt.value)">{{ opt.label }}</li>
          </ul>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="exams-grid">
        <div v-for="i in pageSize" :key="i" class="skeleton-card"></div>
      </div>

      <!-- Exam Cards -->
      <div v-else-if="exams.length" class="exams-grid">
        <article v-for="e in exams" :key="e.id" class="exam-card" :class="{ done: isDone(e.id) }">
          <div class="exam-body">
            <span class="subject-badge" :class="getSubjectClass(subj(e))">{{ subj(e) }}</span>
            <h2>{{ e.title }}</h2>
            <div class="exam-meta">
              <span>{{ qCount(e) }} câu</span>
              <span class="dot">•</span>
              <span>{{ toMin(e.durationSec) }} phút</span>
              <span class="dot">•</span>
              <span>Đạt ≥ {{ e.passCount }} câu</span>
            </div>
          </div>
          <div class="exam-footer">
            <span class="level-badge" :class="e.level">{{ labelLevel(e.level) }}</span>
            <div class="exam-actions">
              <span v-if="isDone(e.id)" class="done-badge">Đã hoàn thành</span>
              <button type="button" class="start-btn" @click="isDone(e.id) ? goResult(e.id) : goExam(e.id)">
                {{ isDone(e.id) ? 'Xem kết quả' : 'Bắt đầu' }}
                <svg class="btn-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </button>
            </div>
          </div>
        </article>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-icon">📝</div>
        <h3>Chưa có bài kiểm tra</h3>
        <p>Hiện chưa có bài kiểm tra nào. Hãy quay lại sau hoặc kiểm tra với giáo viên.</p>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <button class="page-btn" :disabled="page <= 1" @click="go(page - 1)">‹</button>
        <button v-for="p in pagesToShow" :key="p.key" class="page-num" :class="{ active: p.num === page, sep: p.sep }"
          :disabled="p.sep" @click="!p.sep && go(p.num!)">{{ p.text }}</button>
        <button class="page-btn" :disabled="page >= totalPages" @click="go(page + 1)">›</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useExamStore } from '@/store/exam.store'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/store/auth.store'
import { useThemeStore } from '@/store/theme.store'

const store = useExamStore()
const { exams, total, page, pageSize, loading } = storeToRefs(store)
const router = useRouter()
const auth = useAuthStore()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const q = ref(store.q)
const level = ref<'' | 'basic' | 'advanced'>(store.level)
const open = ref(false)
const levelOptions: Array<{ value: '' | 'basic' | 'advanced'; label: string }> = [
  { value: '', label: 'Tất cả cấp độ' },
  { value: 'basic', label: 'Cơ bản' },
  { value: 'advanced', label: 'Nâng cao' },
]

const levelLabel = computed(() => level.value === 'basic' ? 'Cơ bản' : level.value === 'advanced' ? 'Nâng cao' : '')

function userStorageKey() { const u = auth.user; return String(u?.id ?? u?.email ?? u?.name ?? 'guest') }
function doneAttemptId(id: number | string) { try { return localStorage.getItem(`exam_done_${id}_${userStorageKey()}`) } catch { return null } }
function isDone(id: number | string) { const found = exams.value.find((x) => String(x.id) === String(id)); if (found && found.done) return true; return !!doneAttemptId(id) }
function goExam(id: number | string) { router.push({ name: 'student-exam-detail', params: { id } }) }
function goResult(id: number | string) { const attemptId = doneAttemptId(id); router.push({ name: 'student-exam-result', params: { id }, query: attemptId ? { attemptId } : undefined }) }
function setLevel(v: '' | 'basic' | 'advanced') { level.value = v; open.value = false; applyFilters() }
function applyFilters() { store.q = q.value; store.level = level.value; store.fetchExamsPage(1, pageSize.value) }

onMounted(() => { store.fetchExamsPage() })
function go(p: number) { store.fetchExamsPage(p, pageSize.value) }

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))
const pagesToShow = computed(() => {
  const max = totalPages.value, cur = page.value, arr: { key: string; num?: number; text: string; sep?: boolean }[] = []
  const push = (n: number) => arr.push({ key: 'p' + n, num: n, text: String(n) })
  const sep = (k: string) => arr.push({ key: k, text: '…', sep: true })
  if (max <= 7) { for (let i = 1; i <= max; i++) push(i) }
  else { push(1); const start = Math.max(2, cur - 1), end = Math.min(max - 1, cur + 1); if (start > 2) sep('s'); for (let i = start; i <= end; i++) push(i); if (end < max - 1) sep('e'); push(max) }
  return arr
})

function qCount(e: any) { return (e?.questionsCount ?? e?.questions ?? 0) as number }
function toMin(s: number) { return Math.round(s / 60) }
function labelLevel(l: 'basic' | 'advanced') { return l === 'advanced' ? 'Nâng cao' : 'Cơ bản' }

const subjectLabels: Record<string, string> = { math: 'Toán học', vietnamese: 'Tiếng Việt', english: 'Tiếng Anh', science: 'Khoa học' }
const subjectBadgeMap: Record<string, string> = { math: 'math', vietnamese: 'vietnamese', english: 'english', science: 'science', default: 'default' }
function subj(e: any) { if (e && 'subject' in e && e.subject) return labelSubject(e.subject); return e?.level === 'advanced' ? 'Nâng cao' : 'Cơ bản' }
function labelSubject(s: keyof typeof subjectLabels) { return subjectLabels[s] || 'Khác' }
function getSubjectClass(subjectLabel: string) { const subjectKey = Object.keys(subjectLabels).find((key) => subjectLabels[key] === subjectLabel); return subjectBadgeMap[subjectKey as keyof typeof subjectBadgeMap] || 'default' }

watch(pageSize, () => store.fetchExamsPage(1, pageSize.value))
</script>

<style scoped>
.page-wrapper { min-height: 100vh; position: relative; transition: background-color 0.3s ease; padding-bottom: 60px; }
.page-wrapper.dark-mode { background: #020617; }
.page-wrapper.light-mode { background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%); }

.bg-elements { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.glow { position: absolute; border-radius: 50%; filter: blur(100px); }
.glow-1 { top: 10%; left: -5%; width: 300px; height: 300px; background: rgba(6, 182, 212, 0.1); }
.glow-2 { bottom: 10%; right: -5%; width: 250px; height: 250px; background: rgba(139, 92, 246, 0.1); }

.page-content { position: relative; z-index: 10; max-width: 1200px; margin: 0 auto; padding: 40px 24px; }

.page-header { margin-bottom: 24px; }
.page-header h1 { font-size: 28px; font-weight: 800; margin: 0 0 8px; }
.dark-mode .page-header h1 { color: white; }
.light-mode .page-header h1 { color: #1e293b; }
.page-header p { font-size: 14px; margin: 0; }
.dark-mode .page-header p { color: #64748b; }
.light-mode .page-header p { color: #64748b; }

.filters-section { display: flex; gap: 16px; margin-bottom: 24px; flex-wrap: wrap; }

.search-box { position: relative; flex: 1; min-width: 200px; }
.search-box input { width: 100%; padding: 12px 12px 12px 44px; border-radius: 12px; font-size: 14px; outline: none; transition: all 0.3s; }
.dark-mode .search-box input { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; }
.light-mode .search-box input { background: white; border: 1px solid #e2e8f0; color: #1e293b; }
.search-box input:focus { }
.dark-mode .search-box input:focus { border-color: #06b6d4; }
.light-mode .search-box input:focus { border-color: #6366f1; }
.search-icon { position: absolute; left: 14px; top: 50%; transform: translateY(-50%); width: 20px; height: 20px; }
.dark-mode .search-icon { stroke: #64748b; }
.light-mode .search-icon { stroke: #94a3b8; }

.filter-dropdown { position: relative; }
.dropdown-btn { display: flex; align-items: center; gap: 8px; padding: 12px 16px; border-radius: 12px; font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.3s; min-width: 160px; }
.dark-mode .dropdown-btn { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; }
.light-mode .dropdown-btn { background: white; border: 1px solid #e2e8f0; color: #1e293b; }
.dropdown-icon { width: 16px; height: 16px; transition: transform 0.3s; margin-left: auto; }
.dropdown-icon.rotate { transform: rotate(180deg); }
.dropdown-menu { position: absolute; top: 100%; left: 0; right: 0; margin-top: 8px; border-radius: 12px; padding: 8px; z-index: 20; list-style: none; }
.dark-mode .dropdown-menu { background: #1e293b; border: 1px solid rgba(255,255,255,0.1); }
.light-mode .dropdown-menu { background: white; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
.dropdown-menu li { padding: 10px 12px; border-radius: 8px; font-size: 14px; cursor: pointer; transition: all 0.2s; }
.dark-mode .dropdown-menu li { color: #94a3b8; }
.light-mode .dropdown-menu li { color: #64748b; }
.dropdown-menu li:hover { }
.dark-mode .dropdown-menu li:hover { background: rgba(255,255,255,0.05); color: white; }
.light-mode .dropdown-menu li:hover { background: #f1f5f9; color: #1e293b; }

.exams-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
@media (max-width: 768px) { .exams-grid { grid-template-columns: 1fr; } }

.skeleton-card { height: 180px; border-radius: 16px; animation: pulse 1.5s infinite; }
.dark-mode .skeleton-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .skeleton-card { background: white; border: 1px solid #e2e8f0; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

.exam-card { border-radius: 16px; padding: 20px; display: flex; flex-direction: column; gap: 16px; transition: all 0.3s; }
.dark-mode .exam-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .exam-card { background: white; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.exam-card:hover { transform: translateY(-4px); }
.dark-mode .exam-card:hover { border-color: rgba(6,182,212,0.3); }
.light-mode .exam-card:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
.exam-card.done { opacity: 0.7; }

.exam-body { flex: 1; }
.exam-body h2 { font-size: 18px; font-weight: 600; margin: 12px 0; }
.dark-mode .exam-body h2 { color: white; }
.light-mode .exam-body h2 { color: #1e293b; }

.subject-badge { display: inline-flex; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.subject-badge.math { background: rgba(239,68,68,0.1); color: #ef4444; }
.subject-badge.vietnamese { background: rgba(245,158,11,0.1); color: #f59e0b; }
.subject-badge.english { background: rgba(59,130,246,0.1); color: #3b82f6; }
.subject-badge.science { background: rgba(20,184,166,0.1); color: #14b8a6; }
.subject-badge.default { background: rgba(100,116,139,0.1); color: #64748b; }

.exam-meta { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; font-size: 13px; }
.dark-mode .exam-meta { color: #64748b; }
.light-mode .exam-meta { color: #64748b; }
.dot { opacity: 0.5; }

.exam-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 16px; border-radius: 12px; }
.dark-mode .exam-footer { background: rgba(255,255,255,0.02); }
.light-mode .exam-footer { background: #f8fafc; }
.exam-footer { padding: 12px 16px; margin: 0 -20px -20px; border-radius: 0 0 16px 16px; }

.level-badge { padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.level-badge.basic { }
.dark-mode .level-badge.basic { background: rgba(59,130,246,0.1); color: #3b82f6; }
.light-mode .level-badge.basic { background: #dbeafe; color: #2563eb; }
.level-badge.advanced { }
.dark-mode .level-badge.advanced { background: rgba(239,68,68,0.1); color: #ef4444; }
.light-mode .level-badge.advanced { background: #fee2e2; color: #dc2626; }

.exam-actions { display: flex; align-items: center; gap: 12px; }
.done-badge { padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
.dark-mode .done-badge { background: rgba(34,197,94,0.1); color: #22c55e; }
.light-mode .done-badge { background: #dcfce7; color: #16a34a; }

.start-btn { display: inline-flex; align-items: center; gap: 8px; padding: 10px 20px; border-radius: 10px; font-size: 14px; font-weight: 600; border: none; cursor: pointer; transition: all 0.3s; }
.dark-mode .start-btn { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; }
.light-mode .start-btn { background: #1e293b; color: white; }
.start-btn:hover { transform: translateY(-2px); }
.btn-icon { width: 16px; height: 16px; }

.empty-state { text-align: center; padding: 60px 20px; border-radius: 20px; margin-top: 24px; }
.dark-mode .empty-state { background: rgba(255,255,255,0.02); border: 2px dashed rgba(255,255,255,0.1); }
.light-mode .empty-state { background: white; border: 2px dashed #e2e8f0; }
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-state h3 { font-size: 18px; font-weight: 600; margin: 0 0 8px; }
.dark-mode .empty-state h3 { color: white; }
.light-mode .empty-state h3 { color: #1e293b; }
.empty-state p { font-size: 14px; margin: 0; }
.dark-mode .empty-state p { color: #64748b; }
.light-mode .empty-state p { color: #64748b; }

.pagination { display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 32px; }
.page-btn, .page-num { width: 36px; height: 36px; border-radius: 10px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.3s; display: flex; align-items: center; justify-content: center; }
.dark-mode .page-btn, .dark-mode .page-num { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .page-btn, .light-mode .page-num { background: white; border: 1px solid #e2e8f0; color: #64748b; }
.page-btn:disabled, .page-num:disabled { opacity: 0.4; cursor: not-allowed; }
.page-num.sep { background: transparent; border: none; cursor: default; }
.page-num.active { }
.dark-mode .page-num.active { background: linear-gradient(135deg, #06b6d4, #8b5cf6); border-color: transparent; color: white; }
.light-mode .page-num.active { background: #1e293b; border-color: #1e293b; color: white; }

@media (max-width: 640px) { .page-content { padding: 24px 16px; } .filters-section { flex-direction: column; } }
</style>
