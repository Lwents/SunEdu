<template>
  <div class="mx-auto max-w-5xl p-6 lg:p-8">
    <!-- Loading -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="h-32 rounded-2xl animate-pulse" :class="isDark ? 'bg-slate-800' : 'bg-slate-200'" />
    </div>

    <!-- Error -->
    <div v-else-if="err" class="rounded-xl border p-4" :class="isDark ? 'border-rose-500/30 bg-rose-500/10 text-rose-400' : 'border-rose-200 bg-rose-50 text-rose-700'">
      {{ err }}
    </div>

    <!-- Form -->
    <form v-else-if="course" @submit.prevent="save" class="space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 :class="pageTitleClass">Chỉnh sửa khoá học</h1>
          <p :class="pageSubtitleClass">Cập nhật thông tin chi tiết cho khoá học của bạn</p>
        </div>
        <button type="submit" :class="primaryButtonSmClass" :disabled="saving || !course.title?.trim()">
          {{ saving ? 'Đang lưu...' : 'Lưu thay đổi' }}
        </button>
      </div>

      <!-- Thông tin cơ bản -->
      <div :class="sectionCardClass">
        <h2 :class="sectionTitleClass" class="mb-4">Thông tin cơ bản</h2>
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
          <!-- Tên khoá học -->
          <label class="md:col-span-2">
            <span :class="labelClass">Tên khoá học <span class="text-rose-500">*</span></span>
            <input
              v-model.trim="course.title"
              type="text"
              required
              :class="inputClass"
              placeholder="Nhập tên khoá học"
            />
          </label>

          <!-- Khối lớp -->
          <div>
            <span :class="labelClass">Khối lớp</span>
            <div :class="readonlyFieldClass">Lớp {{ course.grade }}</div>
          </div>

          <!-- Môn học -->
          <div>
            <span :class="labelClass">Môn học</span>
            <div :class="readonlyFieldClass">{{ subjectLabel(course.subject) }}</div>
          </div>

          <!-- Giá khóa học -->
          <label class="md:col-span-2">
            <span :class="labelClass">Giá khóa học (VNĐ)</span>
            <input v-model.number="course.price" type="number" min="0" step="1000" :class="inputClass" placeholder="0" />
            <p :class="hintClass">Nhập 0 để khóa học miễn phí</p>
          </label>

          <!-- Mô tả ngắn -->
          <label class="md:col-span-2">
            <span :class="labelClass">Mô tả ngắn</span>
            <textarea
              v-model.trim="course.description"
              rows="3"
              :class="[inputClass, 'resize-y']"
              placeholder="Mô tả ngắn gọn về khóa học"
            ></textarea>
          </label>

          <!-- Giới thiệu chi tiết -->
          <label class="md:col-span-2">
            <span :class="labelClass">Giới thiệu chi tiết</span>
            <textarea
              v-model.trim="course.introduction"
              rows="8"
              :class="[inputClass, 'resize-y']"
              placeholder="Giới thiệu chi tiết về khóa học (sẽ hiển thị ở trang chi tiết khóa học)"
            ></textarea>
            <p :class="hintClass">Nội dung này sẽ hiển thị ở trang chi tiết khóa học cho học sinh</p>
          </label>
        </div>
      </div>

      <!-- Ảnh khoá học -->
      <div :class="sectionCardClass">
        <h2 :class="sectionTitleClass" class="mb-4">Ảnh khoá học</h2>
        <div class="flex flex-col items-start gap-4 sm:flex-row sm:items-center">
          <div class="relative h-32 w-48 shrink-0 overflow-hidden rounded-lg border" :class="isDark ? 'border-slate-700 bg-slate-800' : 'border-slate-200 bg-slate-100'">
            <img v-if="coverPreview" :src="coverPreview" alt="Ảnh bìa" class="h-full w-full object-cover" />
            <div v-else class="flex h-full items-center justify-center">
              <svg class="h-12 w-12" :class="isDark ? 'text-slate-500' : 'text-slate-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          <div class="flex-1">
            <input ref="coverInput" type="file" accept="image/*" class="hidden" @change="onPickCover" />
            <button type="button" :class="secondaryButtonClass" @click="coverInput?.click()">
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              {{ coverPreview ? 'Đổi ảnh' : 'Chọn ảnh bìa' }}
            </button>
            <p v-if="coverFile" :class="coverFileClass">
              Đã chọn ảnh mới: <b>{{ coverFile.name }}</b> ({{ formatFileSize(coverFile.size) }})
            </p>
            <p :class="hintClass">JPG/PNG, tối đa 5MB. Giữ ảnh cũ nếu không đổi.</p>
          </div>
        </div>
      </div>

      <!-- Quản lý nội dung -->
      <div :class="sectionCardClass">
        <div class="mb-4 flex items-center justify-between">
          <h2 :class="sectionTitleClass">Quản lý nội dung</h2>
          <div class="flex items-center gap-3">
            <button type="button" :class="libraryButtonClass" @click="goToLibrary">
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              Thêm từ thư viện
            </button>
            <button type="button" :class="contentButtonClass" @click="goToContent">
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
              </svg>
              Quản lý nội dung
            </button>
          </div>
        </div>
        <div :class="infoPanelClass">
          <div class="flex items-center gap-4 text-sm" :class="mutedTextClass">
            <div class="flex items-center gap-2">
              <svg class="h-5 w-5" :class="isDark ? 'text-cyan-400' : 'text-cyan-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              <span class="font-medium" :class="strongTextClass">{{ course.lessonsCount || 0 }}</span>
              <span>bài học</span>
            </div>
            <div :class="dividerClass">•</div>
            <p :class="mutedTextClass">
              Quản lý các chương và bài học của khóa học. Bạn có thể thêm nội dung từ thư viện hoặc tạo mới.
            </p>
          </div>
        </div>
      </div>

      <!-- Form Actions -->
      <div class="flex items-center justify-end gap-3 pt-6 border-t" :class="isDark ? 'border-white/5' : 'border-gray-100'">
        <button type="button" :class="cancelButtonClass" @click="router.back()">Huỷ</button>
        <button type="submit" :class="primaryButtonClass" :disabled="saving || !course.title?.trim()">
          {{ saving ? 'Đang lưu…' : 'Lưu thay đổi' }}
        </button>
      </div>
    </form>

    <!-- Not Found -->
    <div v-else class="flex items-center justify-center gap-3 rounded-2xl p-12" :class="emptyCardClass">
      <svg class="h-6 w-6" :class="isDark ? 'text-gray-500' : 'text-gray-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span class="text-lg font-medium" :class="isDark ? 'text-gray-400' : 'text-gray-600'">Không tìm thấy khoá học.</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, reactive, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { courseService, type CourseDetail, type Subject } from '@/services/course.service'
import { resolveMediaUrl } from '@/utils/media'
import { showToast } from '@/utils/toast'
import { useThemeStore } from '@/store/theme.store'

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)

// ============ Styles ============
const pageTitleClass = computed(() => isDark.value ? 'text-2xl font-bold text-white' : 'text-2xl font-bold text-gray-900')
const pageSubtitleClass = computed(() => isDark.value ? 'mt-1 text-sm text-gray-400' : 'mt-1 text-sm text-gray-600')
const sectionCardClass = computed(() => isDark.value ? 'rounded-2xl border border-slate-800 bg-slate-900/60 p-6 shadow-sm' : 'rounded-2xl border border-slate-200 bg-white p-6 shadow-sm')
const sectionTitleClass = computed(() => isDark.value ? 'text-lg font-semibold text-white' : 'text-lg font-semibold text-gray-900')
const emptyCardClass = computed(() => isDark.value ? 'border border-slate-800 bg-slate-900/60' : 'border border-slate-200 bg-white shadow-sm')

const labelClass = computed(() => ['mb-2 block text-sm font-semibold', isDark.value ? 'text-gray-300' : 'text-gray-700'])
const inputClass = computed(() => [
  'w-full rounded-lg border px-4 py-2.5 outline-none transition',
  isDark.value
    ? 'bg-slate-800 border-slate-700 text-white placeholder-gray-500 focus:border-cyan-500'
    : 'bg-white border-gray-300 text-gray-900 placeholder-gray-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20'
])
const readonlyFieldClass = computed(() => [
  'w-full rounded-lg border px-4 py-2.5 font-medium',
  isDark.value ? 'border-slate-700 bg-slate-800 text-slate-200' : 'border-gray-200 bg-gray-50 text-gray-600'
])
const hintClass = computed(() => ['mt-1 text-xs', isDark.value ? 'text-gray-400' : 'text-gray-500'])

const primaryButtonClass = computed(() => [
  'rounded-xl px-6 py-3 font-bold text-white transition disabled:opacity-50 disabled:cursor-not-allowed',
  isDark.value ? 'bg-cyan-600 hover:bg-cyan-500' : 'bg-gradient-to-r from-blue-600 to-blue-800 hover:from-blue-700 hover:to-blue-900'
])
const primaryButtonSmClass = computed(() => [
  'rounded-xl px-4 py-2 text-sm font-semibold text-white transition disabled:opacity-50 disabled:cursor-not-allowed',
  isDark.value ? 'bg-cyan-600 hover:bg-cyan-500' : 'bg-cyan-600 hover:bg-cyan-700'
])
const secondaryButtonClass = computed(() => [
  'inline-flex items-center gap-2 rounded-lg border px-4 py-2 text-sm font-medium transition',
  isDark.value ? 'border-slate-600 bg-slate-800 text-gray-200 hover:bg-slate-700' : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'
])
const cancelButtonClass = computed(() => [
  'rounded-xl px-6 py-3 font-semibold transition',
  isDark.value ? 'text-gray-300 hover:bg-white/5' : 'border border-gray-300 bg-white text-gray-700 hover:bg-gray-100'
])

const coverFileClass = computed(() => isDark.value
  ? 'mt-3 rounded-lg bg-emerald-500/10 px-3 py-2 text-sm text-emerald-300'
  : 'mt-3 rounded-lg bg-emerald-50 px-3 py-2 text-sm text-emerald-700'
)
const infoPanelClass = computed(() => isDark.value
  ? 'rounded-lg border border-slate-700 bg-slate-800/60 p-4'
  : 'rounded-lg border border-slate-200 bg-slate-50 p-4'
)
const mutedTextClass = computed(() => isDark.value ? 'text-gray-400' : 'text-gray-600')
const strongTextClass = computed(() => isDark.value ? 'text-slate-100' : 'text-gray-900')
const dividerClass = computed(() => isDark.value ? 'text-slate-600' : 'text-gray-400')

const libraryButtonClass = computed(() => [
  'inline-flex items-center gap-2 rounded-lg border px-4 py-2 text-sm font-medium transition',
  isDark.value ? 'border-cyan-500/40 bg-cyan-500/10 text-cyan-300 hover:bg-cyan-500/20' : 'border-cyan-300 bg-cyan-50 text-cyan-700 hover:bg-cyan-100'
])
const contentButtonClass = computed(() => [
  'inline-flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold text-white transition',
  isDark.value ? 'bg-cyan-600 hover:bg-cyan-500' : 'bg-cyan-600 hover:bg-cyan-700'
])

// ============ Router & state ============
const route = useRoute()
const router = useRouter()
const idParam = route.params.id
const id = Array.isArray(idParam) ? idParam[0] : String(idParam || '')

const loading = ref(true)
const saving = ref(false)
const err = ref('')
const course = ref<CourseDetail | null>(null)

// ============ File inputs & previews ============
const coverInput = ref<HTMLInputElement | null>(null)
const coverFile = ref<File | null>(null)
const coverPreview = ref<string>('')
const previewFromFile = ref(false)
const coverErr = ref('')

// ============ Helpers ============
const subjectLabel = (s: Subject) =>
  s === 'math' ? 'Toán' :
  s === 'vietnamese' ? 'Tiếng Việt' :
  s === 'english' ? 'Tiếng Anh' :
  s === 'science' ? 'Khoa học' : 'Lịch sử'

function goToContent() {
  router.push({ name: 'teacher-course-content', params: { id } })
}

function goToLibrary() {
  router.push({ path: '/teacher/courses/content-library', query: { courseId: id } })
}

// ============ File pick handlers ============
function onPickCover(e: Event) {
  coverErr.value = ''
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    coverErr.value = 'Vui lòng chọn file ảnh (JPG/PNG)'
    showToast('Vui lòng chọn file ảnh (JPG/PNG).', 'warning')
    input.value = ''
    return
  }

  const maxSize = 5 * 1024 * 1024
  if (file.size > maxSize) {
    coverErr.value = `File ảnh tối đa 5MB. File của bạn: ${formatFileSize(file.size)}`
    showToast(`File ảnh tối đa 5MB. File của bạn: ${formatFileSize(file.size)}`, 'warning')
    input.value = ''
    return
  }

  coverFile.value = file
  if (previewFromFile.value && coverPreview.value) URL.revokeObjectURL(coverPreview.value)
  coverPreview.value = URL.createObjectURL(file)
  previewFromFile.value = true
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

// ============ Load detail ============
onMounted(async () => {
  try {
    if (!id) {
      err.value = 'Thiếu mã khoá học hợp lệ.'
      loading.value = false
      return
    }
    loading.value = true
    const detail = await courseService.detail(id)
    course.value = reactive(detail)

    if (course.value.thumbnail) {
      coverPreview.value = resolveMediaUrl(course.value.thumbnail)
      previewFromFile.value = false
    }
  } catch (e: any) {
    err.value = e?.message || 'Không tải được khoá học.'
  } finally {
    loading.value = false
  }
})

// ============ Save ============
async function save() {
  if (!course.value) return

  if (!course.value.title?.trim()) {
    showToast('Vui lòng nhập tên khoá học.', 'warning')
    return
  }
  saving.value = true
  try {
    const fd = new FormData()
    fd.append('title', course.value.title)
    fd.append('grade', String(course.value.grade))
    fd.append('subject', course.value.subject)
    if (course.value.description) fd.append('description', course.value.description)
    if (course.value.introduction) fd.append('introduction', course.value.introduction)
    if (course.value.price !== undefined) fd.append('price', String(course.value.price || 0))

    if (coverFile.value) {
      fd.append('thumbnail', coverFile.value, coverFile.value.name)
    }

    await courseService.update(id, fd as unknown as Partial<CourseDetail>)

    showToast('Đã lưu thành công!', 'success')
    router.push({ path: `/teacher/courses/${id}` })
  } catch (e: any) {
    showToast(e?.message || 'Lưu thất bại, thử lại.', 'error')
  } finally {
    saving.value = false
  }
}

// ============ Cleanup ============
onBeforeUnmount(() => {
  if (previewFromFile.value && coverPreview.value) URL.revokeObjectURL(coverPreview.value)
})
</script>
