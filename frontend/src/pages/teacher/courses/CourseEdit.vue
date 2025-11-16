<template>
  <div class="mx-auto max-w-5xl p-6">
    <!-- Loading -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="h-32 rounded-2xl bg-slate-200 animate-pulse" />
    </div>

    <!-- Error -->
    <div v-else-if="err" class="rounded-xl border border-rose-200 bg-rose-50 p-4 text-rose-700">
      {{ err }}
    </div>

    <!-- Form -->
    <div v-else-if="course">
      <!-- Header -->
      <div class="mb-6 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Chỉnh sửa khoá học</h1>
          <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">Cập nhật thông tin chi tiết cho khoá học của bạn</p>
        </div>
        <button
          class="rounded-xl bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700 transition"
          @click="save"
          :disabled="saving"
        >
          {{ saving ? 'Đang lưu...' : 'Lưu thay đổi' }}
        </button>
      </div>

      <div class="space-y-6">
        <!-- Thông tin cơ bản -->
        <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 class="mb-4 text-lg font-semibold text-gray-900">Thông tin cơ bản</h2>
          <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
            <!-- Tên khoá học -->
            <label class="md:col-span-2">
              <span class="mb-2 block text-sm font-semibold text-gray-700">
                Tên khoá học <span class="text-rose-600">*</span>
              </span>
              <input
                v-model.trim="course.title"
                type="text"
                required
                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 placeholder-gray-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 outline-none transition"
                placeholder="Nhập tên khoá học"
              />
            </label>

            <!-- Khối lớp -->
            <div>
              <span class="mb-2 block text-sm font-semibold text-gray-700">Khối lớp</span>
              <div class="w-full rounded-lg border border-gray-200 bg-gray-50 px-4 py-2.5 text-gray-600 font-medium">
                Lớp {{ course.grade }}
              </div>
            </div>

            <!-- Môn học -->
            <div>
              <span class="mb-2 block text-sm font-semibold text-gray-700">Môn học</span>
              <div class="w-full rounded-lg border border-gray-200 bg-gray-50 px-4 py-2.5 text-gray-600 font-medium">
                {{ subjectLabel(course.subject) }}
              </div>
            </div>

            <!-- Mức độ -->
            <label>
              <span class="mb-2 block text-sm font-semibold text-gray-700">Mức độ</span>
              <select
                v-model="course.level"
                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 outline-none transition"
              >
                <option value="basic">Cơ bản</option>
                <option value="advanced">Mở rộng</option>
              </select>
            </label>

            <!-- Trạng thái -->
            <label>
              <span class="mb-2 block text-sm font-semibold text-gray-700">Trạng thái</span>
              <select
                v-model="course.status"
                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 outline-none transition"
              >
                <option value="draft">Lưu trữ (Nháp)</option>
                <option value="published">Xuất bản</option>
              </select>
            </label>

            <!-- Giá khóa học -->
            <label>
              <span class="mb-2 block text-sm font-semibold text-gray-700">Giá khóa học (VNĐ)</span>
              <input
                v-model.number="course.price"
                type="number"
                min="0"
                step="1000"
                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 placeholder-gray-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 outline-none transition"
                placeholder="0"
              />
              <p class="mt-1 text-xs text-gray-500">Nhập 0 để khóa học miễn phí</p>
            </label>

            <!-- Số bài học -->
            <label>
              <span class="mb-2 block text-sm font-semibold text-gray-700">Số bài học</span>
              <input
                v-model.number="lessonsProxy"
                type="number"
                min="0"
                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 placeholder-gray-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 outline-none transition"
              />
            </label>

            <!-- Mô tả ngắn -->
            <label class="md:col-span-2">
              <span class="mb-2 block text-sm font-semibold text-gray-700">Mô tả ngắn</span>
              <textarea
                v-model.trim="course.description"
                rows="3"
                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 placeholder-gray-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 outline-none transition resize-y"
                placeholder="Mô tả ngắn gọn về khóa học"
              ></textarea>
            </label>

            <!-- Giới thiệu chi tiết -->
            <label class="md:col-span-2">
              <span class="mb-2 block text-sm font-semibold text-gray-700">
                Giới thiệu chi tiết <span class="text-rose-600">*</span>
              </span>
              <textarea
                v-model.trim="course.introduction"
                rows="8"
                required
                class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-gray-900 placeholder-gray-400 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20 outline-none transition resize-y"
                placeholder="Giới thiệu chi tiết về khóa học (sẽ hiển thị ở trang chi tiết khóa học)"
              ></textarea>
              <p class="mt-1 text-xs text-gray-500">Nội dung này sẽ hiển thị ở trang chi tiết khóa học cho học sinh</p>
            </label>
          </div>
        </div>

        <!-- Ảnh khoá học -->
        <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 class="mb-4 text-lg font-semibold text-gray-900">Ảnh khoá học</h2>
          <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4">
            <div class="relative h-32 w-48 rounded-lg border border-slate-200 bg-slate-100 overflow-hidden shrink-0">
              <img
                v-if="coverPreview"
                :src="coverPreview"
                alt="Ảnh bìa"
                class="h-full w-full object-cover"
              />
              <div v-else class="flex h-full items-center justify-center">
                <svg class="h-12 w-12 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </div>
            </div>
            <div class="flex-1">
              <input ref="coverInput" type="file" accept="image/*" class="hidden" @change="onPickCover" />
              <button
                type="button"
                class="inline-flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 transition"
                @click="coverInput?.click()"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                </svg>
                Đổi ảnh
              </button>
              <p v-if="coverFile" class="mt-3 text-sm text-emerald-700 bg-emerald-50 px-3 py-2 rounded-lg">
                Đã chọn ảnh mới: <b>{{ coverFile.name }}</b> ({{ formatFileSize(coverFile.size) }})
              </p>
              <p v-if="coverErr" class="mt-2 text-sm text-rose-600 font-medium">{{ coverErr }}</p>
              <p class="mt-2 text-xs text-gray-500">JPG/PNG, tối đa 5MB. Giữ ảnh cũ nếu không đổi.</p>
            </div>
          </div>
        </div>

        <!-- Quản lý nội dung -->
        <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-900">Quản lý nội dung</h2>
            <div class="flex items-center gap-3">
              <button
                type="button"
                class="inline-flex items-center gap-2 rounded-lg border border-cyan-300 bg-cyan-50 px-4 py-2 text-sm font-medium text-cyan-700 hover:bg-cyan-100 transition"
                @click="goToLibrary"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Thêm từ thư viện
              </button>
              <button
                type="button"
                class="inline-flex items-center gap-2 rounded-lg bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700 transition"
                @click="goToContent"
              >
                <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
                Quản lý nội dung
              </button>
            </div>
          </div>
          <div class="rounded-lg border border-slate-200 bg-slate-50 p-4">
            <div class="flex items-center gap-4 text-sm text-gray-600">
              <div class="flex items-center gap-2">
                <svg class="h-5 w-5 text-cyan-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                <span class="font-medium text-gray-900">{{ course.lessonsCount || 0 }}</span>
                <span>bài học</span>
              </div>
              <div class="text-gray-400">•</div>
              <p class="text-gray-600">
                Quản lý các chương và bài học của khóa học. Bạn có thể thêm nội dung từ thư viện hoặc tạo mới.
              </p>
            </div>
          </div>
        </div>

      </div>

      <!-- Form Actions -->
      <div class="mt-6 flex items-center justify-end gap-3">
        <button
          type="button"
          class="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 transition"
          @click="router.back()"
        >
          Hủy
        </button>
        <button
          type="button"
          class="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-semibold text-white hover:bg-cyan-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
          @click="save"
          :disabled="saving"
        >
          {{ saving ? 'Đang lưu...' : 'Lưu thay đổi' }}
        </button>
      </div>
    </div>

    <!-- Not Found -->
    <div v-else class="flex items-center justify-center gap-3 rounded-2xl border border-slate-200 bg-white p-12 shadow-sm">
      <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span class="text-lg font-medium text-gray-600">Không tìm thấy khoá học.</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, reactive, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { courseService, type CourseDetail, type Subject } from '@/services/course.service'
import { showToast } from '@/utils/toast'

/* ===== Router & state ===== */
const route = useRoute()
const router = useRouter()
const idParam = route.params.id
const id = Array.isArray(idParam) ? idParam[0] : String(idParam || '')

const loading = ref(true)
const saving = ref(false)
const err = ref('')

const course = ref<CourseDetail | null>(null)

/* Nếu mở từ ContentLibrary: ?add=<contentId> */
const addedContentHint = ref<string | null>(null)

/* ===== File inputs & previews ===== */
const coverInput = ref<HTMLInputElement | null>(null)

const coverFile = ref<File | null>(null)
const coverPreview = ref<string>('')   // URL để hiển thị
const previewFromFile = ref(false)     // true nếu preview từ file mới -> revoke khi unmount
const coverErr = ref('')

/* ===== Helpers ===== */
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

/* Proxy lessons (CourseDetail không có field "lessons" cố định; ta dùng lessonsCount) */
const lessonsProxy = computed({
  get: () => course.value?.lessonsCount ?? 0,
  set: (v: number) => { if (course.value) course.value.lessonsCount = v }
})

/* ===== File pick handlers ===== */
function onPickCover(e: Event) {
  coverErr.value = ''
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  coverErr.value = ''

  if (!file.type.startsWith('image/')) {
    coverErr.value = 'Vui lòng chọn file ảnh (JPG/PNG)'
    input.value = ''
    return
  }
  
  const maxSize = 5 * 1024 * 1024 // 5MB
  if (file.size > maxSize) {
    coverErr.value = `File ảnh tối đa 5MB. File của bạn: ${formatFileSize(file.size)}`
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

/* ===== Load detail ===== */
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
    
    // Ensure status is set (fallback for backward compatibility)
    if (!course.value.status) {
      // If status is not present, derive from published field or default to draft
      course.value.status = (detail as any).published ? 'published' : 'draft'
    }

    // preview ảnh ban đầu = thumbnail (nếu có)
    if (course.value.thumbnail) {
      coverPreview.value = course.value.thumbnail
      previewFromFile.value = false
    }

    // nếu có query add (từ ContentLibrary)
    const add = route.query.add ? String(route.query.add) : ''
    if (add) addedContentHint.value = add
  } catch (e: any) {
    err.value = e?.message || 'Không tải được khoá học.'
  } finally {
    loading.value = false
  }
})

/* ===== Save ===== */
async function save() {
  if (!course.value) return
  
  // Validation
  if (!course.value.title?.trim()) {
    showToast('Vui lòng nhập tên khoá học.', 'warning')
    return
  }
  if (!course.value.introduction?.trim()) {
    showToast('Vui lòng nhập giới thiệu chi tiết.', 'warning')
    return
  }

  saving.value = true
  try {
    const fd = new FormData()
    fd.append('title', course.value.title)
    fd.append('lessonsCount', String(course.value.lessonsCount ?? 0))
    fd.append('grade', String(course.value.grade))
    fd.append('subject', course.value.subject)
    if (course.value.level) fd.append('level', course.value.level)
    if (course.value.description) fd.append('description', course.value.description)
    if (course.value.introduction) fd.append('introduction', course.value.introduction)
    if (course.value.price !== undefined) fd.append('price', String(course.value.price || 0))

    // Map status to published: if status is 'published', set published=true, otherwise false
    const shouldPublish = course.value.status === 'published'
    fd.append('published', String(shouldPublish))

    // Ảnh mới (nếu có). Nếu không gửi, backend giữ thumbnail cũ
    if (coverFile.value) {
      // Đảm bảo file được append đúng cách
      fd.append('thumbnail', coverFile.value, coverFile.value.name)
      console.log('Appending thumbnail file:', coverFile.value.name, coverFile.value.size, 'bytes')
    }

    // Debug: Log FormData contents
    console.log('FormData entries:')
    for (const [key, value] of fd.entries()) {
      if (value instanceof File) {
        console.log(`  ${key}: File(${value.name}, ${value.size} bytes, ${value.type})`)
      } else {
        console.log(`  ${key}: ${value}`)
      }
    }

    // Gọi API update
    await courseService.update(id, fd as unknown as Partial<CourseDetail>)
    
    // Nếu muốn publish, gọi thêm publish endpoint để đảm bảo validation
    if (shouldPublish) {
      try {
        await courseService.publishCourse(id)
      } catch (publishErr: any) {
        // Nếu publish fail, vẫn giữ update nhưng cảnh báo
        console.warn('Update thành công nhưng publish thất bại:', publishErr)
        showToast('Đã lưu thay đổi, nhưng không thể xuất bản khóa học. Vui lòng kiểm tra lại điều kiện xuất bản.', 'warning')
      }
    }

    showToast('Đã lưu thành công!', 'success')
    router.push({ path: `/teacher/courses/${id}` })
  } catch (e: any) {
    showToast(e?.message || 'Lưu thất bại, thử lại.', 'error')
  } finally {
    saving.value = false
  }
}

/* ===== Cleanup ===== */
onBeforeUnmount(() => {
  if (previewFromFile.value && coverPreview.value) URL.revokeObjectURL(coverPreview.value)
})
</script>
