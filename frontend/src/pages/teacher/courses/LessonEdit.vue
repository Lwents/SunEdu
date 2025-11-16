<!-- src/pages/teacher/courses/LessonEdit.vue -->
<template>
  <div class="mx-auto max-w-4xl p-6">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Chỉnh sửa bài học</h1>
        <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">{{ lessonTitle }}</p>
      </div>
      <button
        class="rounded-xl bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700"
        @click="saveLesson"
        :disabled="saving"
      >
        {{ saving ? 'Đang lưu...' : 'Lưu thay đổi' }}
      </button>
    </div>

    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="h-32 rounded-2xl bg-slate-200 animate-pulse" />
    </div>

    <div v-else-if="error" class="rounded-xl border border-rose-200 bg-rose-50 p-4 text-rose-700">
      {{ error }}
    </div>

    <div v-else class="space-y-6">
      <!-- Thông tin cơ bản -->
      <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">Thông tin cơ bản</h2>
        <div class="space-y-4">
          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">Tên bài học</label>
            <input
              v-model="form.title"
              type="text"
              class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
              placeholder="Tên bài học"
            />
          </div>
          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">Giới thiệu bài học</label>
            <textarea
              v-model="form.introduction"
              rows="4"
              class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
              placeholder="Giới thiệu ngắn gọn về bài học (hiển thị trước video)"
            ></textarea>
            <p class="mt-1 text-xs text-gray-500">Nội dung này sẽ hiển thị trước khi học sinh xem video</p>
          </div>
        </div>
      </div>

      <!-- Video bài học -->
      <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 class="mb-4 text-lg font-semibold text-gray-900">Video bài học</h2>
        <div class="space-y-4">
          <div class="mb-3 flex gap-4">
            <label class="flex items-center gap-2">
              <input type="radio" v-model="videoInputType" value="url" class="h-4 w-4" />
              <span class="text-sm">Link URL</span>
            </label>
            <label class="flex items-center gap-2">
              <input type="radio" v-model="videoInputType" value="file" class="h-4 w-4" />
              <span class="text-sm">Upload file</span>
            </label>
          </div>
          <input
            v-if="videoInputType === 'url'"
            v-model="form.video_url"
            type="url"
            class="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
            placeholder="https://www.youtube.com/watch?v=..."
          />
          <div v-else class="flex items-center gap-4">
            <input
              ref="videoInput"
              type="file"
              accept="video/*"
              class="hidden"
              @change="onPickVideo"
            />
            <button
              type="button"
              class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
              @click="videoInput?.click()"
            >
              Chọn video
            </button>
            <span v-if="videoFile" class="text-sm text-gray-600">{{ videoFile.name }}</span>
          </div>
        </div>
      </div>

      <!-- Bài tập -->
      <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900">Bài tập</h2>
          <button
            type="button"
            class="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700"
            @click="showAddExercise = true"
          >
            + Thêm bài tập
          </button>
        </div>
        
        <div class="mb-4">
          <label class="flex items-center gap-2">
            <input
              type="checkbox"
              v-model="form.requires_exercise_completion"
              class="h-4 w-4 rounded border-gray-300"
            />
            <span class="text-sm font-medium text-gray-700">
              Yêu cầu hoàn thành bài tập trước khi tiếp tục bài học tiếp theo
            </span>
          </label>
        </div>

        <div v-if="exercises.length === 0" class="rounded-xl border-2 border-dashed border-gray-300 bg-gray-50 p-8 text-center">
          <p class="text-gray-500">Chưa có bài tập nào. Nhấn "+ Thêm bài tập" để thêm.</p>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="(exercise, idx) in exercises"
            :key="exercise.id || idx"
            class="flex items-center justify-between rounded-lg border border-gray-200 bg-gray-50 p-4"
          >
            <div>
              <p class="font-semibold text-gray-900">{{ exercise.title }}</p>
              <p class="text-xs text-gray-500">{{ exercise.type === 'mcq' ? 'Trắc nghiệm' : exercise.type === 'short_answer' ? 'Tự luận' : 'Nối' }}</p>
            </div>
            <button
              type="button"
              class="rounded-lg border border-rose-200 px-3 py-1.5 text-xs font-medium text-rose-700 hover:bg-rose-50"
              @click="removeExercise(exercise.id)"
            >
              Xóa
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Exercise Modal -->
    <div
      v-if="showAddExercise"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      @click.self="showAddExercise = false"
    >
      <div class="w-full max-w-2xl rounded-2xl bg-white p-6 shadow-xl">
        <h3 class="mb-4 text-lg font-bold">Thêm bài tập mới</h3>
        <div class="space-y-4">
          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">Tên bài tập</label>
            <input
              v-model.trim="exerciseForm.title"
              type="text"
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
              placeholder="Ví dụ: Bài tập về biến số"
            />
          </div>
          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">Loại bài tập</label>
            <select
              v-model="exerciseForm.type"
              class="w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
            >
              <option value="mcq">Trắc nghiệm</option>
              <option value="short_answer">Tự luận</option>
              <option value="matching">Nối</option>
            </select>
          </div>
        </div>
        <div class="mt-6 flex justify-end gap-3">
          <button
            type="button"
            class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            @click="showAddExercise = false"
          >
            Hủy
          </button>
          <button
            type="button"
            class="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-medium text-white hover:bg-cyan-700"
            @click="addExercise"
          >
            Thêm
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { contentService } from '@/services/content.service'
import http from '@/config/axios'
import { showToast } from '@/utils/toast'
import { showConfirm } from '@/utils/confirm'

const route = useRoute()
const router = useRouter()

const lessonId = route.params.id as string
const lessonTitle = ref('')
const loading = ref(true)
const error = ref('')
const saving = ref(false)

const form = ref({
  title: '',
  introduction: '',
  video_url: '',
  video_file: null as File | null,
  requires_exercise_completion: false
})

const videoInputType = ref<'url' | 'file'>('url')
const videoInput = ref<HTMLInputElement | null>(null)
const videoFile = ref<File | null>(null)

const exercises = ref<any[]>([])
const showAddExercise = ref(false)
const exerciseForm = ref({ title: '', type: 'mcq' })

async function loadLesson() {
  try {
    const { data } = await http.get(`/content/lessons/${lessonId}/`)
    lessonTitle.value = data.title
    form.value = {
      title: data.title || '',
      introduction: data.introduction || '',
      video_url: data.video_url || '',
      video_file: null,
      requires_exercise_completion: data.requires_exercise_completion || false
    }
    videoInputType.value = data.video_url ? 'url' : 'file'
    
    // Load exercises
    if (data.exercises) {
      exercises.value = data.exercises
    } else {
      const { data: exData } = await http.get(`/activities/exercises/?lesson=${lessonId}`)
      exercises.value = Array.isArray(exData) ? exData : exData.results || []
    }
  } catch (e: any) {
    error.value = e?.message || 'Không thể tải thông tin bài học'
  } finally {
    loading.value = false
  }
}

function onPickVideo(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  if (!file.type.startsWith('video/')) {
    showToast('Vui lòng chọn file video', 'warning')
    return
  }
  videoFile.value = file
  form.value.video_file = file
}

async function addExercise() {
  if (!exerciseForm.value.title.trim()) return
  try {
    const { data } = await http.post('/activities/exercises/', {
      title: exerciseForm.value.title,
      type: exerciseForm.value.type,
      lesson: lessonId
    })
    exercises.value.push(data)
    exerciseForm.value = { title: '', type: 'mcq' }
    showAddExercise.value = false
  } catch (e: any) {
    showToast(e?.message || 'Không thể tạo bài tập', 'error')
  }
}

async function removeExercise(exerciseId: string) {
  const confirmed = await showConfirm({
    message: 'Bạn có chắc muốn xóa bài tập này?',
    title: 'Xác nhận xóa bài tập',
    type: 'danger',
    confirmText: 'Xóa',
    cancelText: 'Hủy'
  })
  if (!confirmed) return
  try {
    await http.delete(`/activities/exercises/${exerciseId}/`)
    exercises.value = exercises.value.filter(e => e.id !== exerciseId)
  } catch (e: any) {
    showToast(e?.message || 'Không thể xóa bài tập', 'error')
  }
}

async function saveLesson() {
  saving.value = true
  try {
    const fd = new FormData()
    fd.append('title', form.value.title)
    if (form.value.introduction) {
      fd.append('introduction', form.value.introduction)
    }
    if (videoInputType.value === 'url' && form.value.video_url) {
      fd.append('video_url', form.value.video_url)
    } else if (videoFile.value) {
      fd.append('video_file', videoFile.value)
    }
    fd.append('requires_exercise_completion', String(form.value.requires_exercise_completion))
    
    await http.patch(`/content/lessons/${lessonId}/`, fd, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    showToast('Đã lưu thay đổi thành công!', 'success')
    router.back()
  } catch (e: any) {
    showToast(e?.message || 'Không thể lưu thay đổi', 'error')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadLesson()
})
</script>







