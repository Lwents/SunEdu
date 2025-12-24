<template>
  <div class="dashboard" :class="isDark ? 'dark' : 'light'">
    <!-- Header Section -->
    <div class="dash-header">
      <div class="header-info">
        <h1 class="title">👋 Xin chào, Admin!</h1>
        <p class="subtitle">Tổng quan hoạt động hệ thống hôm nay</p>
      </div>
      <div class="header-actions">
        <el-date-picker
          v-model="range"
          type="daterange"
          range-separator="→"
          start-placeholder="Từ ngày"
          end-placeholder="Đến ngày"
          size="default"
        />
        <el-select v-model="granularity" placeholder="Thời gian" style="width: 120px">
          <el-option label="Ngày" value="day" />
          <el-option label="Tuần" value="week" />
          <el-option label="Tháng" value="month" />
        </el-select>
        <button class="refresh-btn" @click="fetchAll">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Làm mới
        </button>
      </div>
    </div>

    <!-- KPI Row - Horizontal Cards -->
    <div class="kpi-row">
      <div class="kpi-card blue">
        <div class="kpi-left">
          <div class="kpi-icon">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
        </div>
        <div class="kpi-right">
          <span class="kpi-value">{{ fmt(kpis.dau) }}</span>
          <span class="kpi-label">Người dùng hoạt động</span>
        </div>
      </div>
      
      <div class="kpi-card green">
        <div class="kpi-left">
          <div class="kpi-icon">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
            </svg>
          </div>
        </div>
        <div class="kpi-right">
          <span class="kpi-value">{{ fmt(kpis.signups7d) }}</span>
          <span class="kpi-label">Đăng ký mới (7 ngày)</span>
        </div>
      </div>
      
      <div class="kpi-card purple">
        <div class="kpi-left">
          <div class="kpi-icon">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
        <div class="kpi-right">
          <span class="kpi-value">{{ currency(kpis.gmvToday) }}</span>
          <span class="kpi-label">Doanh thu hôm nay</span>
        </div>
      </div>
      
      <div class="kpi-card orange">
        <div class="kpi-left">
          <div class="kpi-icon">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
          </div>
        </div>
        <div class="kpi-right">
          <span class="kpi-value">{{ fmt(kpis.txToday) }}</span>
          <span class="kpi-label">Giao dịch hôm nay</span>
        </div>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="main-grid">
      <!-- Left Column - Chart -->
      <div class="chart-section">
        <div class="section-card full-height">
          <div class="card-header">
            <h3>📊 Biểu đồ doanh thu & giao dịch</h3>
          </div>
          <div class="chart-container">
            <v-chart :option="chartOption" autoresize style="height: 100%; width: 100%" />
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="right-column">
        <!-- Top Courses -->
        <div class="section-card top-courses">
          <div class="card-header">
            <h3>🏆 Top khóa học</h3>
          </div>
          <div class="course-list scrollable">
            <div v-for="(course, idx) in topCourses.slice(0, 5)" :key="idx" class="course-item">
              <div class="course-rank" :class="getRankClass(idx)">{{ idx + 1 }}</div>
              <div class="course-info">
                <span class="course-title">{{ course.title }}</span>
              </div>
              <div class="course-count">{{ course.enrollments }} đăng ký</div>
            </div>
            <div v-if="!topCourses.length" class="empty-state">Chưa có dữ liệu</div>
          </div>
        </div>

        <!-- Active Users Mini -->
        <div class="section-card compact online-card">
          <div class="card-header">
            <h3>🟢 Đang online</h3>
            <span class="online-badge">{{ fmt(activeUsers.count) }}</span>
          </div>
          <p class="mini-desc">{{ activeUsers.windowMinutes }} phút gần nhất</p>
        </div>
      </div>
    </div>

    <!-- Bottom Section -->
    <div class="bottom-grid">
      <!-- Recent Transactions -->
      <div class="section-card">
        <div class="card-header">
          <h3>💳 Giao dịch gần đây</h3>
        </div>
        <el-table :data="recentTransactions.slice(0, 5)" size="small" :max-height="220">
          <el-table-column prop="id" label="Mã GD" width="110" />
          <el-table-column prop="user" label="Người mua" min-width="140" />
          <el-table-column prop="course" label="Khóa học" min-width="160" />
          <el-table-column prop="amount" label="Số tiền" width="120" align="right">
            <template #default="{ row }">
              <span class="amount">{{ currency(row.amount) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="Trạng thái" width="100">
            <template #default="{ row }">
              <span class="status-badge" :class="getStatusClass(row.status)">{{ row.status }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- System Stats -->
      <div class="section-card">
        <div class="card-header">
          <h3>⚡ Hệ thống</h3>
        </div>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-bar">
              <div class="stat-fill cpu" :style="{ width: (system.cpuP95 || 0) + '%' }"></div>
            </div>
            <div class="stat-info">
              <span class="stat-label">CPU</span>
              <span class="stat-value">{{ formatPercentValue(system.cpuP95) }}</span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-bar">
              <div class="stat-fill ram" :style="{ width: (system.ramP95 || 0) + '%' }"></div>
            </div>
            <div class="stat-info">
              <span class="stat-label">RAM</span>
              <span class="stat-value">{{ formatPercentValue(system.ramP95) }}</span>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-bar">
              <div class="stat-fill disk" :style="{ width: (system.disk || 0) + '%' }"></div>
            </div>
            <div class="stat-info">
              <span class="stat-label">Disk</span>
              <span class="stat-value">{{ formatPercentValue(system.disk) }}</span>
            </div>
          </div>
        </div>
        <div class="backup-info">
          <span class="backup-label">🔄 Backup:</span>
          <span class="backup-value">{{ system.backup.lastRun }} - {{ system.backup.status }}</span>
        </div>
      </div>

      <!-- Security -->
      <div class="section-card">
        <div class="card-header">
          <h3>🔒 Bảo mật</h3>
        </div>
        <div class="security-list">
          <div class="security-item">
            <span class="security-label">Đăng nhập thất bại (24h)</span>
            <span class="security-value" :class="security.failedLogins24h > 10 ? 'warning' : ''">
              {{ security.failedLogins24h }}
            </span>
          </div>
          <div class="security-item">
            <span class="security-label">Tài khoản bị khóa</span>
            <span class="security-value" :class="security.lockedAccounts > 0 ? 'warning' : ''">
              {{ security.lockedAccounts }}
            </span>
          </div>
          <div class="security-item">
            <span class="security-label">SSL hết hạn trong</span>
            <span class="security-value" :class="security.sslDaysToExpire < 30 ? 'warning' : ''">
              {{ security.sslDaysToExpire }} ngày
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeUnmount, computed } from 'vue'
import { dashboardService } from '@/services/dashboard.service'
import { systemService } from '@/services/system.service'
import { reportService } from '@/services/report.service'
import { showToast } from '@/utils/toast'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { LineChart, BarChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { useThemeStore } from '@/store/theme.store'

use([CanvasRenderer, LineChart, BarChart, GridComponent, TooltipComponent, LegendComponent])

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const range = ref<[Date, Date] | null>(null)
const granularity = ref<'day' | 'week' | 'month'>('day')

const kpis = reactive({
  dau: 0,
  signups7d: 0,
  gmvToday: 0,
  txToday: 0,
})
const topCourses = ref<any[]>([])
const recentTransactions = ref<any[]>([])
const activeUsers = reactive({ count: 0, windowMinutes: 10, recent: [] as any[] })
const security = reactive({ failedLogins24h: 0, lockedAccounts: 0, sslDaysToExpire: 30 })
const system = reactive({ cpuP95: 0, ramP95: 0, disk: 0, backup: { lastRun: '-', status: '-' } })
const chartData = ref<{ labels: string[]; gross: number[]; tx: number[] }>({ labels: [], gross: [], tx: [] })

function fmt(v: number) {
  return new Intl.NumberFormat().format(v)
}

function currency(v: number) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(v)
}

function formatPercentValue(v: number | null | undefined) {
  if (typeof v !== 'number' || Number.isNaN(v)) return '0%'
  return `${v.toFixed(1)}%`
}

function getRankClass(idx: number) {
  if (idx === 0) return 'gold'
  if (idx === 1) return 'silver'
  if (idx === 2) return 'bronze'
  return ''
}

function getStatusClass(status: string) {
  const s = status?.toLowerCase()
  if (s === 'success' || s === 'completed') return 'success'
  if (s === 'pending') return 'pending'
  if (s === 'failed') return 'failed'
  return ''
}

const chartOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { 
    data: ['Doanh thu', 'Giao dịch'], 
    bottom: 0,
    textStyle: { color: isDark.value ? '#94a3b8' : '#64748b', fontSize: 12 }
  },
  grid: { left: 60, right: 30, top: 30, bottom: 50 },
  xAxis: { 
    type: 'category', 
    data: chartData.value.labels,
    axisLine: { lineStyle: { color: isDark.value ? '#334155' : '#e2e8f0' } },
    axisLabel: { color: isDark.value ? '#94a3b8' : '#64748b', fontSize: 11 }
  },
  yAxis: [
    { 
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: isDark.value ? '#94a3b8' : '#64748b', fontSize: 11 },
      splitLine: { lineStyle: { color: isDark.value ? '#1e293b' : '#f1f5f9' } }
    },
    { 
      type: 'value',
      axisLine: { show: false },
      axisLabel: { color: isDark.value ? '#94a3b8' : '#64748b', fontSize: 11 },
      splitLine: { show: false }
    },
  ],
  series: [
    {
      name: 'Doanh thu',
      type: 'line',
      smooth: true,
      data: chartData.value.gross,
      lineStyle: { color: '#06b6d4', width: 3 },
      itemStyle: { color: '#06b6d4' },
      areaStyle: { color: isDark.value ? 'rgba(6, 182, 212, 0.15)' : 'rgba(6, 182, 212, 0.08)' },
      symbol: 'circle',
      symbolSize: 6
    },
    {
      name: 'Giao dịch',
      type: 'line',
      yAxisIndex: 1,
      smooth: true,
      data: chartData.value.tx,
      lineStyle: { color: '#f97316', width: 3 },
      itemStyle: { color: '#f97316' },
      symbol: 'circle',
      symbolSize: 6
    },
  ],
}))

async function fetchSystemHealth() {
  try {
    const health = await systemService.getHealth()
    system.cpuP95 = health.cpu.p95
    system.ramP95 = health.ram.p95
    system.disk = health.disk.current
    
    if (health.backup.status === 'success' && health.backup.lastBackup) {
      const backupDate = new Date(health.backup.lastBackup)
      system.backup.lastRun = backupDate.toLocaleString('vi-VN', {
        day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit'
      })
      system.backup.status = 'OK'
    } else if (health.backup.status === 'no_backup') {
      system.backup.lastRun = 'Chưa có'
      system.backup.status = '⚠️'
    } else {
      system.backup.lastRun = 'Lỗi'
      system.backup.status = '❌'
    }
  } catch {
    console.error('Failed to fetch system health')
  }
}

async function fetchActiveUsers() {
  try {
    const data = await dashboardService.getActiveUsers()
    activeUsers.count = data.count
    activeUsers.windowMinutes = data.windowMinutes
    activeUsers.recent = data.recent
  } catch {
    console.error('Failed to fetch active users')
  }
}

function buildRangeParams() {
  if (range.value && range.value[0] && range.value[1]) {
    return {
      from: range.value[0].toISOString().slice(0, 10),
      to: range.value[1].toISOString().slice(0, 10),
      granularity: granularity.value,
    }
  }
  const to = new Date()
  const from = new Date()
  from.setDate(to.getDate() - 30)
  return { from: from.toISOString().slice(0, 10), to: to.toISOString().slice(0, 10), granularity: granularity.value }
}

async function fetchChart() {
  try {
    const params = buildRangeParams()
    const series = await reportService.revenueTimeseries(params)
    const byDate: Record<string, { gross: number; tx: number }> = {}
    series.forEach((p) => {
      byDate[p.date] = { gross: p.gross, tx: 0 }
    })
    recentTransactions.value.forEach((tx) => {
      const d = tx.createdAt ? tx.createdAt.slice(0, 10) : ''
      if (!byDate[d]) byDate[d] = { gross: 0, tx: 0 }
      byDate[d].tx += 1
    })
    const labels = Object.keys(byDate).sort()
    chartData.value = {
      labels: labels.map(d => d.slice(5)),
      gross: labels.map((d) => byDate[d].gross),
      tx: labels.map((d) => byDate[d].tx),
    }
  } catch {
    console.error('Chart load error')
  }
}

async function fetchAll() {
  try {
    const data = await dashboardService.getDashboard()
    Object.assign(kpis, data.kpis)
    topCourses.value = data.topCourses
    recentTransactions.value = data.recentTransactions
    Object.assign(activeUsers, data.activeUsers)
    Object.assign(security, data.security)
    Object.assign(system, data.system)
    
    await fetchChart()
    await Promise.all([fetchSystemHealth(), fetchActiveUsers()])
  } catch (e: any) {
    showToast(e?.message || 'Không tải được dữ liệu', 'error')
  }
}

let healthInterval: ReturnType<typeof setInterval> | null = null
let activeUsersInterval: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  fetchAll()
  healthInterval = setInterval(fetchSystemHealth, 5000)
  activeUsersInterval = setInterval(fetchActiveUsers, 5000)
})

onBeforeUnmount(() => {
  if (healthInterval) clearInterval(healthInterval)
  if (activeUsersInterval) clearInterval(activeUsersInterval)
})
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding-bottom: 24px;
}

/* Header */
.dash-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  flex-wrap: wrap;
}

.title {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
}

.dashboard.dark .title { color: white; }
.dashboard.light .title { color: #1e293b; }

.subtitle {
  font-size: 14px;
  margin: 4px 0 0;
}

.dashboard.dark .subtitle { color: #64748b; }
.dashboard.light .subtitle { color: #94a3b8; }

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.dashboard.dark .refresh-btn {
  background: linear-gradient(135deg, #06b6d4, #8b5cf6);
  color: white;
}

.dashboard.light .refresh-btn {
  background: #1e293b;
  color: white;
}

.refresh-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* KPI Row */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

@media (min-width: 768px) {
  .kpi-row {
    grid-template-columns: repeat(4, 1fr);
  }
}

.kpi-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-radius: 16px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.kpi-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.kpi-card.blue::before { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.kpi-card.green::before { background: linear-gradient(90deg, #22c55e, #4ade80); }
.kpi-card.purple::before { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
.kpi-card.orange::before { background: linear-gradient(90deg, #f97316, #fb923c); }

.dashboard.dark .kpi-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.04);
  box-shadow: 0 10px 24px rgba(2, 6, 23, 0.35);
}

.dashboard.light .kpi-card {
  background: white;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.kpi-card:hover {
  transform: translateY(-2px);
}

.kpi-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.kpi-card.blue .kpi-icon { background: rgba(59, 130, 246, 0.15); color: #3b82f6; }
.kpi-card.green .kpi-icon { background: rgba(34, 197, 94, 0.15); color: #22c55e; }
.kpi-card.purple .kpi-icon { background: rgba(139, 92, 246, 0.15); color: #8b5cf6; }
.kpi-card.orange .kpi-icon { background: rgba(249, 115, 22, 0.15); color: #f97316; }

.kpi-right {
  display: flex;
  flex-direction: column;
}

.kpi-value {
  font-size: 24px;
  font-weight: 700;
  line-height: 1.2;
}

.dashboard.dark .kpi-value { color: white; }
.dashboard.light .kpi-value { color: #1e293b; }

.kpi-label {
  font-size: 13px;
  margin-top: 2px;
}

.dashboard.dark .kpi-label { color: #64748b; }
.dashboard.light .kpi-label { color: #94a3b8; }

/* Main Grid */
.main-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  align-items: stretch;
}

@media (min-width: 1024px) {
  .main-grid {
    grid-template-columns: 2fr 1fr;
  }
}

/* Section Card */
.section-card {
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.dashboard.dark .section-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.04);
  box-shadow: 0 12px 28px rgba(2, 6, 23, 0.35);
}

.dashboard.light .section-card {
  background: white;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.section-card.full-height {
  min-height: 380px;
  display: flex;
  flex-direction: column;
}

.section-card.compact {
  padding: 16px 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-header h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.dashboard.dark .card-header h3 { color: white; }
.dashboard.light .card-header h3 { color: #1e293b; }

/* Right Column */
.right-column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-card.top-courses {
  flex: 1;
  min-height: 320px;
}

.course-list.scrollable {
  max-height: 260px;
  overflow-y: auto;
  padding-right: 6px;
}

.course-list.scrollable::-webkit-scrollbar {
  width: 6px;
}

.course-list.scrollable::-webkit-scrollbar-track {
  background: transparent;
}

.course-list.scrollable::-webkit-scrollbar-thumb {
  border-radius: 999px;
}

.dashboard.dark .course-list.scrollable::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.14);
}

.dashboard.light .course-list.scrollable::-webkit-scrollbar-thumb {
  background: rgba(15, 23, 42, 0.25);
}

/* Course List */
.course-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.course-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 10px;
  transition: all 0.2s;
}

.dashboard.dark .course-item { background: rgba(255, 255, 255, 0.03); }
.dashboard.light .course-item { background: #f8fafc; }

.course-item:hover {
  transform: translateX(4px);
}

.course-rank {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}

.dashboard.dark .course-rank { background: rgba(255, 255, 255, 0.1); color: #94a3b8; }
.dashboard.light .course-rank { background: #e2e8f0; color: #64748b; }

.course-rank.gold { background: linear-gradient(135deg, #fbbf24, #f59e0b); color: white; }
.course-rank.silver { background: linear-gradient(135deg, #94a3b8, #64748b); color: white; }
.course-rank.bronze { background: linear-gradient(135deg, #d97706, #b45309); color: white; }

.course-info {
  flex: 1;
  min-width: 0;
}

.course-title {
  font-size: 14px;
  font-weight: 500;
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dashboard.dark .course-title { color: #e2e8f0; }
.dashboard.light .course-title { color: #1e293b; }

.course-count {
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.dashboard.dark .course-count { color: #22d3ee; }
.dashboard.light .course-count { color: #6366f1; }

/* Online Badge */
.online-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 700;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
}

.mini-desc {
  font-size: 13px;
  margin: 0;
}

.dashboard.dark .mini-desc { color: #64748b; }
.dashboard.light .mini-desc { color: #94a3b8; }

/* Chart */
.chart-container {
  flex: 1;
  min-height: 280px;
}

.chart-section {
  height: 100%;
}

.chart-section .section-card.full-height {
  height: 100%;
}

/* Bottom Grid */
.bottom-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

@media (min-width: 1024px) {
  .bottom-grid {
    grid-template-columns: 2fr 1fr 1fr;
  }
}

/* Amount */
.amount {
  font-weight: 600;
}

.dashboard.dark .amount { color: #22d3ee; }
.dashboard.light .amount { color: #6366f1; }

/* Status Badge */
.status-badge {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.status-badge.success { background: rgba(34, 197, 94, 0.15); color: #22c55e; }
.status-badge.pending { background: rgba(251, 191, 36, 0.15); color: #f59e0b; }
.status-badge.failed { background: rgba(239, 68, 68, 0.15); color: #ef4444; }

/* Stats Grid */
.stats-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.stat-bar {
  height: 8px;
  border-radius: 4px;
  overflow: hidden;
}

.dashboard.dark .stat-bar { background: rgba(255, 255, 255, 0.1); }
.dashboard.light .stat-bar { background: #e2e8f0; }

.stat-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.stat-fill.cpu { background: linear-gradient(90deg, #3b82f6, #60a5fa); }
.stat-fill.ram { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
.stat-fill.disk { background: linear-gradient(90deg, #22c55e, #4ade80); }

.stat-info {
  display: flex;
  justify-content: space-between;
}

.stat-label {
  font-size: 13px;
}

.dashboard.dark .stat-label { color: #94a3b8; }
.dashboard.light .stat-label { color: #64748b; }

.stat-value {
  font-size: 13px;
  font-weight: 600;
}

.dashboard.dark .stat-value { color: white; }
.dashboard.light .stat-value { color: #1e293b; }

/* Backup Info */
.backup-info {
  display: flex;
  gap: 8px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid;
  font-size: 13px;
}

.dashboard.dark .backup-info { border-color: rgba(255, 255, 255, 0.08); }
.dashboard.light .backup-info { border-color: #e2e8f0; }

.dashboard.dark .backup-label { color: #64748b; }
.dashboard.light .backup-label { color: #94a3b8; }

.dashboard.dark .backup-value { color: white; }
.dashboard.light .backup-value { color: #1e293b; }

/* Security List */
.security-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.security-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-radius: 10px;
}

.dashboard.dark .security-item { background: rgba(255, 255, 255, 0.03); }
.dashboard.light .security-item { background: #f8fafc; }

.security-label {
  font-size: 13px;
}

.dashboard.dark .security-label { color: #94a3b8; }
.dashboard.light .security-label { color: #64748b; }

.security-value {
  font-size: 14px;
  font-weight: 700;
}

.dashboard.dark .security-value { color: #22c55e; }
.dashboard.light .security-value { color: #22c55e; }

.security-value.warning { color: #f59e0b !important; }

/* Empty State */
.empty-state {
  text-align: center;
  padding: 20px;
  font-size: 14px;
}

.dashboard.dark .empty-state { color: #64748b; }
.dashboard.light .empty-state { color: #94a3b8; }

/* Element Plus Override */
.dashboard.dark :deep(.el-table) {
  --el-table-bg-color: transparent;
  --el-table-tr-bg-color: transparent;
  --el-table-header-bg-color: rgba(255, 255, 255, 0.03);
  --el-table-row-hover-bg-color: rgba(255, 255, 255, 0.05);
  --el-table-border-color: rgba(255, 255, 255, 0.06);
  --el-table-text-color: #e2e8f0;
  --el-table-header-text-color: #94a3b8;
}

.dashboard.dark :deep(.el-table th.el-table__cell) {
  background: rgba(255, 255, 255, 0.03);
}
</style>
