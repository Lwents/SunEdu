<template>
  <div class="student-shell">
    <div class="student-container max-w-4xl">
      <div class="mb-6">
        <h1 class="text-3xl font-black text-gray-900 dark:text-gray-100">Hoạt động của tôi</h1>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Lịch sử các hoạt động học tập và tương tác của bạn trên hệ thống
        </p>
      </div>

      <div class="space-y-4">
        <div class="flex items-center gap-3 rounded-2xl border border-slate-200 bg-white p-4">
          <div class="flex items-center gap-3">
            <select
              v-model="filterType"
              class="rounded-xl border border-slate-200 px-3 py-2 text-sm outline-none"
            >
              <option value="">Tất cả hoạt động</option>
              <option value="login">Đăng nhập</option>
              <option value="course">Khóa học</option>
              <option value="exam">Bài thi</option>
              <option value="payment">Thanh toán</option>
            </select>
          </div>
        </div>

        <div v-if="loading" class="space-y-3">
          <div
            v-for="i in 5"
            :key="i"
            class="h-20 animate-pulse rounded-2xl border border-slate-200 bg-slate-100"
          ></div>
        </div>

        <ul v-else class="flex flex-col gap-3">
          <li
            v-for="(it, i) in filteredItems"
            :key="i"
            class="flex items-start gap-4 rounded-2xl border border-slate-200 bg-white px-4 py-3 shadow-sm shadow-slate-100 transition hover:shadow-md"
          >
            <div
              class="mt-2 h-2.5 w-2.5 shrink-0 rounded-full"
              :class="getActivityColor(it.type)"
            ></div>
            <div class="flex-1">
              <p class="text-sm font-semibold text-slate-900">{{ it.title }}</p>
              <p class="mt-1 text-xs text-slate-500">{{ formatTime(it.time) }}</p>
              <p v-if="it.details" class="mt-1 text-xs text-slate-600">{{ it.details }}</p>
            </div>
            <div v-if="it.action" class="shrink-0">
              <button
                class="rounded-lg border border-slate-200 px-3 py-1 text-xs font-semibold text-slate-700 hover:bg-slate-50"
                @click="handleAction(it)"
              >
                {{ it.action }}
              </button>
            </div>
          </li>
        </ul>

        <div v-if="!loading && !filteredItems.length" class="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center text-slate-500">
          Không có hoạt động nào.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const filterType = ref('')
const items = ref<Array<{
  type: string
  title: string
  time: string
  details?: string
  action?: string
  actionId?: string | number
}>>([])

const filteredItems = computed(() => {
  if (!filterType.value) return items.value
  return items.value.filter((it) => it.type === filterType.value)
})

function getActivityColor(type: string) {
  const colors: Record<string, string> = {
    login: 'bg-blue-500',
    course: 'bg-cyan-500',
    exam: 'bg-amber-500',
    payment: 'bg-emerald-500',
  }
  return colors[type] || 'bg-slate-400'
}

function formatTime(time: string) {
  return time
}

function handleAction(item: any) {
  if (item.type === 'course' && item.actionId) {
    router.push({ name: 'student-course-detail', params: { id: item.actionId } })
  } else if (item.type === 'exam' && item.actionId) {
    router.push({ name: 'student-exam-detail', params: { id: item.actionId } })
  }
}

async function loadActivities() {
  loading.value = true
  try {
    // Mock data - thay bằng API call thực tế
    await new Promise((r) => setTimeout(r, 500))
    items.value = [
      {
        type: 'login',
        title: 'Đăng nhập hệ thống',
        time: new Date().toISOString(),
        details: 'Đăng nhập từ trình duyệt Chrome',
      },
      {
        type: 'course',
        title: 'Hoàn thành bài học: Phép cộng',
        time: new Date(Date.now() - 3600000).toISOString(),
        details: 'Khóa học: Toán lớp 3',
        action: 'Xem khóa học',
        actionId: 1,
      },
      {
        type: 'exam',
        title: 'Nộp bài thi: Đề thi thử #1',
        time: new Date(Date.now() - 7200000).toISOString(),
        details: 'Điểm: 85/100',
        action: 'Xem kết quả',
        actionId: 1,
      },
      {
        type: 'payment',
        title: 'Thanh toán thành công',
        time: new Date(Date.now() - 86400000).toISOString(),
        details: 'Số tiền: 500,000 VNĐ',
      },
      {
        type: 'course',
        title: 'Bắt đầu khóa học: Tiếng Việt lớp 4',
        time: new Date(Date.now() - 172800000).toISOString(),
        details: 'Tiến độ: 15%',
        action: 'Tiếp tục học',
        actionId: 2,
      },
    ]
  } catch (e: any) {
    console.error('Load activities error:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadActivities()
})
</script>
