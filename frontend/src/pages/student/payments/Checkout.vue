<template>
  <div class="min-h-screen bg-slate-50 pb-16 pt-8">
    <div class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-slate-900 mb-2">Nạp tiền</h1>
        <p class="text-slate-600">Hoàn tất thanh toán để nạp tiền vào tài khoản</p>
      </div>

      <div class="grid gap-6 lg:grid-cols-[1fr_400px]">
        <!-- Main Form -->
        <section class="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <h2 class="text-lg font-semibold text-slate-900 mb-4">Nạp tiền qua MoMo</h2>
          <p class="text-sm text-slate-600 mb-6">
            Chọn gói và bấm nút bên dưới, bạn sẽ được chuyển đến cổng MoMo Collection Link để hoàn tất.
          </p>

          <div class="space-y-6">
            <!-- Description Input -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">
                Nội dung hiển thị khi nạp tiền
              </label>
              <input
                v-model="descriptionText"
                placeholder="Ví dụ: Nạp học phí tháng 11"
                class="w-full rounded-lg border border-slate-300 px-4 py-2.5 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
              />
              <p class="mt-1.5 text-xs text-slate-500">
                Dòng mô tả sẽ xuất hiện trên màn hình xác nhận của MoMo.
              </p>
            </div>

            <!-- Amount Input -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">
                Số tiền (VND)
              </label>
              <input
                v-model="amountText"
                @input="onAmountInput(true)"
                inputmode="numeric"
                placeholder="Nhập số tiền, ví dụ 215000"
                class="w-full rounded-lg border border-slate-300 px-4 py-2.5 text-right text-lg font-semibold text-slate-900 focus:outline-none focus:ring-2 focus:ring-slate-200 focus:border-slate-400"
              />
              <p class="mt-1.5 text-xs text-slate-500">
                <template v-if="selectedPlanId"> Số tiền được cố định từ gói {{ plan }}. </template>
                <template v-else> Chỉ nhập chữ số. Bạn có thể đặt số tiền tuỳ ý. </template>
              </p>
            </div>

            <!-- Summary Display -->
            <div class="rounded-lg border border-slate-200 bg-slate-50 p-4">
              <div class="flex items-center justify-between mb-3">
                <span class="text-sm font-medium text-slate-600">Số tiền nạp</span>
                <span class="text-xl font-bold text-slate-900">{{ vnd(amountNumber) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm font-medium text-slate-600">Gói</span>
                <span class="text-sm font-semibold text-slate-900">{{ planDisplay }}</span>
              </div>
            </div>

            <!-- Steps -->
            <div>
              <h3 class="text-sm font-semibold text-slate-700 mb-3">Các bước thực hiện</h3>
              <ol class="list-decimal space-y-2 pl-5 text-sm text-slate-600">
                <li>Mở app MoMo hoặc chọn liên kết nạp tiền được chuyển tới.</li>
                <li>Kiểm tra thông tin đơn hàng, số tiền và xác nhận nạp tiền.</li>
                <li>Sau khi hoàn tất, hệ thống sẽ tự đồng bộ trạng thái.</li>
              </ol>
            </div>

            <!-- Submit Button -->
            <div>
              <button
                type="button"
                class="w-full rounded-lg bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
                :disabled="!amountNumber || isMomoLoading"
                @click="payWithMomo"
              >
                <span v-if="isMomoLoading" class="inline-flex items-center gap-2">
                  <span class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                  Đang chuyển hướng...
                </span>
                <span v-else>Nạp tiền với MoMo</span>
              </button>
              <p class="mt-2 text-xs text-slate-500 text-center">
                Bạn sẽ được chuyển đến trang nạp tiền an toàn của MoMo.
              </p>
            </div>
          </div>
        </section>

        <!-- Summary Sidebar -->
        <section class="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-slate-900">Tóm tắt</h2>
            <button
              type="button"
              class="text-sm font-medium text-slate-600 hover:text-slate-900 transition disabled:opacity-50"
              :disabled="planLoading"
              @click="loadPlans"
            >
              {{ planLoading ? 'Đang tải...' : 'Làm mới' }}
            </button>
          </div>

          <div class="space-y-3 rounded-lg border border-slate-200 bg-slate-50 p-4">
            <div class="flex items-center justify-between text-sm">
              <span class="text-slate-600">Gói</span>
              <span class="font-semibold text-slate-900">{{ planDisplay }}</span>
            </div>
            <div v-if="planDuration" class="flex items-center justify-between text-sm">
              <span class="text-slate-600">Thời hạn</span>
              <span class="font-semibold text-slate-900">{{ planDuration }} ngày</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-slate-600">Thành tiền</span>
              <span class="font-semibold text-slate-900">{{ vnd(amountNumber) }}</span>
            </div>
            <div class="flex items-center justify-between text-sm">
              <span class="text-slate-600">Phí nền tảng</span>
              <span class="font-semibold text-slate-900">0đ</span>
            </div>
            <div class="border-t border-slate-200 pt-3 mt-3">
              <div class="flex items-center justify-between">
                <span class="text-base font-semibold text-slate-900">Tổng nạp</span>
                <span class="text-lg font-bold text-slate-900">{{ vnd(amountNumber) }}</span>
              </div>
            </div>
          </div>

          <div v-if="planFeatures.length" class="mt-6 rounded-lg border border-amber-200 bg-amber-50 p-4">
            <h3 class="text-sm font-semibold text-amber-900 mb-2">Quyền lợi gói</h3>
            <ul class="list-disc space-y-1 pl-5 text-sm text-amber-800">
              <li v-for="(feature, idx) in planFeatures" :key="idx">{{ feature }}</li>
            </ul>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { showToast } from '@/utils/toast'

import {
  paymentService,
  type SubscriptionPlan,
  type MomoInitPayload,
} from '@/services/payment.service'

const route = useRoute()

const plans = ref<SubscriptionPlan[]>([])
const planLoading = ref(false)
const selectedPlanId = ref(typeof route.query.planId === 'string' ? route.query.planId : '')
const fallbackPlanLabel = ref(String(route.query.plan || 'Nạp tiền tuỳ chỉnh'))
const plan = ref(fallbackPlanLabel.value)

const amountText = ref(String(route.query.amount || '0'))
const amountNumber = computed(() => {
  const digits = amountText.value.replace(/[^\d]/g, '')
  return digits ? parseInt(digits, 10) : 0
})
const descriptionText = ref(
  typeof route.query.description === 'string' ? route.query.description : '',
)
const description = computed(() => descriptionText.value || `Nạp tiền ${plan.value}`)
const planDisplay = computed(() => plan.value || 'Nạp tiền tuỳ chỉnh')

const selectedPlan = computed(
  () => plans.value.find((item) => item.id === selectedPlanId.value) || null,
)
const planDuration = computed(() => selectedPlan.value?.durationDays ?? null)
const planFeatures = computed(() => selectedPlan.value?.features ?? [])

async function loadPlans() {
  planLoading.value = true
  try {
    const data = await paymentService.listPlans()
    plans.value = data
    if (!selectedPlanId.value && data.length) {
      selectedPlanId.value = data[0].id
    } else {
      syncPlanWithSelection()
    }
  } catch (err) {
    console.error(err)
  } finally {
    planLoading.value = false
    if (!plans.value.length) {
      syncPlanWithSelection()
    }
  }
}

function syncPlanWithSelection() {
  if (selectedPlanId.value) {
    const found = plans.value.find((p) => p.id === selectedPlanId.value)
    if (found) {
      fallbackPlanLabel.value = found.name
      plan.value = found.name
      amountText.value = String(Math.round(found.price))
    } else if (!planLoading.value) {
      selectedPlanId.value = ''
      return
    }
  } else {
    plan.value = fallbackPlanLabel.value || 'Nạp tiền tuỳ chỉnh'
  }
}

watch(selectedPlanId, () => {
  syncPlanWithSelection()
})

onMounted(() => {
  loadPlans()
})

const isMomoLoading = ref(false)
async function payWithMomo() {
  if (!amountNumber.value) {
    showToast('Vui lòng nhập số tiền hợp lệ', 'warning')
    return
  }
  isMomoLoading.value = true
  try {
    const payload: MomoInitPayload = {
      description: description.value,
    }
    if (selectedPlanId.value) payload.planId = selectedPlanId.value
    else payload.amount = amountNumber.value
    payload.flow = 'pay_with_method'

    const res = await paymentService.initiateMomo(payload)
    showToast('Đang chuyển đến MoMo...', 'success')
    const target = res.payUrl || res.deeplink || res.qrCodeUrl
    if (target) window.location.href = target
  } catch (err: any) {
    showToast(err?.message || 'Không khởi tạo được yêu cầu nạp MoMo', 'error')
  } finally {
    isMomoLoading.value = false
  }
}

function vnd(n: number) {
  return n.toLocaleString('vi-VN') + 'đ'
}

function onAmountInput(manual = false) {
  amountText.value = amountText.value.replace(/[^\d]/g, '')
  if (manual) {
    selectedPlanId.value = ''
    fallbackPlanLabel.value = 'Nạp tiền tuỳ chỉnh'
    plan.value = fallbackPlanLabel.value
  }
}
</script>
