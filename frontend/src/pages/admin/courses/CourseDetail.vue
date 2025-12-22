<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
      <div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div class="flex min-w-0 items-center gap-4">
          <div class="relative h-16 w-28 shrink-0 overflow-hidden rounded bg-gray-100">
            <img
              :src="thumbnailUrl"
              class="h-full w-full object-cover"
              alt="Course thumbnail"
              @error="onThumbError"
            />
            <div
              v-if="!detail.thumbnail"
              class="absolute inset-0 flex items-center justify-center text-[10px] text-gray-400"
            >
              Không có ảnh
            </div>
          </div>
          <div class="min-w-0">
            <div class="flex flex-wrap items-center gap-2">
              <h2 class="truncate text-xl font-semibold text-gray-800">{{ detail.title }}</h2>
              <el-tag size="small">Lớp {{ detail.grade }}</el-tag>
              <el-tag size="small" type="info">{{ subjectName(detail.subject) }}</el-tag>
              <el-tag size="small" :type="statusTagType(detail.status)">{{
                statusLabel(detail.status)
              }}</el-tag>
            </div>
            <div class="mt-1 text-sm text-gray-500">
              GV: {{ detail.teacherName }} • {{ detail.lessonsCount }} bài •
              {{ detail.enrollments }} HV
            </div>
            <div class="mt-1 text-xs text-gray-500">
              Cập nhật: <b>{{ fmtDate(detail.updatedAt) }}</b>
            </div>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-2">
          <el-button v-if="detail.status === 'pending_review'" type="success" plain @click="approve"
            >Duyệt</el-button
          >
          <el-button v-if="detail.status === 'pending_review'" type="danger" plain @click="reject"
            >Từ chối</el-button
          >

          <el-button
            v-if="detail.status !== 'published' && detail.status !== 'archived'"
            type="success"
            @click="publish"
            >Xuất bản</el-button
          >
          <el-button v-if="detail.status === 'published'" @click="unpublish">Gỡ</el-button>

          <el-button v-if="detail.status !== 'archived'" type="warning" plain @click="archive"
            >Lưu trữ</el-button
          >
          <el-button v-else type="info" plain @click="restore">Khôi phục</el-button>
        </div>
      </div>
    </div>

    <!-- Tabs -->
    <el-tabs v-model="activeTab">
      <el-tab-pane label="Tổng quan" name="overview">
        <div
          class="rounded-lg bg-white p-4 ring-1 ring-black/5 grid grid-cols-1 gap-4 md:grid-cols-3"
        >
          <div class="md:col-span-2 space-y-3">
            <div class="text-gray-700 whitespace-pre-line" v-if="detail.description">
              {{ detail.description }}
            </div>
            <div class="grid grid-cols-3 gap-3">
              <div class="rounded border p-3">
                <div class="text-xs text-gray-500">Trình độ</div>
                <div class="mt-1 font-medium">{{ levelLabel(detail.level) }}</div>
              </div>
              <div class="rounded border p-3">
                <div class="text-xs text-gray-500">Thời lượng</div>
                <div class="mt-1 font-medium">{{ minutes(detail.durationMinutes) }}</div>
              </div>
              <div class="rounded border p-3">
                <div class="text-xs text-gray-500">Bài học</div>
                <div class="mt-1 font-medium">{{ detail.lessonsCount }}</div>
              </div>
            </div>
          </div>
          <div class="space-y-3">
            <div class="rounded border p-3">
              <div class="text-xs text-gray-500">Giáo viên</div>
              <div class="mt-1 font-medium">{{ detail.teacherName }}</div>
            </div>
            <div class="rounded border p-3">
              <div class="text-xs text-gray-500">Trạng thái</div>
              <div class="mt-1">
                <el-tag :type="statusTagType(detail.status)">{{
                  statusLabel(detail.status)
                }}</el-tag>
              </div>
            </div>
            <div class="rounded border p-3">
              <div class="text-xs text-gray-500">Ngày tạo</div>
              <div class="mt-1 font-medium">{{ fmtDate(detail.createdAt) }}</div>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="Chương trình học" name="curriculum">
        <div class="rounded-lg bg-white p-4 ring-1 ring-black/5 space-y-4">
          <div v-for="sec in detail.sections" :key="sec.id" class="rounded border p-3">
            <div class="mb-2 flex items-center justify-between">
              <div class="font-semibold">Chương {{ sec.order }}: {{ sec.title }}</div>
              <div class="text-xs text-gray-500">{{ sec.lessons.length }} bài</div>
            </div>
            <el-table :data="sec.lessons" size="small">
              <el-table-column type="index" label="#" width="50" />
              <el-table-column prop="title" label="Bài học" min-width="220" />
              <el-table-column prop="type" label="Loại" width="120">
                <template #default="{ row }">{{ typeLabel(row.type) }}</template>
              </el-table-column>
              <el-table-column prop="durationMinutes" label="Thời lượng" width="120">
                <template #default="{ row }">{{ minutes(row.durationMinutes) }}</template>
              </el-table-column>
              <el-table-column prop="isPreview" label="Học thử" width="110" align="center">
                <template #default="{ row }">
                  <el-tag v-if="row.isPreview" type="success" size="small">Có</el-tag>
                  <span v-else>—</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import {
  courseService,
  type CourseDetail,
  type CourseStatus,
  type Subject,
  type Level,
} from '@/services/course.service'
import { showToast } from '@/utils/toast'
import { showConfirm } from '@/utils/confirm'
import { resolveMediaUrl } from '@/utils/media'

const route = useRoute()
const id = computed(() => route.params.id as string)

const activeTab = ref<'overview' | 'curriculum'>('overview')
const detail = reactive<CourseDetail>({
  id: id.value,
  title: '',
  grade: 1,
  subject: 'math',
  teacherId: 0,
  teacherName: '',
  lessonsCount: 0,
  enrollments: 0,
  status: 'draft',
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  sections: [],
  thumbnail: '',
})

const placeholderThumb =
  'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="160" height="90" viewBox="0 0 160 90"><rect width="160" height="90" fill="%23f3f4f6" rx="8"/><path d="M52 56l14-18 12 14 8-10 20 24H52z" fill="%23d1d5db"/><circle cx="65" cy="38" r="6" fill="%23d1d5db"/><text x="80" y="82" text-anchor="middle" font-family="Arial" font-size="12" fill="%239ca3af">No image</text></svg>'

const thumbnailUrl = computed(() => resolveMediaUrl(detail.thumbnail) || placeholderThumb)

function onThumbError(event: Event) {
  const target = event.target as HTMLImageElement | null
  if (target) target.src = placeholderThumb
}

const subjects = courseService.subjects()
function subjectName(s: Subject) {
  return subjects.find((x) => x.value === s)?.label || s
}
function statusLabel(s: CourseStatus) {
  return s === 'draft'
    ? 'Bản nháp'
    : s === 'pending_review'
      ? 'Chờ duyệt'
      : s === 'published'
        ? 'Đã xuất bản'
        : s === 'rejected'
          ? 'Từ chối'
          : 'Lưu trữ'
}
function statusTagType(s: CourseStatus) {
  return s === 'draft'
    ? 'info'
    : s === 'pending_review'
      ? 'warning'
      : s === 'published'
        ? 'success'
        : s === 'rejected'
          ? 'danger'
          : 'info'
}
const fmtDate = (iso?: string) => (iso ? new Date(iso).toLocaleString('vi-VN') : '')
const typeLabel = (t: 'video' | 'pdf' | 'quiz') =>
  t === 'video' ? 'Video' : t === 'pdf' ? 'Tài liệu' : 'Quiz'
const levelLabel = (l?: Level) => (l === 'advanced' ? 'Nâng cao' : 'Cơ bản')
const minutes = (m?: number) => (m ? `${m} phút` : '—')

async function load() {
  try {
  const d = await courseService.detail(id.value, true)
  Object.assign(detail, d)
  } catch (error: any) {
    showToast(error?.message || 'Không tải được khoá học', 'error')
  }
}

// Actions
async function approve() {
  const confirmed = await showConfirm({
    title: 'Xác nhận',
    message: 'Duyệt khoá học này?',
  })
  if (!confirmed) return
  await courseService.approve(detail.id)
  detail.status = 'published'
  showToast('Đã duyệt khoá học', 'success')
}
async function reject() {
  const reason = window.prompt('Nhập lý do từ chối', '')
  if (reason === null) return
  await courseService.reject(detail.id, reason)
    detail.status = 'rejected'
  showToast('Đã từ chối khoá học', 'warning')
}
async function publish() {
  await courseService.publish(detail.id)
  detail.status = 'published'
  showToast('Đã xuất bản khoá học', 'success')
}
async function unpublish() {
  await courseService.unpublish(detail.id)
  detail.status = 'draft'
  showToast('Đã gỡ khoá học', 'info')
}
async function archive() {
  const confirmed = await showConfirm({
    title: 'Xác nhận',
    message: 'Lưu trữ khoá học này?',
    type: 'warning',
  })
  if (!confirmed) return
  await courseService.archive(detail.id)
  detail.status = 'archived'
  showToast('Đã lưu trữ khoá học', 'info')
}
async function restore() {
  await courseService.restore(detail.id)
  detail.status = 'draft'
  showToast('Đã khôi phục khoá học', 'success')
}

onMounted(load)
watch(() => route.params.id, load)
</script>
