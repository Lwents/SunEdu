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
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
        </div>
        <div class="kpi-right">
          <span class="kpi-value">{{ fmt(kpi.totalPublished) }}</span>
          <span class="kpi-label">Khóa đã xuất bản</span>
        </div>
      </div>

      <div class="kpi-card green">
        <div class="kpi-left">
          <div class="kpi-icon">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
        </div>
        <div class="kpi-right">
          <span class="kpi-value">{{ fmt(kpi.totalEnrollments) }}</span>
          <span class="kpi-label">Tổng ghi danh</span>
        </div>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="main-grid">
      <!-- Bar Chart -->
      <div class="section-card">
        <div class="card-header">
          <h3>📊 Lượt xem theo môn</h3>
        </div>
        <div class="chart-container">
          <v-chart :option="barOption" autoresize style="height: 320px; width: 100%" />
        </div>
      </div>

      <!-- Top Content Table -->
      <div class="section-card table-section">
        <div class="card-header">
          <h3>🏆 Top nội dung phổ biến</h3>
        </div>
        <div class="table-container">
          <div class="content-list">
            <div v-for="(item, idx) in tops" :key="idx" class="content-item">
              <div class="content-rank" :class="getRankClass(idx)">{{ idx + 1 }}</div>
              <div class="content-info">
                <span class="content-title">{{ item.title }}</span>
              </div>
              <div class="content-stats">
                <div class="stat">
                  <span class="stat-value">{{ fmt(item.views) }}</span>
                  <span class="stat-label">Lượt xem</span>
                </div>
                <div class="stat">
                  <span class="stat-value">{{ fmt(item.enrollments) }}</span>
                  <span class="stat-label">Ghi danh</span>
                </div>
              </div>
            </div>
            <div v-if="!tops.length" class="empty-state">Chưa có dữ liệu</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import {
  reportService,
  type ContentKPIs,
  type ViewsBySubject,
  type TopContentRow,
} from '@/services/report.service'
import { useThemeStore } from '@/store/theme.store'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
} from 'echarts/components'

use([CanvasRenderer, BarChart, GridComponent, TooltipComponent, LegendComponent])

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const range = ref<[string, string] | null>(null)
const exporting = ref(false)

const kpi = reactive<ContentKPIs>({ totalPublished: 0, totalEnrollments: 0, avgRating: 0 })
const subjectViews = ref<ViewsBySubject[]>([])
const tops = ref<TopContentRow[]>([])

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

function getRankClass(idx: number) {
  if (idx === 0) return 'gold'
  if (idx === 1) return 'silver'
  if (idx === 2) return 'bronze'
  return ''
}

async function exportCsv() {
  exporting.value = true
  try {
    const blob = await reportService.exportContentCsv(params())
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `content_${new Date().toISOString().slice(0, 10)}.csv`
    a.click()
    URL.revokeObjectURL(url)
  } finally {
    exporting.value = false
  }
}

async function reload() {
  const [k, v, t] = await Promise.all([
    reportService.contentKpis(params()),
    reportService.viewsBySubject(params()),
    reportService.topContents(params()),
  ])
  Object.assign(kpi, k)
  subjectViews.value = v
  tops.value = t
}

onMounted(reload)

const barOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: 50, right: 20, top: 20, bottom: 40 },
  xAxis: {
    type: 'category',
    data: subjectViews.value.map((x) => x.subject),
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
      name: 'Lượt xem',
      type: 'bar',
      barWidth: '60%',
      itemStyle: {
        borderRadius: [6, 6, 0, 0],
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: '#6366f1' },
            { offset: 1, color: '#8b5cf6' },
          ],
        },
      },
      data: subjectViews.value.map((x) => x.views),
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

@media (max-width: 768px) {
  .kpi-row { grid-template-columns: 1fr; }
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
  .main-grid { grid-template-columns: 1fr 2fr; }
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
  min-height: 300px;
}

/* Content List */
.content-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.content-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 12px;
  transition: all 0.2s;
}

.analytics.dark .content-item { background: rgba(255, 255, 255, 0.03); }
.analytics.light .content-item { background: #f8fafc; }

.content-item:hover {
  transform: translateX(4px);
}

.content-rank {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  flex-shrink: 0;
}

.analytics.dark .content-rank { background: rgba(255, 255, 255, 0.1); color: #94a3b8; }
.analytics.light .content-rank { background: #e2e8f0; color: #64748b; }

.content-rank.gold { background: linear-gradient(135deg, #fbbf24, #f59e0b); color: white; }
.content-rank.silver { background: linear-gradient(135deg, #94a3b8, #64748b); color: white; }
.content-rank.bronze { background: linear-gradient(135deg, #d97706, #b45309); color: white; }

.content-info {
  flex: 1;
  min-width: 0;
}

.content-title {
  font-size: 14px;
  font-weight: 500;
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.analytics.dark .content-title { color: #e2e8f0; }
.analytics.light .content-title { color: #1e293b; }

.content-stats {
  display: flex;
  gap: 24px;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 60px;
}

.stat-value {
  font-size: 14px;
  font-weight: 600;
}

.analytics.dark .stat-value { color: #22d3ee; }
.analytics.light .stat-value { color: #6366f1; }

.stat-value.rating { color: #f59e0b !important; }

.stat-label {
  font-size: 11px;
  margin-top: 2px;
}

.analytics.dark .stat-label { color: #64748b; }
.analytics.light .stat-label { color: #94a3b8; }

/* Empty State */
.empty-state {
  text-align: center;
  padding: 40px 20px;
  font-size: 14px;
}

.analytics.dark .empty-state { color: #64748b; }
.analytics.light .empty-state { color: #94a3b8; }

@media (max-width: 768px) {
  .content-stats {
    flex-direction: column;
    gap: 8px;
  }
  
  .stat {
    flex-direction: row;
    gap: 8px;
    min-width: auto;
  }
}
</style>
