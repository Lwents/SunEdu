<template>
  <div class="min-h-screen bg-slate-50 pb-16 pt-8">
    <div class="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
      <div class="flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <p class="text-sm font-semibold uppercase tracking-[0.3em] text-emerald-500">Checkout</p>
          <h1 class="text-3xl font-black text-slate-900 sm:text-4xl">Thanh toán</h1>
        </div>
        <button
          type="button"
          class="inline-flex items-center gap-2 rounded-2xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm shadow-slate-100 transition hover:border-emerald-300"
          @click="loadPlans"
          :disabled="planLoading"
        >
          <span
            v-if="planLoading"
            class="h-4 w-4 animate-spin rounded-full border-2 border-slate-300 border-t-emerald-500"
          ></span>
          <svg
            v-else
            class="h-4 w-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            />
          </svg>
          <span>{{ planLoading ? 'Đang tải...' : 'Làm mới gói' }}</span>
        </button>
      </div>

      <div class="mt-8 grid gap-6 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
        <section
          class="rounded-3xl border border-slate-200/80 bg-white/95 p-6 shadow-xl shadow-slate-100"
        >
          <h2 class="text-lg font-bold text-slate-900">Thanh toán qua MoMo</h2>
          <p class="mt-2 text-sm text-slate-500">
            Chọn gói và bấm nút bên dưới, bạn sẽ được chuyển đến cổng MoMo Collection Link để hoàn
            tất.
          </p>

          <div class="mt-6 space-y-6">
            <div class="space-y-2">
              <label class="text-xs font-semibold uppercase tracking-wide text-slate-500">
                Nội dung hiển thị khi thanh toán
              </label>
              <input
                v-model="descriptionText"
                placeholder="Ví dụ: Thanh toán học phí tháng 11"
                class="w-full rounded-2xl border border-slate-200 px-4 py-3 text-sm text-slate-900 shadow-sm shadow-slate-100 transition focus:border-emerald-500 focus-visible:outline-none focus:ring-4 focus:ring-emerald-100"
              />
              <p class="text-xs text-slate-500">
                Dòng mô tả sẽ xuất hiện trên màn hình xác nhận của MoMo.
              </p>
            </div>

            <div class="space-y-2">
              <label class="text-xs font-semibold uppercase tracking-wide text-slate-500">
                Số tiền (VND)
              </label>
              <input
                v-model="amountText"
                @input="onAmountInput(true)"
                inputmode="numeric"
                placeholder="Nhập số tiền, ví dụ 215000"
                class="w-full rounded-2xl border border-slate-200 px-4 py-3 text-right text-lg font-bold text-slate-900 shadow-sm shadow-slate-100 transition focus:border-emerald-500 focus-visible:outline-none focus:ring-4 focus:ring-emerald-100"
              />
              <p class="text-xs text-slate-500">
                <template v-if="selectedPlanId"> Số tiền được cố định từ gói {{ plan }}. </template>
                <template v-else> Chỉ nhập chữ số. Bạn có thể đặt số tiền tuỳ ý. </template>
              </p>
            </div>

            <div
              class="flex flex-col gap-4 rounded-2xl border border-slate-200 bg-slate-50/60 p-4 sm:flex-row sm:items-center sm:justify-between"
            >
              <div>
                <p class="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Số tiền thanh toán
                </p>
                <p class="text-2xl font-black text-slate-900">{{ vnd(amountNumber) }}</p>
              </div>
              <div>
                <p class="text-xs font-semibold uppercase tracking-wide text-slate-500">Gói</p>
                <p class="text-sm font-semibold text-slate-900">{{ planDisplay }}</p>
              </div>
            </div>

            <div>
              <h3 class="text-sm font-bold uppercase tracking-wide text-slate-500">
                Các bước thực hiện
              </h3>
              <ol class="mt-3 list-decimal space-y-2 pl-5 text-sm text-slate-600">
                <li>Mở app MoMo hoặc chọn liên kết thanh toán được chuyển tới.</li>
                <li>Kiểm tra thông tin đơn hàng, số tiền và xác nhận thanh toán.</li>
                <li>Sau khi hoàn tất, hệ thống sẽ tự đồng bộ trạng thái.</li>
              </ol>
            </div>

            <div class="space-y-2">
              <button
                type="button"
                class="inline-flex w-full items-center justify-center gap-2 rounded-2xl border border-transparent bg-emerald-500 px-4 py-3 text-sm font-extrabold uppercase tracking-wide text-white shadow-lg shadow-emerald-200 transition hover:bg-emerald-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-600 disabled:cursor-not-allowed disabled:border-slate-200 disabled:bg-slate-200 disabled:text-slate-500"
                :disabled="!amountNumber"
                @click="payWithMomo"
              >
                <span
                  v-if="isMomoLoading"
                  class="h-4 w-4 animate-spin rounded-full border-2 border-white/60 border-t-white"
                ></span>
                {{ isMomoLoading ? 'Đang chuyển hướng...' : 'Thanh toán với MoMo' }}
              </button>
              <p class="text-xs text-slate-500">
                Bạn sẽ được chuyển đến trang thanh toán an toàn của MoMo.
              </p>
            </div>
          </div>
        </section>

        <section
          class="rounded-3xl border border-slate-200/80 bg-white/95 p-6 shadow-xl shadow-slate-100"
        >
          <h2 class="text-lg font-bold text-slate-900">Tóm tắt</h2>
          <div class="mt-4 space-y-4 rounded-2xl border border-slate-100 bg-slate-50/60 p-4">
            <div class="flex items-center justify-between text-sm text-slate-600">
              <span>Gói</span>
              <b class="text-slate-900">{{ planDisplay }}</b>
            </div>
            <div
              class="flex items-center justify-between text-sm text-slate-600"
              v-if="planDuration"
            >
              <span>Thời hạn</span>
              <b class="text-slate-900">{{ planDuration }} ngày</b>
            </div>
            <div class="flex items-center justify-between text-sm text-slate-600">
              <span>Thành tiền</span>
              <b class="text-slate-900">{{ vnd(amountNumber) }}</b>
            </div>
            <div class="flex items-center justify-between text-sm text-slate-600">
              <span>Phí nền tảng</span>
              <b class="text-slate-900">0đ</b>
            </div>
            <div class="h-px bg-slate-200"></div>
            <div class="flex items-center justify-between text-base font-black text-slate-900">
              <span>Tổng thanh toán</span>
              <b>{{ vnd(amountNumber) }}</b>
            </div>
          </div>

          <div
            v-if="planFeatures.length"
            class="mt-6 rounded-2xl border border-emerald-100 bg-emerald-50/40 p-4"
          >
            <h3 class="text-sm font-bold text-emerald-800">Quyền lợi gói</h3>
            <ul class="mt-3 list-disc space-y-1 pl-5 text-sm text-emerald-700">
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
import { ElMessage } from 'element-plus'

import {
  paymentService,
  type SubscriptionPlan,
  type MomoInitPayload,
} from '@/services/payment.service'

const route = useRoute()

const plans = ref<SubscriptionPlan[]>([])
const planLoading = ref(false)
const selectedPlanId = ref(typeof route.query.planId === 'string' ? route.query.planId : '')
const fallbackPlanLabel = ref(String(route.query.plan || 'Thanh toán tuỳ chỉnh'))
const plan = ref(fallbackPlanLabel.value)

const amountText = ref(String(route.query.amount || '0'))
const amountNumber = computed(() => {
  const digits = amountText.value.replace(/[^\d]/g, '')
  return digits ? parseInt(digits, 10) : 0
})
const descriptionText = ref(
  typeof route.query.description === 'string' ? route.query.description : '',
)
const description = computed(() => descriptionText.value || `Thanh toán ${plan.value}`)
const planDisplay = computed(() => plan.value || 'Thanh toán tuỳ chỉnh')

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
    plan.value = fallbackPlanLabel.value || 'Thanh toán tuỳ chỉnh'
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
    ElMessage.warning('Vui lòng nhập số tiền hợp lệ')
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
    ElMessage.success('Đang chuyển đến MoMo...')
    const target = res.payUrl || res.deeplink || res.qrCodeUrl
    if (target) window.location.href = target
  } catch (err: any) {
    ElMessage.error(err?.message || 'Không khởi tạo được thanh toán MoMo')
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
    fallbackPlanLabel.value = 'Thanh toán tuỳ chỉnh'
    plan.value = fallbackPlanLabel.value
  }
}
</script>
