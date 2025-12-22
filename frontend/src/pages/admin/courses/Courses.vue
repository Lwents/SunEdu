<template>
  <div class="space-y-4">
    <!-- Toolbar -->
    <div class="grid grid-cols-1 gap-3 md:grid-cols-4 xl:grid-cols-6 items-start">
      <el-input
        v-model="query.q"
        clearable
        placeholder="Tìm tên / mã / giáo viên"
        @clear="applyFilters"
        @keyup.enter="applyFilters"
        class="md:col-span-2 xl:col-span-2 w-full"
      >
        <template #prefix>🔎</template>
      </el-input>

      <el-select v-model="query.grade" clearable placeholder="Lớp" @change="applyFilters">
        <el-option v-for="g in [1, 2, 3, 4, 5]" :key="g" :label="`Lớp ${g}`" :value="g" />
      </el-select>

      <el-select v-model="query.subject" clearable placeholder="Môn" @change="applyFilters">
        <el-option v-for="s in subjects" :key="s.value" :label="s.label" :value="s.value" />
      </el-select>

      <el-select
        v-model="query.teacherId"
        clearable
        filterable
        placeholder="Giáo viên"
        @change="applyFilters"
      >
        <el-option v-for="t in teachers" :key="t.id" :label="t.name" :value="t.id" />
      </el-select>

      <el-select
        v-model="query.status"
        clearable
        placeholder="Trạng thái"
        @change="applyFilters"
        class="xl:col-span-1"
      >
        <el-option label="Bản nháp" value="draft" />
        <el-option label="Chờ duyệt" value="pending_review" />
        <el-option label="Đã xuất bản" value="published" />
        <el-option label="Từ chối" value="rejected" />
        <el-option label="Lưu trữ" value="archived" />
      </el-select>

      <div class="md:col-span-2 xl:col-span-2 min-w-0">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          unlink-panels
          range-separator="–"
          start-placeholder="Tạo từ"
          end-placeholder="đến"
          value-format="YYYY-MM-DD"
          class="w-full"
          @change="applyDateRange"
        />
      </div>

      <div class="md:col-span-2 xl:col-span-1 flex items-center gap-2 md:justify-end">
        <el-button @click="resetFilters">Xoá lọc</el-button>
        <el-button type="primary" plain @click="applyFilters">Lọc</el-button>
      </div>
    </div>

    <!-- Table -->
    <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
      <div class="mb-3 flex items-center justify-between">
        <div class="text-sm text-gray-600">Tổng: {{ total }}</div>
        <div class="flex items-center gap-2">
          <el-button @click="goApproval">Hàng chờ duyệt</el-button>
          <el-button type="primary" @click="refresh" :loading="loading">Tải lại</el-button>
        </div>
      </div>

      <el-table :data="items" v-loading="loading" height="560" @row-dblclick="goDetail">
        <el-table-column label="" width="90">
          <template #default="{ row }">
            <div class="thumb-box">
              <img
                :src="row.thumbnail || placeholderThumb"
                class="thumb-img"
                alt="Course thumbnail"
                @error="(e: any) => { e.target.src = placeholderThumb }"
              />
              <div v-if="!row.thumbnail" class="thumb-badge">Không có ảnh</div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="title" label="Khoá học" min-width="240" show-overflow-tooltip>
          <template #default="{ row }">
            <div
              class="font-medium text-gray-800 hover:text-blue-600 cursor-pointer"
              @click="goDetail(row)"
            >
              {{ row.title }}
            </div>
            <div class="text-xs text-gray-500">GV: {{ row.teacherName }}</div>
          </template>
        </el-table-column>

        <el-table-column label="Lớp/Môn" width="160">
          <template #default="{ row }">
            <div class="text-sm">Lớp {{ row.grade }}</div>
            <div class="text-xs text-gray-500 truncate">
              {{ subjectDisplay(row) || '—' }}
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="lessonsCount" label="Bài" width="80" align="center" />
        <el-table-column prop="enrollments" label="HV" width="90" align="center" />

        <el-table-column prop="status" label="Trạng thái" width="140" align="center">
          <template #default="{ row }">
            <el-tag :type="statusTagType(row.status)" size="small">{{
              statusLabel(row.status)
            }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="updatedAt" label="Cập nhật" min-width="160">
          <template #default="{ row }">{{ fmtDate(row.updatedAt) }}</template>
        </el-table-column>

        <el-table-column fixed="right" label="" width="250">
          <template #default="{ row }">
            <div class="flex gap-2 justify-end">
              <el-button size="small" @click="goDetail(row)">Xem</el-button>
              <el-button
                v-if="row.status !== 'published' && row.status !== 'archived'"
                size="small"
                type="success"
                plain
                @click="publish(row)"
                >Xuất bản</el-button
              >
              <el-button v-if="row.status === 'published'" size="small" @click="unpublish(row)"
                >Gỡ</el-button
              >
              <el-button
                v-if="row.status !== 'archived'"
                size="small"
                type="warning"
                plain
                @click="archive(row)"
                >Lưu trữ</el-button
              >
              <el-button v-else size="small" type="info" plain @click="restore(row)"
                >Khôi phục</el-button
              >
            </div>
          </template>
        </el-table-column>
      </el-table>

      <div class="mt-3 flex justify-end">
        <el-pagination
          background
          layout="total, prev, pager, next"
          :total="total"
          :current-page="page"
          :page-size="pageSize"
          @current-change="
            (p: number) => {
              page = p
              fetch()
            }
          "
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from '@/utils/toast'
import { showConfirm } from '@/utils/confirm'
import {
  courseService,
  type CourseSummary,
  type CourseStatus,
  type PageParams,
  type Subject,
} from '@/services/course.service'

const router = useRouter()

const subjects = courseService.subjects()
const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i
const teachers = ref<{ id: number | string; name: string }[]>([])
const items = ref<CourseSummary[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)

const query = reactive<PageParams>({
  q: '',
  grade: undefined,
  subject: undefined,
  teacherId: undefined,
  status: undefined,
  page: page.value,
  pageSize,
})
const dateRange = ref<[string, string] | null>(null)

function subjectName(s: Subject) {
  return subjects.find((x) => x.value === s)?.label || s
}
function subjectDisplay(row: Partial<CourseSummary> & Record<string, any>) {
  const fromBackend =
    row.subjectLabel ||
    row.subject_label ||
    row.subjectName ||
    row.subject_name ||
    row.subjectTitle ||
    row.subject_title
  if (typeof fromBackend === 'string' && !uuidRegex.test(fromBackend)) {
    return fromBackend
  }
  const fallback = row.subject ? subjectName(row.subject as Subject) : ''
  if (typeof fallback === 'string' && fallback && !uuidRegex.test(fallback)) {
    return fallback
  }
  if (row.title && typeof row.title === 'string') {
    return row.title
  }
  return ''
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
const fmtDate = (iso?: string) => {
  if (!iso) return ''
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return ''
  return d.toLocaleString('vi-VN')
}

function applyDateRange() {
  query.from = dateRange.value?.[0]
  query.to = dateRange.value?.[1]
  applyFilters()
}
function resetFilters() {
  query.q = ''
  query.grade = undefined
  query.subject = undefined
  query.teacherId = undefined
  query.status = undefined
  query.from = undefined
  query.to = undefined
  dateRange.value = null
  page.value = 1
  fetch()
}
function applyFilters() {
  page.value = 1
  fetch()
}

async function fetch() {
  loading.value = true
  try {
    const { items: rows, total: t } = await courseService.list({
      ...query,
      page: page.value,
      pageSize,
    }, true)
    items.value = rows
    total.value = t
  } finally {
    loading.value = false
  }
}
function refresh() {
  fetch()
}

function goDetail(row: CourseSummary) {
  router.push(`/admin/courses/${row.id}`)
}
function goApproval() {
  router.push('/admin/courses/approval')
}

// Actions
async function publish(row: CourseSummary) {
  const confirmed = await showConfirm({
    title: 'Xác nhận',
    message: `Xuất bản khoá “${row.title}”?`,
  })
  if (!confirmed) return
  try {
  await courseService.publish(row.id)
    showToast('Đã xuất bản khoá học', 'success')
  fetch()
  } catch (error: any) {
    showToast(error?.message || 'Không thể xuất bản khoá học', 'error')
  }
}
async function unpublish(row: CourseSummary) {
  const confirmed = await showConfirm({
    title: 'Xác nhận',
    message: `Xoá khoá học “${row.title}”?`,
  })
  if (!confirmed) return
  try {
  await courseService.delete(row.id, true)
    showToast('Đã xoá khoá học', 'info')
  fetch()
  } catch (error: any) {
    showToast(error?.message || 'Không thể xoá khoá học', 'error')
  }
}
async function archive(row: CourseSummary) {
  const confirmed = await showConfirm({
    title: 'Xác nhận',
    message: `Lưu trữ khoá “${row.title}”?`,
    type: 'warning',
  })
  if (!confirmed) return
  try {
  await courseService.archive(row.id)
    showToast('Đã lưu trữ khoá học', 'info')
  fetch()
  } catch (error: any) {
    showToast(error?.message || 'Không thể lưu trữ khoá học', 'error')
  }
}
async function restore(row: CourseSummary) {
  try {
  await courseService.restore(row.id)
    showToast('Đã khôi phục khoá học', 'success')
  fetch()
  } catch (error: any) {
    showToast(error?.message || 'Không thể khôi phục khoá học', 'error')
  }
}

onMounted(async () => {
  fetch()
  try {
    teachers.value = await courseService.listTeachers()
  } catch (error: any) {
    showToast(error?.message || 'Không tải được danh sách giáo viên', 'warning')
  }
})

const placeholderThumb =
  'data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"160\" height=\"90\" viewBox=\"0 0 160 90\"><rect width=\"160\" height=\"90\" fill=\"%23f3f4f6\" rx=\"8\"/><path d=\"M52 56l14-18 12 14 8-10 20 24H52z\" fill=\"%23d1d5db\"/><circle cx=\"65\" cy=\"38\" r=\"6\" fill=\"%23d1d5db\"/><text x=\"80\" y=\"82\" text-anchor=\"middle\" font-family=\"Arial\" font-size=\"12\" fill=\"%239ca3af\">No image</text></svg>'
</script>

<style scoped>
.thumb-box {
  position: relative;
  width: 72px;
  height: 48px;
  border-radius: 8px;
  overflow: hidden;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
}
.thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.thumb-badge {
  position: absolute;
  bottom: 4px;
  left: 4px;
  right: 4px;
  background: rgba(0, 0, 0, 0.55);
  color: #fff;
  font-size: 10px;
  padding: 2px 4px;
  border-radius: 4px;
  text-align: center;
  line-height: 1.2;
}
</style>
