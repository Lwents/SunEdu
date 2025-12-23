<template>
  <div :class="isDark ? 'dark-mode' : 'light-mode'">
    <!-- Background glow effects for dark mode -->
    <div v-if="isDark" class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 -left-32 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 -right-32 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>
    </div>

    <div class="min-h-screen relative z-10">
      <div class="mx-auto max-w-4xl px-4 py-6 sm:px-6 lg:px-8">
        <!-- Header -->
        <div class="mb-8">
          <div class="flex items-center gap-3 mb-2">
            <div 
              class="w-10 h-10 rounded-lg flex items-center justify-center"
              :class="isDark ? 'bg-gradient-to-r from-cyan-500 to-purple-500' : 'bg-slate-900'"
            >
              <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
            </div>
            <h1 class="text-3xl font-bold" :class="isDark ? 'text-white' : 'text-slate-900'">Thanh toán</h1>
          </div>
          <p class="text-sm ml-13" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Chọn số tiền và phương thức thanh toán</p>
        </div>

        <!-- Step 1: Amount Selection -->
        <div 
          class="mb-8 rounded-lg border shadow-sm"
          :class="isDark 
            ? 'border-slate-700/50 bg-slate-800/50 backdrop-blur-sm' 
            : 'border-slate-200 bg-white'"
        >
          <div class="border-b px-6 py-4" :class="isDark ? 'border-slate-700' : 'border-slate-200'">
            <h2 class="text-lg font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Chọn số tiền</h2>
          </div>

          <div class="p-6 space-y-6">
            <!-- Quick Amount Buttons -->
            <div>
              <label class="block text-sm font-medium mb-3" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Chọn nhanh</label>
              <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
                <button
                  v-for="amount in quickAmounts"
                  :key="amount"
                  type="button"
                  @click="selectAmount(amount)"
                  class="px-4 py-3 rounded-lg border text-sm font-semibold transition focus:outline-none focus:ring-2"
                  :class="selectedAmount === amount
                    ? isDark 
                      ? 'border-cyan-500 bg-cyan-500 text-white'
                      : 'border-slate-900 bg-slate-900 text-white'
                    : isDark 
                      ? 'border-slate-600 bg-slate-700/50 text-white hover:border-cyan-500 hover:bg-slate-700'
                      : 'border-slate-300 bg-white text-slate-700 hover:border-slate-400 hover:bg-slate-50'"
                >
                  {{ vnd(amount) }}
                </button>
              </div>
            </div>

            <!-- Custom Amount Input -->
            <div>
              <label class="block text-sm font-medium mb-3" :class="isDark ? 'text-slate-300' : 'text-slate-700'">Hoặc nhập số tiền tùy chỉnh</label>
              <div class="relative">
                <input
                  v-model.number="customAmount"
                  type="number"
                  min="10000"
                  step="10000"
                  placeholder="Nhập số tiền (tối thiểu 10,000đ)"
                  @input="onCustomAmountInput"
                  class="w-full rounded-lg border px-4 py-3 pr-20 text-sm transition focus:outline-none focus:ring-2"
                  :class="isDark 
                    ? 'border-slate-600 bg-slate-700/50 text-white placeholder-slate-400 focus:border-cyan-500 focus:ring-cyan-500/20'
                    : 'border-slate-300 text-slate-900 focus:border-slate-400 focus:ring-slate-200'"
                />
                <span class="absolute right-4 top-1/2 -translate-y-1/2 text-sm font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-500'">đ</span>
              </div>
              <p v-if="customAmountError" class="mt-2 text-xs text-red-500">{{ customAmountError }}</p>
            </div>

            <!-- Selected Amount Display -->
            <div 
              v-if="finalAmount > 0" 
              class="rounded-lg border px-4 py-3"
              :class="isDark 
                ? 'border-slate-600 bg-slate-700/30' 
                : 'border-slate-200 bg-slate-50'"
            >
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium" :class="isDark ? 'text-slate-400' : 'text-slate-700'">Số tiền nạp:</span>
                <span class="text-xl font-bold" :class="isDark ? 'text-cyan-400' : 'text-slate-900'">{{ vnd(finalAmount) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Step 2: Payment Methods -->
        <div 
          v-if="finalAmount > 0" 
          class="mb-8 rounded-lg border shadow-sm"
          :class="isDark 
            ? 'border-slate-700/50 bg-slate-800/50 backdrop-blur-sm' 
            : 'border-slate-200 bg-white'"
        >
          <div class="border-b px-6 py-4" :class="isDark ? 'border-slate-700' : 'border-slate-200'">
            <h2 class="text-lg font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Chọn phương thức thanh toán</h2>
          </div>

          <div class="p-6 space-y-3">
            <!-- MoMo Payment Method -->
            <button
              @click="goCheckout('momo')"
              :disabled="loadingMethod === 'momo'"
              class="w-full flex items-center justify-between rounded-lg border px-4 py-3 transition focus:outline-none focus:ring-2 disabled:opacity-50 disabled:cursor-not-allowed"
              :class="isDark 
                ? 'border-slate-600 bg-slate-700/50 hover:border-cyan-500 hover:bg-slate-700 focus:ring-cyan-500/20'
                : 'border-slate-300 bg-white hover:border-slate-400 hover:bg-slate-50 focus:ring-slate-200'"
            >
              <div class="flex items-center gap-3">
                <div class="w-16 h-16 bg-white rounded-lg flex items-center justify-center p-1.5">
                  <img src="/[MOMO]_Logo_Primary_Colored.svg" alt="MoMo" class="w-full h-full object-contain" />
                </div>
                <span class="text-sm font-semibold" :class="isDark ? 'text-white' : 'text-slate-900'">Ví MoMo</span>
              </div>
              <div class="flex items-center gap-2">
                <span v-if="loadingMethod === 'momo'" class="w-4 h-4 border-2 border-t-transparent rounded-full animate-spin" :class="isDark ? 'border-slate-400' : 'border-slate-400'"></span>
                <svg class="w-5 h-5" :class="isDark ? 'text-slate-500' : 'text-slate-400'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </button>

            <!-- Bank Transfer Method (Coming Soon) -->
            <button
              disabled
              class="w-full flex items-center justify-between rounded-lg border px-4 py-3 opacity-60 cursor-not-allowed"
              :class="isDark 
                ? 'border-slate-700 bg-slate-800/50' 
                : 'border-slate-200 bg-slate-50'"
            >
              <div class="flex items-center gap-3">
                <div 
                  class="w-10 h-10 rounded-lg flex items-center justify-center"
                  :class="isDark ? 'bg-slate-700' : 'bg-slate-100'"
                >
                  <svg class="w-5 h-5" :class="isDark ? 'text-slate-400' : 'text-slate-500'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z" />
                  </svg>
                </div>
                <span class="text-sm font-semibold" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Chuyển khoản VietQR</span>
              </div>
              <span class="px-2 py-0.5 bg-amber-100 text-amber-700 text-xs font-semibold rounded">Sắp ra mắt</span>
            </button>
          </div>
        </div>

        <!-- Empty State -->
        <div 
          v-else 
          class="rounded-lg border shadow-sm p-12 text-center"
          :class="isDark 
            ? 'border-slate-700/50 bg-slate-800/50 backdrop-blur-sm' 
            : 'border-slate-200 bg-white'"
        >
          <div 
            class="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4"
            :class="isDark ? 'bg-slate-700' : 'bg-slate-100'"
          >
            <svg class="w-8 h-8" :class="isDark ? 'text-slate-500' : 'text-slate-400'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
            </svg>
          </div>
          <h3 class="text-lg font-semibold mb-2" :class="isDark ? 'text-white' : 'text-slate-900'">Chọn số tiền để tiếp tục</h3>
          <p class="text-sm" :class="isDark ? 'text-slate-400' : 'text-slate-600'">Vui lòng chọn số tiền nạp hoặc nhập số tiền tùy chỉnh</p>
        </div>

        <!-- Transaction History -->
        <div class="mt-12">
          <HistoryList ref="historyRef" :limit="5" :showHeader="true" :showViewAll="true" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showToast } from '@/utils/toast'
import { useThemeStore } from '@/store/theme.store'
import { paymentService } from '@/services/payment.service'
import HistoryList from '@/pages/student/payments/HistoryList.vue'

const router = useRouter()
const route = useRoute()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const historyRef = ref<InstanceType<typeof HistoryList> | null>(null)
const handlingMomoReturn = ref(false)

const quickAmounts = [50000, 100000, 200000, 500000, 1000000, 2000000]
const selectedAmount = ref<number | null>(null)
const customAmount = ref<number | null>(null)
const customAmountError = ref<string>('')

const finalAmount = computed(() => {
  if (selectedAmount.value !== null) return selectedAmount.value
  if (customAmount.value !== null && customAmount.value >= 10000) return customAmount.value
  return 0
})

function selectAmount(amount: number) {
  selectedAmount.value = amount
  customAmount.value = null
  customAmountError.value = ''
}

function onCustomAmountInput() {
  selectedAmount.value = null
  if (customAmount.value !== null) {
    customAmountError.value = customAmount.value < 10000 ? 'Số tiền tối thiểu là 10,000đ' : ''
  } else {
    customAmountError.value = ''
  }
}

const loadingMethod = ref<'momo' | 'bank' | ''>('')

async function goCheckout(method: 'momo' | 'bank') {
  if (loadingMethod.value) return
  if (finalAmount.value < 10000) {
    showToast('Số tiền tối thiểu là 10,000đ', 'error')
    return
  }
  loadingMethod.value = method
  try {
    const query: Record<string, string> = {
      method,
      flow: 'pay_with_method',
      amount: String(Math.round(finalAmount.value)),
    }
    await router.push({ name: 'student-payments-checkout', query })
  } catch (err: any) {
    showToast(err?.message || 'Có lỗi xảy ra', 'error')
  } finally {
    loadingMethod.value = ''
  }
}

onMounted(() => { handleMomoReturn() })
watch(() => route.fullPath, () => { handleMomoReturn() })

async function handleMomoReturn() {
  const resultCode = toQueryString(route.query.resultCode)
  const extraData = toQueryString(route.query.extraData)
  const orderId = toQueryString(route.query.orderId)
  if (!resultCode && !extraData && !orderId) return
  if (handlingMomoReturn.value) return
  handlingMomoReturn.value = true
  try {
    let paymentId: string | null = null
    if (extraData) {
      const decoded = decodeExtraData(extraData)
      if (decoded?.payment_id) paymentId = decoded.payment_id
    }
    if (!paymentId && orderId) paymentId = convertOrderIdToUuid(orderId)
    const message = toQueryString(route.query.message)
    if (paymentId) {
      await nextTick()
      try {
        const syncRes = await paymentService.syncMomoPayment(paymentId)
        if (resultCode === '0' || syncRes.status === 'paid') {
          showToast('Thanh toán MoMo thành công! Lịch sử đã được cập nhật.', 'success')
        } else {
          showToast(message || 'MoMo đang xử lý giao dịch. Vui lòng kiểm tra lại sau.', 'warning')
        }
        await historyRef.value?.reload?.()
      } catch (err: any) {
        showToast(err?.message || 'Không thể đồng bộ trạng thái giao dịch MoMo', 'error')
      }
    } else if (resultCode) {
      showToast('Không xác định được giao dịch MoMo vừa thanh toán. Vui lòng kiểm tra lịch sử.', 'warning')
    }
  } finally {
    clearMomoQuery()
    handlingMomoReturn.value = false
  }
}

function clearMomoQuery() {
  const query = { ...route.query }
  const keys = ['resultCode', 'message', 'orderId', 'requestId', 'extraData', 'signature', 'partnerCode', 'lang', 'resultcode']
  let hasChange = false
  for (const key of keys) {
    if (key in query) { delete query[key]; hasChange = true }
  }
  if (hasChange) router.replace({ path: route.path, query }).catch(() => undefined)
}

function decodeExtraData(value: string): any | null {
  try {
    const normalized = value.replace(/ /g, '+')
    if (typeof atob === 'function') return JSON.parse(atob(normalized))
  } catch (error) { console.error('Failed to decode MoMo extraData', error) }
  return null
}

function convertOrderIdToUuid(value: string): string | null {
  const hex = value.replace(/-/g, '')
  if (hex.length !== 32) return null
  return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`
}

function toQueryString(input: unknown): string | null {
  if (typeof input === 'string' && input.length) return input
  if (Array.isArray(input) && input.length) return typeof input[0] === 'string' ? input[0] : null
  return null
}

function vnd(n: number) { return n.toLocaleString('vi-VN') + 'đ' }
</script>

<style scoped>
.dark-mode {
  @apply bg-slate-950;
}
.light-mode {
  @apply bg-slate-50;
}
</style>
