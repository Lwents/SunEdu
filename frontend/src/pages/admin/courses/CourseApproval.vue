<template>
  <div class="space-y-4">
    <div class="flex flex-wrap items-center gap-2">
      <el-input
        v-model="query.q"
        placeholder="Tìm theo tên / GV"
        clearable
        @keyup.enter="apply"
        @clear="apply"
      >
        <template #prefix>🔎</template>
      </el-input>
      <el-select v-model="query.subject" clearable placeholder="Môn" @change="apply">
        <el-option v-for="s in subjects" :key="s.value" :label="s.label" :value="s.value" />
      </el-select>
      <el-select
        v-model="query.teacherId"
        clearable
        filterable
        placeholder="Giáo viên"
        @change="apply"
      >
        <el-option v-for="t in teachers" :key="t.id" :label="t.name" :value="t.id" />
      </el-select>
      <el-button @click="reset">Xoá lọc</el-button>
      <el-button type="primary" plain @click="apply">Lọc</el-button>
      <div class="ml-auto flex items-center gap-2">
        <el-button type="success" :disabled="selIds.length === 0" @click="bulkApprove"
          >Duyệt {{ selIds.length }}</el-button
        >
        <el-button type="danger" :disabled="selIds.length === 0" @click="bulkReject"
          >Từ chối {{ selIds.length }}</el-button
        >
      </div>
    </div>

    <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
      <el-table :data="items" v-loading="loading" height="560" @selection-change="onSelection">
        <el-table-column type="selection" width="42" fixed="left" />
        <el-table-column label="" width="72">
          <template #default="{ row }"
            ><img :src="row.thumbnail" class="h-10 w-16 rounded object-cover"
          /></template>
        </el-table-column>
        <el-table-column label="Khoá học" min-width="260" show-overflow-tooltip>
          <template #default="{ row }">
            <div class="font-medium text-gray-800">{{ row.title }}</div>
            <div class="text-xs text-gray-500">
              GV: {{ row.teacherName }} • Lớp {{ row.grade }} • {{ subjectName(row.subject) }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="lessonsCount" label="Bài" width="80" align="center" />
        <el-table-column prop="updatedAt" label="Cập nhật" min-width="160">
          <template #default="{ row }">{{ fmtDate(row.updatedAt) }}</template>
        </el-table-column>
        <el-table-column fixed="right" width="240">
          <template #default="{ row }">
            <div class="flex justify-end gap-2">
              <el-button size="small" type="success" plain @click="approve(row)">Duyệt</el-button>
              <el-button size="small" type="danger" plain @click="reject(row)">Từ chối</el-button>
              <el-button size="small" @click="view(row)">Xem</el-button>
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
import {
  courseService,
  type CourseSummary,
  type PageParams,
  type Subject,
} from '@/services/course.service'
import { showToast } from '@/utils/toast'
import { showConfirm } from '@/utils/confirm'

const router = useRouter()
const subjects = courseService.subjects()
const teachers = ref<{ id: number | string; name: string }[]>([])
const items = ref<CourseSummary[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)
const selIds = ref<(number | string)[]>([])

const query = reactive<PageParams>({ q: '', subject: undefined, teacherId: undefined })

function subjectName(s: Subject) {
  return subjects.find((x) => x.value === s)?.label || s
}
const fmtDate = (iso?: string) => (iso ? new Date(iso).toLocaleString('vi-VN') : '')

async function fetch() {
  loading.value = true
  try {
    const { items: rows, total: t } = await courseService.list({
      ...query,
      status: 'pending_review',
      page: page.value,
      pageSize,
    })
    items.value = rows
    total.value = t
  } catch (error: any) {
    showToast(error?.message || 'Không tải được danh sách khoá chờ duyệt', 'error')
  } finally {
    loading.value = false
  }
}
function onSelection(rows: CourseSummary[]) {
  selIds.value = rows.map((r) => r.id)
}
function reset() {
  query.q = ''
  query.subject = undefined
  query.teacherId = undefined
  page.value = 1
  fetch()
}
function apply() {
  page.value = 1
  fetch()
}

async function approve(row: CourseSummary) {
  const confirmed = await showConfirm({
    title: 'Xác nhận',
    message: `Duyệt khoá “${row.title}”?`,
  })
  if (!confirmed) return
  await courseService.approve(row.id)
  showToast('Đã duyệt khoá học', 'success')
  fetch()
}
async function reject(row: CourseSummary) {
  const reason = window.prompt('Lý do từ chối (tuỳ chọn)', '')
  if (reason === null) return
  await courseService.reject(row.id, reason)
  showToast('Đã từ chối khoá học', 'warning')
    fetch()
}
async function bulkApprove() {
  const confirmed = await showConfirm({
    title: 'Xác nhận',
    message: `Duyệt ${selIds.value.length} khoá đã chọn?`,
  })
  if (!confirmed) return
  await courseService.bulkApprove(selIds.value)
  showToast('Đã duyệt các khoá đã chọn', 'success')
  fetch()
}
async function bulkReject() {
  const reason = window.prompt(
    `Nhập lý do từ chối (áp dụng cho ${selIds.value.length} khoá)`,
    '',
  )
  if (reason === null) return
  await courseService.bulkReject(selIds.value, reason)
  showToast('Đã từ chối các khoá đã chọn', 'warning')
    fetch()
}
function view(row: CourseSummary) {
  router.push(`/admin/courses/${row.id}`)
}

onMounted(async () => {
  teachers.value = await courseService.listTeachers()
  fetch()
})
</script>
