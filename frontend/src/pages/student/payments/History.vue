<template>
  <div class="min-h-screen bg-slate-50">
    <div class="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 bg-slate-900 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <h1 class="text-3xl font-bold text-slate-900">Lịch sử nạp tiền</h1>
        </div>
        <p class="text-slate-600">Xem tất cả các giao dịch nạp tiền của bạn</p>
      </div>

      <!-- Filters -->
      <div class="mb-6 flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
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
          <button
            type="button"
            class="px-4 py-2 bg-white border border-slate-300 rounded-lg text-sm font-medium text-slate-700 hover:bg-slate-50 transition disabled:opacity-50"
            :disabled="loading"
            @click="load()"
          >
            {{ loading ? 'Đang tải...' : 'Làm mới' }}
          </button>
        </div>
        <RouterLink
          to="/student/payments"
          class="inline-flex items-center gap-2 px-4 py-2 bg-slate-900 text-white rounded-lg text-sm font-semibold hover:bg-slate-800 transition"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Quay lại nạp tiền
        </RouterLink>
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
        <div v-if="items.length > 0" class="overflow-x-auto">
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
              <tr v-for="item in items" :key="item.id" class="hover:bg-slate-50 transition">
                <td class="px-4 py-3">
                  <span class="text-xs font-mono text-slate-600 break-all">{{ item.orderId }}</span>
                </td>
                <td class="px-4 py-3 text-sm text-slate-700 whitespace-nowrap">{{ item.plan }}</td>
                <td class="px-4 py-3">
                  <span class="text-sm font-semibold text-slate-900">{{ vnd(item.amount) }}</span>
                </td>
                <td class="px-4 py-3">
                  <span class="inline-flex items-center gap-1.5 px-2 py-1 rounded-lg bg-slate-100 text-slate-700 text-xs font-medium whitespace-nowrap">
                    <svg class="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
                      <path
                        d="M11 17a1 1 0 001 1h3a1 1 0 001-1V7a1 1 0 00-1-1h-3a1 1 0 00-1 1v10zM4 17a1 1 0 001 1h3a1 1 0 001-1V3a1 1 0 00-1-1H5a1 1 0 00-1 1v14z"
                      />
                    </svg>
                    {{ item.method }}
                  </span>
                </td>
                <td class="px-4 py-3">
                  <div class="text-sm text-slate-700 whitespace-nowrap">{{ formatDate(item.date) }}</div>
                  <div class="text-xs text-slate-500 mt-0.5 whitespace-nowrap">{{ formatTime(item.date) }}</div>
                </td>
                <td class="px-4 py-3">
                  <span
                    :class="[
                      'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium whitespace-nowrap',
                      item.status === 'success'
                        ? 'bg-green-100 text-green-700'
                        : item.status === 'pending'
                          ? 'bg-amber-100 text-amber-700'
                          : 'bg-red-100 text-red-700',
                    ]"
                  >
                    <span
                      class="w-1.5 h-1.5 rounded-full"
                      :class="
                        item.status === 'success'
                          ? 'bg-green-500'
                          : item.status === 'pending'
                            ? 'bg-amber-500'
                            : 'bg-red-500'
                      "
                    ></span>
                    {{ statusText(item.status) }}
                  </span>
                </td>
                <td class="px-4 py-3 text-center">
                  <button
                    @click="refresh(item)"
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
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter } from 'vue-router'
import { paymentService } from '@/services/payment.service'
import { showToast } from '@/utils/toast'

type Item = {
  id: string
  orderId: string
  plan: string
  amount: number
  method: string
  date: string
  status: 'success' | 'pending' | 'failed'
}

const router = useRouter()
const items = ref<Item[]>([])
const loading = ref(false)
const status = ref<string>('')

const totalPaid = computed(() =>
  items.value.filter((t) => t.status === 'success').reduce((s, t) => s + t.amount, 0),
)
const pendingCount = computed(() => items.value.filter((t) => t.status === 'pending').length)
const successCount = computed(() => items.value.filter((t) => t.status === 'success').length)
const failedCount = computed(() => items.value.filter((t) => t.status === 'failed').length)

async function load() {
  loading.value = true
  try {
    const { items: data } = await paymentService.listMyPayments(
      status.value ? { status: status.value as any } : undefined,
    )
    items.value = (data as unknown as Item[]) || []
  } catch (e: any) {
    showToast(e?.message || 'Không tải được lịch sử', 'error')
    items.value = []
  } finally {
    loading.value = false
  }
}

async function refresh(item: Item) {
  try {
    await paymentService.syncMomoPayment(item.id)
    await load()
    showToast('Đã cập nhật trạng thái', 'success')
  } catch (e: any) {
    showToast(e?.message || 'Không thể cập nhật', 'error')
  }
}

onMounted(load)
watch(status, load)

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
</script>
