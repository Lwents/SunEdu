<!-- src/pages/teacher/courses/CourseContent.vue -->
<template>
  <div class="mx-auto max-w-6xl p-6">
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <button
          type="button"
          class="inline-flex items-center gap-2 rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-slate-50 transition"
          @click="goBack"
        >
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Quay lại
        </button>
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">
            Quản lý nội dung khóa học
          </h1>
          <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">{{ courseTitle }}</p>
        </div>
      </div>
      <button
        class="rounded-xl bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700"
        @click="openAddModule"
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
            <div
              class="flex h-10 w-10 items-center justify-center rounded-lg bg-cyan-100 text-cyan-700 font-bold"
            >
              {{ mIdx + 1 }}
            </div>
            <div>
              <h3 class="font-semibold text-gray-900 dark:text-gray-100">{{ module.title }}</h3>
              <p class="text-xs text-gray-500">
                {{ lessonsByModule[module.id]?.length || 0 }} bài học
              </p>
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
                  {{ getContentTypeLabel(lesson.content_type) }}
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
          <div
            v-if="!lessonsByModule[module.id]?.length"
            class="px-6 py-8 text-center text-sm text-gray-500"
          >
            Chưa có bài học nào. Nhấn "+ Thêm bài học" để thêm.
          </div>
        </div>
      </div>

      <div
        v-if="!modules.length"
        class="rounded-2xl border-2 border-dashed border-slate-300 bg-slate-50 p-12 text-center"
      >
        <p class="text-gray-600 dark:text-gray-400">
          Chưa có chương nào. Nhấn "+ Thêm chương mới" để bắt đầu.
        </p>
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
          <!-- Loại nội dung -->
          <div class="mb-4">
            <label class="mb-2 block text-sm font-medium text-gray-700">Loại nội dung</label>
            <div class="grid grid-cols-2 gap-2">
              <button
                v-for="option in contentTypeOptions"
                :key="option.value"
                type="button"
                :class="[
                  'flex items-center gap-2 rounded-lg border px-3 py-2 text-sm font-medium transition',
                  lessonForm.content_type === option.value
                    ? 'border-cyan-500 bg-cyan-50 text-cyan-700'
                    : 'border-slate-300 bg-white text-gray-700 hover:bg-slate-50'
                ]"
                @click="lessonForm.content_type = option.value"
              >
                <span>{{ option.icon }}</span>
                <span>{{ option.label }}</span>
              </button>
            </div>
          </div>

          <!-- Video Section (chỉ hiện khi chọn video hoặc lesson) -->
          <div v-if="lessonForm.content_type === 'video' || lessonForm.content_type === 'lesson'" class="mb-4">
            <label class="mb-2 block text-sm font-medium text-gray-700">Video</label>
            <div class="mb-2 flex gap-2">
              <button
                type="button"
                class="flex-1 rounded-lg border px-3 py-2 text-sm font-medium transition"
                :class="
                  lessonForm.videoType === 'url'
                    ? 'border-cyan-500 bg-cyan-50 text-cyan-700'
                    : 'border-slate-300 bg-white text-gray-700 hover:bg-slate-50'
                "
                @click="lessonForm.videoType = 'url'"
              >
                Video URL
              </button>
              <button
                type="button"
                class="flex-1 rounded-lg border px-3 py-2 text-sm font-medium transition"
                :class="
                  lessonForm.videoType === 'file'
                    ? 'border-cyan-500 bg-cyan-50 text-cyan-700'
                    : 'border-slate-300 bg-white text-gray-700 hover:bg-slate-50'
                "
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
                Đã chọn: {{ lessonForm.videoFile.name }} ({{
                  formatFileSize(lessonForm.videoFile.size)
                }})
              </p>
              <p v-else class="mt-1 text-xs text-gray-500">
                Chọn file video (MP4, AVI, MOV, v.v.) - Tối đa 500MB
              </p>
            </div>
          </div>

          <!-- PDF Upload -->
          <div v-if="lessonForm.content_type === 'pdf'" class="mb-4">
            <label class="mb-2 block text-sm font-medium text-gray-700">Tải lên file PDF</label>
            <input
              ref="documentFileInput"
              type="file"
              accept=".pdf"
              class="w-full rounded-lg border border-slate-300 px-4 py-2 text-sm focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/20"
              @change="onDocumentFileChange"
            />
            <p v-if="lessonForm.documentFile" class="mt-1 text-xs text-emerald-600">
              Đã chọn: {{ lessonForm.documentFile.name }} ({{ formatFileSize(lessonForm.documentFile.size) }})
            </p>
            <p v-else class="mt-1 text-xs text-gray-500">Tối đa 50MB</p>
          </div>

          <!-- Document (Word) Upload -->
          <div v-if="lessonForm.content_type === 'document'" class="mb-4">
            <label class="mb-2 block text-sm font-medium text-gray-700">Tải lên tài liệu Word</label>
            <input
              ref="documentFileInput"
              type="file"
              accept=".doc,.docx,.odt"
              class="w-full rounded-lg border border-slate-300 px-4 py-2 text-sm focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/20"
              @change="onDocumentFileChange"
            />
            <p v-if="lessonForm.documentFile" class="mt-1 text-xs text-emerald-600">
              Đã chọn: {{ lessonForm.documentFile.name }} ({{ formatFileSize(lessonForm.documentFile.size) }})
            </p>
            <p v-else class="mt-1 text-xs text-gray-500">Hỗ trợ: DOC, DOCX, ODT. Tối đa 50MB</p>
          </div>

          <!-- Text Content -->
          <div v-if="lessonForm.content_type === 'text'" class="mb-4">
            <label class="mb-2 block text-sm font-medium text-gray-700">Nội dung văn bản</label>
            <textarea
              v-model="lessonForm.text_content"
              rows="5"
              class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-cyan-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/20"
              placeholder="Nhập nội dung bài học..."
            ></textarea>
            <p class="mt-1 text-xs text-gray-500">Bạn có thể thêm nội dung chi tiết sau</p>
          </div>

          <!-- Exercise Notice -->
          <div v-if="lessonForm.content_type === 'exercise'" class="mb-4">
            <div class="rounded-lg border border-amber-200 bg-amber-50 p-3">
              <p class="text-sm text-amber-700">
                ✏️ Bài tập sẽ được tạo. Bạn có thể thêm câu hỏi và đáp án sau khi tạo bài học.
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
const documentFileInput = ref<HTMLInputElement | null>(null)

const contentTypeOptions = [
  { value: 'video', label: 'Video bài giảng', icon: '🎬' },
  { value: 'pdf', label: 'Tài liệu PDF', icon: '📄' },
  { value: 'text', label: 'Văn bản', icon: '📝' },
  { value: 'exercise', label: 'Bài tập', icon: '✏️' },
  { value: 'document', label: 'Tài liệu Word', icon: '📑' },
  { value: 'lesson', label: 'Bài học (cơ bản)', icon: '📚' },
]

function getContentTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    video: '🎬 Video',
    pdf: '📄 PDF',
    text: '📝 Văn bản',
    exercise: '✏️ Bài tập',
    document: '📑 Word',
    lesson: '📚 Bài học',
    exploration: '🔍 Khám phá',
  }
  return labels[type] || type
}

const lessonForm = ref<{
  title: string
  content_type: string
  video_url: string
  videoType: 'url' | 'file'
  videoFile: File | null
  documentFile: File | null
  text_content: string
}>({
  title: '',
  content_type: 'video',
  video_url: '',
  videoType: 'url',
  videoFile: null,
  documentFile: null,
  text_content: '',
})

async function loadCourse() {
  try {
    const course = await courseService.detail(courseId)
    courseTitle.value = course.title
  } catch (e: any) {
    console.error('Error loading course:', e)
  }
}

async function loadModules() {
  try {
    lessonsByModule.value = {}
    modules.value = await contentService.listModules(courseId)
    await Promise.all(
      modules.value.map(async (module) => {
        lessonsByModule.value[String(module.id)] = await contentService.listLessons(module.id)
      }),
    )
  } catch (e: any) {
    error.value = e?.message || 'Không thể tải danh sách chương'
  } finally {
    loading.value = false
  }
}

function showAddLesson(moduleId: ID) {
  showAddLessonModuleId.value = String(moduleId)
  
  // Tự động tạo tên bài học: X.Y (X = số chương, Y = số bài tiếp theo)
  const moduleIndex = modules.value.findIndex(m => String(m.id) === String(moduleId))
  const moduleNumber = moduleIndex + 1
  const lessonsInModule = lessonsByModule.value[String(moduleId)] || []
  const lessonNumber = lessonsInModule.length + 1
  const autoTitle = `Bài ${moduleNumber}.${lessonNumber}`
  
  lessonForm.value = {
    title: autoTitle,
    content_type: 'video',
    video_url: '',
    videoType: 'url',
    videoFile: null,
    documentFile: null,
    text_content: '',
  }
  editingLesson.value = null
  if (videoFileInput.value) {
    videoFileInput.value.value = ''
  }
  if (documentFileInput.value) {
    documentFileInput.value.value = ''
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
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

function onDocumentFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    const file = input.files[0]
    // Validate file size (50MB max)
    const maxSize = 50 * 1024 * 1024 // 50MB
    if (file.size > maxSize) {
      showToast('File quá lớn. Tối đa 50MB', 'error')
      input.value = ''
      lessonForm.value.documentFile = null
      return
    }
    lessonForm.value.documentFile = file
  } else {
    lessonForm.value.documentFile = null
  }
}

function openAddModule() {
  // Tự động tạo tên chương: "Chương X" (X = số chương tiếp theo)
  moduleForm.value = { title: getNextModuleLabel() }
  editingModule.value = null
  showAddModule.value = true
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
    content_type: lesson.content_type || 'video',
    video_url: (lesson as any).video_url || '',
    videoType: 'url',
    videoFile: null,
    documentFile: null,
    text_content: (lesson as any).text_content || '',
  }
  showAddLessonModuleId.value = String(lesson.module)
}

function goEditLesson(lessonId: string) {
  router.push({ name: 'teacher-lesson-edit', params: { id: lessonId } })
}

function closeModuleModal() {
  showAddModule.value = false
  editingModule.value = null
  // Không reset title để giữ lại giá trị cho lần sau
  // moduleForm.value = { title: '' }
}

function closeLessonModal() {
  showAddLessonModuleId.value = null
  editingLesson.value = null
  // Không reset form để giữ lại giá trị cho lần sau
  // Chỉ reset file inputs
  lessonForm.value.videoFile = null
  lessonForm.value.video_url = ''
  lessonForm.value.documentFile = null
  lessonForm.value.text_content = ''
  if (videoFileInput.value) {
    videoFileInput.value.value = ''
  }
  if (documentFileInput.value) {
    documentFileInput.value.value = ''
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
        course: courseId,
        position: getNextModulePosition(),
      })
    }
    if (!editingModule.value) {
      // Nếu là thêm mới, giữ lại form để có thể thêm tiếp
      // Không đóng modal, chỉ reload danh sách
      await loadModules()
      moduleForm.value.title = getNextModuleLabel()
      showToast('Đã thêm chương thành công', 'success')
    } else {
      // Nếu là sửa, đóng modal
      closeModuleModal()
      await loadModules()
    }
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
    const currentTitle = lessonForm.value.title
    const moduleId = showAddLessonModuleId.value
    const nextLessonPosition = getNextLessonPosition(moduleId)

    // Kiểm tra có file cần upload không
    const hasVideoFile = lessonForm.value.videoFile && (lessonForm.value.content_type === 'video' || lessonForm.value.content_type === 'lesson')
    const hasDocumentFile = lessonForm.value.documentFile && (lessonForm.value.content_type === 'pdf' || lessonForm.value.content_type === 'document')
    const needsFormData = hasVideoFile || hasDocumentFile

    if (editingLesson.value) {
      // Update existing lesson
      if (needsFormData) {
        const formData = new FormData()
        formData.append('title', lessonForm.value.title)
        formData.append('content_type', lessonForm.value.content_type)
        if (hasVideoFile) {
          formData.append('video_file', lessonForm.value.videoFile!)
        }
        if (hasDocumentFile) {
          formData.append('document_file', lessonForm.value.documentFile!)
        }
        if (lessonForm.value.text_content) {
          formData.append('text_content', lessonForm.value.text_content)
        }
        await contentService.updateLesson(editingLesson.value.id, formData)
      } else {
        const lessonData: any = {
          title: lessonForm.value.title,
          content_type: lessonForm.value.content_type,
        }
        if (lessonForm.value.video_url && lessonForm.value.video_url.trim()) {
          lessonData.video_url = lessonForm.value.video_url.trim()
        }
        if (lessonForm.value.text_content) {
          lessonData.text_content = lessonForm.value.text_content
        }
        await contentService.updateLesson(editingLesson.value.id, lessonData)
      }
      closeLessonModal()
      await loadModules()
      showToast('Đã cập nhật bài học thành công', 'success')
    } else {
      // Create new lesson
      if (needsFormData) {
        const formData = new FormData()
        formData.append('title', lessonForm.value.title)
        formData.append('content_type', lessonForm.value.content_type)
        formData.append('module', String(moduleId))
        formData.append('position', String(nextLessonPosition))
        if (hasVideoFile) {
          formData.append('video_file', lessonForm.value.videoFile!)
        }
        if (hasDocumentFile) {
          formData.append('document_file', lessonForm.value.documentFile!)
        }
        if (lessonForm.value.text_content) {
          formData.append('text_content', lessonForm.value.text_content)
        }
        await contentService.createLesson(moduleId, formData as any)
      } else {
        const lessonData: any = {
          title: lessonForm.value.title,
          content_type: lessonForm.value.content_type,
          module: moduleId,
          position: nextLessonPosition,
        }
        if (
          lessonForm.value.videoType === 'url' &&
          lessonForm.value.video_url &&
          lessonForm.value.video_url.trim()
        ) {
          lessonData.video_url = lessonForm.value.video_url.trim()
        }
        if (lessonForm.value.text_content) {
          lessonData.text_content = lessonForm.value.text_content
        }
        await contentService.createLesson(moduleId, lessonData)
      }
      
      // Tự động tăng số bài học cho lần sau
      await loadModules() // Reload để có số bài học mới nhất
      const moduleIndex = modules.value.findIndex(m => String(m.id) === String(moduleId))
      const moduleNumber = moduleIndex + 1
      const lessonsInModule = lessonsByModule.value[String(moduleId)] || []
      const nextLessonNumber = lessonsInModule.length + 1
      
      // Tự động tạo tên bài học tiếp theo
      lessonForm.value.title = `Bài ${moduleNumber}.${nextLessonNumber}`
      // Reset fields để có thể thêm tiếp
      lessonForm.value.videoFile = null
      lessonForm.value.video_url = ''
      lessonForm.value.documentFile = null
      lessonForm.value.text_content = ''
      if (videoFileInput.value) {
        videoFileInput.value.value = ''
      }
      if (documentFileInput.value) {
        documentFileInput.value.value = ''
      }
      
      showToast('Đã thêm bài học thành công', 'success')
      // Không đóng modal để có thể thêm tiếp
    }
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
    cancelText: 'Hủy',
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
    cancelText: 'Hủy',
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

function getNextModulePosition() {
  if (!modules.value.length) return 1
  const maxPos = Math.max(
    ...modules.value.map((m, idx) => (typeof m.position === 'number' ? m.position : idx + 1)),
  )
  return maxPos + 1
}

function getNextModuleLabel() {
  return `Chương ${getNextModulePosition()}`
}

function getNextLessonPosition(moduleId: ID) {
  const lessons = lessonsByModule.value[String(moduleId)] || []
  if (!lessons.length) return 1
  const maxPos = Math.max(
    ...lessons.map((lesson, idx) =>
      typeof lesson.position === 'number' ? lesson.position : idx + 1,
    ),
  )
  return maxPos + 1
}

function goBack() {
  // Lưu tất cả thay đổi trước khi quay lại
  // Các thay đổi đã được lưu tự động khi user thêm/sửa/xóa
  router.push({ name: 'teacher-courses' }).catch(() => {
    window.history.length > 1 ? window.history.back() : router.push('/teacher/courses')
  })
}

onMounted(async () => {
  await loadCourse()
  await loadModules()
})
</script>
