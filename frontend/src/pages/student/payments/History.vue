<template>
  <div class="student-shell">
    <div class="student-container">
      <div class="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p class="student-section-title">Thanh toán</p>
          <h1 class="text-3xl font-black text-gray-900 dark:text-gray-100">Lịch sử thanh toán</h1>
        </div>
        <div class="flex flex-col gap-2 sm:flex-row sm:items-center">
          <select
            v-model="status"
            class="rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-gray-900 dark:text-gray-100 shadow-sm shadow-slate-100 focus:border-cyan-500 dark:border-cyan-600 focus:outline-none focus:ring-4 focus:ring-cyan-500/30"
          >
            <option value="">Tất cả trạng thái</option>
            <option value="paid">Thành công</option>
            <option value="pending">Đang xử lý</option>
            <option value="failed">Thất bại</option>
            <option value="refunded">Hoàn tiền</option>
          </select>
          <button
            type="button"
            class="rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-gray-600 dark:text-gray-400 shadow-sm shadow-slate-100 transition hover:bg-slate-50 disabled:opacity-60"
            :disabled="loading"
            @click="load()"
          >
            {{ loading ? 'Đang tải...' : 'Làm mới' }}
          </button>
        </div>
      </div>

      <div class="student-card divide-y divide-slate-100 p-0">
        <div
          v-for="item in items"
          :key="item.id"
          class="grid gap-4 px-5 py-5 sm:grid-cols-[1.2fr,1.2fr,1fr,1fr,1.4fr,1fr]"
        >
          <div>
            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-gray-600 dark:text-gray-400">Mã đơn</p>
            <p class="text-sm font-bold text-gray-900 dark:text-gray-100">{{ item.orderId }}</p>
          </div>
          <div>
            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-gray-600 dark:text-gray-400">Gói</p>
            <p class="text-sm font-semibold text-gray-900 dark:text-gray-100">{{ item.plan }}</p>
          </div>
          <div>
            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-gray-600 dark:text-gray-400">Số tiền</p>
            <p class="text-sm font-semibold text-gray-900 dark:text-gray-100">{{ vnd(item.amount) }}</p>
          </div>
          <div>
            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-gray-600 dark:text-gray-400">Phương thức</p>
            <p class="text-sm font-semibold text-gray-900 dark:text-gray-100">{{ item.method }}</p>
          </div>
          <div>
            <p class="text-xs font-semibold uppercase tracking-[0.2em] text-gray-600 dark:text-gray-400">Ngày & giờ</p>
            <p class="text-sm font-semibold text-gray-900 dark:text-gray-100">{{ formatDate(item.date) }}</p>
            <p class="text-xs font-medium text-gray-600 dark:text-gray-400">{{ formatTime(item.date) }}</p>
          </div>
          <div class="flex items-center">
            <span
              :class="[
                'student-badge',
                mapBadge(item.status) === 'success'
                  ? 'student-badge--success'
                  : mapBadge(item.status) === 'pending'
                    ? 'bg-amber-50 text-amber-700'
                    : 'bg-rose-50 text-rose-600',
              ]"
            >
              {{ statusText(item.status) }}
            </span>
          </div>
        </div>

        <div v-if="!loading && !items.length" class="px-6 py-10 text-center text-sm text-gray-600 dark:text-gray-400">
          Chưa có giao dịch nào.
        </div>
      </div>

      <div class="mt-6 flex justify-end">
        <RouterLink
          class="inline-flex items-center justify-center rounded-2xl border border-transparent bg-cyan-50 dark:bg-cyan-900/200 px-5 py-3 text-sm font-extrabold uppercase tracking-wide text-white shadow-lg shadow-ocean-glow transition hover:bg-cyan-600"
          to="/student/payments"
        >
          Quay lại Thanh toán
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { paymentService } from '@/services/payment.service'

type Item = { id: string; orderId: string; plan: string; amount: number; method: string; date: string; status: 'success'|'pending'|'failed' }

const items = ref<Item[]>([])
const loading = ref(false)
const status = ref<string>('')

async function load(){
  loading.value = true
  try{
    const { items: data } = await paymentService.listMyPayments({ status: status.value as any })
    items.value = data as unknown as Item[]
  } finally { loading.value = false }
}

onMounted(load)
watch(status, load)

function vnd(n:number){ return n.toLocaleString('vi-VN') + 'đ' }
function formatDate(s:string){ const d = new Date(s); return d.toLocaleDateString('vi-VN') }
function formatTime(s:string){ const d = new Date(s); return d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit', second: '2-digit' }) }
function statusText(st:string){ return ({ success:'Thành công', pending:'Đang xử lý', failed:'Thất bại' } as any)[st] || st }
function mapBadge(st:string){ return st === 'success' ? 'success' : st }
</script>
