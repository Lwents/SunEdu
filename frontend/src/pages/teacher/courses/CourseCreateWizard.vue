<!-- src/pages/teacher/courses/CourseCreateWizard.vue -->
<template>
  <div class="mx-auto max-w-5xl p-6">
    <!-- Progress Steps -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div
          v-for="(step, index) in steps"
          :key="index"
          class="flex items-center flex-1"
        >
          <div class="flex items-center">
            <div
              :class="[
                'flex h-10 w-10 items-center justify-center rounded-full border-2 font-semibold transition',
                currentStep > index
                  ? 'border-slate-900 bg-slate-900 text-white'
                  : currentStep === index
                  ? 'border-slate-900 bg-white text-slate-900'
                  : 'border-slate-300 bg-white text-slate-400'
              ]"
            >
              <svg
                v-if="currentStep > index"
                class="h-6 w-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span v-else>{{ index + 1 }}</span>
            </div>
            <div class="ml-3 hidden sm:block">
              <p
                :class="[
                  'text-sm font-medium',
                  currentStep >= index ? 'text-gray-900' : 'text-gray-500'
                ]"
              >
                {{ step.title }}
              </p>
              <p class="text-xs text-gray-500">{{ step.description }}</p>
            </div>
          </div>
          <div v-if="index < steps.length - 1" class="mx-4 hidden sm:block flex-1 h-0.5 bg-gray-300">
            <div
              :class="[
                'h-full transition-all duration-300',
                currentStep > index ? 'bg-slate-900' : 'bg-slate-300'
              ]"
              :style="{ width: currentStep > index ? '100%' : '0%' }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Step Content -->
    <div class="rounded-2xl border border-slate-200 bg-white p-8 shadow-lg">
      <!-- Step 1: Thông tin cơ bản -->
      <div v-if="currentStep === 0" class="space-y-6">
        <h2 class="text-2xl font-bold text-gray-900">Thông tin cơ bản</h2>
        
        <div class="grid grid-cols-1 gap-6 md:grid-cols-2">
          <div class="md:col-span-2">
            <label class="mb-2 block text-sm font-semibold text-gray-700">
              Tên khoá học <span class="text-rose-600">*</span>
            </label>
            <input
              v-model.trim="form.title"
              type="text"
              class="w-full rounded-lg border border-slate-300 px-4 py-2.5 focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
              placeholder="Ví dụ: Luyện thi Toán lớp 3"
              required
            />
          </div>

          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">Môn học</label>
            <select
              v-model="form.subject"
              class="w-full rounded-lg border border-slate-300 px-4 py-2.5 focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
            >
              <option value="math">Toán</option>
              <option value="vietnamese">Tiếng Việt</option>
              <option value="english">Tiếng Anh</option>
              <option value="science">Khoa học</option>
              <option value="history">Lịch sử</option>
            </select>
          </div>

          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">Khối lớp</label>
            <select
              v-model.number="form.grade"
              class="w-full rounded-lg border border-slate-300 px-4 py-2.5 focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
            >
              <option :value="1">Lớp 1</option>
              <option :value="2">Lớp 2</option>
              <option :value="3">Lớp 3</option>
              <option :value="4">Lớp 4</option>
              <option :value="5">Lớp 5</option>
            </select>
          </div>

          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">Giá khóa học (VNĐ)</label>
            <input
              v-model.number="form.price"
              type="number"
              min="0"
              step="1000"
              class="w-full rounded-lg border border-slate-300 px-4 py-2.5 focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
              placeholder="0"
            />
            <p class="mt-1 text-xs text-gray-500">Nhập 0 để khóa học miễn phí</p>
          </div>

          <div class="md:col-span-2">
            <label class="mb-2 block text-sm font-semibold text-gray-700">Giới thiệu chi tiết <span class="text-rose-600">*</span></label>
            <textarea
              v-model.trim="form.introduction"
              rows="6"
              class="w-full rounded-lg border border-slate-300 px-4 py-2.5 focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
              placeholder="Giới thiệu chi tiết về khóa học..."
              required
            ></textarea>
          </div>

          <div class="md:col-span-2">
            <label class="mb-2 block text-sm font-semibold text-gray-700">Mô tả ngắn</label>
            <textarea
              v-model.trim="form.description"
              rows="3"
              class="w-full rounded-lg border border-slate-300 px-4 py-2.5 focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
              placeholder="Mô tả ngắn gọn về khóa học"
            ></textarea>
          </div>

          <div class="md:col-span-2">
            <label class="mb-2 block text-sm font-semibold text-gray-700">Ảnh khoá học (tuỳ chọn)</label>
            <div class="flex items-center gap-4">
              <input
                ref="thumbnailInput"
                type="file"
                accept="image/*"
                class="hidden"
                @change="onPickThumbnail"
              />
              <button
                type="button"
                class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                @click="thumbnailInput?.click()"
              >
                Chọn ảnh
              </button>
              <span v-if="thumbnailFile" class="text-sm text-gray-600">
                {{ thumbnailFile.name }}
              </span>
              <img
                v-if="thumbnailPreview"
                :src="thumbnailPreview"
                alt="Preview"
                class="h-20 w-32 rounded-lg object-cover border"
              />
            </div>
          </div>

        </div>
      </div>

      <!-- Step 2: Nội dung khóa học -->
      <div v-if="currentStep === 1" class="space-y-6">
        <div class="flex items-center justify-between">
          <h2 class="text-2xl font-bold text-gray-900">Nội dung khóa học</h2>
          <button
            type="button"
            class="rounded-lg bg-slate-900 px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800"
            @click="showAddModule = true"
          >
            + Thêm chương
          </button>
        </div>

        <p class="text-sm text-gray-600">
          Tạo các chương và bài học cho khóa học. Bạn có thể thêm sau khi tạo khóa học.
        </p>

        <div v-if="modules.length === 0" class="rounded-xl border-2 border-dashed border-gray-300 bg-gray-50 p-12 text-center">
          <p class="text-gray-500">Chưa có chương nào. Nhấn "+ Thêm chương" để bắt đầu.</p>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="(module, mIdx) in modules"
            :key="module.id || mIdx"
            class="rounded-xl border border-gray-200 bg-white p-4"
          >
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-3">
                <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-slate-100 text-slate-700 font-bold text-sm">
                  {{ mIdx + 1 }}
                </div>
                <div>
                  <input
                    v-model="module.title"
                    type="text"
                    class="text-base font-semibold text-gray-900 border-none bg-transparent focus:outline-none focus:ring-2 focus:ring-slate-200 rounded px-2"
                    placeholder="Tên chương"
                    @blur="updateModuleTitle(mIdx)"
                  />
                </div>
              </div>
              <div class="flex items-center gap-2">
                <button
                  type="button"
                  class="rounded-lg border border-gray-300 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50"
                  @click="showAddLesson(mIdx)"
                >
                  + Bài học
                </button>
                <button
                  type="button"
                  class="rounded-lg border border-rose-200 px-3 py-1.5 text-xs font-medium text-rose-700 hover:bg-rose-50"
                  @click="removeModule(mIdx)"
                >
                  Xóa
                </button>
              </div>
            </div>
            <div class="ml-11 space-y-2">
              <div
                v-for="(lesson, lIdx) in module.lessons"
                :key="lesson.id || lIdx"
                class="flex items-center justify-between rounded-lg bg-gray-50 px-3 py-2"
              >
                <div class="flex items-center gap-3 flex-1 min-w-0">
                  <span class="text-sm font-medium text-gray-500 shrink-0">{{ mIdx + 1 }}.{{ lIdx + 1 }}</span>
                  <input
                    v-model="lesson.title"
                    type="text"
                    class="text-sm text-gray-900 border-none bg-transparent focus:outline-none focus:ring-2 focus:ring-slate-200 rounded px-2 flex-1 min-w-0"
                    placeholder="Tên bài học"
                    @blur="updateLessonTitle(mIdx, lIdx)"
                  />
                  <div v-if="lesson.video_url || lesson.video_file" class="shrink-0 flex items-center gap-1 text-xs text-slate-600">
                    <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                    <span>{{ lesson.video_file ? 'Video file' : 'Video URL' }}</span>
                  </div>
                </div>
                <button
                  type="button"
                  class="rounded-lg border border-rose-200 px-2 py-1 text-xs font-medium text-rose-700 hover:bg-rose-50"
                  @click="removeLesson(mIdx, lIdx)"
                >
                  Xóa
                </button>
              </div>
              <div v-if="!module.lessons.length" class="text-sm text-gray-400 italic px-3 py-2">
                Chưa có bài học
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Step 3: Xem lại -->
      <div v-if="currentStep === 2" class="space-y-6">
        <h2 class="text-2xl font-bold text-gray-900">Xem lại và hoàn tất</h2>
        
        <div class="space-y-4 rounded-xl border border-gray-200 bg-gray-50 p-6">
          <div>
            <h3 class="font-semibold text-gray-900 mb-2">Thông tin khóa học</h3>
            <div class="space-y-1 text-sm text-gray-700">
              <p><span class="font-medium">Tên:</span> {{ form.title }}</p>
              <p><span class="font-medium">Môn:</span> {{ getSubjectLabel(form.subject) }}</p>
              <p><span class="font-medium">Khối:</span> Lớp {{ form.grade }}</p>
              <p><span class="font-medium">Giá:</span> {{ form.price === 0 ? 'Miễn phí' : new Intl.NumberFormat('vi-VN').format(form.price) + 'đ' }}</p>
            </div>
          </div>
          
          <div v-if="modules.length > 0">
            <h3 class="font-semibold text-gray-900 mb-2">Nội dung</h3>
            <div class="space-y-2 text-sm text-gray-700">
              <div v-for="(module, mIdx) in modules" :key="mIdx">
                <p class="font-medium">{{ mIdx + 1 }}. {{ module.title || 'Chưa có tên' }}</p>
                <ul class="ml-4 space-y-1 text-gray-600">
                  <li v-for="(lesson, lIdx) in module.lessons" :key="lIdx">
                    {{ mIdx + 1 }}.{{ lIdx + 1 }} {{ lesson.title || 'Chưa có tên' }}
                  </li>
                  <li v-if="!module.lessons.length" class="text-gray-400 italic">Chưa có bài học</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="mt-8 flex justify-between border-t border-gray-200 pt-6">
        <button
          type="button"
          class="rounded-lg border border-gray-300 px-6 py-2.5 font-semibold text-gray-700 hover:bg-gray-50"
          :disabled="currentStep === 0"
          @click="currentStep--"
        >
          Quay lại
        </button>
        <button
          v-if="currentStep < steps.length - 1"
          type="button"
          class="rounded-lg bg-slate-900 px-6 py-2.5 font-semibold text-white hover:bg-slate-800 disabled:opacity-50"
          :disabled="!canProceed"
          @click="currentStep++"
        >
          Tiếp theo
        </button>
        <button
          v-else
          type="button"
          class="rounded-lg bg-slate-900 px-6 py-2.5 font-semibold text-white hover:bg-slate-800 disabled:opacity-50"
          :disabled="submitting || !canSubmit"
          @click="submit"
        >
          {{ submitting ? 'Đang tạo...' : 'Tạo khóa học' }}
        </button>
      </div>
    </div>

    <!-- Add Module Modal -->
    <div
      v-if="showAddModule"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
      @click.self="showAddModule = false"
    >
      <div class="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
        <h3 class="mb-4 text-lg font-bold">Thêm chương mới</h3>
        <input
          v-model.trim="newModuleTitle"
          type="text"
          class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
          placeholder="Tên chương"
          @keyup.enter="addModule"
        />
        <div class="mt-4 flex justify-end gap-3">
          <button
            type="button"
            class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            @click="showAddModule = false"
          >
            Hủy
          </button>
          <button
            type="button"
            class="rounded-lg bg-cyan-600 px-4 py-2 text-sm font-medium text-white hover:bg-cyan-700"
            @click="addModule"
          >
            Thêm
          </button>
        </div>
      </div>
    </div>

    <!-- Add Lesson Modal -->
    <div
      v-if="showAddLessonModuleIdx !== null"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 overflow-y-auto"
      @click.self="showAddLessonModuleIdx = null"
    >
      <div class="w-full max-w-2xl rounded-2xl bg-white p-6 shadow-xl my-8">
        <h3 class="mb-4 text-lg font-bold">Thêm bài học mới</h3>
        
        <div class="space-y-4">
          <!-- Tên bài học -->
          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">
              Tên bài học <span class="text-rose-600">*</span>
            </label>
            <input
              v-model.trim="newLessonTitle"
              type="text"
              class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
              placeholder="Ví dụ: Bài 1: Giới thiệu về số tự nhiên"
              @keyup.enter="addLesson"
            />
          </div>

          <!-- Video URL hoặc File -->
          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-700">
              Video bài học (tùy chọn)
            </label>
            <div class="space-y-3">
              <!-- Tab chọn: URL hoặc File -->
              <div class="flex gap-2 border-b border-gray-200">
                <button
                  type="button"
                  :class="[
                    'px-4 py-2 text-sm font-medium border-b-2 transition',
                    newLessonVideoType === 'url'
                      ? 'border-slate-900 text-slate-900'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  ]"
                  @click="newLessonVideoType = 'url'"
                >
                  Video URL
                </button>
                <button
                  type="button"
                  :class="[
                    'px-4 py-2 text-sm font-medium border-b-2 transition',
                    newLessonVideoType === 'file'
                      ? 'border-slate-900 text-slate-900'
                      : 'border-transparent text-gray-500 hover:text-gray-700'
                  ]"
                  @click="newLessonVideoType = 'file'"
                >
                  Tải video lên
                </button>
              </div>

              <!-- Video URL Input -->
              <div v-if="newLessonVideoType === 'url'">
                <input
                  v-model.trim="newLessonVideoUrl"
                  type="url"
                  class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-slate-900 focus:ring-2 focus:ring-slate-200"
                  placeholder="https://www.youtube.com/watch?v=... hoặc link video trực tiếp"
                />
                <p class="mt-1 text-xs text-gray-500">
                  Nhập link YouTube, Vimeo hoặc link video trực tiếp
                </p>
              </div>

              <!-- Video File Upload -->
              <div v-if="newLessonVideoType === 'file'">
                <input
                  ref="newLessonVideoFileInput"
                  type="file"
                  accept="video/*"
                  class="hidden"
                  @change="onPickLessonVideo"
                />
                <div class="flex items-center gap-3">
                  <button
                    type="button"
                    class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
                    @click="newLessonVideoFileInput?.click()"
                  >
                    Chọn video
                  </button>
                  <span v-if="newLessonVideoFile" class="text-sm text-gray-600 flex-1 truncate">
                    {{ newLessonVideoFile.name }}
                  </span>
                  <button
                    v-if="newLessonVideoFile"
                    type="button"
                    class="text-rose-600 hover:text-rose-700 text-sm"
                    @click="newLessonVideoFile = null; newLessonVideoFileInput && (newLessonVideoFileInput.value = '')"
                  >
                    Xóa
                  </button>
                </div>
                <p class="mt-1 text-xs text-gray-500">
                  Hỗ trợ: MP4, AVI, MOV. Tối đa 500MB
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-6 flex justify-end gap-3">
          <button
            type="button"
            class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            @click="cancelAddLesson"
          >
            Hủy
          </button>
          <button
            type="button"
            class="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:opacity-50"
            :disabled="!newLessonTitle.trim()"
            @click="addLesson"
          >
            Thêm
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { courseService } from '@/services/course.service'
import { contentService } from '@/services/content.service'
import { showToast } from '@/utils/toast'
import { showConfirm } from '@/utils/confirm'

const router = useRouter()

const steps = [
  { title: 'Thông tin cơ bản', description: 'Điền thông tin khóa học' },
  { title: 'Nội dung', description: 'Thêm chương và bài học' },
  { title: 'Hoàn tất', description: 'Xem lại và tạo' }
]

const currentStep = ref(0)

const form = ref({
  title: '',
  subject: 'math',
  grade: 3,
  price: 0,
  introduction: '',
  description: ''
})

const thumbnailInput = ref<HTMLInputElement | null>(null)
const thumbnailFile = ref<File | null>(null)
const thumbnailPreview = ref<string>('')

const modules = ref<Array<{ id?: string; title: string; lessons: Array<{ id?: string; title: string; video_url?: string; video_file?: File }> }>>([])
const showAddModule = ref(false)
const newModuleTitle = ref('')
const showAddLessonModuleIdx = ref<number | null>(null)
const newLessonTitle = ref('')
const newLessonVideoType = ref<'url' | 'file'>('url')
const newLessonVideoUrl = ref('')
const newLessonVideoFile = ref<File | null>(null)
const newLessonVideoFileInput = ref<HTMLInputElement | null>(null)

const submitting = ref(false)

const canProceed = computed(() => {
  if (currentStep.value === 0) {
    return form.value.title.trim() && form.value.introduction.trim()
  }
  return true
})

const canSubmit = computed(() => {
  return form.value.title.trim() && form.value.introduction.trim()
})

function getSubjectLabel(subject: string): string {
  const labels: Record<string, string> = {
    math: 'Toán',
    vietnamese: 'Tiếng Việt',
    english: 'Tiếng Anh',
    science: 'Khoa học',
    history: 'Lịch sử'
  }
  return labels[subject] || subject
}

function onPickThumbnail(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  if (!file.type.startsWith('image/')) {
    showToast('Vui lòng chọn file ảnh', 'warning')
    return
  }
  thumbnailFile.value = file
  if (thumbnailPreview.value) URL.revokeObjectURL(thumbnailPreview.value)
  thumbnailPreview.value = URL.createObjectURL(file)
}

function addModule() {
  if (!newModuleTitle.value.trim()) return
  modules.value.push({
    title: newModuleTitle.value,
    lessons: []
  })
  newModuleTitle.value = ''
  showAddModule.value = false
}

async function removeModule(index: number) {
  const confirmed = await showConfirm({
    message: 'Bạn có chắc muốn xóa chương này?',
    title: 'Xác nhận xóa chương',
    type: 'danger',
    confirmText: 'Xóa',
    cancelText: 'Hủy'
  })
  if (confirmed) {
    modules.value.splice(index, 1)
  }
}

function updateModuleTitle(index: number) {
  // Title được update trực tiếp qua v-model
}

function showAddLesson(moduleIdx: number) {
  showAddLessonModuleIdx.value = moduleIdx
  newLessonTitle.value = ''
  newLessonVideoType.value = 'url'
  newLessonVideoUrl.value = ''
  newLessonVideoFile.value = null
  if (newLessonVideoFileInput.value) {
    newLessonVideoFileInput.value.value = ''
  }
}

function onPickLessonVideo(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  if (!file.type.startsWith('video/')) {
    showToast('Vui lòng chọn file video', 'warning')
    input.value = ''
    return
  }
  if (file.size > 500 * 1024 * 1024) {
    showToast('File video tối đa 500MB', 'warning')
    input.value = ''
    return
  }
  newLessonVideoFile.value = file
}

function cancelAddLesson() {
  showAddLessonModuleIdx.value = null
  newLessonTitle.value = ''
  newLessonVideoUrl.value = ''
  newLessonVideoFile.value = null
  if (newLessonVideoFileInput.value) {
    newLessonVideoFileInput.value.value = ''
  }
}

function addLesson() {
  if (showAddLessonModuleIdx.value === null || !newLessonTitle.value.trim()) return
  const module = modules.value[showAddLessonModuleIdx.value]
  if (module) {
    const lesson: { id?: string; title: string; video_url?: string; video_file?: File } = {
      title: newLessonTitle.value
    }
    if (newLessonVideoType.value === 'url' && newLessonVideoUrl.value.trim()) {
      lesson.video_url = newLessonVideoUrl.value.trim()
    } else if (newLessonVideoType.value === 'file' && newLessonVideoFile.value) {
      lesson.video_file = newLessonVideoFile.value
    }
    module.lessons.push(lesson)
    newLessonTitle.value = ''
    newLessonVideoUrl.value = ''
    newLessonVideoFile.value = null
    if (newLessonVideoFileInput.value) {
      newLessonVideoFileInput.value.value = ''
    }
    showAddLessonModuleIdx.value = null
  }
}

async function removeLesson(moduleIdx: number, lessonIdx: number) {
  const confirmed = await showConfirm({
    message: 'Bạn có chắc muốn xóa bài học này?',
    title: 'Xác nhận xóa bài học',
    type: 'danger',
    confirmText: 'Xóa',
    cancelText: 'Hủy'
  })
  if (confirmed) {
    modules.value[moduleIdx].lessons.splice(lessonIdx, 1)
  }
}

function updateLessonTitle(moduleIdx: number, lessonIdx: number) {
  // Title được update trực tiếp qua v-model
}

async function submit() {
  if (!canSubmit.value) {
    showToast('Vui lòng điền đầy đủ thông tin bắt buộc', 'warning')
    return
  }
  submitting.value = true
  try {
    // Tạo khóa học
    const fd = new FormData()
    fd.append('title', form.value.title)
    fd.append('grade', String(form.value.grade))
    fd.append('subject_slug', form.value.subject)
    fd.append('description', form.value.description || '')
    fd.append('introduction', form.value.introduction)
    fd.append('price', String(form.value.price || 0))
    
    if (thumbnailFile.value) {
      fd.append('thumbnail', thumbnailFile.value)
    }

    const response = await courseService.create(fd as any)
    const courseId = (response as any)?.id

    // Tạo modules và lessons
    for (let mIdx = 0; mIdx < modules.value.length; mIdx++) {
      const module = modules.value[mIdx]
      try {
        const createdModule = await contentService.createModule(courseId, {
          title: module.title,
          course: courseId,
          position: mIdx
        })
        
        // Tạo lessons cho module
        for (let lIdx = 0; lIdx < module.lessons.length; lIdx++) {
          const lesson = module.lessons[lIdx]
          try {
            // Nếu có video_file, cần upload riêng sau khi tạo lesson
            if (lesson.video_file) {
              // Tạo lesson trước
              const createdLesson = await contentService.createLesson(createdModule.id, {
                title: lesson.title,
                module: createdModule.id,
                position: lIdx,
                content_type: 'lesson',
                video_url: undefined
              })
              // Upload video file sau
              const lessonFd = new FormData()
              lessonFd.append('video_file', lesson.video_file)
              try {
                await contentService.updateLesson(createdLesson.id, lessonFd as any)
              } catch (videoErr) {
                console.warn('Error uploading video file:', videoErr)
              }
            } else {
              // Tạo lesson với video_url nếu có
              await contentService.createLesson(createdModule.id, {
                title: lesson.title,
                module: createdModule.id,
                position: lIdx,
                content_type: 'lesson',
                video_url: lesson.video_url
              })
            }
          } catch (e) {
            console.error('Error creating lesson:', e)
          }
        }
      } catch (e) {
        console.error('Error creating module:', e)
      }
    }

    showToast('Đã tạo khóa học thành công!', 'success')
    router.push({ name: 'teacher-course-content', params: { id: courseId } })
  } catch (e: any) {
    showToast(e?.message || 'Tạo khóa học thất bại', 'error')
  } finally {
    submitting.value = false
  }
}

onBeforeUnmount(() => {
  if (thumbnailPreview.value) URL.revokeObjectURL(thumbnailPreview.value)
})
</script>





