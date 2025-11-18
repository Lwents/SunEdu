<template>
  <div>
    <!-- Header + actions -->
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div class="space-y-1">
        <h2 class="text-lg font-semibold text-gray-800">Quản lý người dùng</h2>
        <p class="text-sm text-gray-500">Tìm kiếm, lọc, tạo/sửa, khoá và reset mật khẩu</p>
      </div>
      <div class="flex items-center gap-2">
        <el-button type="primary" @click="openCreate">Tạo người dùng</el-button>
        <el-button @click="exportCsv" :loading="loadingExport">Export CSV</el-button>
      </div>
    </div>

    <!-- Toolbar -->
    <div class="grid grid-cols-1 gap-3 md:grid-cols-4 xl:grid-cols-6 items-start">
      <el-input
        v-model="query.q"
        clearable
        placeholder="Tìm theo tên / email / username"
        @clear="applyFilters"
        @keyup.enter="applyFilters"
        class="md:col-span-2 xl:col-span-2 w-full"
      >
        <template #prefix>🔎</template>
      </el-input>

      <el-select
        v-model="query.role"
        clearable
        placeholder="Vai trò"
        @change="applyFilters"
        class="w-full"
      >
        <el-option label="Admin" value="admin" />
        <el-option label="Giáo viên" value="instructor" />
        <el-option label="Học sinh" value="student" />
      </el-select>

      <el-select
        v-model="query.status"
        clearable
        placeholder="Trạng thái"
        @change="applyFilters"
        class="w-full"
      >
        <el-option label="Hoạt động" value="active" />
        <el-option label="Tạm khoá" value="locked" />
        <el-option label="Cấm vĩnh viễn" value="banned" />
      </el-select>

      <!-- Bọc DatePicker để nó co đúng, chiếm 2 cột ở md/xl -->
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
          :style="{ width: '100%' }"
          @change="applyDateRange"
        />
      </div>

      <!-- Action buttons: full width ở mobile, 2 cột ở md, 1 cột ở xl -->
      <div class="md:col-span-2 xl:col-span-1 flex items-center gap-2 md:justify-end">
        <el-button @click="resetFilters">Xoá lọc</el-button>
        <el-button type="primary" plain @click="applyFilters">Lọc</el-button>
      </div>
    </div>

    <!-- Bulk actions -->
    <div class="flex items-center justify-between">
      <div class="text-sm text-gray-500">
        Đã chọn: <b>{{ selection.length }}</b>
      </div>
      <div class="flex items-center gap-2">
        <el-dropdown trigger="click">
          <el-button :disabled="selection.length === 0">
            Thao tác hàng loạt
            <el-icon class="i-ep-arrow-down ml-1" />
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="bulkChangeRole">Đổi vai trò…</el-dropdown-item>
              <el-dropdown-item @click="bulkLock">Khoá</el-dropdown-item>
              <el-dropdown-item @click="bulkUnlock">Mở khoá</el-dropdown-item>
              <el-dropdown-item divided @click="bulkBan" class="text-red-600">
                Cấm vĩnh viễn
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- Table -->
    <div class="rounded-lg bg-white p-3 ring-1 ring-black/5">
      <el-table
        :data="rows"
        v-loading="loading"
        height="520"
        @selection-change="onSelectionChange"
        @sort-change="onSortChange"
        :default-sort="defaultSort"
      >
        <el-table-column type="selection" width="44" />

        <el-table-column label="Người dùng" min-width="260">
          <template #default="{ row }">
            <div class="flex items-center gap-3">
              <img
                :src="getUserAvatar(row)"
                class="h-9 w-9 rounded-full object-cover"
                alt="avatar"
              />
              <div class="min-w-0">
                <div class="truncate font-medium text-gray-800">{{ row.name }}</div>
                <div class="truncate text-xs text-gray-500">{{ row.email }}</div>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="username" label="Username" min-width="140" show-overflow-tooltip />

        <el-table-column label="Vai trò" width="120">
          <template #default="{ row }">
            <el-tag
              :type="
                row.role === 'admin' ? 'danger' : row.role === 'instructor' ? 'warning' : 'success'
              "
              size="small"
              round
            >
              {{ roleLabel(row.role) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="Trạng thái" width="130">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small" round>
              {{ statusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <!-- <el-table-column
          prop="lastLoginAt"
          label="Lần đăng nhập cuối"
          min-width="170"
          sortable="custom"
        >
          <template #default="{ row }">
            <span class="text-gray-700">{{ fmtDate(row.lastLoginAt) || '—' }}</span>
          </template>
        </el-table-column> -->

        <el-table-column prop="createdAt" label="Ngày tạo" min-width="150" sortable="custom">
          <template #default="{ row }">
            {{ fmtDate(row.createdAt) }}
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="Hành động" width="260">
          <template #default="{ row }">
            <div class="flex flex-wrap items-center gap-1">
              <el-button size="small" @click="openEdit(row)">Sửa</el-button>
              <el-button size="small" @click="gotoDetail(row)">Chi tiết</el-button>
              <el-button size="small" type="danger" @click="deleteUser(row)">Xóa</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="mt-3 flex items-center justify-end">
        <el-pagination
          background
          layout="total, sizes, prev, pager, next"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="query.pageSize"
          :current-page="query.page"
          @size-change="onPageSizeChange"
          @current-change="onPageChange"
        />
      </div>
    </div>

    <!-- Create / Edit dialog -->
    <el-dialog
      v-model="formDialog.open"
      :title="formDialog.mode === 'create' ? 'Tạo người dùng' : 'Sửa người dùng'"
      width="520px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
        <!-- <el-form-item label="Họ và tên" prop="name">
          <el-input v-model="form.name" />
        </el-form-item> -->
        <el-form-item label="Username" prop="username">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="Email" prop="email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="Số điện thoại" prop="phone">
          <el-input v-model="form.phone" />
        </el-form-item>
        <el-form-item v-if="formDialog.mode === 'create'" label="Password" prop="password">
          <el-input
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            :suffix-icon="showPassword ? 'el-icon-view' : 'el-icon-view-off'"
            @click-suffix="togglePasswordVisibility"
          />
        </el-form-item>
        <div class="grid grid-cols-2 gap-3">
          <el-form-item label="Vai trò" prop="role">
            <el-select
              v-model="form.role"
              placeholder="Chọn vai trò"
              :disabled="formDialog.mode === 'edit'"
            >
              <!-- <el-option label="Admin" value="admin" /> -->
              <el-option label="Giáo viên" value="instructor" />
              <el-option label="Học sinh" value="student" />
            </el-select>
          </el-form-item>
          <!-- <el-form-item label="Trạng thái" prop="status">
            <el-select v-model="form.status" placeholder="Chọn trạng thái">
              <el-option label="Hoạt động" value="active" />
              <el-option label="Tạm khoá" value="locked" />
              <el-option label="Cấm vĩnh viễn" value="banned" />
              <el-option label="Chờ duyệt" value="pending_approval" />
            </el-select>
          </el-form-item> -->
        </div>
      </el-form>
      <template #footer>
        <el-button @click="formDialog.open = false">Huỷ</el-button>
        <el-button type="primary" :loading="saving" @click="submitForm">
          {{ formDialog.mode === 'create' ? 'Tạo' : 'Lưu' }}
        </el-button>
      </template>
    </el-dialog>

    <!-- Bulk change role dialog -->
    <el-dialog v-model="bulkRoleDialog" title="Đổi vai trò (hàng loạt)" width="420px">
      <el-select v-model="bulkRoleValue" placeholder="Chọn vai trò mới" class="w-full">
        <el-option label="Admin" value="admin" />
        <el-option label="Giáo viên" value="instructor" />
        <el-option label="Học sinh" value="student" />
      </el-select>
      <template #footer>
        <el-button @click="bulkRoleDialog = false">Huỷ</el-button>
        <el-button type="primary" @click="confirmBulkChangeRole" :disabled="!bulkRoleValue">
          Xác nhận ({{ selection.length }})
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { userService } from '@/services/user.service'
import { showToast } from '@/utils/toast'
import { showConfirm } from '@/utils/confirm'
import { getAvatarSrc } from '@/utils/avatar'

type ID = string | number
type Role = 'admin' | 'instructor' | 'student'
type UserStatus = 'active' | 'locked' | 'banned' | 'inactive'
interface User {
  id: ID
  name?: string
  username: string
  email: string
  phone?: string | null
  avatar?: string
  gender?: 'male' | 'female' | 'other' | null
  role: Role
  status: UserStatus
  lastLoginAt?: string
  createdAt: string
  password?: string // Added password property
}
interface PageResult<T> {
  items: T[]
  total: number
}

const route = useRoute()
const router = useRouter()

// query state (URL-synced)
const query = reactive({
  q: (route.query.q as string) || '',
  role: (route.query.role as Role) || '',
  status: (route.query.status as UserStatus) || '',
  from: (route.query.from as string) || '',
  to: (route.query.to as string) || '',
  page: Number(route.query.page || 1),
  pageSize: Number(route.query.pageSize || 20),
  sortBy: (route.query.sortBy as string) || 'createdAt',
  sortDir: (route.query.sortDir as 'ascending' | 'descending') || 'descending',
})
const dateRange = ref<[string, string] | null>(
  query.from && query.to ? [query.from, query.to] : null,
)

const rows = ref<User[]>([])
const total = ref(0)
const loading = ref(false)
const loadingExport = ref(false)

const selection = ref<User[]>([])
const defaultSort = computed(() => ({ prop: query.sortBy, order: query.sortDir }))

function statusType(s: UserStatus) {
  if (s === 'active') return 'success'
  if (s === 'locked') return 'warning'
  if (s === 'banned') return 'danger'
  return 'info'
}
function getUserAvatar(user: User): string {
  return getAvatarSrc(
    user.avatar,
    user.gender,
    user.role
  )
}

const roleLabel = (r: Role) =>
  r === 'admin' ? 'Admin' : r === 'instructor' ? 'Giáo viên' : 'Học sinh'
const statusLabel = (s: UserStatus) =>
  s === 'active'
    ? 'Hoạt động'
    : s === 'locked'
      ? 'Tạm khoá'
      : s === 'banned'
        ? 'Cấm vĩnh viễn'
        : 'Chờ duyệt'
const fmtDate = (iso?: string) => (iso ? new Date(iso).toLocaleString('vi-VN') : '')

// URL sync
function pushQuery() {
  router.replace({
    query: {
      ...route.query,
      q: query.q || undefined,
      role: query.role || undefined,
      status: query.status === 'inactive' ? undefined : query.status || undefined,
      from: query.from || undefined,
      to: query.to || undefined,
      page: query.page.toString(),
      pageSize: query.pageSize.toString(),
      sortBy: query.sortBy || undefined,
      sortDir: query.sortDir || undefined,
    },
  })
}

// fetch
async function fetchList() {
  loading.value = true
  try {
    const params = {
      q: query.q || undefined,
      role: query.role || undefined,
      status: query.status || undefined,
      from: query.from || undefined,
      to: query.to || undefined,
      page: query.page,
      pageSize: query.pageSize,
      sortBy: query.sortBy || 'createdAt',
      sortDir: query.sortDir || 'descending',
    }
    const res: PageResult<User> = await userService.list(params)
    rows.value = res.items
    total.value = res.total
  } catch (error: any) {
    console.error('Error fetching user list:', error)
    showToast(error?.message || 'Không tải được danh sách người dùng', 'error')
  } finally {
    loading.value = false
  }
}

function applyFilters() {
  query.page = 1
  pushQuery()
  fetchList()
}
function resetFilters() {
  query.q = ''
  query.role = '' as any
  query.status = '' as any
  dateRange.value = null
  query.from = ''
  query.to = ''
  query.page = 1
  pushQuery()
  fetchList()
}
function applyDateRange(val: [string, string] | null) {
  if (!val) {
    query.from = ''
    query.to = ''
  } else {
    query.from = val[0]
    query.to = val[1]
  }
  applyFilters()
}
function onPageChange(p: number) {
  query.page = p
  pushQuery()
  fetchList()
}
function onPageSizeChange(sz: number) {
  query.pageSize = sz
  query.page = 1
  pushQuery()
  fetchList()
}
function onSortChange({ prop, order }: { prop: string; order: 'ascending' | 'descending' | null }) {
  query.sortBy = prop || 'createdAt'
  query.sortDir = (order || 'descending') as any
  pushQuery()
  fetchList()
}
function onSelectionChange(val: User[]) {
  selection.value = val
}

// row actions
// async function resetPassword(row: User) {
//   const ok = await showConfirm({ title: 'Xác nhận', message: `Reset mật khẩu cho “${row.name}”?`, type: 'warning' })
//   if (!ok) return
//   await userService.resetPassword(row.id)
//   showToast('Đã gửi hướng dẫn reset mật khẩu', 'info')
// }

async function deleteUser(row: User) {
  const confirmed = await showConfirm({
    title: 'Cảnh báo',
    message: `Bạn có chắc chắn muốn xóa người dùng “${row.name || row.username}”?`,
    type: 'danger',
    })
  if (!confirmed) return
  try {
    await userService.delete(row.id)
    showToast('Người dùng đã được xóa thành công', 'success')
    fetchList()
  } catch (error: any) {
    console.error('Error deleting user:', error)
    showToast(error?.message || 'Không thể xóa người dùng', 'error')
  }
}
// async function lock(row: User) {
//   const ok = await showConfirm({ title: 'Xác nhận', message: `Khoá tài khoản “${row.name}”?`, type: 'warning' })
//   await userService.lock(row.id)
//   showToast('Đã khoá tài khoản', 'info')
//   fetchList()
// }
// async function unlock(row: User) {
//   const ok = await showConfirm({ title: 'Xác nhận', message: `Mở khoá tài khoản “${row.name}”?` })
//   await userService.unlock(row.id)
//   showToast('Đã mở khoá', 'success')
//   fetchList()
// }
// async function ban(row: User) {
//   const ok = await showConfirm({ title: 'Cảnh báo', message: `Cấm vĩnh viễn “${row.name}”?`, type: 'danger' })
//   await userService.ban(row.id)
//   showToast('Đã cấm tài khoản', 'warning')
//   fetchList()
// }
function gotoDetail(row: User) {
  // đảm bảo bạn đã có route /admin/users/:id
  router.push(`/admin/users/${row.id}`)
}

// create / edit
const formDialog = reactive<{ open: boolean; mode: 'create' | 'edit'; id?: ID }>({
  open: false,
  mode: 'create',
})
const formRef = ref()
const form = reactive<User>({
  id: '',
  name: '',
  username: '',
  email: '',
  phone: '',
  avatar: '',
  role: 'student',
  status: 'active',
  createdAt: new Date().toISOString(),
})
const rules = {
  name: [{ required: true, message: 'Nhập họ tên', trigger: 'blur' }],
  username: [{ required: true, message: 'Nhập username', trigger: 'blur' }],
  email: [
    { required: true, message: 'Nhập email', trigger: 'blur' },
    { type: 'email', message: 'Email không hợp lệ', trigger: 'blur' },
  ],
  role: [{ required: true, message: 'Chọn vai trò', trigger: 'change' }],
  status: [{ required: true, message: 'Chọn trạng thái', trigger: 'change' }],
}
const saving = ref(false)
const showPassword = ref(false)

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value
}

function openCreate() {
  formDialog.mode = 'create'
  Object.assign(form, {
    id: '',
    name: '',
    username: '',
    email: '',
    phone: '',
    avatar: '',
    role: 'student',
    status: 'active',
    createdAt: new Date().toISOString(),
  } as User)
  formDialog.open = true
}
function openEdit(row: User) {
  formDialog.mode = 'edit'
  Object.assign(form, row)
  formDialog.open = true
}
async function submitForm() {
  await formRef.value?.validate() // Validate form trước khi gửi
  saving.value = true
  try {
    if (formDialog.mode === 'create') {
      // Gửi payload tạo tài khoản
      await userService.create({
        username: form.username,
        email: form.email,
        password: form.password || '', // Đảm bảo password được gửi
        role: form.role,
      })
      showToast('Tạo người dùng thành công', 'success')
    } else {
      // Gửi payload cập nhật tài khoản
      await userService.update(form.id, {
        username: form.username,
        email: form.email,
        phone: form.phone,
      })
      showToast('Cập nhật thành công', 'success')
    }
    formDialog.open = false
    fetchList() // Refresh danh sách sau khi tạo/cập nhật
  } catch (error: any) {
    console.error('Error saving user:', error)
    showToast(error?.message || 'Không thể lưu dữ liệu', 'error')
  } finally {
    saving.value = false
  }
}

// bulk actions
const bulkRoleDialog = ref(false)
const bulkRoleValue = ref<Role | ''>('')

function bulkChangeRole() {
  if (!selection.value.length) return
  bulkRoleValue.value = '' as any
  bulkRoleDialog.value = true
}
async function confirmBulkChangeRole() {
  const ids = selection.value.map((x) => x.id)
  try {
  await userService.bulkChangeRole(ids, bulkRoleValue.value as Role)
  bulkRoleDialog.value = false
    showToast('Đã đổi vai trò', 'success')
  fetchList()
  } catch (error: any) {
    showToast(error?.message || 'Không thể đổi vai trò', 'error')
  }
}
async function bulkLock() {
  if (!selection.value.length) return
  const confirmed = await showConfirm({
    title: 'Xác nhận',
    message: `Khoá ${selection.value.length} tài khoản đã chọn?`,
    type: 'warning',
  })
  if (!confirmed) return
  await userService.bulkLock(selection.value.map((x) => x.id))
  showToast('Đã khoá tài khoản đã chọn', 'info')
  fetchList()
}
async function bulkUnlock() {
  if (!selection.value.length) return
  const confirmed = await showConfirm({
    title: 'Xác nhận',
    message: `Mở khoá ${selection.value.length} tài khoản đã chọn?`,
  })
  if (!confirmed) return
  await userService.bulkUnlock(selection.value.map((x) => x.id))
  showToast('Đã mở khoá tài khoản đã chọn', 'success')
  fetchList()
}
async function bulkBan() {
  if (!selection.value.length) return
  const confirmed = await showConfirm({
    title: 'Cảnh báo',
    message: `Cấm vĩnh viễn ${selection.value.length} tài khoản?`,
    type: 'danger',
  })
  if (!confirmed) return
  await userService.bulkBan(selection.value.map((x) => x.id))
  showToast('Đã cấm tài khoản đã chọn', 'warning')
  fetchList()
}

// export
async function exportCsv() {
  loadingExport.value = true
  try {
    const blob = await userService.exportCsv({
      q: query.q,
      role: query.role,
      status: query.status || undefined, // ✅ sửa ở đây
      from: query.from,
      to: query.to,
      sortBy: query.sortBy,
      sortDir: query.sortDir,
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `users_${new Date().toISOString().slice(0, 10)}.csv`
    a.click()
    URL.revokeObjectURL(url)
  } catch (error: any) {
    showToast(error?.message || 'Export thất bại', 'error')
  } finally {
    loadingExport.value = false
  }
}

onMounted(fetchList)
watch(
  () => route.query,
  () => {
    // đồng bộ nếu user bấm back/forward
    query.q = (route.query.q as string) || ''
    query.role = (route.query.role as Role) || ('' as any)
    query.status = (route.query.status as UserStatus) || ('' as any)
    query.from = (route.query.from as string) || ''
    query.to = (route.query.to as string) || ''
    query.page = Number(route.query.page || 1)
    query.pageSize = Number(route.query.pageSize || 20)
    query.sortBy = (route.query.sortBy as string) || 'createdAt'
    query.sortDir = (route.query.sortDir as any) || 'descending'
  },
  { deep: true },
)
</script>

<style scoped>
/* Optional: icon space placeholder (Element Plus icon class used above) */
.i-ep-arrow-down::before {
  content: '▾';
  display: inline-block;
}
/* tránh DatePicker giữ width cứng */
/* .el-date-editor.el-input,
.el-date-editor.el-input__wrapper {
  width: 100% !important;
} */
</style>
