<template>
  <div class="min-h-screen bg-slate-50">
    <div class="mx-auto max-w-4xl px-4 py-6 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-10 h-10 bg-slate-900 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"
              />
            </svg>
          </div>
          <h1 class="text-3xl font-bold text-slate-900">Nạp tiền</h1>
        </div>
        <p class="text-slate-600 text-sm ml-13">Chọn số tiền và phương thức thanh toán</p>
      </div>

      <!-- Step 1: Amount Selection -->
      <div class="mb-8 rounded-lg border border-slate-200 bg-white shadow-sm">
        <div class="border-b border-slate-200 px-6 py-4">
          <h2 class="text-lg font-semibold text-slate-900">Chọn số tiền</h2>
        </div>

        <div class="p-6 space-y-6">
          <!-- Quick Amount Buttons -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">Chọn nhanh</label>
            <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3">
              <button
                v-for="amount in quickAmounts"
                :key="amount"
                type="button"
                @click="selectAmount(amount)"
                :class="[
                  'px-4 py-3 rounded-lg border text-sm font-semibold transition focus:outline-none focus:ring-2 focus:ring-slate-200',
                  selectedAmount === amount
                    ? 'border-slate-900 bg-slate-900 text-white'
                    : 'border-slate-300 bg-white text-slate-700 hover:border-slate-400 hover:bg-slate-50'
                ]"
              >
                {{ vnd(amount) }}
              </button>
            </div>
          </div>

          <!-- Custom Amount Input -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-3">Hoặc nhập số tiền tùy chỉnh</label>
            <div class="relative">
              <input
                v-model.number="customAmount"
                type="number"
                min="10000"
                step="10000"
                placeholder="Nhập số tiền (tối thiểu 10,000đ)"
                @input="onCustomAmountInput"
                class="w-full rounded-lg border border-slate-300 px-4 py-3 pr-20 text-sm text-slate-900 transition focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
              />
              <span class="absolute right-4 top-1/2 -translate-y-1/2 text-sm font-medium text-slate-500">đ</span>
            </div>
            <p v-if="customAmountError" class="mt-2 text-xs text-red-600">{{ customAmountError }}</p>
          </div>

          <!-- Selected Amount Display -->
          <div v-if="finalAmount > 0" class="rounded-lg border border-slate-200 bg-slate-50 px-4 py-3">
            <div class="flex items-center justify-between">
              <span class="text-sm font-medium text-slate-700">Số tiền nạp:</span>
              <span class="text-xl font-bold text-slate-900">{{ vnd(finalAmount) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 2: Payment Methods (only show if amount selected) -->
      <div v-if="finalAmount > 0" class="mb-8 rounded-lg border border-slate-200 bg-white shadow-sm">
        <div class="border-b border-slate-200 px-6 py-4">
          <h2 class="text-lg font-semibold text-slate-900">Chọn phương thức thanh toán</h2>
        </div>

        <div class="p-6 space-y-3">
          <!-- MoMo Payment Method -->
          <button
            @click="goCheckout('momo')"
            :disabled="loadingMethod === 'momo'"
            class="w-full flex items-center justify-between rounded-lg border border-slate-300 bg-white px-4 py-3 hover:border-slate-400 hover:bg-slate-50 transition focus:outline-none focus:ring-2 focus:ring-slate-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-cyan-50 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-cyan-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M21 12a2.25 2.25 0 00-2.25-2.25H15a3 3 0 11-6 0H5.25A2.25 2.25 0 003 12m18 0v6a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 18v-6m18 0V9M3 12V9m18 0a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 9m18 0V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v3"
                  />
                </svg>
              </div>
              <span class="text-sm font-semibold text-slate-900">Ví MoMo</span>
            </div>
            <div class="flex items-center gap-2">
              <span
                v-if="loadingMethod === 'momo'"
                class="w-4 h-4 border-2 border-slate-400 border-t-transparent rounded-full animate-spin"
              ></span>
              <svg class="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </button>

          <!-- Bank Transfer Method (Coming Soon) -->
          <button
            disabled
            class="w-full flex items-center justify-between rounded-lg border border-slate-200 bg-slate-50 px-4 py-3 opacity-60 cursor-not-allowed"
          >
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"
                  />
                </svg>
              </div>
              <span class="text-sm font-semibold text-slate-600">Chuyển khoản VietQR</span>
            </div>
            <span class="px-2 py-0.5 bg-amber-100 text-amber-700 text-xs font-semibold rounded">Sắp ra mắt</span>
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="rounded-lg border border-slate-200 bg-white shadow-sm p-12 text-center">
        <div class="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"
            />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-slate-900 mb-2">Chọn số tiền để tiếp tục</h3>
        <p class="text-sm text-slate-600">Vui lòng chọn số tiền nạp hoặc nhập số tiền tùy chỉnh</p>
      </div>

      <!-- Transaction History -->
      <div class="mt-12">
        <HistoryList :limit="5" :showHeader="true" :showViewAll="true" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from '@/utils/toast'
import { paymentService } from '@/services/payment.service'
import HistoryList from '@/pages/student/payments/HistoryList.vue'

const router = useRouter()

// Quick amount options
const quickAmounts = [50000, 100000, 200000, 500000, 1000000, 2000000]

// Amount selection
const selectedAmount = ref<number | null>(null)
const customAmount = ref<number | null>(null)
const customAmountError = ref<string>('')

const finalAmount = computed(() => {
  if (selectedAmount.value !== null) {
    return selectedAmount.value
  }
  if (customAmount.value !== null && customAmount.value >= 10000) {
    return customAmount.value
  }
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
    if (customAmount.value < 10000) {
      customAmountError.value = 'Số tiền tối thiểu là 10,000đ'
    } else {
      customAmountError.value = ''
    }
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
    await router.push({
      name: 'student-payments-checkout',
      query,
    })
  } catch (err: any) {
    showToast(err?.message || 'Có lỗi xảy ra', 'error')
  } finally {
    loadingMethod.value = ''
  }
}

function vnd(n: number) {
  return n.toLocaleString('vi-VN') + 'đ'
}
</script>
