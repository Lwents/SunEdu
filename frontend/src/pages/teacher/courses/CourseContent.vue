<!-- src/pages/teacher/courses/CourseContent.vue -->
<template>
  <div class="mx-auto max-w-6xl p-6">
    <div class="mb-6 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <button type="button" :class="secondaryBtnClass" @click="goBack">
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Quay lại
        </button>
        <div>
          <h1 :class="isDark ? 'text-white' : 'text-gray-900'" class="text-2xl font-bold">Quản lý nội dung khóa học</h1>
          <p :class="isDark ? 'text-gray-400' : 'text-gray-600'" class="mt-1 text-sm">{{ courseTitle }}</p>
        </div>
      </div>
      <button :class="primaryBtnClass" @click="openAddModule">+ Thêm chương mới</button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="h-32 rounded-2xl animate-pulse" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'" />
    </div>

    <!-- Error -->
    <div v-else-if="error" class="rounded-xl border p-4" :class="isDark ? 'border-rose-500/30 bg-rose-500/10 text-rose-400' : 'border-rose-200 bg-rose-50 text-rose-700'">
      {{ error }}
    </div>

    <!-- Modules List -->
    <div v-else class="space-y-4">
      <div v-for="(module, mIdx) in modules" :key="module.id" :class="cardClass" class="rounded-2xl">
        <!-- Module Header -->
        <div class="flex items-center justify-between px-6 py-4 border-b" :class="isDark ? 'border-white/5' : 'border-slate-100'">
          <div class="flex items-center gap-4">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg font-bold" :class="isDark ? 'bg-cyan-500/20 text-cyan-400' : 'bg-cyan-100 text-cyan-700'">
              {{ mIdx + 1 }}
            </div>
            <div>
              <h3 :class="isDark ? 'text-white' : 'text-gray-900'" class="font-semibold">{{ module.title }}</h3>
              <p :class="isDark ? 'text-gray-500' : 'text-gray-500'" class="text-xs">{{ lessonsByModule[module.id]?.length || 0 }} bài học</p>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <button :class="smallBtnClass" @click="editModule(module)">Sửa</button>
            <button :class="smallBtnClass" @click="showAddLesson(module.id)">+ Thêm bài học</button>
            <button :class="smallDangerBtnClass" @click="deleteModule(module.id)">Xóa</button>
          </div>
        </div>

        <!-- Lessons List -->
        <div class="divide-y" :class="isDark ? 'divide-white/5' : 'divide-slate-100'">
          <div v-for="(lesson, lIdx) in lessonsByModule[module.id] || []" :key="lesson.id" 
               class="flex items-center justify-between px-6 py-3 transition" :class="isDark ? 'hover:bg-white/5' : 'hover:bg-slate-50'">
            <div class="flex items-center gap-4">
              <span :class="isDark ? 'text-gray-500' : 'text-gray-500'" class="text-sm font-medium">{{ mIdx + 1 }}.{{ lIdx + 1 }}</span>
              <div>
                <p :class="isDark ? 'text-gray-200' : 'text-gray-900'" class="font-medium">{{ lesson.title }}</p>
                <p :class="isDark ? 'text-gray-500' : 'text-gray-500'" class="text-xs">
                  {{ getContentTypeLabel(lesson.content_type) }}
                  <span v-if="lesson.published" class="ml-2 text-emerald-500">• Đã xuất bản</span>
                  <span v-else class="ml-2 text-amber-500">• Nháp</span>
                </p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <button :class="smallBtnClass" @click="goEditLesson(String(lesson.id))">Sửa</button>
              <button :class="smallDangerBtnClass" @click="deleteLesson(lesson.id)">Xóa</button>
            </div>
          </div>
          <div v-if="!lessonsByModule[module.id]?.length" :class="isDark ? 'text-gray-500' : 'text-gray-500'" class="px-6 py-8 text-center text-sm">
            Chưa có bài học nào. Nhấn "+ Thêm bài học" để thêm.
          </div>
        </div>
      </div>

      <div v-if="!modules.length" class="rounded-2xl border-2 border-dashed p-12 text-center" :class="isDark ? 'border-slate-700 bg-slate-900/50' : 'border-slate-300 bg-slate-50'">
        <p :class="isDark ? 'text-gray-400' : 'text-gray-600'">Chưa có chương nào. Nhấn "+ Thêm chương mới" để bắt đầu.</p>
      </div>
    </div>

    <!-- Add/Edit Module Modal -->
    <div v-if="showAddModule || editingModule" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4" @click.self="closeModuleModal">
      <div :class="modalClass" class="w-full max-w-md rounded-2xl p-6">
        <h2 :class="isDark ? 'text-white' : 'text-gray-900'" class="mb-4 text-xl font-bold">{{ editingModule ? 'Sửa chương' : 'Thêm chương mới' }}</h2>
        <form @submit.prevent="saveModule">
          <div class="mb-4">
            <label :class="labelClass">Tên chương</label>
            <input v-model="moduleForm.title" type="text" :class="inputClass" placeholder="Ví dụ: Chương 1 - Giới thiệu" required />
          </div>
          <div class="flex justify-end gap-3">
            <button type="button" :class="cancelBtnClass" @click="closeModuleModal">Hủy</button>
            <button type="submit" :class="primaryBtnClass" :disabled="saving">{{ saving ? 'Đang lưu...' : editingModule ? 'Cập nhật' : 'Thêm' }}</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Add/Edit Lesson Modal -->
    <div v-if="showAddLessonModuleId || editingLesson" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4" @click.self="closeLessonModal">
      <div :class="modalClass" class="w-full max-w-md rounded-2xl p-6 max-h-[90vh] overflow-y-auto">
        <h2 :class="isDark ? 'text-white' : 'text-gray-900'" class="mb-4 text-xl font-bold">{{ editingLesson ? 'Sửa bài học' : 'Thêm bài học mới' }}</h2>
        <form @submit.prevent="saveLesson">
          <div class="mb-4">
            <label :class="labelClass">Tên bài học</label>
            <input v-model="lessonForm.title" type="text" :class="inputClass" placeholder="Ví dụ: Bài 1 - Khái niệm cơ bản" required />
          </div>
          
          <!-- Loại nội dung -->
          <div class="mb-4">
            <label :class="labelClass">Loại nội dung</label>
            <div class="grid grid-cols-2 gap-2">
              <button v-for="option in contentTypeOptions" :key="option.value" type="button"
                :class="[
                  'flex items-center gap-2 rounded-lg border px-3 py-2 text-sm font-medium transition',
                  lessonForm.content_type === option.value
                    ? (isDark ? 'border-cyan-500 bg-cyan-500/20 text-cyan-400' : 'border-cyan-500 bg-cyan-50 text-cyan-700')
                    : (isDark ? 'border-slate-700 text-gray-300 hover:bg-white/5' : 'border-slate-300 bg-white text-gray-700 hover:bg-slate-50')
                ]"
                @click="lessonForm.content_type = option.value">
                <span>{{ option.icon }}</span>
                <span>{{ option.label }}</span>
              </button>
            </div>
          </div>

          <!-- Video Section -->
          <div v-if="lessonForm.content_type === 'video' || lessonForm.content_type === 'lesson'" class="mb-4">
            <label :class="labelClass">Video</label>
            <div class="mb-2 flex gap-2">
              <button type="button" class="flex-1 rounded-lg border px-3 py-2 text-sm font-medium transition"
                :class="lessonForm.videoType === 'url' ? (isDark ? 'border-cyan-500 bg-cyan-500/20 text-cyan-400' : 'border-cyan-500 bg-cyan-50 text-cyan-700') : (isDark ? 'border-slate-700 text-gray-300 hover:bg-white/5' : 'border-slate-300 bg-white text-gray-700 hover:bg-slate-50')"
                @click="lessonForm.videoType = 'url'">Video URL</button>
              <button type="button" class="flex-1 rounded-lg border px-3 py-2 text-sm font-medium transition"
                :class="lessonForm.videoType === 'file' ? (isDark ? 'border-cyan-500 bg-cyan-500/20 text-cyan-400' : 'border-cyan-500 bg-cyan-50 text-cyan-700') : (isDark ? 'border-slate-700 text-gray-300 hover:bg-white/5' : 'border-slate-300 bg-white text-gray-700 hover:bg-slate-50')"
                @click="lessonForm.videoType = 'file'">Tải video lên</button>
            </div>
            <div v-if="lessonForm.videoType === 'url'">
              <input v-model="lessonForm.video_url" type="url" :class="inputClass" placeholder="https://www.youtube.com/watch?v=..." />
              <p :class="hintClass">Có thể thêm sau khi tạo bài học</p>
            </div>
            <div v-else>
              <input ref="videoFileInput" type="file" accept="video/*" :class="inputClass" @change="onVideoFileChange" />
              <p v-if="lessonForm.videoFile" class="mt-1 text-xs text-emerald-500">Đã chọn: {{ lessonForm.videoFile.name }} ({{ formatFileSize(lessonForm.videoFile.size) }})</p>
              <p v-else :class="hintClass">Chọn file video (MP4, AVI, MOV) - Tối đa 500MB</p>
            </div>
          </div>

          <!-- PDF Upload -->
          <div v-if="lessonForm.content_type === 'pdf'" class="mb-4">
            <label :class="labelClass">Tải lên file PDF</label>
            <input ref="documentFileInput" type="file" accept=".pdf" :class="inputClass" @change="onDocumentFileChange" />
            <p v-if="lessonForm.documentFile" class="mt-1 text-xs text-emerald-500">Đã chọn: {{ lessonForm.documentFile.name }}</p>
            <p v-else :class="hintClass">Tối đa 50MB</p>
          </div>

          <!-- Document Upload -->
          <div v-if="lessonForm.content_type === 'document'" class="mb-4">
            <label :class="labelClass">Tải lên tài liệu Word</label>
            <input ref="documentFileInput" type="file" accept=".doc,.docx,.odt" :class="inputClass" @change="onDocumentFileChange" />
            <p v-if="lessonForm.documentFile" class="mt-1 text-xs text-emerald-500">Đã chọn: {{ lessonForm.documentFile.name }}</p>
            <p v-else :class="hintClass">Hỗ trợ: DOC, DOCX, ODT. Tối đa 50MB</p>
          </div>

          <!-- Text Content -->
          <div v-if="lessonForm.content_type === 'text'" class="mb-4">
            <label :class="labelClass">Nội dung văn bản</label>
            <textarea v-model="lessonForm.text_content" rows="5" :class="inputClass" placeholder="Nhập nội dung bài học..." />
            <p :class="hintClass">Bạn có thể thêm nội dung chi tiết sau</p>
          </div>

          <!-- Exercise Notice -->
          <div v-if="lessonForm.content_type === 'exercise'" class="mb-4">
            <div class="rounded-lg border p-3" :class="isDark ? 'border-amber-500/30 bg-amber-500/10' : 'border-amber-200 bg-amber-50'">
              <p :class="isDark ? 'text-amber-400' : 'text-amber-700'" class="text-sm">✏️ Bài tập sẽ được tạo. Bạn có thể thêm câu hỏi và đáp án sau.</p>
            </div>
          </div>

          <div class="flex justify-end gap-3">
            <button type="button" :class="cancelBtnClass" @click="closeLessonModal">Hủy</button>
            <button type="submit" :class="primaryBtnClass" :disabled="saving">{{ saving ? 'Đang lưu...' : editingLesson ? 'Cập nhật' : 'Thêm' }}</button>
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
import { useThemeStore } from '@/store/theme.store'

const route = useRoute()
const router = useRouter()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

// ============ Styles ============
const cardClass = computed(() => isDark.value ? 'bg-slate-900/50' : 'border border-slate-200 bg-white shadow-sm')
const modalClass = computed(() => isDark.value ? 'bg-slate-900' : 'bg-white shadow-xl')
const labelClass = computed(() => ['mb-2 block text-sm font-medium', isDark.value ? 'text-gray-300' : 'text-gray-700'])
const inputClass = computed(() => [
  'w-full rounded-lg border px-4 py-2 outline-none transition',
  isDark.value ? 'bg-slate-800 border-slate-700 text-white placeholder-gray-500 focus:border-cyan-500' : 'border-slate-300 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20'
])
const hintClass = computed(() => ['mt-1 text-xs', isDark.value ? 'text-gray-500' : 'text-gray-500'])
const primaryBtnClass = computed(() => [
  'rounded-xl px-4 py-2 text-sm font-semibold text-white transition disabled:opacity-50',
  isDark.value ? 'bg-cyan-600 hover:bg-cyan-500' : 'bg-cyan-600 hover:bg-cyan-700'
])
const secondaryBtnClass = computed(() => [
  'inline-flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium transition',
  isDark.value ? 'text-gray-300 hover:bg-white/5' : 'border border-slate-300 text-gray-700 hover:bg-slate-50'
])
const cancelBtnClass = computed(() => [
  'rounded-lg px-4 py-2 text-sm font-medium transition',
  isDark.value ? 'text-gray-300 hover:bg-white/5' : 'border border-slate-300 text-gray-700 hover:bg-slate-50'
])
const smallBtnClass = computed(() => [
  'rounded-lg border px-3 py-1.5 text-xs font-medium transition',
  isDark.value ? 'border-slate-700 text-gray-300 hover:bg-white/5' : 'border-slate-200 text-gray-700 hover:bg-slate-50'
])
const smallDangerBtnClass = computed(() => [
  'rounded-lg border px-3 py-1.5 text-xs font-medium transition',
  isDark.value ? 'border-rose-500/30 text-rose-400 hover:bg-rose-500/10' : 'border-rose-200 text-rose-700 hover:bg-rose-50'
])

// ============ Data ============
const courseId = Array.isArray(route.params.id) ? route.params.id[0] : String(route.params.id || '')
const courseTitle = ref('')
const modules = ref<Module[]>([])
const lessonsByModule = ref<Record<string, Lesson[]>>({})
const loading = ref(true)
const error = ref('')
const saving = ref(false)

const showAddModule = ref(false)
const editingModule = ref<Module | null>(null)
const moduleForm = ref({ title: '' })

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
]

const lessonForm = ref<{
  title: string; content_type: string; video_url: string; videoType: 'url' | 'file'
  videoFile: File | null; documentFile: File | null; text_content: string
}>({ title: '', content_type: 'video', video_url: '', videoType: 'url', videoFile: null, documentFile: null, text_content: '' })

// ============ Functions ============
function getContentTypeLabel(type: string): string {
  const labels: Record<string, string> = { video: '🎬 Video', pdf: '📄 PDF', text: '📝 Văn bản', exercise: '✏️ Bài tập', document: '📑 Word', exploration: '🔍 Khám phá' }
  return labels[type] || type
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  const k = 1024, sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

async function loadCourse() {
  try { courseTitle.value = (await courseService.detail(courseId)).title } catch { /* ignore */ }
}

async function loadModules() {
  try {
    lessonsByModule.value = {}
    modules.value = await contentService.listModules(courseId)
    await Promise.all(modules.value.map(async (m) => { lessonsByModule.value[String(m.id)] = await contentService.listLessons(m.id) }))
  } catch (e: any) { error.value = e?.message || 'Không thể tải danh sách chương' }
  finally { loading.value = false }
}

function showAddLesson(moduleId: ID) {
  showAddLessonModuleId.value = String(moduleId)
  const mIdx = modules.value.findIndex(m => String(m.id) === String(moduleId))
  const lessons = lessonsByModule.value[String(moduleId)] || []
  lessonForm.value = { title: `Bài ${mIdx + 1}.${lessons.length + 1}`, content_type: 'video', video_url: '', videoType: 'url', videoFile: null, documentFile: null, text_content: '' }
  editingLesson.value = null
}

function onVideoFileChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  if (!file.type.startsWith('video/')) { showToast('Vui lòng chọn file video hợp lệ', 'error'); return }
  if (file.size > 500 * 1024 * 1024) { showToast('File video quá lớn. Tối đa 500MB', 'error'); return }
  lessonForm.value.videoFile = file
}

function onDocumentFileChange(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  if (file.size > 50 * 1024 * 1024) { showToast('File quá lớn. Tối đa 50MB', 'error'); return }
  lessonForm.value.documentFile = file
}

function openAddModule() { moduleForm.value = { title: `Chương ${modules.value.length + 1}` }; editingModule.value = null; showAddModule.value = true }
function editModule(m: Module) { editingModule.value = m; moduleForm.value = { title: m.title }; showAddModule.value = true }
function closeModuleModal() { showAddModule.value = false; editingModule.value = null }
function closeLessonModal() { showAddLessonModuleId.value = null; editingLesson.value = null }
function goEditLesson(id: string) { router.push({ name: 'teacher-lesson-edit', params: { id } }) }
function goBack() { router.push({ name: 'teacher-courses' }).catch(() => router.push('/teacher/courses')) }

async function saveModule() {
  if (!moduleForm.value.title.trim()) return
  saving.value = true
  try {
    if (editingModule.value) {
      await contentService.updateModule(editingModule.value.id, moduleForm.value)
      closeModuleModal()
    } else {
      await contentService.createModule(courseId, { title: moduleForm.value.title, course: courseId, position: modules.value.length })
      moduleForm.value.title = `Chương ${modules.value.length + 2}`
    }
    await loadModules()
    showToast(editingModule.value ? 'Đã cập nhật chương' : 'Đã thêm chương', 'success')
  } catch (e: any) { showToast(e?.message || 'Không thể lưu chương', 'error') }
  finally { saving.value = false }
}

async function saveLesson() {
  if (!lessonForm.value.title.trim() || !showAddLessonModuleId.value) return
  saving.value = true
  const moduleId = showAddLessonModuleId.value
  try {
    const hasFile = lessonForm.value.videoFile || lessonForm.value.documentFile
    if (hasFile) {
      const fd = new FormData()
      fd.append('title', lessonForm.value.title)
      fd.append('content_type', lessonForm.value.content_type)
      fd.append('module', moduleId)
      fd.append('position', String((lessonsByModule.value[moduleId]?.length || 0) + 1))
      if (lessonForm.value.videoFile) fd.append('video_file', lessonForm.value.videoFile)
      if (lessonForm.value.documentFile) fd.append('document_file', lessonForm.value.documentFile)
      if (lessonForm.value.text_content) fd.append('text_content', lessonForm.value.text_content)
      await contentService.createLesson(moduleId, fd as any)
    } else {
      const data: any = { title: lessonForm.value.title, content_type: lessonForm.value.content_type, module: moduleId, position: (lessonsByModule.value[moduleId]?.length || 0) + 1 }
      if (lessonForm.value.video_url?.trim()) data.video_url = lessonForm.value.video_url.trim()
      if (lessonForm.value.text_content) data.text_content = lessonForm.value.text_content
      await contentService.createLesson(moduleId, data)
    }
    await loadModules()
    const mIdx = modules.value.findIndex(m => String(m.id) === moduleId)
    lessonForm.value = { title: `Bài ${mIdx + 1}.${(lessonsByModule.value[moduleId]?.length || 0) + 1}`, content_type: 'video', video_url: '', videoType: 'url', videoFile: null, documentFile: null, text_content: '' }
    showToast('Đã thêm bài học', 'success')
  } catch (e: any) { showToast(e?.response?.data?.detail || e?.message || 'Không thể lưu bài học', 'error') }
  finally { saving.value = false }
}

async function deleteModule(id: ID) {
  if (!await showConfirm({ message: 'Bạn có chắc muốn xóa chương này?', title: 'Xác nhận xóa', type: 'danger', confirmText: 'Xóa', cancelText: 'Hủy' })) return
  try { await contentService.deleteModule(id); await loadModules(); showToast('Đã xóa chương', 'success') }
  catch (e: any) { showToast(e?.message || 'Không thể xóa chương', 'error') }
}

async function deleteLesson(id: ID) {
  if (!await showConfirm({ message: 'Bạn có chắc muốn xóa bài học này?', title: 'Xác nhận xóa', type: 'danger', confirmText: 'Xóa', cancelText: 'Hủy' })) return
  try { await contentService.deleteLesson(id); await loadModules(); showToast('Đã xóa bài học', 'success') }
  catch (e: any) { showToast(e?.message || 'Không thể xóa bài học', 'error') }
}

onMounted(async () => { await loadCourse(); await loadModules() })
</script>
