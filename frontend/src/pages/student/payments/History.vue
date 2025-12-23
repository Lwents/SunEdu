<template>
  <div class="page-wrapper" :class="isDark ? 'dark-mode' : 'light-mode'">
    <!-- Background Elements -->
    <div v-if="isDark" class="bg-elements">
      <div class="glow glow-1"></div>
      <div class="glow glow-2"></div>
    </div>

    <div class="page-content">
      <!-- Header -->
      <div class="page-header">
        <div class="header-icon">
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <h1>Lịch sử thanh toán</h1>
          <p>Xem tất cả các giao dịch thanh toán của bạn</p>
        </div>
      </div>

      <!-- Filters -->
      <div class="filter-bar">
        <div class="custom-select" :class="{ open: selectOpen }">
          <button type="button" class="select-trigger" @click="selectOpen = !selectOpen">
            <span>{{ statusLabel }}</span>
            <svg class="select-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M6 9l6 6 6-6"/>
            </svg>
          </button>
          <div v-if="selectOpen" class="select-dropdown">
            <button 
              v-for="opt in statusOptions" 
              :key="opt.value" 
              type="button"
              class="select-option" 
              :class="{ active: status === opt.value }"
              @click="status = opt.value; selectOpen = false"
            >{{ opt.label }}</button>
          </div>
        </div>
        <button type="button" class="btn-refresh" :disabled="loading" @click="load()">
          {{ loading ? 'Đang tải...' : 'Làm mới' }}
        </button>
      </div>

      <!-- Stats -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-label">Tổng thanh toán</div>
          <div class="stat-value">{{ vnd(totalPaid) }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Đang xử lý</div>
          <div class="stat-value">{{ pendingCount }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Thành công</div>
          <div class="stat-value stat-success">{{ successCount }}</div>
        </div>
        <div class="stat-card">
          <div class="stat-label">Thất bại</div>
          <div class="stat-value stat-failed">{{ failedCount }}</div>
        </div>
      </div>

      <!-- Table -->
      <div class="table-card">
        <div v-if="items.length > 0" class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>Mã đơn</th>
                <th>Gói học</th>
                <th>Số tiền</th>
                <th>Phương thức</th>
                <th>Ngày & giờ</th>
                <th>Trạng thái</th>
                <th class="text-center">Thao tác</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in items" :key="item.id">
                <td><span class="order-id">{{ item.orderId }}</span></td>
                <td class="plan-name">{{ item.plan }}</td>
                <td class="amount">{{ vnd(item.amount) }}</td>
                <td><span class="method-badge">{{ item.method }}</span></td>
                <td>
                  <div class="date-text">{{ formatDate(item.date) }}</div>
                  <div class="time-text">{{ formatTime(item.date) }}</div>
                </td>
                <td>
                  <span class="status-badge" :class="'status-' + item.status">
                    <span class="status-dot"></span>
                    {{ statusText(item.status) }}
                  </span>
                </td>
                <td class="text-center">
                  <button @click="refresh(item)" class="btn-action" title="Cập nhật trạng thái">
                    <svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v6h6M20 20v-6h-6M20 8a8 8 0 00-15.5 2M4 16a8 8 0 0015.5 2" />
                    </svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="empty-state">
          <div class="empty-icon">📋</div>
          <h3>Chưa có giao dịch nào</h3>
          <p>Lịch sử nạp tiền của bạn sẽ hiển thị ở đây</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { paymentService } from '@/services/payment.service'
import { showToast } from '@/utils/toast'
import { courseService } from '@/services/course.service'
import { useThemeStore } from '@/store/theme.store'

type Item = { id: string; orderId: string; plan: string; amount: number; method: string; date: string; status: 'success' | 'pending' | 'failed' }

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const items = ref<Item[]>([])
const loading = ref(false)
const status = ref<string>('')
const selectOpen = ref(false)

const statusOptions = [
  { value: '', label: 'Tất cả trạng thái' },
  { value: 'paid', label: 'Thành công' },
  { value: 'pending', label: 'Đang xử lý' },
  { value: 'failed', label: 'Thất bại' },
  { value: 'refunded', label: 'Hoàn tiền' }
]

const statusLabel = computed(() => statusOptions.find(o => o.value === status.value)?.label || 'Tất cả trạng thái')

const totalPaid = computed(() => items.value.filter((t) => t.status === 'success').reduce((s, t) => s + t.amount, 0))
const pendingCount = computed(() => items.value.filter((t) => t.status === 'pending').length)
const successCount = computed(() => items.value.filter((t) => t.status === 'success').length)
const failedCount = computed(() => items.value.filter((t) => t.status === 'failed').length)

const refreshTimer = ref<ReturnType<typeof setInterval> | null>(null)
const route = useRoute()
const router = useRouter()

async function load() {
  loading.value = true
  try {
    const { items: data } = await paymentService.listMyPayments(status.value ? { status: status.value as any } : undefined)
    items.value = (data as unknown as Item[]) || []
    if (pendingCount.value > 0) startAutoRefresh()
    else stopAutoRefresh()
  } catch (e: any) {
    showToast(e?.message || 'Không tải được lịch sử', 'error')
    items.value = []
  } finally { loading.value = false }
}

async function refresh(item: Item) {
  try {
    await paymentService.syncMomoPayment(item.id)
    await load()
    showToast('Đã cập nhật trạng thái', 'success')
  } catch (e: any) { showToast(e?.message || 'Không thể cập nhật', 'error') }
}

async function enrollCoursesFromCart() {
  const pendingEnroll = localStorage.getItem('pending_cart_enroll')
  if (!pendingEnroll) return
  try {
    const courseIds = JSON.parse(pendingEnroll) as (string | number)[]
    if (!Array.isArray(courseIds) || courseIds.length === 0) { localStorage.removeItem('pending_cart_enroll'); return }
    const results = await Promise.all(courseIds.map((id) => courseService.enroll(id).catch((err) => { console.error('Enroll failed for', id, err); return { success: false } })))
    const ok = results.filter((r: any) => r?.success !== false).length
    if (ok > 0) { showToast(`Đã kích hoạt ${ok} khóa học vào "Khóa học của tôi"`, 'success'); localStorage.removeItem('pending_cart_enroll'); await load() }
  } catch (e) { console.error('Error enroll from cart', e) }
}

async function handlePaymentReturn() {
  const resultCode = route.query.resultCode
  const statusQuery = route.query.status
  if (!resultCode && !statusQuery) return
  try {
    const paymentId = (route.query.orderId as string) || undefined
    if (paymentId) await paymentService.syncMomoPayment(paymentId).catch(() => {})
  } catch (e) { console.warn('Sync payment error', e) }
  if (resultCode === '0' || statusQuery === 'paid' || statusQuery === 'success') await enrollCoursesFromCart()
  const clean = { ...route.query }
  delete clean.resultCode; delete clean.status; delete clean.orderId; delete clean.partnerCode; delete clean.extraData; delete clean.requestId; delete clean.message
  if (Object.keys(clean).length !== Object.keys(route.query).length) router.replace({ query: clean })
}

onMounted(async () => { await load(); await handlePaymentReturn() })
onUnmounted(() => stopAutoRefresh())
watch(status, load)
watch(pendingCount, (val) => { if (val > 0) startAutoRefresh() })

function startAutoRefresh() { if (refreshTimer.value) return; refreshTimer.value = setInterval(() => { load() }, 5000) }
function stopAutoRefresh() { if (refreshTimer.value) { clearInterval(refreshTimer.value); refreshTimer.value = null } }
function vnd(n: number) { return n.toLocaleString('vi-VN') + 'đ' }
function formatDate(s: string) { const d = new Date(s); return d.toLocaleDateString('vi-VN') }
function formatTime(s: string) { const d = new Date(s); return d.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit', second: '2-digit' }) }
function statusText(st: string) { return ({ success: 'Thành công', pending: 'Đang xử lý', failed: 'Thất bại' } as any)[st] || st }
</script>

<style scoped>
.page-wrapper { min-height: 100vh; position: relative; transition: background-color 0.3s ease; }
.page-wrapper.dark-mode { background: #020617; }
.page-wrapper.light-mode { background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%); }

.bg-elements { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.glow { position: absolute; border-radius: 50%; filter: blur(100px); }
.glow-1 { top: 10%; left: -5%; width: 300px; height: 300px; background: rgba(6, 182, 212, 0.1); }
.glow-2 { bottom: 10%; right: -5%; width: 250px; height: 250px; background: rgba(139, 92, 246, 0.1); }

.page-content { position: relative; z-index: 10; max-width: 1200px; margin: 0 auto; padding: 32px 24px; }

.page-header { display: flex; align-items: center; gap: 16px; margin-bottom: 32px; }
.header-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
.dark-mode .header-icon { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; }
.light-mode .header-icon { background: #1e293b; color: white; }
.page-header h1 { font-size: 28px; font-weight: 700; margin: 0; }
.dark-mode .page-header h1 { color: white; }
.light-mode .page-header h1 { color: #1e293b; }
.page-header p { font-size: 14px; margin: 4px 0 0; }
.dark-mode .page-header p { color: #64748b; }
.light-mode .page-header p { color: #64748b; }

.filter-bar { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; margin-bottom: 24px; }

/* Custom Select */
.custom-select { position: relative; min-width: 180px; }
.select-trigger { display: flex; align-items: center; justify-content: space-between; gap: 8px; width: 100%; padding: 10px 14px; border-radius: 10px; font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.2s; }
.dark-mode .select-trigger { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: white; }
.light-mode .select-trigger { background: white; border: 1px solid #e2e8f0; color: #1e293b; }
.select-trigger:hover { }
.dark-mode .select-trigger:hover { border-color: rgba(255,255,255,0.2); }
.light-mode .select-trigger:hover { border-color: #cbd5e1; }
.custom-select.open .select-trigger { }
.dark-mode .custom-select.open .select-trigger { border-color: #06b6d4; }
.light-mode .custom-select.open .select-trigger { border-color: #6366f1; }
.select-arrow { width: 16px; height: 16px; transition: transform 0.2s; }
.custom-select.open .select-arrow { transform: rotate(180deg); }

.select-dropdown { position: absolute; top: calc(100% + 4px); left: 0; right: 0; border-radius: 10px; overflow: hidden; z-index: 50; }
.dark-mode .select-dropdown { background: #1e293b; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 10px 40px rgba(0,0,0,0.3); }
.light-mode .select-dropdown { background: white; border: 1px solid #e2e8f0; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }

.select-option { display: block; width: 100%; padding: 10px 14px; font-size: 14px; text-align: left; cursor: pointer; transition: all 0.2s; border: none; }
.dark-mode .select-option { background: transparent; color: #94a3b8; }
.light-mode .select-option { background: transparent; color: #64748b; }
.select-option:hover { }
.dark-mode .select-option:hover { background: rgba(6,182,212,0.1); color: #22d3ee; }
.light-mode .select-option:hover { background: #f1f5f9; color: #1e293b; }
.select-option.active { }
.dark-mode .select-option.active { background: rgba(6,182,212,0.15); color: #22d3ee; }
.light-mode .select-option.active { background: #eef2ff; color: #6366f1; }

.filter-select { padding: 10px 16px; border-radius: 10px; font-size: 14px; font-weight: 500; cursor: pointer; outline: none; }
.btn-refresh { padding: 10px 16px; border-radius: 10px; font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.3s; }
.dark-mode .btn-refresh { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .btn-refresh { background: white; border: 1px solid #e2e8f0; color: #64748b; }
.btn-refresh:hover { }
.dark-mode .btn-refresh:hover { border-color: #06b6d4; color: #06b6d4; }
.light-mode .btn-refresh:hover { border-color: #6366f1; color: #6366f1; }
.btn-refresh:disabled { opacity: 0.5; cursor: not-allowed; }

.stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 24px; }
@media (min-width: 1024px) { .stats-grid { grid-template-columns: repeat(4, 1fr); } }
.stat-card { padding: 16px; border-radius: 12px; }
.dark-mode .stat-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .stat-card { background: white; border: 1px solid #e2e8f0; }
.stat-label { font-size: 12px; margin-bottom: 4px; }
.dark-mode .stat-label { color: #64748b; }
.light-mode .stat-label { color: #64748b; }
.stat-value { font-size: 20px; font-weight: 700; }
.dark-mode .stat-value { color: white; }
.light-mode .stat-value { color: #1e293b; }
.stat-success { color: #22c55e !important; }
.stat-failed { color: #ef4444 !important; }

.table-card { border-radius: 16px; overflow: hidden; }
.dark-mode .table-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .table-card { background: white; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }

.table-wrapper { overflow-x: auto; }
.data-table { width: 100%; min-width: 900px; border-collapse: collapse; font-size: 14px; }
.data-table thead { }
.dark-mode .data-table thead { background: rgba(255,255,255,0.03); }
.light-mode .data-table thead { background: #f8fafc; }
.data-table th { padding: 12px 16px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; text-align: left; }
.dark-mode .data-table th { color: #64748b; }
.light-mode .data-table th { color: #64748b; }
.data-table tbody tr { transition: background 0.3s; }
.dark-mode .data-table tbody tr { border-top: 1px solid rgba(255,255,255,0.05); }
.light-mode .data-table tbody tr { border-top: 1px solid #f1f5f9; }
.data-table tbody tr:hover { }
.dark-mode .data-table tbody tr:hover { background: rgba(255,255,255,0.02); }
.light-mode .data-table tbody tr:hover { background: #f8fafc; }
.data-table td { padding: 12px 16px; }

.order-id { font-size: 12px; font-family: monospace; }
.dark-mode .order-id { color: #64748b; }
.light-mode .order-id { color: #64748b; }
.plan-name { font-weight: 500; }
.dark-mode .plan-name { color: #94a3b8; }
.light-mode .plan-name { color: #64748b; }
.amount { font-weight: 600; }
.dark-mode .amount { color: white; }
.light-mode .amount { color: #1e293b; }

.method-badge { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 8px; font-size: 12px; font-weight: 500; }
.dark-mode .method-badge { background: rgba(255,255,255,0.05); color: #94a3b8; }
.light-mode .method-badge { background: #f1f5f9; color: #64748b; }

.date-text { font-size: 14px; }
.dark-mode .date-text { color: #94a3b8; }
.light-mode .date-text { color: #64748b; }
.time-text { font-size: 12px; margin-top: 2px; }
.dark-mode .time-text { color: #64748b; }
.light-mode .time-text { color: #94a3b8; }

.status-badge { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 500; }
.status-dot { width: 6px; height: 6px; border-radius: 50%; }
.status-success { background: rgba(34,197,94,0.1); color: #22c55e; }
.status-success .status-dot { background: #22c55e; }
.status-pending { background: rgba(251,191,36,0.1); color: #f59e0b; }
.status-pending .status-dot { background: #f59e0b; }
.status-failed { background: rgba(239,68,68,0.1); color: #ef4444; }
.status-failed .status-dot { background: #ef4444; }

.btn-action { width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; border-radius: 8px; cursor: pointer; transition: all 0.3s; }
.dark-mode .btn-action { background: transparent; border: 1px solid rgba(255,255,255,0.1); color: #64748b; }
.light-mode .btn-action { background: transparent; border: 1px solid #e2e8f0; color: #64748b; }
.btn-action:hover { }
.dark-mode .btn-action:hover { border-color: #06b6d4; color: #06b6d4; }
.light-mode .btn-action:hover { border-color: #6366f1; color: #6366f1; }

.empty-state { text-align: center; padding: 60px 20px; }
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-state h3 { font-size: 18px; font-weight: 600; margin: 0 0 8px; }
.dark-mode .empty-state h3 { color: white; }
.light-mode .empty-state h3 { color: #1e293b; }
.empty-state p { font-size: 14px; margin: 0; }
.dark-mode .empty-state p { color: #64748b; }
.light-mode .empty-state p { color: #64748b; }
</style>
