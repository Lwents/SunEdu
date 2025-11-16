<!-- src/pages/teacher/courses/CourseContent.vue -->
<template>
  <div class="mx-auto max-w-6xl p-6">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Quản lý nội dung khóa học</h1>
        <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">{{ courseTitle }}</p>
      </div>
      <button
        class="rounded-xl bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700"
        @click="showAddModule = true"
      >
        + Thêm chương mới
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="h-32 rounded-2xl bg-slate-200 animate-pulse" />
    </div>

    <!-- Error -->
    <div v-else-if="error" class="rounded-xl border border-rose-200 bg-rose-50 p-4 text-rose-700">
      {{ error }}
    </div>

    <!-- Modules List -->
    <div v-else class="space-y-4">
      <div
        v-for="(module, mIdx) in modules"
        :key="module.id"
        class="rounded-2xl border border-slate-200 bg-white shadow-sm"
      >
        <!-- Module Header -->
        <div class="flex items-center justify-between border-b border-slate-100 px-6 py-4">
          <div class="flex items-center gap-4">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-cyan-100 text-cyan-700 font-bold">
              {{ mIdx + 1 }}
            </div>
            <div>
              <h3 class="font-semibold text-gray-900 dark:text-gray-100">{{ module.title }}</h3>
              <p class="text-xs text-gray-500">{{ lessonsByModule[module.id]?.length || 0 }} bài học</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button
              class="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-slate-50"
              @click="editModule(module)"
            >
              Sửa
            </button>
            <button
              class="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-slate-50"
              @click="showAddLesson(module.id)"
            >
              + Thêm bài học
            </button>
            <button
              class="rounded-lg border border-rose-200 px-3 py-1.5 text-xs font-medium text-rose-700 hover:bg-rose-50"
              @click="deleteModule(module.id)"
            >
              Xóa
            </button>
          </div>
        </div>

        <!-- Lessons List -->
        <div class="divide-y divide-slate-100">
          <div
            v-for="(lesson, lIdx) in lessonsByModule[module.id] || []"
            :key="lesson.id"
            class="flex items-center justify-between px-6 py-3 hover:bg-slate-50"
          >
            <div class="flex items-center gap-4">
              <span class="text-sm font-medium text-gray-500">{{ mIdx + 1 }}.{{ lIdx + 1 }}</span>
              <div>
                <p class="font-medium text-gray-900 dark:text-gray-100">{{ lesson.title }}</p>
                <p class="text-xs text-gray-500">
                  {{ lesson.content_type === 'lesson' ? 'Bài học' : lesson.content_type === 'exercise' ? 'Bài tập' : 'Khám phá' }}
                  <span v-if="lesson.published" class="ml-2 text-emerald-600">• Đã xuất bản</span>
                  <span v-else class="ml-2 text-amber-600">• Nháp</span>
                </p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <button
                class="rounded-lg border border-slate-200 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-slate-50"
                @click="goEditLesson(String(lesson.id))"
              >
                Sửa
              </button>
              <button
                class="rounded-lg border border-rose-200 px-3 py-1.5 text-xs font-medium text-rose-700 hover:bg-rose-50"
                @click="deleteLesson(lesson.id)"
              >
                Xóa
              </button>
            </div>
          </div>
          <div v-if="!lessonsByModule[module.id]?.length" class="px-6 py-8 text-center text-sm text-gray-500">
            Chưa có bài học nào. Nhấn "+ Thêm bài học" để thêm.
          </div>
        </div>
      </div>

      <div v-if="!modules.length" class="rounded-2xl border-2 border-dashed border-slate-300 bg-slate-50 p-12 text-center">
        <p class="text-gray-600 dark:text-gray-400">Chưa có chương nào. Nhấn "+ Thêm chương mới" để bắt đầu.</p>
      </div>
    </div>

    <!-- Add/Edit Module Modal -->
    <div
      v-if="showAddModule || editingModule"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      @click.self="closeModuleModal"
    >
      <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
        <h2 class="mb-4 text-xl font-bold text-gray-900">
          {{ editingModule ? 'Sửa chương' : 'Thêm chương mới' }}
        </h2>
        <form @submit.prevent="saveModule">
          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-gray-700">Tên chương</label>
            <input
              v-model="moduleForm.title"
              type="text"
              class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/20"
              placeholder="Ví dụ: Chương 1 - Giới thiệu"
              required
            />
          </div>
          <div class="flex justify-end gap-3">
            <button
              type="button"
              class="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-slate-50"
              @click="closeModuleModal"
            >
              Hủy
            </button>
            <button
              type="submit"
              class="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-medium text-white hover:bg-cyan-700"
              :disabled="saving"
            >
              {{ saving ? 'Đang lưu...' : editingModule ? 'Cập nhật' : 'Thêm' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Add/Edit Lesson Modal -->
    <div
      v-if="showAddLessonModuleId || editingLesson"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      @click.self="closeLessonModal"
    >
      <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
        <h2 class="mb-4 text-xl font-bold text-gray-900">
          {{ editingLesson ? 'Sửa bài học' : 'Thêm bài học mới' }}
        </h2>
        <form @submit.prevent="saveLesson">
          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-gray-700">Tên bài học</label>
            <input
              v-model="lessonForm.title"
              type="text"
              class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/20"
              placeholder="Ví dụ: Bài 1 - Khái niệm cơ bản"
              required
            />
          </div>
          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-gray-700">Loại nội dung</label>
            <select
              v-model="lessonForm.content_type"
              class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/20"
            >
              <option value="lesson">Bài học</option>
              <option value="exercise">Bài tập</option>
              <option value="exploration">Khám phá</option>
            </select>
          </div>
          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-gray-700">Video</label>
            <div class="mb-2 flex gap-2">
              <button
                type="button"
                class="flex-1 rounded-lg border px-3 py-2 text-sm font-medium transition"
                :class="lessonForm.videoType === 'url' 
                  ? 'border-cyan-500 bg-cyan-50 text-cyan-700' 
                  : 'border-slate-300 bg-white text-gray-700 hover:bg-slate-50'"
                @click="lessonForm.videoType = 'url'"
              >
                Video URL
              </button>
              <button
                type="button"
                class="flex-1 rounded-lg border px-3 py-2 text-sm font-medium transition"
                :class="lessonForm.videoType === 'file' 
                  ? 'border-cyan-500 bg-cyan-50 text-cyan-700' 
                  : 'border-slate-300 bg-white text-gray-700 hover:bg-slate-50'"
                @click="lessonForm.videoType = 'file'"
              >
                Tải video lên
              </button>
            </div>
            
            <!-- Video URL Input -->
            <div v-if="lessonForm.videoType === 'url'">
              <input
                v-model="lessonForm.video_url"
                type="url"
                class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/20"
                placeholder="https://www.youtube.com/watch?v=... hoặc URL video khác"
              />
              <p class="mt-1 text-xs text-gray-500">Có thể thêm sau khi tạo bài học</p>
            </div>
            
            <!-- Video File Upload -->
            <div v-else>
              <input
                ref="videoFileInput"
                type="file"
                accept="video/*"
                class="w-full rounded-lg border border-slate-300 px-4 py-2 text-sm focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/20"
                @change="onVideoFileChange"
              />
              <p v-if="lessonForm.videoFile" class="mt-1 text-xs text-emerald-600">
                Đã chọn: {{ lessonForm.videoFile.name }} ({{ formatFileSize(lessonForm.videoFile.size) }})
              </p>
              <p v-else class="mt-1 text-xs text-gray-500">
                Chọn file video (MP4, AVI, MOV, v.v.) - Tối đa 500MB
              </p>
            </div>
          </div>
          <div class="flex justify-end gap-3">
            <button
              type="button"
              class="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-slate-50"
              @click="closeLessonModal"
            >
              Hủy
            </button>
            <button
              type="submit"
              class="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-medium text-white hover:bg-cyan-700"
              :disabled="saving"
            >
              {{ saving ? 'Đang lưu...' : editingLesson ? 'Cập nhật' : 'Thêm' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { contentService, type Module, type Lesson, type ID } from '@/services/content.service'
import { courseService } from '@/services/course.service'
import { showToast } from '@/utils/toast'
import { showConfirm } from '@/utils/confirm'

const route = useRoute()
const router = useRouter()

const courseId = Array.isArray(route.params.id) ? route.params.id[0] : String(route.params.id || '')
const courseTitle = ref('')
const modules = ref<Module[]>([])
const lessonsByModule = ref<Record<string, Lesson[]>>({})
const loading = ref(true)
const error = ref('')
const saving = ref(false)

// Module form
const showAddModule = ref(false)
const editingModule = ref<Module | null>(null)
const moduleForm = ref({ title: '' })

// Lesson form
const showAddLessonModuleId = ref<string | null>(null)
const editingLesson = ref<Lesson | null>(null)
const videoFileInput = ref<HTMLInputElement | null>(null)
const lessonForm = ref<{ 
  title: string
  content_type: Lesson['content_type']
  video_url: string
  videoType: 'url' | 'file'
  videoFile: File | null
}>({ 
  title: '', 
  content_type: 'lesson',
  video_url: '',
  videoType: 'url',
  videoFile: null
})

async function loadCourse() {
  try {
    const course = await courseService.detail(courseId, true)
    courseTitle.value = course.title
  } catch (e: any) {
    console.error('Error loading course:', e)
  }
}

async function loadModules() {
  try {
    modules.value = await contentService.listModules(courseId)
    // Load lessons for each module
    for (const module of modules.value) {
      lessonsByModule.value[String(module.id)] = await contentService.listLessons(module.id)
    }
  } catch (e: any) {
    error.value = e?.message || 'Không thể tải danh sách chương'
  } finally {
    loading.value = false
  }
}

function showAddLesson(moduleId: ID) {
  showAddLessonModuleId.value = String(moduleId)
  lessonForm.value = { 
    title: '', 
    content_type: 'lesson', 
    video_url: '',
    videoType: 'url',
    videoFile: null
  }
  editingLesson.value = null
  if (videoFileInput.value) {
    videoFileInput.value.value = ''
  }
}

function onVideoFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    const file = input.files[0]
    // Validate file type
    if (!file.type.startsWith('video/')) {
      showToast('Vui lòng chọn file video hợp lệ', 'error')
      input.value = ''
      lessonForm.value.videoFile = null
      return
    }
    // Validate file size (500MB max)
    const maxSize = 500 * 1024 * 1024 // 500MB
    if (file.size > maxSize) {
      showToast('File video quá lớn. Tối đa 500MB', 'error')
      input.value = ''
      lessonForm.value.videoFile = null
      return
    }
    lessonForm.value.videoFile = file
  } else {
    lessonForm.value.videoFile = null
  }
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

function editModule(module: Module) {
  editingModule.value = module
  moduleForm.value = { title: module.title }
  showAddModule.value = true
}

function editLesson(lesson: Lesson) {
  editingLesson.value = lesson
  lessonForm.value = { 
    title: lesson.title, 
    content_type: lesson.content_type,
    video_url: (lesson as any).video_url || ''
  }
  showAddLessonModuleId.value = String(lesson.module)
}

function goEditLesson(lessonId: string) {
  router.push({ name: 'teacher-lesson-edit', params: { id: lessonId } })
}

function closeModuleModal() {
  showAddModule.value = false
  editingModule.value = null
  moduleForm.value = { title: '' }
}

function closeLessonModal() {
  showAddLessonModuleId.value = null
  editingLesson.value = null
  lessonForm.value = { 
    title: '', 
    content_type: 'lesson', 
    video_url: '',
    videoType: 'url',
    videoFile: null
  }
  if (videoFileInput.value) {
    videoFileInput.value.value = ''
  }
}

async function saveModule() {
  if (!moduleForm.value.title.trim()) return
  saving.value = true
  try {
    if (editingModule.value) {
      await contentService.updateModule(editingModule.value.id, moduleForm.value)
    } else {
      await contentService.createModule(courseId, {
        title: moduleForm.value.title,
        course: courseId
      })
    }
    closeModuleModal()
    await loadModules()
  } catch (e: any) {
    showToast(e?.message || 'Không thể lưu chương', 'error')
  } finally {
    saving.value = false
  }
}

async function saveLesson() {
  if (!lessonForm.value.title.trim() || !showAddLessonModuleId.value) return
  saving.value = true
  try {
    if (editingLesson.value) {
      // Update existing lesson
      if (lessonForm.value.videoType === 'file' && lessonForm.value.videoFile) {
        // Upload video file using FormData
        const formData = new FormData()
        formData.append('title', lessonForm.value.title)
        formData.append('content_type', lessonForm.value.content_type)
        formData.append('video_file', lessonForm.value.videoFile)
        await contentService.updateLesson(editingLesson.value.id, formData)
      } else {
        // Update with video_url or other fields
        const lessonData: any = {
          title: lessonForm.value.title,
          content_type: lessonForm.value.content_type
        }
        if (lessonForm.value.video_url && lessonForm.value.video_url.trim()) {
          lessonData.video_url = lessonForm.value.video_url.trim()
        }
        await contentService.updateLesson(editingLesson.value.id, lessonData)
      }
    } else {
      // Create new lesson
      if (lessonForm.value.videoType === 'file' && lessonForm.value.videoFile) {
        // Create lesson with video file using FormData
        const formData = new FormData()
        formData.append('title', lessonForm.value.title)
        formData.append('content_type', lessonForm.value.content_type)
        formData.append('module', String(showAddLessonModuleId.value))
        formData.append('video_file', lessonForm.value.videoFile)
        // Create lesson with FormData (backend will handle it)
        await contentService.createLesson(showAddLessonModuleId.value, formData as any)
      } else {
        // Create lesson with video_url or without video
        const lessonData: any = {
          title: lessonForm.value.title,
          content_type: lessonForm.value.content_type,
          module: showAddLessonModuleId.value
        }
        
        // Add video_url if provided
        if (lessonForm.value.videoType === 'url' && lessonForm.value.video_url && lessonForm.value.video_url.trim()) {
          lessonData.video_url = lessonForm.value.video_url.trim()
        }
        
        await contentService.createLesson(showAddLessonModuleId.value, lessonData)
      }
    }
    closeLessonModal()
    await loadModules()
    showToast('Đã lưu bài học thành công', 'success')
  } catch (e: any) {
    console.error('Error saving lesson:', e)
    showToast(e?.response?.data?.detail || e?.message || 'Không thể lưu bài học', 'error')
  } finally {
    saving.value = false
  }
}

async function deleteModule(moduleId: ID) {
  const confirmed = await showConfirm({
    message: 'Bạn có chắc muốn xóa chương này? Tất cả bài học trong chương cũng sẽ bị xóa.',
    title: 'Xác nhận xóa chương',
    type: 'danger',
    confirmText: 'Xóa',
    cancelText: 'Hủy'
  })
  if (!confirmed) return
  try {
    await contentService.deleteModule(moduleId)
    showToast('Đã xóa chương thành công', 'success')
    await loadModules()
  } catch (e: any) {
    showToast(e?.message || 'Không thể xóa chương', 'error')
  }
}

async function deleteLesson(lessonId: ID) {
  const confirmed = await showConfirm({
    message: 'Bạn có chắc muốn xóa bài học này?',
    title: 'Xác nhận xóa bài học',
    type: 'danger',
    confirmText: 'Xóa',
    cancelText: 'Hủy'
  })
  if (!confirmed) return
  try {
    await contentService.deleteLesson(lessonId)
    showToast('Đã xóa bài học thành công', 'success')
    await loadModules()
  } catch (e: any) {
    showToast(e?.message || 'Không thể xóa bài học', 'error')
  }
}

onMounted(async () => {
  await loadCourse()
  await loadModules()
})
</script>
