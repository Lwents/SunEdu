<template>
  <div class="min-h-screen bg-slate-50">
    <div class="mx-auto max-w-6xl px-4 py-8">
      <div class="mb-6 flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-extrabold text-slate-900">Lộ trình học tập</h1>
          <p class="mt-2 text-slate-600">Lộ trình học tập được cá nhân hóa dựa trên tiến độ và mục tiêu của bạn.</p>
        </div>
        <router-link
          class="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
          :to="{ name: 'MyCourses' }"
        >
          Về My Courses
        </router-link>
      </div>

      <!-- Personalized Paths -->
      <div v-if="loading" class="space-y-4">
        <div v-for="i in 3" :key="i" class="h-48 animate-pulse rounded-2xl border border-slate-200 bg-white"></div>
      </div>

      <div v-else-if="personalizedPaths.length" class="space-y-6">
        <section
          v-for="path in personalizedPaths"
          :key="path.id"
          class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
        >
          <div class="mb-4 flex items-center justify-between">
            <div>
              <h2 class="text-xl font-bold text-slate-900">{{ path.courseTitle }}</h2>
              <p class="mt-1 text-sm text-slate-600">
                Tạo ngày {{ formatDate(path.createdAt) }} · {{ path.progress }}% hoàn thành
              </p>
            </div>
            <span
              class="rounded-full border px-3 py-1 text-xs font-semibold"
              :class="
                path.progress >= 100
                  ? 'border-emerald-200 bg-emerald-50 text-emerald-700'
                  : 'border-cyan-200 bg-cyan-50 text-cyan-700'
              "
            >
              {{ path.progress >= 100 ? 'Hoàn thành' : 'Đang học' }}
            </span>
          </div>

          <div class="mb-4">
            <div class="mb-2 flex items-center justify-between text-sm">
              <span class="text-slate-600">Tiến độ</span>
              <span class="font-semibold text-slate-900">{{ path.completedSteps }}/{{ path.totalSteps }} bước</span>
            </div>
            <div class="h-2 overflow-hidden rounded-full bg-slate-100">
              <div
                class="h-full rounded-full bg-gradient-to-r from-cyan-500 to-cyan-600 transition-all"
                :style="{ width: `${path.progress}%` }"
              ></div>
            </div>
          </div>

          <div class="mb-4 rounded-xl bg-slate-50 p-4">
            <h3 class="mb-3 text-sm font-semibold text-slate-900">Các bước tiếp theo</h3>
            <ul class="space-y-2">
              <li
                v-for="(step, idx) in path.nextSteps"
                :key="idx"
                class="flex items-center gap-3 text-sm"
              >
                <div
                  class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-semibold"
                  :class="
                    step.completed
                      ? 'bg-emerald-500 text-white'
                      : step.current
                        ? 'bg-cyan-500 text-white'
                        : 'bg-slate-200 text-slate-600'
                  "
                >
                  {{ step.completed ? '✓' : idx + 1 }}
                </div>
                <span
                  class="flex-1"
                  :class="step.completed ? 'text-slate-500 line-through' : 'text-slate-900'"
                >
                  {{ step.title }}
                </span>
                <button
                  v-if="!step.completed && step.current"
                  class="rounded-lg bg-cyan-600 px-3 py-1 text-xs font-semibold text-white hover:bg-cyan-700"
                  @click="startStep(path, step)"
                >
                  Bắt đầu
                </button>
              </li>
            </ul>
          </div>

          <div class="flex gap-3">
            <button
              class="rounded-xl border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              @click="viewFullPath(path)"
            >
              Xem chi tiết
            </button>
            <button
              class="rounded-xl border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50"
              @click="regeneratePath(path)"
            >
              Tạo lại lộ trình
            </button>
          </div>
        </section>
      </div>

      <!-- Default Paths -->
      <div v-else class="mt-5 grid gap-4 sm:grid-cols-2">
        <!-- basic -->
        <section class="rounded-2xl border border-slate-200 bg-white p-5">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-extrabold text-slate-900">Khối 1–2 (Cơ bản)</h2>
            <span class="rounded-full border border-cyan-200 dark:border-cyan-700 bg-cyan-50 dark:bg-cyan-900/20 px-3 py-1 text-xs font-bold text-cyan-700 dark:text-cyan-300">Nền tảng</span>
          </div>
          <p class="mt-2 text-slate-700">Củng cố Toán, Tiếng Việt, Tiếng Anh với các bài ngắn dễ tiếp thu.</p>
          <ul class="mt-3 space-y-1 text-sm text-slate-700">
            <li>• Kiến thức cốt lõi theo tuần</li>
            <li>• Bài tập luyện thói quen học</li>
            <li>• Theo dõi tiến độ đơn giản</li>
          </ul>
          <div class="mt-4">
            <router-link
              class="inline-flex items-center rounded-xl bg-slate-900 px-4 py-2 text-sm font-extrabold text-white hover:bg-slate-800"
              :to="{ name: 'student-catalog', query: { grade: 1 } }"
            >
              Bắt đầu ngay
            </router-link>
          </div>
        </section>

        <!-- advanced -->
        <section class="rounded-2xl border border-slate-200 bg-white p-5">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-extrabold text-slate-900">Khối 3–5 (Nâng cao)</h2>
            <span class="rounded-full border border-sky-200 bg-sky-50 px-3 py-1 text-xs font-bold text-sky-700">Mở rộng</span>
          </div>
          <p class="mt-2 text-slate-700">Hệ thống hoá & luyện thi: Toán, TV, Anh + Khoa học/Lịch sử.</p>
          <ul class="mt-3 space-y-1 text-sm text-slate-700">
            <li>• Quiz ôn tập định kỳ</li>
            <li>• Lộ trình theo mục tiêu</li>
            <li>• Báo cáo tiến bộ chi tiết</li>
          </ul>
          <div class="mt-4">
            <router-link
              class="inline-flex items-center rounded-xl bg-slate-900 px-4 py-2 text-sm font-extrabold text-white hover:bg-slate-800"
              :to="{ name: 'student-catalog', query: { grade: 3 } }"
            >
              Chọn khóa
            </router-link>
          </div>
        </section>
      </div>

      <!-- Create New Path -->
      <div class="mt-6 rounded-2xl border border-dashed border-slate-300 bg-white p-6 text-center">
        <h3 class="text-lg font-semibold text-slate-900">Tạo lộ trình mới</h3>
        <p class="mt-2 text-sm text-slate-600">Chọn khóa học để tạo lộ trình học tập cá nhân hóa</p>
        <button
          class="mt-4 rounded-xl bg-cyan-600 px-6 py-2.5 text-sm font-semibold text-white hover:bg-cyan-700"
          @click="showCreateModal = true"
        >
          Tạo lộ trình
        </button>
      </div>

      <!-- Create Path Modal -->
      <div
        v-if="showCreateModal"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
        @click.self="showCreateModal = false"
      >
        <div class="w-full max-w-2xl rounded-2xl bg-white p-6">
          <h3 class="mb-4 text-lg font-semibold">Tạo lộ trình học tập mới</h3>
          <div class="space-y-4">
            <div>
              <label class="mb-1 block text-sm font-medium">Chọn khóa học</label>
              <select
                v-model="selectedCourseId"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none"
              >
                <option value="">— Chọn khóa học —</option>
                <option v-for="c in availableCourses" :key="c.id" :value="c.id">
                  {{ c.title }}
                </option>
              </select>
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium">Mức độ khó</label>
              <select
                v-model="difficulty"
                class="w-full rounded-xl border border-slate-200 px-3 py-2 outline-none"
              >
                <option value="adaptive">Tự động điều chỉnh</option>
                <option value="easy">Dễ</option>
                <option value="medium">Trung bình</option>
                <option value="hard">Khó</option>
              </select>
            </div>
          </div>
          <div class="mt-6 flex justify-end gap-3">
            <button
              class="rounded-xl border px-4 py-2 text-sm hover:bg-slate-50"
              @click="showCreateModal = false"
            >
              Hủy
            </button>
            <button
              class="rounded-xl bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700"
              @click="createPath"
            >
              Tạo lộ trình
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { courseService } from '@/services/course.service'

const router = useRouter()

const loading = ref(false)
const personalizedPaths = ref<any[]>([])
const availableCourses = ref<any[]>([])
const showCreateModal = ref(false)
const selectedCourseId = ref('')
const difficulty = ref('adaptive')

function formatDate(iso?: string) {
  if (!iso) return ''
  try {
    return new Date(iso).toLocaleDateString('vi-VN')
  } catch {
    return iso
  }
}

async function loadPaths() {
  loading.value = true
  try {
    // Mock data - thay bằng API call thực tế
    personalizedPaths.value = [
      {
        id: 1,
        courseId: 1,
        courseTitle: 'Toán lớp 3',
        progress: 65,
        completedSteps: 13,
        totalSteps: 20,
        createdAt: new Date().toISOString(),
        nextSteps: [
          { title: 'Bài 14: Phép nhân', completed: false, current: true },
          { title: 'Bài 15: Phép chia', completed: false, current: false },
          { title: 'Bài 16: Ôn tập', completed: false, current: false },
        ],
      },
      {
        id: 2,
        courseId: 2,
        courseTitle: 'Tiếng Việt lớp 4',
        progress: 30,
        completedSteps: 6,
        totalSteps: 20,
        createdAt: new Date(Date.now() - 86400000).toISOString(),
        nextSteps: [
          { title: 'Bài 7: Từ đồng nghĩa', completed: false, current: true },
          { title: 'Bài 8: Từ trái nghĩa', completed: false, current: false },
        ],
      },
    ]
  } catch (e: any) {
    console.error('Load paths error:', e)
  } finally {
    loading.value = false
  }
}

async function loadCourses() {
  try {
    const { items } = await courseService.list({ page: 1, pageSize: 50, status: 'published' })
    availableCourses.value = items || []
  } catch (e: any) {
    console.error('Load courses error:', e)
  }
}

function startStep(path: any, step: any) {
  router.push({
    name: 'student-course-player',
    params: { id: path.courseId, lessonId: step.lessonId || '1' },
  })
}

function viewFullPath(path: any) {
  router.push({ name: 'student-course-detail', params: { id: path.courseId } })
}

async function regeneratePath(path: any) {
  if (confirm('Bạn có chắc muốn tạo lại lộ trình này?')) {
    // Call API to regenerate
    console.log('Regenerate path:', path.id)
    await loadPaths()
  }
}

async function createPath() {
  if (!selectedCourseId.value) {
    alert('Vui lòng chọn khóa học')
    return
  }
  // Call API to create path
  console.log('Create path:', { courseId: selectedCourseId.value, difficulty: difficulty.value })
  showCreateModal.value = false
  await loadPaths()
}

onMounted(async () => {
  await loadPaths()
  await loadCourses()
})
</script>
