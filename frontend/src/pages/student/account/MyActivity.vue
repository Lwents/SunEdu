<template>
  <div class="page-wrapper" :class="isDark ? 'dark-mode' : 'light-mode'">
    <!-- Background Elements -->
    <div v-if="isDark" class="bg-elements">
      <div class="glow glow-1"></div>
      <div class="glow glow-2"></div>
    </div>

    <div class="page-content">
      <div class="page-header">
        <h1>Hoạt động của tôi</h1>
        <p>Lịch sử các hoạt động học tập và tương tác của bạn trên hệ thống</p>
      </div>

      <div class="filter-bar">
        <select v-model="filterType" class="filter-select">
          <option value="">Tất cả hoạt động</option>
          <option value="login">Đăng nhập</option>
          <option value="course">Khóa học</option>
          <option value="exam">Bài thi</option>
          <option value="payment">Thanh toán</option>
        </select>
      </div>

      <div v-if="loading" class="loading-state">
        <div v-for="i in 5" :key="i" class="skeleton"></div>
      </div>

      <ul v-else class="activity-list">
        <li v-for="(it, i) in filteredItems" :key="i" class="activity-item">
          <div class="activity-dot" :class="getActivityColor(it.type)"></div>
          <div class="activity-content">
            <p class="activity-title">{{ it.title }}</p>
            <p class="activity-time">{{ formatTime(it.time) }}</p>
            <p v-if="it.details" class="activity-details">{{ it.details }}</p>
          </div>
          <div v-if="it.action" class="activity-action">
            <button class="btn-action" @click="handleAction(it)">{{ it.action }}</button>
          </div>
        </li>
      </ul>

      <div v-if="!loading && !filteredItems.length" class="empty-state">
        <div class="empty-icon">📋</div>
        <h3>Không có hoạt động nào</h3>
        <p>Bắt đầu học để có hoạt động đầu tiên!</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useThemeStore } from '@/store/theme.store'

const router = useRouter()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const loading = ref(false)
const filterType = ref('')
const items = ref<Array<{
  type: string
  title: string
  time: string
  details?: string
  action?: string
  actionId?: string | number
}>>([])

const filteredItems = computed(() => {
  if (!filterType.value) return items.value
  return items.value.filter((it) => it.type === filterType.value)
})

function getActivityColor(type: string) {
  const colors: Record<string, string> = {
    login: 'dot-blue',
    course: 'dot-cyan',
    exam: 'dot-amber',
    payment: 'dot-emerald',
  }
  return colors[type] || 'dot-slate'
}

function formatTime(time: string) {
  try {
    return new Date(time).toLocaleString('vi-VN')
  } catch {
    return time
  }
}

function handleAction(item: any) {
  if (item.type === 'course' && item.actionId) {
    router.push({ name: 'student-course-detail', params: { id: item.actionId } })
  } else if (item.type === 'exam' && item.actionId) {
    router.push({ name: 'student-exam-detail', params: { id: item.actionId } })
  }
}

async function loadActivities() {
  loading.value = true
  try {
    await new Promise((r) => setTimeout(r, 500))
    items.value = [
      { type: 'login', title: 'Đăng nhập hệ thống', time: new Date().toISOString(), details: 'Đăng nhập từ trình duyệt Chrome' },
      { type: 'course', title: 'Hoàn thành bài học: Phép cộng', time: new Date(Date.now() - 3600000).toISOString(), details: 'Khóa học: Toán lớp 3', action: 'Xem khóa học', actionId: 1 },
      { type: 'exam', title: 'Nộp bài thi: Đề thi thử #1', time: new Date(Date.now() - 7200000).toISOString(), details: 'Điểm: 85/100', action: 'Xem kết quả', actionId: 1 },
      { type: 'payment', title: 'Thanh toán thành công', time: new Date(Date.now() - 86400000).toISOString(), details: 'Số tiền: 500,000 VNĐ' },
      { type: 'course', title: 'Bắt đầu khóa học: Tiếng Việt lớp 4', time: new Date(Date.now() - 172800000).toISOString(), details: 'Tiến độ: 15%', action: 'Tiếp tục học', actionId: 2 },
    ]
  } catch (e: any) {
    console.error('Load activities error:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => { loadActivities() })
</script>

<style scoped>
.page-wrapper { min-height: 100vh; position: relative; transition: background-color 0.3s ease; }
.page-wrapper.dark-mode { background: #020617; }
.page-wrapper.light-mode { background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%); }

.bg-elements { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.glow { position: absolute; border-radius: 50%; filter: blur(100px); }
.glow-1 { top: 10%; left: -5%; width: 300px; height: 300px; background: rgba(6, 182, 212, 0.1); }
.glow-2 { bottom: 10%; right: -5%; width: 250px; height: 250px; background: rgba(139, 92, 246, 0.1); }

.page-content { position: relative; z-index: 10; max-width: 800px; margin: 0 auto; padding: 32px 24px; }

.page-header { margin-bottom: 24px; }
.page-header h1 { font-size: 28px; font-weight: 800; margin: 0; }
.dark-mode .page-header h1 { color: white; }
.light-mode .page-header h1 { color: #1e293b; }
.page-header p { font-size: 14px; margin: 8px 0 0; }
.dark-mode .page-header p { color: #64748b; }
.light-mode .page-header p { color: #64748b; }

.filter-bar { margin-bottom: 16px; padding: 16px; border-radius: 16px; }
.dark-mode .filter-bar { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .filter-bar { background: white; border: 1px solid #e2e8f0; }

.filter-select { padding: 10px 16px; border-radius: 12px; font-size: 14px; outline: none; cursor: pointer; }
.dark-mode .filter-select { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; }
.light-mode .filter-select { background: #f8fafc; border: 1px solid #e2e8f0; color: #1e293b; }

.loading-state { display: flex; flex-direction: column; gap: 12px; }
.skeleton { height: 80px; border-radius: 16px; animation: pulse 2s infinite; }
.dark-mode .skeleton { background: rgba(255,255,255,0.05); }
.light-mode .skeleton { background: #e2e8f0; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

.activity-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }

.activity-item { display: flex; align-items: flex-start; gap: 16px; padding: 16px; border-radius: 16px; transition: all 0.3s; }
.dark-mode .activity-item { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .activity-item { background: white; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.activity-item:hover { transform: translateY(-2px); }
.dark-mode .activity-item:hover { box-shadow: 0 8px 24px rgba(6,182,212,0.1); }
.light-mode .activity-item:hover { box-shadow: 0 8px 24px rgba(0,0,0,0.1); }

.activity-dot { width: 10px; height: 10px; border-radius: 50%; margin-top: 6px; flex-shrink: 0; }
.dot-blue { background: #3b82f6; }
.dot-cyan { background: #06b6d4; }
.dot-amber { background: #f59e0b; }
.dot-emerald { background: #10b981; }
.dot-slate { background: #64748b; }

.activity-content { flex: 1; min-width: 0; }
.activity-title { font-size: 14px; font-weight: 600; margin: 0; }
.dark-mode .activity-title { color: white; }
.light-mode .activity-title { color: #1e293b; }
.activity-time { font-size: 12px; margin: 4px 0 0; }
.dark-mode .activity-time { color: #64748b; }
.light-mode .activity-time { color: #94a3b8; }
.activity-details { font-size: 12px; margin: 4px 0 0; }
.dark-mode .activity-details { color: #94a3b8; }
.light-mode .activity-details { color: #64748b; }

.activity-action { flex-shrink: 0; }
.btn-action { padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.dark-mode .btn-action { background: transparent; border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .btn-action { background: transparent; border: 1px solid #e2e8f0; color: #64748b; }
.btn-action:hover { }
.dark-mode .btn-action:hover { border-color: #06b6d4; color: #06b6d4; }
.light-mode .btn-action:hover { border-color: #6366f1; color: #6366f1; }

.empty-state { text-align: center; padding: 60px 20px; border-radius: 20px; }
.dark-mode .empty-state { background: rgba(255,255,255,0.02); border: 2px dashed rgba(255,255,255,0.1); }
.light-mode .empty-state { background: #f8fafc; border: 2px dashed #e2e8f0; }
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-state h3 { font-size: 18px; font-weight: 600; margin: 0 0 8px; }
.dark-mode .empty-state h3 { color: white; }
.light-mode .empty-state h3 { color: #1e293b; }
.empty-state p { font-size: 14px; margin: 0; }
.dark-mode .empty-state p { color: #64748b; }
.light-mode .empty-state p { color: #64748b; }
</style>
