<template>
  <div class="student-shell">
    <div class="student-container">
      <div class="mb-4">
        <p class="student-section-title">Thanh toán</p>
        <h1 class="text-3xl font-black text-gray-900 dark:text-gray-100">Giỏ hàng</h1>
      </div>

      <div v-if="items.length" class="student-card space-y-6">
        <div class="overflow-hidden rounded-2xl border border-slate-100">
          <table class="min-w-full divide-y divide-slate-100 text-sm">
            <thead class="bg-slate-50 text-xs font-semibold uppercase tracking-wide text-gray-600 dark:text-gray-400">
              <tr>
                <th class="px-4 py-3 text-left">Khoá học</th>
                <th class="px-4 py-3 text-right">Giá</th>
                <th class="px-4 py-3 text-center">Hành động</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="it in items" :key="it.id" class="bg-white/80">
                <td class="px-4 py-3 font-semibold text-gray-900 dark:text-gray-100">{{ it.name }}</td>
                <td class="px-4 py-3 text-right font-semibold text-gray-900 dark:text-gray-100">{{ vnd(it.price) }}</td>
                <td class="px-4 py-3 text-center">
                  <button
                    type="button"
                    class="inline-flex items-center rounded-xl border border-slate-200 px-3 py-1.5 text-xs font-semibold text-gray-600 dark:text-gray-400 transition hover:bg-slate-50"
                    @click="remove(it.id)"
                  >
                    Xoá
                  </button>
                </td>
              </tr>
            </tbody>
            <tfoot class="bg-slate-50 text-sm font-bold text-gray-900 dark:text-gray-100">
              <tr>
                <td class="px-4 py-3">Tổng cộng</td>
                <td class="px-4 py-3 text-right">{{ vnd(total) }}</td>
                <td></td>
              </tr>
            </tfoot>
          </table>
        </div>

        <div class="flex justify-end">
          <button
            type="button"
            class="inline-flex items-center justify-center rounded-2xl border border-transparent bg-gradient-to-r from-cyan-500 to-cyan-600 px-5 py-3 text-sm font-extrabold uppercase tracking-wide text-white shadow-lg shadow-cyan-500/40 transition hover:from-cyan-600 hover:to-cyan-700 hover:shadow-xl hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:border-slate-200 disabled:bg-slate-200 disabled:text-slate-500 disabled:hover:translate-y-0"
            :disabled="!items.length || total === 0"
            @click="goCheckout"
          >
            Thanh toán
          </button>
        </div>
      </div>

      <div
        v-else
        class="student-card flex flex-col items-center justify-center text-center text-sm text-gray-600 dark:text-gray-400"
      >
        Giỏ hàng trống.
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

const router = useRouter()
const route = useRoute()

// Cart items - lấy từ localStorage hoặc tạo mới
const items = reactive<Array<{ id: string | number; name: string; price: number }>>([])

const total = computed(() => items.reduce((s, i) => s + (Number(i.price) || 0), 0))
function vnd(n: number) { return n.toLocaleString('vi-VN') + 'đ' }

// Load cart from localStorage
function loadCart() {
  const saved = localStorage.getItem('student_cart')
  if (saved) {
    try {
      const parsed = JSON.parse(saved)
      items.splice(0, items.length, ...parsed)
    } catch (e) {
      console.error('Error loading cart:', e)
    }
  }
}

// Save cart to localStorage
function saveCart() {
  localStorage.setItem('student_cart', JSON.stringify(items))
}

// Add course to cart
async function addCourse(courseId: string | number) {
  try {
    const course = await courseService.detail(courseId)
    const price = Number(course.price) || 0
    
    // Nếu khóa học miễn phí, enroll trực tiếp
    if (price === 0) {
      try {
        await courseService.enroll(courseId)
        // Sau khi enroll thành công, tự động mở khóa học để xem
        // Kiểm tra xem có video không
        if (course.video_url || course.video_file) {
          router.push({ name: 'student-course-player', params: { id: courseId } })
        } else {
          // Nếu không có video, vào lesson đầu tiên
          const firstSection = course.sections?.[0]
          const firstLesson = firstSection?.lessons?.[0]
          if (firstLesson) {
            router.push({ 
              name: 'student-course-player', 
              params: { id: courseId, lessonId: firstLesson.id } 
            })
          } else {
            router.push({ name: 'student-course-player', params: { id: courseId } })
          }
        }
        return
      } catch (e: any) {
        showToast(e?.message || 'Đăng ký khóa học thất bại', 'error')
        return
      }
    }
    
    // Nếu đã có trong cart, không thêm lại
    if (items.find(i => String(i.id) === String(courseId))) {
      // Đã có trong giỏ hàng, bỏ qua để tránh spam toast
      return
    }
    
    // Thêm vào cart
    items.push({
      id: courseId,
      name: course.title,
      price: price
    })
    saveCart()
  } catch (e: any) {
    showToast(e?.message || 'Không thể thêm khóa học vào giỏ hàng', 'error')
  }
}

function remove(id: number | string) {
  const idx = items.findIndex(i => String(i.id) === String(id))
  if (idx >= 0) {
    items.splice(idx, 1)
    saveCart()
  }
}

async function goCheckout() {
  if (total.value === 0) {
    showToast('Giỏ hàng trống hoặc tất cả khóa học đều miễn phí', 'warning')
    return
  }
  // Chặn mua thêm khi còn giao dịch đang xử lý
  try {
    const pending = await paymentService.listMyPayments({ status: 'pending' } as any)
    if (pending?.items && pending.items.length > 0) {
      showToast('Bạn đang có giao dịch đang xử lý, hãy đợi hoàn tất trước khi thanh toán tiếp', 'warning')
      return
    }
  } catch (e: any) {
    console.warn('Không kiểm tra được giao dịch pending:', e)
  }
  // Lưu cart items để enroll sau khi thanh toán thành công
  localStorage.setItem('pending_cart_enroll', JSON.stringify(items.map(i => i.id)))
  // Gọi trực tiếp init MoMo và chuyển hướng sang payUrl
  paymentService.initiateMomo({
    amount: total.value,
    description: items[0]?.name || 'Thanh toán khóa học',
    flow: 'pay_with_method',
    courseIds: items.map(i => i.id),
    courseTitles: items.map(i => i.name),
  }).then((res) => {
    const payUrl = res.payUrl || res.deeplink
    if (!payUrl) {
      showToast(res.message || 'Không nhận được link thanh toán', 'error')
      return
    }
    window.location.href = payUrl
  }).catch((err: any) => {
    showToast(err?.message || 'Không thể khởi tạo thanh toán', 'error')
  })
}

// Enroll các course trong cart sau khi thanh toán thành công
async function enrollCoursesFromCart() {
  const pendingEnroll = localStorage.getItem('pending_cart_enroll')
  if (!pendingEnroll) return
  
  try {
    const courseIds = JSON.parse(pendingEnroll) as (string | number)[]
    if (!Array.isArray(courseIds) || courseIds.length === 0) {
      localStorage.removeItem('pending_cart_enroll')
      return
    }
    
    // Enroll từng course
    const enrollPromises = courseIds.map(courseId => 
      courseService.enroll(courseId).catch(err => {
        console.error(`Failed to enroll course ${courseId}:`, err)
        return { success: false, courseId }
      })
    )
    
    const results = await Promise.all(enrollPromises)
    const successCount = results.filter(r => r?.success !== false).length
    
    // Xóa cart sau khi enroll thành công
    if (successCount > 0) {
      items.splice(0, items.length)
      saveCart()
      showToast(`Đã đăng ký ${successCount} khóa học vào "Khóa học của tôi"!`, 'success')
    }
    
    // Xóa pending enroll
    localStorage.removeItem('pending_cart_enroll')
  } catch (e) {
    console.error('Error enrolling courses from cart:', e)
  }
}

// Kiểm tra thanh toán thành công từ query params
function checkPaymentSuccess() {
  const resultCode = route.query.resultCode
  const hasPendingEnroll = localStorage.getItem('pending_cart_enroll')
  
  // Chỉ enroll nếu có pending enroll và thanh toán thành công
  if (!hasPendingEnroll) return
  
  // Nếu thanh toán thành công (resultCode = '0' hoặc 'paid')
  if (resultCode === '0' || route.query.status === 'paid') {
    // Đợi một chút để payment được sync
    setTimeout(() => {
      enrollCoursesFromCart()
    }, 1500)
    
    // Xóa query params sau khi xử lý
    const cleanQuery = { ...route.query }
    delete cleanQuery.resultCode
    delete cleanQuery.status
    delete cleanQuery.extraData
    delete cleanQuery.orderId
    delete cleanQuery.message
    router.replace({ query: cleanQuery })
  }
}

onMounted(() => {
  loadCart()
  // Nếu có query param 'add', thêm course vào cart
  const addId = route.query.add
  if (addId) {
    addCourse(addId as string)
    // Xóa query param sau khi xử lý
    router.replace({ query: {} })
  } else {
    // Kiểm tra thanh toán thành công
    checkPaymentSuccess()
  }
})

// Watch route changes để detect payment success
watch(() => route.query, () => {
  checkPaymentSuccess()
}, { deep: true })
</script>
