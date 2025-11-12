<template>
  <section>
    <div
      v-if="showHeader"
      class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6"
    >
      <div class="flex items-center gap-3">
        <div
          class="w-8 h-8 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-lg flex items-center justify-center"
        >
          <svg class="w-5 h-5 text-white" viewBox="0 0 24 24" fill="currentColor">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>
        <h2 class="text-2xl sm:text-3xl font-black text-slate-900">Lịch sử thanh toán</h2>
      </div>
      <div class="flex items-center gap-3">
        <select
          v-model="status"
          class="px-4 py-3 bg-white border-2 border-slate-200 rounded-xl font-semibold text-slate-700 cursor-pointer"
        >
          <option value="">Tất cả trạng thái</option>
          <option value="paid">✓ Thành công</option>
          <option value="pending">⌛ Đang xử lý</option>
          <option value="failed">✕ Thất bại</option>
          <option value="refunded">↺ Hoàn tiền</option>
        </select>
        <RouterLink
          v-if="showViewAll"
          class="px-4 py-3 bg-white border-2 border-slate-200 rounded-xl font-extrabold text-slate-700 hover:border-purple-500 hover:text-purple-700 transition"
          to="/student/payments/history"
          >Xem tất cả</RouterLink
        >
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5 mb-6">
      <div class="bg-white/90 border-2 border-white shadow-xl rounded-2xl p-5">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600" viewBox="0 0 20 20" fill="currentColor">
              <path
                d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z"
              />
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-2xl sm:text-3xl font-black text-slate-900 mb-0.5 truncate">
              {{ vnd(totalPaid) }}
            </div>
            <div class="text-xs sm:text-sm text-slate-600 font-medium">Tổng thanh toán</div>
          </div>
        </div>
      </div>
      <div class="bg-white/90 border-2 border-white shadow-xl rounded-2xl p-5">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-amber-600" viewBox="0 0 20 20" fill="currentColor">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-2xl sm:text-3xl font-black text-slate-900 mb-0.5">
              {{ pendingCount }}
            </div>
            <div class="text-xs sm:text-sm text-slate-600 font-medium">Đang xử lý</div>
          </div>
        </div>
      </div>
      <div class="bg-white/90 border-2 border-white shadow-xl rounded-2xl p-5">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-indigo-600" viewBox="0 0 20 20" fill="currentColor">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-2xl sm:text-3xl font-black text-slate-900 mb-0.5">
              {{ successCount }}
            </div>
            <div class="text-xs sm:text-sm text-slate-600 font-medium">Giao dịch thành công</div>
          </div>
        </div>
      </div>
      <div class="bg-white/90 border-2 border-white shadow-xl rounded-2xl p-5">
        <div class="flex items-center gap-4">
          <div class="w-12 h-12 bg-rose-100 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-rose-600" viewBox="0 0 20 20" fill="currentColor">
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3-9a1 1 0 00-1-1H8a1 1 0 100 2h1v3a1 1 0 102 0v-3h1a1 1 0 001-1zm-3-4a1 1 0 100 2 1 1 0 000-2z"
                clip-rule="evenodd"
              />
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-2xl sm:text-3xl font-black text-slate-900 mb-0.5">
              {{ failedCount }}
            </div>
            <div class="text-xs sm:text-sm text-slate-600 font-medium">Thất bại</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white/90 border-2 border-white shadow-xl rounded-2xl overflow-hidden">
      <div v-if="rows.length > 0" class="overflow-x-auto">
        <div class="history-scroll" :style="{ maxHeight: props.scrollHeight }">
          <table class="w-full">
            <thead class="bg-gradient-to-r from-slate-50 to-slate-100">
              <tr>
                <th
                  class="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider"
                >
                  Mã đơn
                </th>
                <th
                  class="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider"
                >
                  Gói học
                </th>
                <th
                  class="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider"
                >
                  Số tiền
                </th>
                <th
                  class="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider"
                >
                  Phương thức
                </th>
                <th
                  class="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider"
                >
                  Ngày & giờ
                </th>
                <th
                  class="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider"
                >
                  Trạng thái
                </th>
                <th class="px-6 py-4"></th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="it in rows" :key="it.id" class="hover:bg-slate-50/70 transition">
                <td class="px-6 py-4 font-bold text-slate-800 truncate max-w-[220px]">
                  {{ it.orderId }}
                </td>
                <td class="px-6 py-4 text-slate-700 whitespace-nowrap">{{ it.plan }}</td>
                <td class="px-6 py-4 font-extrabold text-green-600 whitespace-nowrap">
                  {{ vnd(it.amount) }}
                </td>
                <td class="px-6 py-4 text-slate-700 flex items-center gap-2 whitespace-nowrap">
                  <span
                    class="inline-flex items-center gap-1.5 px-2 py-1 rounded-lg bg-slate-100 text-slate-700 text-xs font-bold"
                  >
                    <svg class="w-4 h-4" viewBox="0 0 20 20" fill="currentColor">
                      <path
                        d="M11 17a1 1 0 001 1h3a1 1 0 001-1V7a1 1 0 00-1-1h-3a1 1 0 00-1 1v10zM4 17a1 1 0 001 1h3a1 1 0 001-1V3a1 1 0 00-1-1H5a1 1 0 00-1 1v14z"
                      />
                    </svg>
                    {{ it.method }}
                  </span>
                </td>
                <td class="px-6 py-4 text-slate-700 whitespace-nowrap">
                  <div class="font-semibold">{{ formatDate(it.date) }}</div>
                  <div class="text-xs text-slate-500">{{ formatTime(it.date) }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    :class="[
                      'inline-flex items-center gap-1.5 px-2 py-1 rounded-full text-xs font-extrabold',
                      it.status === 'success'
                        ? 'bg-emerald-100 text-emerald-700'
                        : it.status === 'pending'
                          ? 'bg-amber-100 text-amber-700'
                          : 'bg-rose-100 text-rose-700',
                    ]"
                  >
                    <span
                      class="w-2 h-2 rounded-full"
                      :class="
                        it.status === 'success'
                          ? 'bg-emerald-500'
                          : it.status === 'pending'
                            ? 'bg-amber-500'
                            : 'bg-rose-500'
                      "
                    ></span>
                    {{ statusText(it.status) }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <button
                    @click="refresh(it)"
                    class="inline-flex items-center justify-center w-9 h-9 rounded-xl border border-slate-200 hover:border-slate-300 text-slate-600 hover:text-slate-800"
                    title="Cập nhật trạng thái"
                  >
                    <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor">
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
      </div>
      <div v-else class="p-6 text-center text-slate-600">
        Lịch sử thanh toán của bạn sẽ hiển thị ở đây
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

<style scoped>
.history-scroll {
  overflow-y: auto;
}

.history-scroll::-webkit-scrollbar {
  width: 8px;
}

.history-scroll::-webkit-scrollbar-thumb {
  background-color: rgba(148, 163, 184, 0.6);
  border-radius: 999px;
}

.history-scroll::-webkit-scrollbar-track {
  background-color: transparent;
}
</style>
