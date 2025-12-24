<template>
  <div class="analytics" :class="isDark ? 'dark' : 'light'">
    <!-- Header -->
    <div class="analytics-header">
      <el-date-picker
        v-model="range"
        type="daterange"
        range-separator="→"
        start-placeholder="Từ ngày"
        end-placeholder="Đến ngày"
        value-format="YYYY-MM-DD"
        @change="reload"
      />
      <div class="header-actions">
        <button class="action-btn secondary" @click="reset">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Đặt lại
        </button>
        <button class="action-btn primary" @click="exportCsv" :disabled="exporting">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          {{ exporting ? 'Đang xuất...' : 'Xuất CSV' }}
        </button>
      </div>
    </div>

    <!-- KPI Row -->
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
          <span class="kpi-value">{{ fmt(kpi.dau) }}</span>
          <span class="kpi-label">Hoạt động hàng ngày</span>
        </div>
      </div>

      <div class="kpi-card purple">
        <div class="kpi-left">
          <div class="kpi-icon">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        </div>
        <div class="kpi-right">
          <span class="kpi-value">{{ fmt(kpi.mau) }}</span>
          <span class="kpi-label">Hoạt động hàng tháng</span>
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
          <span class="kpi-value">{{ fmt(kpi.newUsers) }}</span>
          <span class="kpi-label">Người dùng mới</span>
        </div>
      </div>

      <div class="kpi-card orange">
        <div class="kpi-left">
          <div class="kpi-icon">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.636 18.364a9 9 0 010-12.728m12.728 0a9 9 0 010 12.728m-9.9-2.829a5 5 0 010-7.07m7.072 0a5 5 0 010 7.07M13 12a1 1 0 11-2 0 1 1 0 012 0z" />
            </svg>
          </div>
        </div>
        <div class="kpi-right">
          <span class="kpi-value">{{ fmt(kpi.activeUsers) }}</span>
          <span class="kpi-label">Đang hoạt động</span>
        </div>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="main-grid">
      <!-- Line Chart -->
      <div class="section-card chart-section">
        <div class="card-header">
          <h3>📈 Hoạt động người dùng theo ngày</h3>
        </div>
        <div class="chart-container">
          <v-chart :option="lineOption" autoresize style="height: 320px; width: 100%" />
        </div>
      </div>

      <!-- Pie Chart -->
      <div class="section-card">
        <div class="card-header">
          <h3>🎯 Phân bố theo vai trò</h3>
        </div>
        <div class="chart-container pie-chart">
          <v-chart :option="roleOption" autoresize style="height: 200px; width: 100%" />
        </div>
        <div class="role-list">
          <div v-for="(item, idx) in byRole" :key="item.role" class="role-item">
            <span class="role-dot" :style="{ background: roleColors[idx] }"></span>
            <span class="role-name">{{ roleLabel(item.role) }}</span>
            <span class="role-count">{{ fmt(item.count) }}</span>
          </div>
          <div v-if="!byRole.length" class="empty-state">Chưa có dữ liệu</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import {
  reportService,
  type UserKPIs,
  type UserSeriesPoint,
  type UserByRole,
} from '@/services/report.service'
import { useThemeStore } from '@/store/theme.store'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
} from 'echarts/components'

use([CanvasRenderer, LineChart, PieChart, GridComponent, TooltipComponent, LegendComponent])

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const range = ref<[string, string] | null>(null)
const exporting = ref(false)
const kpi = reactive<UserKPIs>({ dau: 0, mau: 0, newUsers: 0, activeUsers: 0 })
const series = ref<UserSeriesPoint[]>([])
const byRole = ref<UserByRole[]>([])

const roleColors = ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444']

function fmt(v: number) {
  return new Intl.NumberFormat().format(v)
}

function params() {
  return { from: range.value?.[0], to: range.value?.[1] }
}

function reset() {
  range.value = null
  reload()
}

async function exportCsv() {
  exporting.value = true
  try {
    const blob = await reportService.exportUsersCsv(params())
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `users_${new Date().toISOString().slice(0, 10)}.csv`
    a.click()
    URL.revokeObjectURL(url)
  } finally {
    exporting.value = false
  }
}

async function reload() {
  kpi.dau = kpi.mau = kpi.newUsers = kpi.activeUsers = 0
  series.value = []
  byRole.value = []
  const [k, s, r] = await Promise.all([
    reportService.userKpis(params()),
    reportService.userSeries(params()),
    reportService.userByRole(params()),
  ])
  Object.assign(kpi, k)
  series.value = s
  byRole.value = r
}

onMounted(reload)

const roleLabel = (role: string) => {
  const map: Record<string, string> = {
    admin: 'Quản trị viên',
    instructor: 'Giáo viên',
    student: 'Học sinh',
  }
  return map[role] || role
}

const lineOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: {
    data: ['Hoạt động hàng ngày', 'Người dùng mới'],
    bottom: 0,
    textStyle: { color: isDark.value ? '#94a3b8' : '#64748b', fontSize: 12 },
  },
  grid: { left: 50, right: 20, top: 20, bottom: 50 },
  xAxis: {
    type: 'category',
    data: series.value.map((x) => x.date),
    axisLine: { lineStyle: { color: isDark.value ? '#334155' : '#e2e8f0' } },
    axisLabel: { color: isDark.value ? '#94a3b8' : '#64748b', fontSize: 11 },
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false },
    axisLabel: { color: isDark.value ? '#94a3b8' : '#64748b', fontSize: 11 },
    splitLine: { lineStyle: { color: isDark.value ? '#1e293b' : '#f1f5f9' } },
  },
  series: [
    {
      name: 'Hoạt động hàng ngày',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: { color: '#06b6d4', width: 3 },
      itemStyle: { color: '#06b6d4' },
      areaStyle: { color: isDark.value ? 'rgba(6, 182, 212, 0.15)' : 'rgba(6, 182, 212, 0.08)' },
      data: series.value.map((x) => x.dau),
    },
    {
      name: 'Người dùng mới',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: { color: '#22c55e', width: 3 },
      itemStyle: { color: '#22c55e' },
      areaStyle: { color: isDark.value ? 'rgba(34, 197, 94, 0.15)' : 'rgba(34, 197, 94, 0.08)' },
      data: series.value.map((x) => x.newUsers),
    },
  ],
}))

const roleOption = computed(() => ({
  tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
  series: [
    {
      type: 'pie',
      radius: ['45%', '70%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: {
        borderRadius: 6,
        borderColor: isDark.value ? '#1e293b' : '#fff',
        borderWidth: 2,
      },
      label: { show: false },
      data: byRole.value.map((x, i) => ({
        name: roleLabel(x.role),
        value: x.count,
        itemStyle: { color: roleColors[i % roleColors.length] },
      })),
    },
  ],
}))
</script>

<style scoped>
.analytics {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding-bottom: 24px;
}

/* Header */
.analytics-header {
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

.analytics.dark .title { color: white; }
.analytics.light .title { color: #1e293b; }

.subtitle {
  font-size: 14px;
  margin: 4px 0 0;
}

.analytics.dark .subtitle { color: #64748b; }
.analytics.light .subtitle { color: #94a3b8; }

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.action-btn {
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

.action-btn.primary {
  background: linear-gradient(135deg, #06b6d4, #8b5cf6);
  color: white;
}

.action-btn.secondary {
  border: 1px solid;
}

.analytics.dark .action-btn.secondary {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
}

.analytics.light .action-btn.secondary {
  background: white;
  border-color: #e2e8f0;
  color: #1e293b;
}

.action-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.action-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

/* KPI Row */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

@media (min-width: 768px) {
  .kpi-row { grid-template-columns: repeat(4, 1fr); }
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
.kpi-card.purple::before { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
.kpi-card.green::before { background: linear-gradient(90deg, #22c55e, #4ade80); }
.kpi-card.orange::before { background: linear-gradient(90deg, #f97316, #fb923c); }

.analytics.dark .kpi-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.analytics.light .kpi-card {
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
.kpi-card.purple .kpi-icon { background: rgba(139, 92, 246, 0.15); color: #8b5cf6; }
.kpi-card.green .kpi-icon { background: rgba(34, 197, 94, 0.15); color: #22c55e; }
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

.analytics.dark .kpi-value { color: white; }
.analytics.light .kpi-value { color: #1e293b; }

.kpi-label {
  font-size: 13px;
  margin-top: 2px;
}

.analytics.dark .kpi-label { color: #64748b; }
.analytics.light .kpi-label { color: #94a3b8; }

/* Main Grid */
.main-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

@media (min-width: 1024px) {
  .main-grid { grid-template-columns: 2fr 1fr; }
}

/* Section Card */
.section-card {
  border-radius: 16px;
  padding: 20px;
  transition: all 0.3s ease;
}

.analytics.dark .section-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.analytics.light .section-card {
  background: white;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.chart-section {
  min-height: 400px;
  display: flex;
  flex-direction: column;
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

.analytics.dark .card-header h3 { color: white; }
.analytics.light .card-header h3 { color: #1e293b; }

.chart-container {
  flex: 1;
  min-height: 280px;
}

.pie-chart {
  min-height: 180px;
}

/* Role List */
.role-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid;
}

.analytics.dark .role-list { border-color: rgba(255, 255, 255, 0.08); }
.analytics.light .role-list { border-color: #e2e8f0; }

.role-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 10px;
  transition: all 0.2s;
}

.analytics.dark .role-item { background: rgba(255, 255, 255, 0.03); }
.analytics.light .role-item { background: #f8fafc; }

.role-item:hover {
  transform: translateX(4px);
}

.role-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.role-name {
  flex: 1;
  font-size: 14px;
}

.analytics.dark .role-name { color: #e2e8f0; }
.analytics.light .role-name { color: #1e293b; }

.role-count {
  font-size: 14px;
  font-weight: 600;
}

.analytics.dark .role-count { color: #22d3ee; }
.analytics.light .role-count { color: #6366f1; }

/* Empty State */
.empty-state {
  text-align: center;
  padding: 20px;
  font-size: 14px;
}

.analytics.dark .empty-state { color: #64748b; }
.analytics.light .empty-state { color: #94a3b8; }
</style>
