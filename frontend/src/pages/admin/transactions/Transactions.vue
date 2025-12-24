<template>
  <div class="space-y-4">
    <!-- KPIs -->
    <div class="grid grid-cols-2 gap-3 md:grid-cols-4">
      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="text-xs text-gray-500">Số giao dịch</div>
        <div class="mt-2 text-2xl font-semibold">{{ metrics.count }}</div>
      </div>
      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="text-xs text-gray-500">Doanh thu gộp</div>
        <div class="mt-2 text-2xl font-semibold">{{ money(metrics.gross) }}</div>
      </div>
      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="text-xs text-gray-500">Net</div>
        <div class="mt-2 text-2xl font-semibold">{{ money(metrics.net) }}</div>
      </div>
      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="text-xs text-gray-500">Hoàn tiền (ước)</div>
        <div class="mt-2 text-2xl font-semibold">{{ money(metrics.refunds) }}</div>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="grid grid-cols-1 items-start gap-3 md:grid-cols-4 xl:grid-cols-7">
      <el-input
        v-model="query.q"
        clearable
        placeholder="Tìm theo Mã GD / email / khoá học"
        @keyup.enter="applyFilters"
        @clear="applyFilters"
        class="md:col-span-2 xl:col-span-2 w-full"
      >
        <template #prefix>🔎</template>
      </el-input>

      <el-select v-model="query.status" clearable placeholder="Trạng thái" @change="applyFilters">
        <el-option label="Pending" value="Pending" />
        <el-option label="Processing" value="Processing" />
        <el-option label="Succeeded" value="Succeeded" />
        <el-option label="Failed" value="Failed" />
        <el-option label="Refunded" value="Refunded" />
        <el-option label="Disputed" value="Disputed" />
      </el-select>

      <el-select
        v-model="query.gateway"
        clearable
        placeholder="Cổng thanh toán"
        @change="applyFilters"
      >
        <el-option label="VNPay" value="VNPay" />
        <el-option label="Momo" value="Momo" />
        <el-option label="QR" value="QR" />
        <el-option label="Ngân hàng" value="Bank" />
      </el-select>

      <div class="md:col-span-2 xl:col-span-2">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          unlink-panels
          range-separator="–"
          start-placeholder="Từ ngày"
          end-placeholder="Đến ngày"
          value-format="YYYY-MM-DD"
          class="w-full"
          @change="applyDateRange"
        />
      </div>

      <div class="xl:col-span-1 flex items-center gap-2 md:justify-end">
        <el-button @click="resetFilters">Xoá lọc</el-button>
        <el-button type="primary" plain @click="applyFilters">Lọc</el-button>
      </div>
    </div>

    <!-- Table -->
    <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
      <div class="mb-3 flex items-center justify-between">
        <div class="text-sm text-gray-600">Tổng: {{ total }}</div>
        <div class="flex items-center gap-2">
          <el-button @click="doExport" :loading="exporting">Xuất CSV</el-button>
          <el-button type="primary" @click="refresh" :loading="loading">Tải lại</el-button>
        </div>
      </div>

      <el-table :data="items" v-loading="loading" height="560" @row-dblclick="goDetail">
        <el-table-column prop="id" label="Mã GD" min-width="140" />
        <el-table-column label="Người mua" min-width="200" show-overflow-tooltip>
          <template #default="{ row }">
            <div class="font-medium text-gray-800">{{ row.buyerName }}</div>
            <div class="text-xs text-gray-500">{{ row.buyerEmail }}</div>
          </template>
        </el-table-column>
        <el-table-column label="Khoá học" min-width="220" show-overflow-tooltip>
          <template #default="{ row }">{{ row.courseTitle }}</template>
        </el-table-column>
        <el-table-column prop="gateway" label="Cổng" width="110" />
        <el-table-column label="Số tiền" width="130" align="right">
          <template #default="{ row }">{{ money(row.amount) }}</template>
        </el-table-column>
        <el-table-column prop="status" label="Trạng thái" width="130" align="center">
          <template #default="{ row }">
            <span 
              class="status-badge"
              :class="{
                'status-succeeded': row.status === 'Succeeded',
                'status-pending': row.status === 'Pending',
                'status-processing': row.status === 'Processing',
                'status-failed': row.status === 'Failed',
                'status-refunded': row.status === 'Refunded',
                'status-disputed': row.status === 'Disputed'
              }"
            >
              {{ row.status }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="Thời gian" min-width="170">
          <template #default="{ row }">{{ fmt(row.createdAt) }}</template>
        </el-table-column>

        <el-table-column fixed="right" width="180">
          <template #default="{ row }">
            <div class="action-buttons">
              <button class="action-btn btn-view" @click="goDetail(row)">Xem</button>
              <button
                v-if="row.status === 'Succeeded'"
                class="action-btn btn-refund"
                @click="promptRefund(row)"
              >
                Hoàn tiền
              </button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <div class="mt-3 flex justify-end">
        <el-pagination
          background
          layout="total, prev, pager, next"
          :total="total"
          :current-page="page"
          :page-size="pageSize"
          @current-change="
            (p: number) => {
              page = p
              fetch()
            }
          "
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  paymentService,
  type TxSummary,
  type TxStatus,
  type Gateway,
  type PageParams,
  type TxMetrics,
} from '@/services/payment.service'
import { showToast } from '@/utils/toast'
import { showConfirm } from '@/utils/confirm'

const router = useRouter()

// state
const items = ref<TxSummary[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)
const exporting = ref(false)
const metrics = reactive<TxMetrics>({ count: 0, gross: 0, net: 0, refunds: 0, disputed: 0 })

const query = reactive<PageParams>({
  q: '',
  status: undefined,
  gateway: undefined,
  page: page.value,
  pageSize,
})
const dateRange = ref<[string, string] | null>(null)

// helpers
const fmt = (iso?: string) => (iso ? new Date(iso).toLocaleString('vi-VN') : '')
const money = (v: number) =>
  new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(v)
const statusTagType = (s: TxStatus) =>
  s === 'Succeeded'
    ? 'success'
    : s === 'Processing'
      ? 'warning'
      : s === 'Pending'
        ? 'info'
        : s === 'Refunded'
          ? 'info'
          : s === 'Disputed'
            ? 'danger'
            : 'danger'

// actions
function applyDateRange() {
  query.from = dateRange.value?.[0]
  query.to = dateRange.value?.[1]
  applyFilters()
}
function resetFilters() {
  query.q = ''
  query.status = undefined
  query.gateway = undefined
  query.from = undefined
  query.to = undefined
  dateRange.value = null
  page.value = 1
  fetch()
}
function applyFilters() {
  page.value = 1
  fetch()
}

async function fetch() {
  loading.value = true
  try {
    const { items: rows, total: t } = await paymentService.list({
      ...query,
      page: page.value,
      pageSize,
    })
    items.value = rows
    total.value = t
    const m = await paymentService.metrics({ ...query })
    Object.assign(metrics, m)
  } catch (error: any) {
    showToast(error?.message || 'Không tải được danh sách giao dịch', 'error')
  } finally {
    loading.value = false
  }
}
function refresh() {
  fetch()
}
function goDetail(row: TxSummary) {
  router.push(`/admin/transactions/${row.id}`)
}

async function doExport() {
  try {
    exporting.value = true
    const blob = await paymentService.exportCsv({ ...query })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `transactions_${new Date().toISOString().slice(0, 10)}.csv`
    a.click()
    URL.revokeObjectURL(url)
    showToast('Đang tải file CSV…', 'info')
  } catch (error: any) {
    showToast(error?.message || 'Xuất CSV thất bại', 'error')
  } finally {
    exporting.value = false
  }
}

async function promptRefund(row: TxSummary) {
  const wantsRefund = await showConfirm({
    title: 'Hoàn tiền',
    message: `Hoàn tiền tối đa ${money(row.amount)} cho giao dịch ${row.id}?`,
  })
  if (!wantsRefund) return
  const input = window.prompt('Nhập số tiền cần hoàn', String(row.amount))
  if (!input) return
  const amount = Number(input)
  if (!Number.isFinite(amount) || amount <= 0 || amount > row.amount) {
    showToast('Số tiền không hợp lệ', 'error')
    return
  }
  try {
    await paymentService.refund(row.id, amount)
    showToast('Đã tạo yêu cầu hoàn tiền', 'success')
    fetch()
  } catch (error: any) {
    showToast(error?.message || 'Không thể hoàn tiền', 'error')
  }
}

onMounted(fetch)
</script>

<style scoped>
/* Dark Mode Base Styles */
.space-y-4 {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* KPI Cards */
.grid-cols-2 > div,
.grid-cols-4 > div,
.md\:grid-cols-4 > div {
  background: rgba(30, 41, 59, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 16px;
}

.grid-cols-2 .text-xs,
.grid-cols-4 .text-xs,
.md\:grid-cols-4 .text-xs {
  color: #94a3b8;
}

.grid-cols-2 .text-2xl,
.grid-cols-4 .text-2xl,
.md\:grid-cols-4 .text-2xl {
  color: #e2e8f0;
}

/* Table Card */
.rounded-lg.bg-white {
  background: rgba(30, 41, 59, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.text-gray-600 {
  color: #94a3b8 !important;
}

.font-medium.text-gray-800 {
  color: #e2e8f0 !important;
}

.text-gray-500 {
  color: #64748b !important;
}

/* Light Mode Overrides */
html:not(.dark) .grid-cols-2 > div,
html:not(.dark) .grid-cols-4 > div,
html:not(.dark) .md\:grid-cols-4 > div {
  background: #fff;
  border-color: #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

html:not(.dark) .grid-cols-2 .text-xs,
html:not(.dark) .grid-cols-4 .text-xs,
html:not(.dark) .md\:grid-cols-4 .text-xs {
  color: #64748b;
}

html:not(.dark) .grid-cols-2 .text-2xl,
html:not(.dark) .grid-cols-4 .text-2xl,
html:not(.dark) .md\:grid-cols-4 .text-2xl {
  color: #1e293b;
}

html:not(.dark) .rounded-lg.bg-white {
  background: #fff !important;
  border-color: #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

html:not(.dark) .text-gray-600 {
  color: #64748b !important;
}

html:not(.dark) .font-medium.text-gray-800 {
  color: #1e293b !important;
}

html:not(.dark) .text-gray-500 {
  color: #64748b !important;
}

/* Status Badges */
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-succeeded {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.status-pending {
  background: rgba(148, 163, 184, 0.15);
  color: #94a3b8;
}

.status-processing {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

.status-failed {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.status-refunded {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.status-disputed {
  background: rgba(168, 85, 247, 0.15);
  color: #a855f7;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 6px;
  justify-content: flex-end;
}

.action-btn {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid;
}

.btn-view {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.15);
  color: #e2e8f0;
}

.btn-view:hover {
  background: rgba(255, 255, 255, 0.12);
}

.btn-refund {
  background: rgba(251, 191, 36, 0.15);
  border-color: rgba(251, 191, 36, 0.3);
  color: #fbbf24;
}

.btn-refund:hover {
  background: rgba(251, 191, 36, 0.25);
}

/* Light Mode for buttons */
html:not(.dark) .btn-view {
  background: #f8fafc;
  border-color: #e2e8f0;
  color: #334155;
}

html:not(.dark) .btn-view:hover {
  background: #f1f5f9;
}

html:not(.dark) .btn-refund {
  background: rgba(251, 191, 36, 0.1);
  border-color: rgba(251, 191, 36, 0.4);
  color: #d97706;
}
</style>
