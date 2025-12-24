<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div class="min-w-0">
          <div class="flex items-center gap-2">
            <h2 class="truncate text-xl font-semibold text-gray-800">{{ tx.id }}</h2>
            <el-tag :type="statusTagType(tx.status)" size="small">{{ tx.status }}</el-tag>
          </div>
          <div class="mt-1 text-sm text-gray-600">
            {{ tx.courseTitle }} • {{ tx.gateway }} • {{ fmt(tx.createdAt) }}
          </div>
          <div class="mt-1 text-xs text-gray-500" v-if="tx.reference">Ref: {{ tx.reference }}</div>
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <el-button type="warning" plain v-if="tx.status === 'Succeeded'" @click="promptRefund"
            >Hoàn tiền</el-button
          >
        </div>
      </div>
    </div>

    <!-- Top cards -->
    <div class="grid grid-cols-2 gap-3 md:grid-cols-4">
      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="text-xs text-gray-500">Số tiền</div>
        <div class="mt-2 text-2xl font-semibold">{{ money(tx.amount) }}</div>
      </div>
      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="text-xs text-gray-500">Phí</div>
        <div class="mt-2 text-2xl font-semibold">{{ money(tx.fees) }}</div>
      </div>
      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="text-xs text-gray-500">Net</div>
        <div class="mt-2 text-2xl font-semibold">{{ money(tx.net) }}</div>
      </div>
      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="text-xs text-gray-500">Cập nhật</div>
        <div class="mt-2 text-2xl font-semibold">{{ fmt(tx.settledAt) || '—' }}</div>
      </div>
    </div>

    <!-- Main -->
    <div class="grid grid-cols-1 gap-4 md:grid-cols-3">
      <!-- Timeline -->
      <div class="md:col-span-2 rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="mb-3 font-semibold">Dòng thời gian</div>
        <ul class="space-y-4">
          <li v-for="(e, idx) in tx.events" :key="idx" class="flex items-start gap-3">
            <div class="mt-1 h-2 w-2 shrink-0 rounded-full bg-gray-400"></div>
            <div>
              <div class="font-medium text-gray-800">{{ eventLabel(e.type) }}</div>
              <div class="text-sm text-gray-600">{{ e.description }}</div>
              <div class="text-xs text-gray-500">{{ fmt(e.time) }}</div>
            </div>
          </li>
        </ul>
      </div>

      <!-- Sidebar info -->
      <div class="space-y-4">
        <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
          <div class="mb-2 font-semibold">Người mua</div>
          <div class="text-gray-800">{{ tx.buyerName }}</div>
          <div class="text-sm text-gray-500">{{ tx.buyerEmail }}</div>
        </div>

        <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
          <div class="mb-2 font-semibold">Khoá học</div>
          <div class="text-gray-800">{{ tx.courseTitle }}</div>
          <div class="text-sm text-gray-500">Mã: {{ tx.courseId }}</div>
        </div>

        <div class="rounded-lg bg-white p-4 ring-1 ring-black/5 space-y-1">
          <div class="font-semibold">Phương thức</div>
          <div class="text-sm text-gray-700">
            Cổng: <b>{{ tx.gateway }}</b>
          </div>
          <div v-if="tx.cardBrand" class="text-sm text-gray-700">
            Thẻ: {{ tx.cardBrand }} **** {{ tx.cardLast4 }}
          </div>
          <div v-if="tx.bankCode" class="text-sm text-gray-700">Ngân hàng: {{ tx.bankCode }}</div>
        </div>

        <div v-if="tx.tags?.length" class="rounded-lg bg-white p-4 ring-1 ring-black/5">
          <div class="mb-2 font-semibold">Nhãn</div>
          <div class="flex flex-wrap gap-2">
            <el-tag v-for="t in tx.tags" :key="t" size="small">{{ t }}</el-tag>
          </div>
        </div>
      </div>
    </div>

    <!-- Dialogs -->
    <el-dialog v-model="refundDialog" title="Hoàn tiền" width="420px">
      <div class="space-y-3">
        <el-input v-model="refundAmount" placeholder="Số tiền" />
        <el-input v-model="refundReason" placeholder="Lý do (tuỳ chọn)" />
      </div>
      <template #footer>
        <el-button @click="refundDialog = false">Huỷ</el-button>
        <el-button type="primary" :loading="doing.refund" @click="doRefund">Xác nhận</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { paymentService, type TxDetail, type TxStatus } from '@/services/payment.service'
import { showToast } from '@/utils/toast'

const route = useRoute()
const id = computed(() => route.params.id as string)

const tx = reactive<TxDetail>({
  id: id.value,
  userId: 0,
  buyerName: '',
  buyerEmail: '',
  courseId: 0,
  courseTitle: '',
  amount: 0,
  currency: 'VND',
  gateway: 'VNPay',
  status: 'Pending',
  createdAt: new Date().toISOString(),
  fees: 0,
  net: 0,
  events: [],
})

const refundDialog = ref(false)
const refundAmount = ref('')
const refundReason = ref('')
const doing = reactive({ refund: false })

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
const eventLabel = (t: TxDetail['events'][number]['type']) =>
  t === 'created'
    ? 'Tạo giao dịch'
    : t === 'authorized'
      ? 'Uỷ quyền'
      : t === 'captured'
        ? 'Thu tiền'
        : t === 'succeeded'
          ? 'Thành công'
          : t === 'failed'
            ? 'Thất bại'
            : t === 'refunded'
              ? 'Hoàn tiền'
              : t === 'dispute_opened'
                ? 'Mở tranh chấp'
                : t === 'dispute_won'
                  ? 'Tranh chấp: Thắng'
                  : 'Tranh chấp: Thua'

async function load() {
  try {
  const d = await paymentService.detail(id.value)
  Object.assign(tx, d)
  } catch (error: any) {
    showToast(error?.message || 'Không tải được giao dịch', 'error')
  }
}

function promptRefund() {
  refundAmount.value = String(tx.amount)
  refundReason.value = ''
  refundDialog.value = true
}
async function doRefund() {
  doing.refund = true
  try {
    await paymentService.refund(tx.id, Number(refundAmount.value), refundReason.value)
    showToast('Đã tạo yêu cầu hoàn tiền', 'success')
    refundDialog.value = false
    load()
  } catch (error: any) {
    showToast(error?.message || 'Không thể hoàn tiền', 'error')
  } finally {
    doing.refund = false
  }
}

onMounted(load)
watch(() => route.params.id, load)
</script>
