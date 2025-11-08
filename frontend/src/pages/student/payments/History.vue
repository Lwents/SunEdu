<template>
  <div class="page">
    <div class="container">
      <div class="page-header">
        <h1 class="title">Lịch sử thanh toán</h1>
        <div class="actions">
          <select v-model="status" class="filter-select">
            <option value="">Tất cả trạng thái</option>
            <option value="paid">Thành công</option>
            <option value="pending">Đang xử lý</option>
            <option value="failed">Thất bại</option>
            <option value="refunded">Hoàn tiền</option>
          </select>
          <button class="btn-light" :disabled="loading" @click="load()">
            {{ loading ? 'Đang tải...' : 'Làm mới' }}
          </button>
        </div>
      </div>

      <div class="list">
        <div v-for="item in items" :key="item.id" class="row">
          <div class="col order">
            <div class="label">Mã đơn</div>
            <div class="value">{{ item.orderId }}</div>
          </div>
          <div class="col plan">
            <div class="label">Gói</div>
            <div class="value">{{ item.plan }}</div>
          </div>
          <div class="col amount">
            <div class="label">Số tiền</div>
            <div class="value">{{ vnd(item.amount) }}</div>
          </div>
          <div class="col method">
            <div class="label">Phương thức</div>
            <div class="value">{{ item.method }}</div>
          </div>
          <div class="col date">
            <div class="label">Ngày & giờ</div>
            <div class="value">
              <div>{{ formatDate(item.date) }}</div>
              <div class="text-xs text-gray-500">{{ formatTime(item.date) }}</div>
            </div>
          </div>
          <div class="col status">
            <span :class="['badge', `badge-${mapBadge(item.status)}`]">{{ statusText(item.status) }}</span>
          </div>
        </div>

        <div v-if="!loading && !items.length" class="empty">
          Chưa có giao dịch nào.
        </div>
      </div>

      <div class="footer">
        <RouterLink class="btn-primary" to="/student/payments">Quay lại Thanh toán</RouterLink>
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

<style scoped>
.page{ background:#f6f7fb; min-height:100vh; }
.container{ max-width:1100px; margin:0 auto; padding:24px 16px 40px; }
.page-header{ display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; gap:12px; flex-wrap:wrap; }
.title{ font-size:22px; font-weight:800; }
.actions{ display:flex; gap:8px; align-items:center; }
.btn-light{ background:#fff; border:1px solid #e5e7eb; border-radius:10px; padding:8px 12px; cursor:pointer; }
.btn-primary{ background:#16a34a; color:#fff; border:1px solid #16a34a; border-radius:10px; padding:10px 16px; font-weight:800; }
.filter-select{ padding:8px 12px; border:1px solid #e5e7eb; border-radius:10px; }
.list{ background:#fff; border:1px solid #e5e7eb; border-radius:14px; }
.row{ display:grid; grid-template-columns: 2fr 2fr 1fr 1fr 1.4fr 1fr; gap:8px; padding:14px 16px; border-bottom:1px solid #f0f2f5; align-items:center; }
.row:last-child{ border-bottom:none; }
.label{ font-size:11px; color:#6b7280; }
.value{ font-weight:700; }
.badge{ display:inline-block; padding:4px 10px; border-radius:999px; font-size:12px; font-weight:700; }
.badge-success{ background:#ecfdf5; color:#10b981; }
.badge-pending{ background:#fef3c7; color:#f59e0b; }
.badge-failed{ background:#fee2e2; color:#ef4444; }
.empty{ text-align:center; color:#6b7280; padding:24px; }
.footer{ margin-top:16px; display:flex; justify-content:flex-end; }
@media (max-width: 860px){ .row{ grid-template-columns: 1fr 1fr; } }
</style>
