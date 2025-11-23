<template>
  <div class="space-y-4">
    <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
      <div class="flex items-center justify-between">
        <div class="text-lg font-semibold">Nhật ký hoạt động</div>
        <div class="flex items-center gap-2">
          <el-button @click="reset">Xoá lọc</el-button>
          <el-button type="primary" plain @click="apply">Lọc</el-button>
          <el-button :loading="exporting" @click="doExport">Xuất CSV</el-button>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="grid grid-cols-1 gap-3 md:grid-cols-4 xl:grid-cols-8">
      <el-input
        v-model="q"
        placeholder="Tìm (actor/action/target...)"
        clearable
        @keyup.enter="apply"
        @clear="apply"
        class="xl:col-span-2"
      />
      <el-select v-model="role" clearable placeholder="Vai trò" @change="apply">
        <el-option label="Admin" value="admin" />
        <el-option label="Giáo viên" value="teacher" />
        <el-option label="Học sinh" value="student" />
        <el-option label="System" value="system" />
      </el-select>
      <el-input v-model="action" placeholder="Action (vd: user.create)" @keyup.enter="apply" />
      <el-select v-model="targetType" clearable placeholder="Target type" @change="apply">
        <el-option label="user" value="user" />
        <el-option label="course" value="course" />
        <el-option label="exam" value="exam" />
        <el-option label="payment" value="payment" />
        <el-option label="config" value="config" />
        <el-option label="security" value="security" />
        <el-option label="system" value="system" />
      </el-select>
      <el-input v-model="targetId" placeholder="Target ID" @keyup.enter="apply" />
      <el-select v-model="result" clearable placeholder="Kết quả" @change="apply">
        <el-option label="success" value="success" />
        <el-option label="failed" value="failed" />
      </el-select>
      <el-input v-model="ip" placeholder="IP" @keyup.enter="apply" />
      <el-date-picker
        v-model="range"
        type="daterange"
        unlink-panels
        value-format="YYYY-MM-DD"
        start-placeholder="Từ"
        end-placeholder="Đến"
        @change="apply"
      />
    </div>

    <!-- Table -->
    <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
      <div class="mb-2 text-sm text-gray-600">Tổng: {{ total }}</div>
      <el-table :data="items" v-loading="loading" height="560" @row-dblclick="open">
        <el-table-column prop="ts" label="Thời gian" width="180">
          <template #default="{ row }">{{ fmt(row.ts) }}</template>
        </el-table-column>
        <el-table-column label="Actor" min-width="180" show-overflow-tooltip>
          <template #default="{ row }">
            <div class="font-medium">{{ row.actorName }}</div>
            <div class="text-xs text-gray-500">{{ row.actorRole }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="action" label="Action" min-width="180" />
        <el-table-column label="Target" min-width="160" show-overflow-tooltip>
          <template #default="{ row }">{{ row.targetType }} #{{ row.targetId }}</template>
        </el-table-column>
        <el-table-column prop="result" label="KQ" width="90" align="center">
          <template #default="{ row }">
            <el-tag size="small" :type="row.result === 'success' ? 'success' : 'danger'">{{
              row.result
            }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="ip" label="IP" width="130" />
        <el-table-column prop="traceId" label="Trace" min-width="160" />
        <el-table-column fixed="right" width="110">
          <template #default="{ row }">
            <el-button size="small" @click="open(row)">Chi tiết</el-button>
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

    <!-- Detail Dialog -->
    <el-dialog
      v-model="drawer"
      title="Chi tiết hoạt động"
      width="90%"
      class="sm:!w-[600px]"
      :close-on-click-modal="false"
    >
      <div v-if="current" class="space-y-4">
        <!-- Header Info -->
        <div class="rounded-xl border-2 border-slate-200 bg-gradient-to-br from-slate-50 to-white p-4">
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-2">
                <h3 class="text-lg font-bold text-slate-900">{{ current.action }}</h3>
                <el-tag size="small" :type="current.result === 'success' ? 'success' : 'danger'">
                  {{ current.result === 'success' ? 'Thành công' : 'Thất bại' }}
                </el-tag>
              </div>
              <p class="text-sm text-slate-600">{{ fmt(current.ts) }}</p>
            </div>
            <div class="text-right">
              <div class="text-xs text-slate-500 mb-1">ID</div>
              <div class="text-sm font-mono text-slate-700">{{ current.id }}</div>
            </div>
          </div>
        </div>

        <!-- Actor Information -->
        <div class="rounded-xl border border-slate-200 bg-white p-4">
          <div class="flex items-center gap-2 mb-3">
            <svg class="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <h4 class="font-semibold text-slate-900">Người thực hiện</h4>
          </div>
          <div class="space-y-2 pl-7">
            <div class="flex items-center gap-2">
              <span class="text-sm font-medium text-slate-700 w-20">Email:</span>
              <span class="text-sm text-slate-900">{{ current.actorName || '—' }}</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-sm font-medium text-slate-700 w-20">Vai trò:</span>
              <el-tag size="small" :type="current.actorRole === 'admin' ? 'danger' : current.actorRole === 'teacher' ? 'warning' : 'success'">
                {{ current.actorRole === 'admin' ? 'Admin' : current.actorRole === 'teacher' ? 'Giáo viên' : 'Học sinh' }}
              </el-tag>
            </div>
            <div v-if="current.actorId" class="flex items-center gap-2">
              <span class="text-sm font-medium text-slate-700 w-20">User ID:</span>
              <span class="text-sm font-mono text-slate-600">#{{ current.actorId }}</span>
            </div>
          </div>
        </div>

        <!-- Action Details -->
        <div class="rounded-xl border border-slate-200 bg-white p-4">
          <div class="flex items-center gap-2 mb-3">
            <svg class="h-5 w-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h4 class="font-semibold text-slate-900">Thông tin hành động</h4>
          </div>
          <div class="space-y-2 pl-7">
            <div class="flex items-center gap-2">
              <span class="text-sm font-medium text-slate-700 w-24">Action:</span>
              <span class="text-sm font-mono text-slate-900 bg-slate-50 px-2 py-1 rounded">{{ current.action }}</span>
            </div>
            <div v-if="current.targetType" class="flex items-center gap-2">
              <span class="text-sm font-medium text-slate-700 w-24">Target:</span>
              <span class="text-sm text-slate-900">{{ current.targetType }} #{{ current.targetId }}</span>
            </div>
            <div v-if="current.message" class="flex items-center gap-2">
              <span class="text-sm font-medium text-slate-700 w-24">Message:</span>
              <span class="text-sm text-slate-900">{{ current.message }}</span>
            </div>
          </div>
        </div>

        <!-- Network Information -->
        <div v-if="current.ip || current.userAgent" class="rounded-xl border border-slate-200 bg-white p-4">
          <div class="flex items-center gap-2 mb-3">
            <svg class="h-5 w-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
            </svg>
            <h4 class="font-semibold text-slate-900">Thông tin mạng</h4>
          </div>
          <div class="space-y-2 pl-7">
            <div v-if="current.ip" class="flex items-center gap-2">
              <span class="text-sm font-medium text-slate-700 w-20">IP Address:</span>
              <span class="text-sm font-mono text-slate-900 bg-slate-50 px-2 py-1 rounded">{{ current.ip }}</span>
            </div>
            <div v-if="current.userAgent" class="flex items-start gap-2">
              <span class="text-sm font-medium text-slate-700 w-20">User Agent:</span>
              <span class="text-xs text-slate-600 bg-slate-50 px-2 py-1 rounded break-all">{{ current.userAgent }}</span>
            </div>
            <div v-if="current.traceId" class="flex items-center gap-2">
              <span class="text-sm font-medium text-slate-700 w-20">Trace ID:</span>
              <span class="text-sm font-mono text-slate-600">{{ current.traceId }}</span>
            </div>
          </div>
        </div>

        <!-- Metadata -->
        <div v-if="current.meta && Object.keys(current.meta).length > 0" class="rounded-xl border border-slate-200 bg-white p-4">
          <div class="flex items-center gap-2 mb-3">
            <svg class="h-5 w-5 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h4 class="font-semibold text-slate-900">Metadata</h4>
          </div>
          <div class="pl-7">
            <pre class="bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs text-slate-700 overflow-auto max-h-64 font-mono">{{ pretty(current.meta) }}</pre>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!current.ip && !current.userAgent && (!current.meta || Object.keys(current.meta).length === 0)" class="rounded-xl border-2 border-dashed border-slate-200 bg-slate-50 p-6 text-center">
          <svg class="h-12 w-12 text-slate-400 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="text-sm text-slate-500">Không có thông tin bổ sung</p>
        </div>
      </div>
      
      <div v-else class="flex items-center justify-center py-12">
        <div class="text-center">
          <div class="h-8 w-8 border-2 border-slate-300 border-t-slate-900 rounded-full animate-spin mx-auto mb-2"></div>
          <p class="text-sm text-slate-500">Đang tải...</p>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end">
          <el-button @click="drawer = false">Đóng</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { logService, type LogItem, type LogQuery } from '@/services/log.service'

const items = ref<LogItem[]>([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)
const exporting = ref(false)

const q = ref('')
const role = ref<'admin' | 'teacher' | 'student' | 'system' | ''>('')
const action = ref('')
const targetType = ref<LogQuery['targetType'] | ''>('')
const targetId = ref('')
const result = ref<'success' | 'failed' | ''>('')
const ip = ref('')
const range = ref<[string, string] | null>(null)

const drawer = ref(false)
const current = ref<LogItem | null>(null)

function params(): LogQuery {
  return {
    q: q.value || undefined,
    role: (role.value || undefined) as any,
    action: action.value || undefined,
    targetType: (targetType.value || undefined) as any,
    targetId: targetId.value ? Number(targetId.value) : undefined,
    result: (result.value || undefined) as any,
    ip: ip.value || undefined,
    from: range.value?.[0],
    to: range.value?.[1],
    page: page.value,
    pageSize,
  }
}
function reset() {
  q.value =
    role.value =
    action.value =
    targetType.value =
    targetId.value =
    result.value =
    ip.value =
      ''
  range.value = null
  page.value = 1
  fetch()
}
function apply() {
  page.value = 1
  fetch()
}
async function fetch() {
  loading.value = true
  try {
    const { items: rows, total: t } = await logService.list(params())
    items.value = rows
    total.value = t
  } finally {
    loading.value = false
  }
}
function fmt(iso?: string) {
  return iso ? new Date(iso).toLocaleString('vi-VN') : ''
}
function pretty(v: any) {
  try {
    return JSON.stringify(v ?? {}, null, 2)
  } catch {
    return String(v)
  }
}
async function doExport() {
  exporting.value = true
  try {
    const blob = await logService.exportCsv(params())
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `logs_${new Date().toISOString().slice(0, 10)}.csv`
    a.click()
    URL.revokeObjectURL(url)
  } finally {
    exporting.value = false
  }
}
async function open(row: LogItem) {
  current.value = await logService.detail(row.id)
  drawer.value = true
}

onMounted(fetch)
</script>
