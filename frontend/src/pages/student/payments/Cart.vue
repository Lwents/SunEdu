<template>
  <div class="page-wrapper" :class="isDark ? 'dark-mode' : 'light-mode'">
    <!-- Background Elements -->
    <div v-if="isDark" class="bg-elements">
      <div class="glow glow-1"></div>
      <div class="glow glow-2"></div>
    </div>

    <div class="page-content">
      <div class="page-header">
        <p class="section-label">Thanh toán</p>
        <h1>Giỏ hàng</h1>
      </div>

      <div v-if="items.length" class="cart-card">
        <div class="table-wrapper">
          <table class="cart-table">
            <thead>
              <tr>
                <th class="text-left">Khoá học</th>
                <th class="text-right">Giá</th>
                <th class="text-center">Hành động</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="it in items" :key="it.id">
                <td class="course-name">{{ it.name }}</td>
                <td class="course-price">{{ vnd(it.price) }}</td>
                <td class="course-action">
                  <button type="button" class="btn-remove" @click="remove(it.id)">Xoá</button>
                </td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td class="total-label">Tổng cộng</td>
                <td class="total-value">{{ vnd(total) }}</td>
                <td></td>
              </tr>
            </tfoot>
          </table>
        </div>

        <div class="checkout-actions">
          <button type="button" class="btn-checkout" :disabled="!items.length || total === 0" @click="goCheckout">
            Thanh toán
          </button>
        </div>
      </div>

      <div v-else class="empty-state">
        <div class="empty-icon">🛒</div>
        <h3>Giỏ hàng trống</h3>
        <p>Hãy thêm khóa học vào giỏ hàng để thanh toán</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { courseService } from '@/services/course.service'
import { showToast } from '@/utils/toast'
import { paymentService } from '@/services/payment.service'
import { useThemeStore } from '@/store/theme.store'

const router = useRouter()
const route = useRoute()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

const items = reactive<Array<{ id: string | number; name: string; price: number }>>([])
const total = computed(() => items.reduce((s, i) => s + (Number(i.price) || 0), 0))
function vnd(n: number) { return n.toLocaleString('vi-VN') + 'đ' }

function loadCart() {
  const saved = localStorage.getItem('student_cart')
  if (saved) {
    try {
      const parsed = JSON.parse(saved)
      items.splice(0, items.length, ...parsed)
    } catch (e) { console.error('Error loading cart:', e) }
  }
}

function saveCart() { localStorage.setItem('student_cart', JSON.stringify(items)) }

async function addCourse(courseId: string | number) {
  try {
    const course = await courseService.detail(courseId)
    const price = Number(course.price) || 0
    if (price === 0) {
      try {
        await courseService.enroll(courseId)
        if (course.video_url || course.video_file) {
          router.push({ name: 'student-course-player', params: { id: courseId } })
        } else {
          const firstSection = course.sections?.[0]
          const firstLesson = firstSection?.lessons?.[0]
          if (firstLesson) router.push({ name: 'student-course-player', params: { id: courseId, lessonId: firstLesson.id } })
          else router.push({ name: 'student-course-player', params: { id: courseId } })
        }
        return
      } catch (e: any) { showToast(e?.message || 'Đăng ký khóa học thất bại', 'error'); return }
    }
    if (items.find(i => String(i.id) === String(courseId))) return
    items.push({ id: courseId, name: course.title, price: price })
    saveCart()
  } catch (e: any) { showToast(e?.message || 'Không thể thêm khóa học vào giỏ hàng', 'error') }
}

function remove(id: number | string) {
  const idx = items.findIndex(i => String(i.id) === String(id))
  if (idx >= 0) { items.splice(idx, 1); saveCart() }
}

async function goCheckout() {
  if (total.value === 0) { showToast('Giỏ hàng trống hoặc tất cả khóa học đều miễn phí', 'warning'); return }
  try {
    const pending = await paymentService.listMyPayments({ status: 'pending' } as any)
    if (pending?.items && pending.items.length > 0) {
      showToast('Bạn đang có giao dịch đang xử lý, hãy đợi hoàn tất trước khi thanh toán tiếp', 'warning')
      return
    }
  } catch (e: any) { console.warn('Không kiểm tra được giao dịch pending:', e) }
  localStorage.setItem('pending_cart_enroll', JSON.stringify(items.map(i => i.id)))
  paymentService.initiateMomo({
    amount: total.value,
    description: items[0]?.name || 'Thanh toán khóa học',
    flow: 'pay_with_method',
    courseIds: items.map(i => i.id),
    courseTitles: items.map(i => i.name),
  }).then((res) => {
    const payUrl = res.payUrl || res.deeplink
    if (!payUrl) { showToast(res.message || 'Không nhận được link thanh toán', 'error'); return }
    window.location.href = payUrl
  }).catch((err: any) => { showToast(err?.message || 'Không thể khởi tạo thanh toán', 'error') })
}

async function enrollCoursesFromCart() {
  const pendingEnroll = localStorage.getItem('pending_cart_enroll')
  if (!pendingEnroll) return
  try {
    const courseIds = JSON.parse(pendingEnroll) as (string | number)[]
    if (!Array.isArray(courseIds) || courseIds.length === 0) { localStorage.removeItem('pending_cart_enroll'); return }
    const enrollPromises = courseIds.map(courseId => courseService.enroll(courseId).catch(err => { console.error(`Failed to enroll course ${courseId}:`, err); return { success: false, courseId } }))
    const results = await Promise.all(enrollPromises)
    const successCount = results.filter(r => r?.success !== false).length
    if (successCount > 0) { items.splice(0, items.length); saveCart(); showToast(`Đã đăng ký ${successCount} khóa học vào "Khóa học của tôi"!`, 'success') }
    localStorage.removeItem('pending_cart_enroll')
  } catch (e) { console.error('Error enrolling courses from cart:', e) }
}

function checkPaymentSuccess() {
  const resultCode = route.query.resultCode
  const hasPendingEnroll = localStorage.getItem('pending_cart_enroll')
  if (!hasPendingEnroll) return
  if (resultCode === '0' || route.query.status === 'paid') {
    setTimeout(() => { enrollCoursesFromCart() }, 1500)
    const cleanQuery = { ...route.query }
    delete cleanQuery.resultCode; delete cleanQuery.status; delete cleanQuery.extraData; delete cleanQuery.orderId; delete cleanQuery.message
    router.replace({ query: cleanQuery })
  }
}

onMounted(() => {
  loadCart()
  const addId = route.query.add
  if (addId) { addCourse(addId as string); router.replace({ query: {} }) }
  else { checkPaymentSuccess() }
})

watch(() => route.query, () => { checkPaymentSuccess() }, { deep: true })
</script>

<style scoped>
.page-wrapper { min-height: 100vh; position: relative; transition: background-color 0.3s ease; }
.page-wrapper.dark-mode { background: #020617; }
.page-wrapper.light-mode { background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%); }

.bg-elements { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.glow { position: absolute; border-radius: 50%; filter: blur(100px); }
.glow-1 { top: 10%; left: -5%; width: 300px; height: 300px; background: rgba(6, 182, 212, 0.1); }
.glow-2 { bottom: 10%; right: -5%; width: 250px; height: 250px; background: rgba(139, 92, 246, 0.1); }

.page-content { position: relative; z-index: 10; max-width: 900px; margin: 0 auto; padding: 32px 24px; }

.page-header { margin-bottom: 24px; }
.section-label { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 8px; }
.dark-mode .section-label { color: #06b6d4; }
.light-mode .section-label { color: #6366f1; }
.page-header h1 { font-size: 28px; font-weight: 800; margin: 0; }
.dark-mode .page-header h1 { color: white; }
.light-mode .page-header h1 { color: #1e293b; }

.cart-card { border-radius: 20px; padding: 24px; }
.dark-mode .cart-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .cart-card { background: white; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }

.table-wrapper { overflow: hidden; border-radius: 16px; margin-bottom: 24px; }
.dark-mode .table-wrapper { border: 1px solid rgba(255,255,255,0.08); }
.light-mode .table-wrapper { border: 1px solid #e2e8f0; }

.cart-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.cart-table thead { }
.dark-mode .cart-table thead { background: rgba(255,255,255,0.03); }
.light-mode .cart-table thead { background: #f8fafc; }
.cart-table th { padding: 12px 16px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
.dark-mode .cart-table th { color: #64748b; }
.light-mode .cart-table th { color: #64748b; }
.cart-table tbody tr { }
.dark-mode .cart-table tbody tr { border-top: 1px solid rgba(255,255,255,0.05); }
.light-mode .cart-table tbody tr { border-top: 1px solid #f1f5f9; }
.cart-table td { padding: 16px; }
.course-name { font-weight: 600; }
.dark-mode .course-name { color: white; }
.light-mode .course-name { color: #1e293b; }
.course-price { text-align: right; font-weight: 600; }
.dark-mode .course-price { color: white; }
.light-mode .course-price { color: #1e293b; }
.course-action { text-align: center; }
.btn-remove { padding: 6px 12px; border-radius: 10px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
.dark-mode .btn-remove { background: transparent; border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .btn-remove { background: transparent; border: 1px solid #e2e8f0; color: #64748b; }
.btn-remove:hover { }
.dark-mode .btn-remove:hover { border-color: #ef4444; color: #ef4444; }
.light-mode .btn-remove:hover { border-color: #ef4444; color: #ef4444; }

.cart-table tfoot { }
.dark-mode .cart-table tfoot { background: rgba(255,255,255,0.03); border-top: 1px solid rgba(255,255,255,0.08); }
.light-mode .cart-table tfoot { background: #f8fafc; border-top: 1px solid #e2e8f0; }
.total-label { font-weight: 700; }
.dark-mode .total-label { color: white; }
.light-mode .total-label { color: #1e293b; }
.total-value { text-align: right; font-weight: 700; }
.dark-mode .total-value { color: white; }
.light-mode .total-value { color: #1e293b; }

.checkout-actions { display: flex; justify-content: flex-end; }
.btn-checkout { padding: 14px 32px; border-radius: 16px; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; border: none; cursor: pointer; transition: all 0.3s; }
.dark-mode .btn-checkout { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; box-shadow: 0 8px 24px rgba(6,182,212,0.3); }
.light-mode .btn-checkout { background: #1e293b; color: white; box-shadow: 0 8px 24px rgba(30,41,59,0.2); }
.btn-checkout:hover { transform: translateY(-2px); }
.btn-checkout:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

.empty-state { text-align: center; padding: 60px 20px; border-radius: 20px; }
.dark-mode .empty-state { background: rgba(255,255,255,0.02); border: 2px dashed rgba(255,255,255,0.1); }
.light-mode .empty-state { background: #f8fafc; border: 2px dashed #e2e8f0; }
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-state h3 { font-size: 18px; font-weight: 600; margin: 0 0 8px; }
.dark-mode .empty-state h3 { color: white; }
.light-mode .empty-state h3 { color: #1e293b; }
.empty-state p { font-size: 14px; margin: 0; }
.dark-mode .empty-state p { color: #64748b; }
.light-mode .empty-state p { color: #64748b; }
</style>
