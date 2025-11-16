<template>
  <section>
    <div
      v-if="showHeader"
      class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6"
    >
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 bg-slate-900 rounded-lg flex items-center justify-center">
          <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <h2 class="text-xl font-semibold text-slate-900">Lịch sử nạp tiền</h2>
      </div>
      <div class="flex items-center gap-3">
        <select
          v-model="status"
          class="px-3 py-2 bg-white border border-slate-300 rounded-lg text-sm font-medium text-slate-700 cursor-pointer focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
        >
          <option value="">Tất cả trạng thái</option>
          <option value="paid">Thành công</option>
          <option value="pending">Đang xử lý</option>
          <option value="failed">Thất bại</option>
          <option value="refunded">Hoàn tiền</option>
        </select>
        <RouterLink
          v-if="showViewAll"
          class="px-4 py-2 bg-white border border-slate-300 rounded-lg text-sm font-semibold text-slate-700 hover:border-slate-400 hover:bg-slate-50 transition"
          to="/student/payments/history"
          >Xem tất cả</RouterLink
        >
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <div class="rounded-lg border border-slate-200 bg-white p-4">
        <div class="text-xs text-slate-500 mb-1">Tổng nạp</div>
        <div class="text-xl font-bold text-slate-900">{{ vnd(totalPaid) }}</div>
      </div>
      <div class="rounded-lg border border-slate-200 bg-white p-4">
        <div class="text-xs text-slate-500 mb-1">Đang xử lý</div>
        <div class="text-xl font-bold text-slate-900">{{ pendingCount }}</div>
      </div>
      <div class="rounded-lg border border-slate-200 bg-white p-4">
        <div class="text-xs text-slate-500 mb-1">Thành công</div>
        <div class="text-xl font-bold text-slate-900">{{ successCount }}</div>
      </div>
      <div class="rounded-lg border border-slate-200 bg-white p-4">
        <div class="text-xs text-slate-500 mb-1">Thất bại</div>
        <div class="text-xl font-bold text-slate-900">{{ failedCount }}</div>
      </div>
    </div>

    <!-- Table -->
    <div class="rounded-lg border border-slate-200 bg-white shadow-sm overflow-hidden">
      <div v-if="rows.length > 0" class="overflow-x-auto">
        <table class="w-full min-w-[1000px]">
          <thead class="bg-slate-50">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider w-[200px]">
                Mã đơn
              </th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider min-w-[180px]">
                Gói học
              </th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider w-[120px]">
                Số tiền
              </th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider w-[140px]">
                Phương thức
              </th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider w-[160px]">
                Ngày & giờ
              </th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-slate-700 uppercase tracking-wider w-[120px]">
                Trạng thái
              </th>
              <th class="px-4 py-3 text-center text-xs font-semibold text-slate-700 uppercase tracking-wider w-[100px]">
                Thao tác
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-100 bg-white">
            <tr v-for="it in rows" :key="it.id" class="hover:bg-slate-50 transition">
              <td class="px-4 py-3">
                <span class="text-xs font-mono text-slate-600 break-all">{{ it.orderId }}</span>
              </td>
              <td class="px-4 py-3 text-sm text-slate-700 whitespace-nowrap">{{ it.plan }}</td>
              <td class="px-4 py-3">
                <span class="text-sm font-semibold text-slate-900">{{ vnd(it.amount) }}</span>
              </td>
              <td class="px-4 py-3">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-slate-100 text-slate-700 text-xs font-medium whitespace-nowrap">
                  <svg class="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
                    <path
                      d="M11 17a1 1 0 001 1h3a1 1 0 001-1V7a1 1 0 00-1-1h-3a1 1 0 00-1 1v10zM4 17a1 1 0 001 1h3a1 1 0 001-1V3a1 1 0 00-1-1H5a1 1 0 00-1 1v14z"
                    />
                  </svg>
                  {{ it.method }}
                </span>
              </td>
              <td class="px-4 py-3">
                <div class="text-sm text-slate-700 whitespace-nowrap">{{ formatDate(it.date) }}</div>
                <div class="text-xs text-slate-500 mt-0.5 whitespace-nowrap">{{ formatTime(it.date) }}</div>
              </td>
              <td class="px-4 py-3">
                <span
                  :class="[
                    'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium whitespace-nowrap',
                    it.status === 'success'
                      ? 'bg-green-100 text-green-700'
                      : it.status === 'pending'
                        ? 'bg-amber-100 text-amber-700'
                        : 'bg-red-100 text-red-700',
                  ]"
                >
                  <span
                    class="w-1.5 h-1.5 rounded-full"
                    :class="
                      it.status === 'success'
                        ? 'bg-green-500'
                        : it.status === 'pending'
                          ? 'bg-amber-500'
                          : 'bg-red-500'
                    "
                  ></span>
                  {{ statusText(it.status) }}
                </span>
              </td>
              <td class="px-4 py-3 text-center">
                <button
                  @click="refresh(it)"
                  class="inline-flex items-center justify-center w-8 h-8 rounded-lg border border-slate-300 hover:border-slate-400 hover:bg-slate-50 text-slate-600 transition"
                  title="Cập nhật trạng thái"
                >
                  <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M4 4v6h6M20 20v-6h-6M20 8a8 8 0 00-15.5 2M4 16a8 8 0 0015.5 2"
                    />
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else class="p-12 text-center">
        <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
            />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-slate-900 mb-2">Chưa có giao dịch nào</h3>
        <p class="text-sm text-slate-600">Lịch sử nạp tiền của bạn sẽ hiển thị ở đây</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch, computed } from 'vue'
import { paymentService } from '@/services/payment.service'

const props = defineProps({
  limit: { type: Number, required: false },
  showHeader: { type: Boolean, default: true },
  showViewAll: { type: Boolean, default: false },
  autoRefresh: { type: Boolean, default: true },
  refreshInterval: { type: Number, default: 15000 },
  autoSyncPending: { type: Boolean, default: true },
  scrollHeight: { type: String, default: '24rem' },
})
const showHeader = computed(() => props.showHeader !== false)
const showViewAll = computed(() => !!props.showViewAll)

type Row = {
  id: string
  orderId: string
  plan: string
  amount: number
  method: string
  date: string
  status: 'success' | 'pending' | 'failed'
}
const rows = ref<Row[]>([])
const summary = ref({ totalAmount: 0, pendingCount: 0, successCount: 0, failedCount: 0 })
const status = ref<string>('')
const isSyncing = ref(false)
const syncedIds = new Set<string>()
let refreshTimer: ReturnType<typeof setInterval> | null = null

const totalPaid = computed(() => summary.value.totalAmount)
const pendingCount = computed(() => summary.value.pendingCount)
const successCount = computed(() => summary.value.successCount)
const failedCount = computed(() => summary.value.failedCount)

async function load(options?: { skipAutoSync?: boolean }) {
  const { items, summary: fetchedSummary } = await paymentService.listMyPayments(
    status.value ? { status: status.value as any } : undefined,
  )
  const max = typeof props.limit === 'number' ? Math.max(0, props.limit) : undefined
  rows.value = max ? (items as Row[]).slice(0, max) : (items as Row[])
  summary.value = fetchedSummary
  if (!options?.skipAutoSync) {
    await autoSyncPending()
  }
}

onMounted(() => {
  load()
  setupAutoRefresh()
})

watch(status, () => load())
watch(() => props.autoRefresh, setupAutoRefresh)

function setupAutoRefresh() {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
  if (props.autoRefresh) {
    refreshTimer = setInterval(
      () => {
        load()
      },
      Math.max(props.refreshInterval, 5000),
    )
  }
}

onUnmounted(() => {
  if (refreshTimer) clearInterval(refreshTimer)
})

function vnd(n: number) {
  return n.toLocaleString('vi-VN') + 'đ'
}
function formatDate(s: string) {
  const d = new Date(s)
  return d.toLocaleDateString('vi-VN')
}
function formatTime(s: string) {
  const d = new Date(s)
  return d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}
function statusText(st: string) {
  return ({ success: 'Thành công', pending: 'Đang xử lý', failed: 'Thất bại' } as any)[st] || st
}

async function refresh(it: Row) {
  try {
    await paymentService.syncMomoPayment(it.id)
    syncedIds.add(it.id)
    await load({ skipAutoSync: true })
  } catch (e) {
    console.error(e)
  }
}

async function autoSyncPending() {
  if (!props.autoSyncPending || isSyncing.value) return
  const pending = rows.value.filter((r) => r.status === 'pending' && !syncedIds.has(r.id))
  if (!pending.length) return
  isSyncing.value = true
  try {
    for (const row of pending) {
      try {
        await paymentService.syncMomoPayment(row.id)
        syncedIds.add(row.id)
      } catch (err) {
        console.error('Failed to sync payment', row.id, err)
      }
    }
    await load({ skipAutoSync: true })
  } finally {
    isSyncing.value = false
  }
}
</script>

