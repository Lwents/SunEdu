<template>
  <div class="courses-page">
    <!-- Filter Bar -->
    <div class="filter-card">
      <div class="filter-grid">
        <el-input
          v-model="query.q"
          clearable
          placeholder="🔎 Tìm tên / mã / giáo viên"
          @clear="applyFilters"
          @keyup.enter="applyFilters"
          class="filter-search"
        />

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



        <el-date-picker
          v-model="dateRange"
          type="daterange"
          unlink-panels
          range-separator="→"
          start-placeholder="Từ ngày"
          end-placeholder="Đến ngày"
          value-format="YYYY-MM-DD"
          @change="applyDateRange"
          class="filter-date"
        />

        <div class="filter-actions">
          <el-button @click="resetFilters">Xoá lọc</el-button>
          <el-button type="primary" @click="applyFilters">Lọc</el-button>
        </div>
      </div>
    </div>

    <!-- Table Card -->
    <div class="table-card">
      <div class="table-header">
        <span class="total-count">Tổng: {{ total }}</span>
        <div class="header-actions">
          <el-button type="primary" @click="refresh" :loading="loading">Tải lại</el-button>
        </div>
      </div>

      <el-table :data="items" v-loading="loading" height="560" @row-dblclick="goDetail">
        <el-table-column label="" width="90">
          <template #default="{ row }">
            <div class="thumb-box">
              <img
                :src="getThumbnailSrc(row.thumbnail)"
                class="thumb-img"
                alt="Course thumbnail"
                @error="(e: any) => { e.target.src = placeholderThumb }"
              />
              <div v-if="!hasThumbnail(row.thumbnail)" class="thumb-badge">Không có ảnh</div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="title" label="Khoá học" min-width="240" show-overflow-tooltip>
          <template #default="{ row }">
            <div class="course-title" @click="goDetail(row)">
              {{ row.title }}
            </div>
            <div class="course-teacher">GV: {{ row.teacherName }}</div>
          </template>
        </el-table-column>

        <el-table-column label="Lớp/Môn" width="160">
          <template #default="{ row }">
            <div class="grade-text">Lớp {{ row.grade }}</div>
            <div class="subject-text">{{ subjectDisplay(row) || '—' }}</div>
          </template>
        </el-table-column>

        <el-table-column prop="lessonsCount" label="Bài" width="80" align="center" />
        <el-table-column prop="enrollments" label="HV" width="90" align="center" />

        <el-table-column prop="status" label="Trạng thái" width="140" align="center">
          <template #default="{ row }">
            <span 
              class="status-badge"
              :class="{
                'status-draft': row.status === 'draft',
                'status-pending': row.status === 'pending_review',
                'status-published': row.status === 'published',
                'status-rejected': row.status === 'rejected',
                'status-archived': row.status === 'archived'
              }"
            >
              {{ statusLabel(row.status) }}
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="updatedAt" label="Cập nhật" min-width="160">
          <template #default="{ row }">
            <span class="date-text">{{ fmtDate(row.updatedAt) }}</span>
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="" width="280">
          <template #default="{ row }">
            <div class="action-buttons">
              <button class="action-btn btn-view" @click="goDetail(row)">Xem</button>
              <button
                v-if="row.status !== 'published' && row.status !== 'archived'"
                class="action-btn btn-publish"
                @click="publish(row)"
              >Xuất bản</button>
              <button 
                v-if="row.status === 'published'" 
                class="action-btn btn-unpublish" 
                @click="unpublish(row)"
              >Gỡ</button>
              <button
                v-if="row.status !== 'archived'"
                class="action-btn btn-archive"
                @click="archive(row)"
              >Lưu trữ</button>
              <button 
                v-else 
                class="action-btn btn-restore" 
                @click="restore(row)"
              >Khôi phục</button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <div class="table-footer">
        <el-pagination
          background
          layout="total, prev, pager, next"
          :total="total"
          :current-page="page"
          :page-size="pageSize"
          @current-change="(p: number) => { page = p; fetch() }"
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
import { resolveMediaUrl } from '@/utils/media'
import {
  courseService,
  type CourseSummary,
  type CourseStatus,
  type PageParams,
  type Subject,
} from '@/services/course.service'

const router = useRouter()

const subjects = ref<{ label: string; value: string }[]>(courseService.subjects())
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
  return subjects.value.find((x: any) => x.value === s)?.label || s
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
const getThumbnailSrc = (thumbnail?: string) => resolveMediaUrl(thumbnail) || placeholderThumb
const hasThumbnail = (thumbnail?: string) => !!resolveMediaUrl(thumbnail)

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
  try {
    subjects.value = await courseService.listSubjects()
  } catch (error: any) {
    console.warn('Could not load subjects from API:', error?.message)
  }
})

const placeholderThumb =
  'data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"160\" height=\"90\" viewBox=\"0 0 160 90\"><rect width=\"160\" height=\"90\" fill=\"%23f3f4f6\" rx=\"8\"/><path d=\"M52 56l14-18 12 14 8-10 20 24H52z\" fill=\"%23d1d5db\"/><circle cx=\"65\" cy=\"38\" r=\"6\" fill=\"%23d1d5db\"/><text x=\"80\" y=\"82\" text-anchor=\"middle\" font-family=\"Arial\" font-size=\"12\" fill=\"%239ca3af\">No image</text></svg>'
</script>

<style scoped>
.courses-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Filter Card */
.filter-card {
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(30, 41, 59, 0.5);
}

.filter-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: end;
}

.filter-grid > * {
  flex: 1;
  min-width: 140px;
}

.filter-search {
  flex: 2;
  min-width: 200px;
}

.filter-date {
  flex: 2;
  min-width: 240px;
}

.filter-actions {
  display: flex;
  gap: 8px;
  flex: 0 0 auto;
}

/* Table Card */
.table-card {
  padding: 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(30, 41, 59, 0.5);
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.total-count {
  font-size: 14px;
  color: #94a3b8;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.table-footer {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

/* Thumbnail */
.thumb-box {
  position: relative;
  width: 72px;
  height: 48px;
  border-radius: 8px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.05);
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
  background: rgba(0, 0, 0, 0.7);
  color: #fff;
  font-size: 9px;
  padding: 2px 4px;
  border-radius: 4px;
  text-align: center;
}

/* Course Info */
.course-title {
  font-weight: 500;
  color: #e2e8f0;
  cursor: pointer;
  transition: color 0.2s;
}

.course-title:hover {
  color: #22d3ee;
}

.course-teacher {
  font-size: 12px;
  color: #64748b;
}

.grade-text {
  font-size: 14px;
  color: #e2e8f0;
}

.subject-text {
  font-size: 12px;
  color: #64748b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.date-text {
  font-size: 13px;
  color: #94a3b8;
}

/* Status Badges */
.status-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-draft {
  background: rgba(148, 163, 184, 0.15);
  color: #94a3b8;
}

.status-pending {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

.status-published {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.status-rejected {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.status-archived {
  background: rgba(100, 116, 139, 0.15);
  color: #64748b;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 6px;
  justify-content: flex-end;
  flex-wrap: nowrap;
}

.action-btn {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid;
  white-space: nowrap;
}

.btn-view {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.15);
  color: #e2e8f0;
}

.btn-view:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.2);
}

.btn-publish {
  background: rgba(34, 197, 94, 0.15);
  border-color: rgba(34, 197, 94, 0.3);
  color: #22c55e;
}

.btn-publish:hover {
  background: rgba(34, 197, 94, 0.25);
}

.btn-unpublish {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.btn-unpublish:hover {
  background: rgba(239, 68, 68, 0.25);
}

.btn-archive {
  background: rgba(251, 191, 36, 0.15);
  border-color: rgba(251, 191, 36, 0.3);
  color: #fbbf24;
}

.btn-archive:hover {
  background: rgba(251, 191, 36, 0.25);
}

.btn-restore {
  background: rgba(59, 130, 246, 0.15);
  border-color: rgba(59, 130, 246, 0.3);
  color: #3b82f6;
}

.btn-restore:hover {
  background: rgba(59, 130, 246, 0.25);
}

/* Responsive */
@media (max-width: 768px) {
  .filter-search {
    grid-column: span 1;
  }
  
  .action-buttons {
    flex-wrap: wrap;
  }
}

/* ============================================== */
/* Light Mode Overrides                          */
/* ============================================== */
html:not(.dark) .filter-card,
html:not(.dark) .table-card {
  background: #fff;
  border-color: #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

html:not(.dark) .total-count {
  color: #64748b;
}

html:not(.dark) .thumb-box {
  background: #f1f5f9;
}

html:not(.dark) .course-title {
  color: #1e293b;
}

html:not(.dark) .course-title:hover {
  color: #0ea5e9;
}

html:not(.dark) .course-teacher,
html:not(.dark) .subject-text {
  color: #64748b;
}

html:not(.dark) .grade-text {
  color: #334155;
}

html:not(.dark) .date-text {
  color: #64748b;
}

html:not(.dark) .btn-view {
  background: #f8fafc;
  border-color: #e2e8f0;
  color: #334155;
}

html:not(.dark) .btn-view:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

html:not(.dark) .btn-publish {
  background: rgba(34, 197, 94, 0.1);
  border-color: rgba(34, 197, 94, 0.4);
  color: #16a34a;
}

html:not(.dark) .btn-unpublish {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.4);
  color: #dc2626;
}

html:not(.dark) .btn-archive {
  background: rgba(251, 191, 36, 0.1);
  border-color: rgba(251, 191, 36, 0.4);
  color: #d97706;
}

html:not(.dark) .btn-restore {
  background: rgba(59, 130, 246, 0.1);
  border-color: rgba(59, 130, 246, 0.4);
  color: #2563eb;
}
</style>
