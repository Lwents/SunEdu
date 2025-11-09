<template>
  <div class="pay-page">
    <div class="container">
      <h1 class="title">Thanh toán</h1>

      <div class="grid">
        <section class="card momo-card">
          <h2 class="section-title">Thanh toán qua MoMo</h2>
          <p class="muted">
            Chọn gói và bấm nút bên dưới, bạn sẽ được chuyển đến cổng MoMo Collection Link để hoàn tất.
          </p>

          <div class="field">
            <span class="label">Nội dung hiển thị khi thanh toán</span>
            <input
              v-model="descriptionText"
              class="input"
              placeholder="Ví dụ: Thanh toán học phí tháng 11"
            />
            <small class="muted">Dòng mô tả sẽ xuất hiện trên màn hình xác nhận của MoMo.</small>
          </div>

          <div class="field">
            <span class="label">Số tiền (VND)</span>
            <input
              v-model="amountText"
              @input="onAmountInput(true)"
              class="input right"
              inputmode="numeric"
              placeholder="Nhập số tiền, ví dụ 215000"
            />
            <small class="muted">
              <template v-if="selectedPlanId">
                Số tiền được cố định từ gói {{ plan }}
              </template>
              <template v-else>
                Chỉ nhập chữ số. Bạn có thể đặt số tiền tuỳ ý.
              </template>
            </small>
          </div>

          <div class="pill">
            <div>
              <small class="muted">Số tiền thanh toán</small>
              <div class="pill-amount">{{ vnd(amountNumber) }}</div>
            </div>
            <div>
              <small class="muted">Gói</small>
              <div class="pill-plan">{{ planDisplay }}</div>
            </div>
          </div>

          <h3 class="sub-title">Các bước thực hiện</h3>
          <ul class="steps">
            <li>Mở app MoMo hoặc chọn liên kết thanh toán được chuyển tới.</li>
            <li>Kiểm tra thông tin đơn hàng, số tiền và xác nhận thanh toán.</li>
            <li>Sau khi hoàn tất, hệ thống sẽ tự đồng bộ trạng thái.</li>
          </ul>

          <button
            class="btn-primary wide"
            :class="{ 'is-busy': isMomoLoading }"
            :disabled="!amountNumber"
            @click="payWithMomo"
          >
            <span v-if="isMomoLoading" class="spinner"></span>
            {{ isMomoLoading ? 'Đang chuyển hướng...' : 'Thanh toán với MoMo' }}
          </button>
          <small class="muted">
            Bạn sẽ được chuyển đến trang thanh toán an toàn của MoMo.
          </small>
        </section>

        <section class="card summary-card">
          <h2 class="section-title">Tóm tắt</h2>
          <div class="summary">
            <div class="line"><span>Gói</span><b>{{ planDisplay }}</b></div>
            <div class="line" v-if="planDuration"><span>Thời hạn</span><b>{{ planDuration }} ngày</b></div>
            <div class="line"><span>Thành tiền</span><b>{{ vnd(amountNumber) }}</b></div>
            <div class="line"><span>Phí nền tảng</span><b>0đ</b></div>
            <div class="divider"></div>
            <div class="line total"><span>Tổng thanh toán</span><b>{{ vnd(amountNumber) }}</b></div>
          </div>

          <div v-if="planFeatures.length" class="feature-list">
            <h3>Quyền lợi gói</h3>
            <ul>
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

import { paymentService, type SubscriptionPlan, type MomoInitPayload } from '@/services/payment.service'

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
const descriptionText = ref(typeof route.query.description === 'string' ? route.query.description : '')
const description = computed(() => descriptionText.value || `Thanh toán ${plan.value}`)
const planDisplay = computed(() => plan.value || 'Thanh toán tuỳ chỉnh')

const selectedPlan = computed(() =>
  plans.value.find((item) => item.id === selectedPlanId.value) || null
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

<style>
:root{
  --bg:#f6f7fb; --card:#fff; --text:#0f172a; --muted:#6b7280; --line:#e5e7eb;
  --accent:#16a34a; --focus-border:#86efac; --focus-ring:rgba(22,163,74,.18);
}
</style>

<style scoped>
.pay-page{ background:var(--bg); min-height:100vh; color:var(--text); }
.container{ max-width:1100px; margin:0 auto; padding:24px 16px 40px; }
.title{ font-size:22px; font-weight:800; margin-bottom:12px; }

.grid{ display:grid; grid-template-columns: 2fr 1fr; gap:16px; }
.card{ background:#fff; border:1px solid var(--line); border-radius:14px; padding:16px; }
.section-title{ font-size:16px; font-weight:800; margin-bottom:8px; }
.muted{ color:var(--muted); font-size:14px; }

.momo-card .field{ margin-top:12px; }
.field{ display:grid; gap:6px; margin-bottom:10px; }
.label{ font-size:12px; color:var(--muted); }
.input{ width:100%; padding:10px 12px; border:1px solid var(--line); border-radius:10px; outline:none; transition:all .2s ease; }
.input:focus{ border-color:var(--focus-border); box-shadow:0 0 0 3px var(--focus-ring); }
.input.right{ text-align:right; }
.select{ appearance:none; background-image: linear-gradient(45deg, transparent 50%, #9ca3af 50%), linear-gradient(135deg, #9ca3af 50%, transparent 50%); background-position: calc(100% - 18px) calc(1em + 2px), calc(100% - 13px) calc(1em + 2px); background-size: 5px 5px; background-repeat:no-repeat; }

.pill{
  margin:16px 0;
  border:1px solid var(--line);
  border-radius:14px;
  padding:12px 16px;
  display:flex;
  justify-content:space-between;
  gap:12px;
}
.pill-amount{ font-size:20px; font-weight:800; }
.pill-plan{ font-weight:700; }

.sub-title{ margin:14px 0 6px; font-weight:700; }
.steps{ margin:0 0 12px; padding-left:18px; color:var(--muted); }
.steps li{ margin:4px 0; }

.btn-primary{
  background:var(--accent); color:#fff; border:1px solid var(--accent);
  padding:10px 16px; border-radius:10px; font-weight:800; cursor:pointer;
  display:inline-flex; align-items:center; gap:8px; transition:all .2s ease;
}
.btn-primary.wide{ width:100%; justify-content:center; }
.btn-primary:not([disabled]):hover{ filter:brightness(1.08); transform:translateY(-1px); }
.btn-primary[disabled]{ opacity:.7; cursor:not-allowed; }
.btn-outline, .btn-light{
  border:1px solid var(--line); border-radius:10px; padding:8px 12px; font-weight:700; cursor:pointer;
  background:#fff;
}
.btn-light{ background:#f9fafb; }
.spinner{ width:16px; height:16px; border:2px solid rgba(255,255,255,.6); border-top-color:#fff; border-radius:50%; animation:spin .8s linear infinite; }
@keyframes spin{ to{ transform:rotate(360deg); } }

.summary-card .summary{ display:grid; gap:10px; }
.line{ display:flex; justify-content:space-between; font-size:14px; }
.line.total b{ font-size:18px; }
.divider{ height:1px; background:var(--line); margin:6px 0; }
.feature-list{ margin-top:14px; }
.feature-list h3{ margin-bottom:6px; font-size:14px; }
.feature-list ul{ margin:0; padding-left:18px; color:var(--muted); font-size:13px; }

@media (max-width: 980px){
  .grid{ grid-template-columns: 1fr; }
}
</style>
