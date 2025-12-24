<template>
  <div class="revenue-page">
    <!-- Filter Bar -->
    <div class="filter-card">
      <div class="filter-grid">
        <el-date-picker
          v-model="range"
          type="daterange"
          unlink-panels
          range-separator="→"
          start-placeholder="Từ ngày"
          end-placeholder="Đến ngày"
          value-format="YYYY-MM-DD"
          class="filter-date"
          @change="applyRange"
        />
        <el-select v-model="gran" @change="reload" placeholder="Theo ngày">
          <el-option label="Theo ngày" value="day" />
          <el-option label="Theo tuần" value="week" />
          <el-option label="Theo tháng" value="month" />
        </el-select>
        <div class="filter-actions">
          <el-button @click="reset">Xoá lọc</el-button>
          <el-button type="primary" @click="reload">Lọc</el-button>
          <el-button @click="exportCsv" :loading="exporting">Xuất CSV</el-button>
        </div>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <div class="kpi-content">
          <div class="kpi-label">Doanh thu gộp</div>
          <div class="kpi-value">{{ money(kpi.gross) }}</div>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon">📊</div>
        <div class="kpi-content">
          <div class="kpi-label">Net</div>
          <div class="kpi-value">{{ money(kpi.net) }}</div>
        </div>
      </div>
      <div class="kpi-card">
        <div class="kpi-icon">🛒</div>
        <div class="kpi-content">
          <div class="kpi-label">Số đơn</div>
          <div class="kpi-value">{{ kpi.orders }}</div>
        </div>
      </div>
    </div>

    <!-- Charts -->
    <div class="charts-grid">
      <div class="chart-card chart-main">
        <div class="card-title">📈 Dòng tiền theo {{ granLabel }}</div>
        <v-chart :option="lineOption" autoresize style="height: 360px" />
      </div>
      <div class="chart-card chart-pie">
        <div class="card-title">🥧 Tỷ trọng theo cổng</div>
        <v-chart :option="pieOption" autoresize style="height: 360px" />
      </div>
    </div>

    <!-- Top Courses -->
    <div class="table-card">
      <div class="card-title">🏆 Khoá học doanh thu cao nhất</div>
      <el-table :data="topCourses" v-loading="loading.top" height="420">
        <el-table-column type="index" width="60" />
        <el-table-column prop="title" label="Khoá học" min-width="240" />
        <el-table-column prop="teacher" label="GV" width="140" />
        <el-table-column label="Doanh thu" width="140" align="right">
          <template #default="{ row }">{{ money(row.gross) }}</template>
        </el-table-column>
        <el-table-column label="Thu ròng" width="140" align="right">
          <template #default="{ row }">{{ money(row.net) }}</template>
        </el-table-column>
        <el-table-column prop="orders" label="Đơn" width="100" align="center" />
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import {
  reportService,
  type RevenuePoint,
  type RevenueByGateway,
  type RevenueTopCourse,
} from '@/services/report.service'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, PieChart } from 'echarts/charts'
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
} from 'echarts/components'
use([
  CanvasRenderer,
  LineChart,
  PieChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
])

const components = { VChart }

const range = ref<[string, string] | null>(null)
const gran = ref<'day' | 'week' | 'month'>('day')
const exporting = ref(false)
const loading = reactive({ series: false, pie: false, top: false })

const series = ref<RevenuePoint[]>([])
const byGateway = ref<RevenueByGateway[]>([])
const topCourses = ref<RevenueTopCourse[]>([])

const kpi = reactive({ gross: 0, net: 0, refunds: 0, orders: 0 })
const granLabel = computed(() =>
  gran.value === 'day' ? 'ngày' : gran.value === 'week' ? 'tuần' : 'tháng',
)
const money = (v: number) =>
  new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(v)

function params() {
  return { from: range.value?.[0], to: range.value?.[1], granularity: gran.value }
}
function applyRange() {
  reload()
}
function reset() {
  range.value = null
  gran.value = 'day'
  reload()
}

async function loadSeries() {
  loading.series = true
  try {
    series.value = await reportService.revenueTimeseries(params())
    // KPI
    const gross = series.value.reduce((a, b) => a + b.gross, 0)
    const net = series.value.reduce((a, b) => a + b.net, 0)
    const refunds = series.value.reduce((a, b) => a + b.refunds, 0)
    kpi.gross = gross
    kpi.net = net
    kpi.refunds = refunds
    kpi.orders = Math.round(gross / 99000)
  } finally {
    loading.series = false
  }
}
async function loadPie() {
  loading.pie = true
  try {
    byGateway.value = await reportService.revenueByGateway(params())
  } finally {
    loading.pie = false
  }
}
async function loadTop() {
  loading.top = true
  try {
    topCourses.value = await reportService.revenueTopCourses(params())
  } finally {
    loading.top = false
  }
}
async function exportCsv() {
  exporting.value = true
  try {
    const blob = await reportService.exportRevenueCsv(params())
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `revenue_${new Date().toISOString().slice(0, 10)}.csv`
    a.click()
    URL.revokeObjectURL(url)
  } finally {
    exporting.value = false
  }
}

async function reload() {
  await Promise.all([loadSeries(), loadPie(), loadTop()])
}

onMounted(reload)

// ----- ECharts options -----
const lineOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { 
    data: ['Doanh thu', 'Thu ròng'],
    textStyle: { color: '#94a3b8' }
  },
  grid: { left: 32, right: 24, top: 36, bottom: 32 },
  xAxis: { 
    type: 'category', 
    data: series.value.map((x) => x.date),
    axisLabel: { color: '#94a3b8' },
    axisLine: { lineStyle: { color: '#334155' } }
  },
  yAxis: { 
    type: 'value',
    axisLabel: { color: '#94a3b8' },
    splitLine: { lineStyle: { color: '#334155' } }
  },
  series: [
    {
      name: 'Doanh thu',
      type: 'line',
      smooth: true,
      data: series.value.map((x) => x.gross),
      itemStyle: { color: '#22c55e' }
    },
    {
      name: 'Thu ròng',
      type: 'line',
      smooth: true,
      data: series.value.map((x) => x.net),
      itemStyle: { color: '#3b82f6' }
    },
  ],
}))
const pieOption = computed(() => ({
  tooltip: { trigger: 'item' },
  legend: { 
    top: 8,
    textStyle: { color: '#94a3b8' }
  },
  series: [
    {
      name: 'Cổng thanh toán',
      type: 'pie',
      radius: ['40%', '70%'],
      itemStyle: { borderRadius: 6, borderColor: 'rgba(255,255,255,0.1)', borderWidth: 2 },
      label: { color: '#e2e8f0' },
      data: byGateway.value.map((x) => ({ name: x.gateway, value: x.amount })),
    },
  ],
}))
</script>

<style scoped>
.revenue-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* Filter Card */
.filter-card {
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(30, 41, 59, 0.5);
}

.filter-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.filter-date {
  flex: 2;
  min-width: 240px;
}

.filter-actions {
  display: flex;
  gap: 8px;
  flex: 0 0 auto;
}

/* KPI Cards */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.kpi-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.6));
  backdrop-filter: blur(10px);
}

.kpi-icon {
  font-size: 32px;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: rgba(59, 130, 246, 0.15);
}

.kpi-content {
  flex: 1;
}

.kpi-label {
  font-size: 13px;
  color: #94a3b8;
  margin-bottom: 4px;
}

.kpi-value {
  font-size: 24px;
  font-weight: 600;
  color: #e2e8f0;
}

/* Charts Grid */
.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 16px;
}

@media (max-width: 1024px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}

.chart-card {
  padding: 20px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(30, 41, 59, 0.5);
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #e2e8f0;
  margin-bottom: 16px;
}

/* Table Card */
.table-card {
  padding: 20px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(30, 41, 59, 0.5);
}

/* ============================================== */
/* Light Mode Overrides                          */
/* ============================================== */
html:not(.dark) .filter-card,
html:not(.dark) .chart-card,
html:not(.dark) .table-card {
  background: #fff;
  border-color: #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

html:not(.dark) .kpi-card {
  background: linear-gradient(135deg, #fff, #f8fafc);
  border-color: #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

html:not(.dark) .kpi-label {
  color: #64748b;
}

html:not(.dark) .kpi-value {
  color: #1e293b;
}

html:not(.dark) .card-title {
  color: #1e293b;
}
</style>
