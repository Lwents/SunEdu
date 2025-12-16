<template>
  <div class="space-y-6">
    <!-- Filters -->
    <div class="flex flex-wrap items-center gap-3">
      <el-date-picker
        v-model="range"
        type="daterange"
        range-separator="–"
        start-placeholder="Từ"
        end-placeholder="Đến"
      />
      <el-select v-model="granularity" placeholder="Granularity" class="w-40">
        <el-option label="Ngày" value="day" />
        <el-option label="Tuần" value="week" />
        <el-option label="Tháng" value="month" />
      </el-select>
      <el-button type="primary" @click="fetchAll">Làm mới</el-button>
    </div>

    <!-- KPI cards -->
    <div class="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-6 gap-3">
      <KpiCard title="DAU" :value="fmt(kpis.dau)" icon="users" />
      <KpiCard title="ĐK mới (7d)" :value="fmt(kpis.signups7d)" icon="user-plus" />
      <KpiCard title="GMV hôm nay" :value="currency(kpis.gmvToday)" icon="credit-card" />
      <KpiCard title="Giao dịch hôm nay" :value="fmt(kpis.txToday)" icon="activity" />
      <KpiCard title="Refund rate (7d)" :value="percent(kpis.refundRate7d)" icon="rotate-ccw" />
      <KpiCard title="Chờ duyệt" :value="fmt(kpis.approvalsPending)" icon="clipboard-check" />
    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-4">
      <div class="xl:col-span-2 rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="mb-3 font-medium">Doanh thu & giao dịch</div>
        <v-chart :option="chartOption" autoresize style="height: 260px" />
      </div>
      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="mb-3 font-medium">Top khóa học</div>
        <el-table :data="topCourses" size="small" height="16rem">
          <el-table-column prop="title" label="Khóa học" />
          <el-table-column prop="enrollments" label="ĐK" width="80" align="right" />
        </el-table>
      </div>
    </div>

    <!-- Tables -->
    <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">
      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="mb-3 font-medium">Giao dịch gần đây</div>
        <el-table :data="recentTransactions" size="small" height="20rem">
          <el-table-column prop="id" label="Mã" width="120" />
          <el-table-column prop="user" label="Người mua" />
          <el-table-column prop="course" label="Khóa học" />
          <el-table-column prop="amount" label="Số tiền" width="110" align="right">
            <template #default="{ row }">{{ currency(row.amount) }}</template>
          </el-table-column>
          <el-table-column prop="gateway" label="Cổng" width="90" />
          <el-table-column prop="status" label="TT" width="110" />
        </el-table>
      </div>

      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="mb-2 flex items-center justify-between">
          <div>
            <div class="font-medium">Người dùng đang hoạt động</div>
            <p class="text-xs text-gray-500">
              Theo dõi hoạt động trong {{ activeUsers.windowMinutes }} phút gần nhất
            </p>
          </div>
          <div class="text-right">
            <p class="text-2xl font-semibold text-indigo-600">{{ fmt(activeUsers.count) }}</p>
            <p class="text-xs text-gray-500">đang online</p>
          </div>
        </div>

        <el-table :data="activeUsers.recent" size="small" height="18rem" :show-header="false">
          <el-table-column>
            <template #default="{ row }">
              <div class="flex items-center justify-between text-sm text-gray-700">
                <div>
                  <p class="font-medium">{{ row.name }}</p>
                  <p class="text-xs text-gray-500">{{ row.email }} • {{ roleLabel(row.role, row.roleLabel) }}</p>
                </div>
                <span class="text-xs text-gray-400">{{ formatTime(row.lastActive) }}</span>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- Security & System -->
    <div class="grid grid-cols-1 xl:grid-cols-2 gap-4">
      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="mb-3 font-medium">Bảo mật</div>
        <ul class="text-sm text-gray-700 space-y-2">
          <li>
            Đăng nhập thất bại 24h: <b>{{ security.failedLogins24h }}</b>
          </li>
          <li>
            Tài khoản bị khóa: <b>{{ security.lockedAccounts }}</b>
          </li>
          <li>
            SSL hết hạn trong: <b>{{ security.sslDaysToExpire }} ngày</b>
          </li>
        </ul>
      </div>
      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="mb-3 font-medium">Sức khỏe hệ thống</div>
        <ul class="text-sm text-gray-700 space-y-2">
          <li>
            CPU p95: <b>{{ system.cpuP95.toFixed(1) }}%</b> • RAM p95: <b>{{ system.ramP95.toFixed(1) }}%</b> • Disk:
            <b>{{ system.disk.toFixed(1) }}%</b>
          </li>
          <li>
            Backup lần gần nhất: <b>{{ system.backup.lastRun }}</b> • Trạng thái:
            <b>{{ system.backup.status }}</b>
          </li>
        </ul>
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
import { LineChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { GridComponent, TooltipComponent, LegendComponent, TitleComponent } from 'echarts/components'

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent, TitleComponent])

const range = ref<[Date, Date] | null>(null)
const granularity = ref<'day' | 'week' | 'month'>('day')

const kpis = reactive({
  dau: 0,
  signups7d: 0,
  gmvToday: 0,
  txToday: 0,
  refundRate7d: 0,
  approvalsPending: 0,
})
const topCourses = ref<any[]>([])
const recentTransactions = ref<any[]>([])
const activeUsers = reactive({ count: 0, windowMinutes: 10, recent: [] as any[] })
const security = reactive({ failedLogins24h: 0, lockedAccounts: 0, sslDaysToExpire: 30 })
const system = reactive({ cpuP95: 0, ramP95: 0, disk: 0, backup: { lastRun: '-', status: '-' } })
const chartData = ref<{ labels: string[]; gross: number[]; tx: number[] }>({ labels: [], gross: [], tx: [] })
const loadingChart = ref(false)

function fmt(v: number) {
  return new Intl.NumberFormat().format(v)
}
function currency(v: number) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(v)
}
function percent(v: number) {
  return `${v.toFixed(1)}%`
}

const chartOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  legend: { data: ['Gross', 'Giao dịch'], bottom: 0 },
  grid: { left: 40, right: 20, top: 20, bottom: 40 },
  xAxis: { type: 'category', data: chartData.value.labels },
  yAxis: [
    { type: 'value', name: '₫' },
    { type: 'value', name: 'Đơn', minInterval: 1 },
  ],
  series: [
    {
      name: 'Gross',
      type: 'line',
      smooth: true,
      data: chartData.value.gross,
      lineStyle: { color: '#2563eb' },
    },
    {
      name: 'Giao dịch',
      type: 'line',
      yAxisIndex: 1,
      smooth: true,
      data: chartData.value.tx,
      lineStyle: { color: '#f59e0b' },
    },
  ],
}))

function formatTime(value: string | null) {
  if (!value) return 'Không rõ'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' })
}
function roleLabel(role?: string, provided?: string) {
  if (provided) return provided
  if (!role) return 'N/A'
  const mapping: Record<string, string> = {
    admin: 'Quản trị viên',
    instructor: 'Giáo viên',
    teacher: 'Giáo viên',
    student: 'Học sinh',
  }
  const key = role.toLowerCase()
  return mapping[key] || role
}

// Fetch system health separately (for realtime updates)
async function fetchSystemHealth() {
  try {
    const health = await systemService.getHealth()
    system.cpuP95 = health.cpu.p95
    system.ramP95 = health.ram.p95
    system.disk = health.disk.current
    
    // Format backup status
    if (health.backup.status === 'success' && health.backup.lastBackup) {
      const backupDate = new Date(health.backup.lastBackup)
      system.backup.lastRun = backupDate.toLocaleString('vi-VN', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
      system.backup.status = 'Thành công'
    } else if (health.backup.status === 'no_backup') {
      system.backup.lastRun = 'Chưa có'
      system.backup.status = 'Chưa backup'
    } else {
      system.backup.lastRun = 'Lỗi'
      system.backup.status = 'Lỗi'
    }
  } catch (healthError: any) {
    console.error('Failed to fetch system health:', healthError)
    // Keep current values if health fetch fails
  }
}

async function fetchActiveUsers() {
  try {
    const data = await dashboardService.getActiveUsers()
    activeUsers.count = data.count
    activeUsers.windowMinutes = data.windowMinutes
    activeUsers.recent = data.recent
  } catch (error) {
    console.error('Failed to fetch active users:', error)
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
  // Mặc định 30 ngày gần nhất
  const to = new Date()
  const from = new Date()
  from.setDate(to.getDate() - 30)
  return { from: from.toISOString().slice(0, 10), to: to.toISOString().slice(0, 10), granularity: granularity.value }
}

async function fetchChart() {
  loadingChart.value = true
  try {
    const params = buildRangeParams()
    const series = await reportService.revenueTimeseries(params)
    const byDate: Record<string, { gross: number; tx: number }> = {}
    series.forEach((p) => {
      byDate[p.date] = { gross: p.gross, tx: 0 }
    })
    // Thêm số đơn từ recent transactions (nếu cùng ngày)
    recentTransactions.value.forEach((tx) => {
      const d = tx.createdAt ? tx.createdAt.slice(0, 10) : ''
      if (!byDate[d]) byDate[d] = { gross: 0, tx: 0 }
      byDate[d].tx += 1
    })
    const labels = Object.keys(byDate).sort()
    chartData.value = {
      labels,
      gross: labels.map((d) => byDate[d].gross),
      tx: labels.map((d) => byDate[d].tx),
    }
  } catch (err) {
    console.error('Chart load error', err)
  } finally {
    loadingChart.value = false
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
    
    // Fetch realtime panels on initial load
    await Promise.all([fetchSystemHealth(), fetchActiveUsers()])
  } catch (e: any) {
    showToast(e?.message || 'Không tải được dữ liệu dashboard', 'error')
  }
}

// Auto-refresh panels every 5 seconds
let healthInterval: ReturnType<typeof setInterval> | null = null
let activeUsersInterval: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  fetchAll()
  // Start auto-refresh for realtime panels
  healthInterval = setInterval(() => {
    fetchSystemHealth()
  }, 5000) // Update every 5 seconds
  activeUsersInterval = setInterval(() => {
    fetchActiveUsers()
  }, 5000)
})

onBeforeUnmount(() => {
  // Clear interval when component is unmounted
  if (healthInterval) {
    clearInterval(healthInterval)
    healthInterval = null
  }
  if (activeUsersInterval) {
    clearInterval(activeUsersInterval)
    activeUsersInterval = null
  }
})
</script>

<!-- KpiCard nhỏ gọn -->
<script lang="ts">
export default {}
</script>

<!-- Bạn có thể đặt KpiCard vào components/ui/KpiCard.vue -->
