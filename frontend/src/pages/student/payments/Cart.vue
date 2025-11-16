<template>
  <div class="student-shell">
    <div class="student-container">
      <div class="mb-4">
        <p class="student-section-title">Nạp tiền</p>
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
            Nạp tiền
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
import { computed, onMounted, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { courseService } from '@/services/course.service'

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
        alert(e?.message || 'Đăng ký khóa học thất bại')
        return
      }
    }
    
    // Nếu đã có trong cart, không thêm lại
    if (items.find(i => String(i.id) === String(courseId))) {
      alert('Khóa học đã có trong giỏ hàng')
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
    alert(e?.message || 'Không thể thêm khóa học vào giỏ hàng')
  }
}

function remove(id: number | string) {
  const idx = items.findIndex(i => String(i.id) === String(id))
  if (idx >= 0) {
    items.splice(idx, 1)
    saveCart()
  }
}

function goCheckout() {
  if (total.value === 0) {
    alert('Giỏ hàng trống hoặc tất cả khóa học đều miễn phí')
    return
  }
  router.push({
    name: 'student-payments-checkout',
    query: { amount: String(total.value), plan: items[0]?.name || 'Nạp tiền' }
  })
}

onMounted(() => {
  loadCart()
  // Nếu có query param 'add', thêm course vào cart
  const addId = route.query.add
  if (addId) {
    addCourse(addId as string)
    // Xóa query param sau khi xử lý
    router.replace({ query: {} })
  }
})
</script>
