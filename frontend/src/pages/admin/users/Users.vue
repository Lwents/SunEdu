<template>
  <div class="users-page">
    <!-- Header -->
    <div class="page-header">
      <div class="header-info">
        <h2 class="page-title">👥 Quản lý người dùng</h2>
        <p class="page-desc">Tìm kiếm, lọc, tạo/sửa, khoá và reset mật khẩu</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="openCreate">
          <span class="btn-icon">+</span> Tạo người dùng
        </el-button>
        <router-link to="/admin/users/bulk-create">
          <el-button type="success">
            📋 Tạo hàng loạt
          </el-button>
        </router-link>
        <el-button @click="exportCsv" :loading="loadingExport">Export CSV</el-button>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="filter-card">
      <div class="filter-grid">
        <el-input
          v-model="query.q"
          clearable
          placeholder="🔎 Tìm theo tên / email / username"
          @clear="applyFilters"
          @keyup.enter="applyFilters"
          @input="debouncedSearch"
          class="filter-search"
        />

        <el-select
          v-model="query.role"
          clearable
          placeholder="Vai trò"
          @change="applyFilters"
        >
          <el-option label="Giáo viên" value="instructor" />
          <el-option label="Học sinh" value="student" />
        </el-select>

        <el-select
          v-model="query.status"
          clearable
          placeholder="Trạng thái"
          @change="applyFilters"
        >
          <el-option label="Hoạt động" value="active" />
          <el-option label="Tạm khoá" value="locked" />
          <el-option label="Cấm vĩnh viễn" value="banned" />
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

    <!-- Bulk Actions Bar -->
    <div class="bulk-bar">
      <span class="selection-count">Đã chọn: <strong>{{ selection.length }}</strong></span>
      <el-dropdown trigger="click" :disabled="selection.length === 0">
        <el-button :disabled="selection.length === 0">
          Thao tác hàng loạt ▾
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="bulkChangeRole">Đổi vai trò…</el-dropdown-item>
            <el-dropdown-item @click="bulkLock">Khoá</el-dropdown-item>
            <el-dropdown-item @click="bulkUnlock">Mở khoá</el-dropdown-item>
            <el-dropdown-item divided @click="bulkBan" class="text-danger">
              Cấm vĩnh viễn
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>

    <!-- Table Card -->
    <div class="table-card">
      <el-table
        :data="rows"
        v-loading="loading"
        height="520"
        @selection-change="onSelectionChange"
        @sort-change="onSortChange"
        :default-sort="defaultSort"
      >
        <!-- Empty state -->
        <template #empty>
          <div class="empty-state">
            <svg class="empty-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
            </svg>
            <p class="empty-title">Không có dữ liệu</p>
            <p class="empty-desc">Thử thay đổi bộ lọc hoặc tạo người dùng mới</p>
          </div>
        </template>
        
        <el-table-column type="selection" width="44" />

        <el-table-column label="Người dùng" min-width="260">
          <template #default="{ row }">
            <div style="display: flex; align-items: center; gap: 12px;">
              <img 
                :src="getUserAvatar(row)" 
                alt="avatar"
                style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover; flex-shrink: 0;"
              />
              <div style="display: flex; flex-direction: column; min-width: 0;">
                <span style="font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ row.name }}</span>
                <span style="font-size: 12px; opacity: 0.7; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ row.email }}</span>
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="username" label="Username" min-width="140" show-overflow-tooltip />

        <el-table-column label="Vai trò" width="120">
          <template #default="{ row }">
            <span 
              class="role-badge"
              :class="{
                'role-admin': row.role === 'admin',
                'role-instructor': row.role === 'instructor',
                'role-student': row.role === 'student'
              }"
            >
              {{ roleLabel(row.role) }}
            </span>
          </template>
        </el-table-column>

        <el-table-column label="Trạng thái" width="130">
          <template #default="{ row }">
            <span 
              class="status-badge"
              :class="{
                'status-active': row.status === 'active',
                'status-locked': row.status === 'locked',
                'status-banned': row.status === 'banned'
              }"
            >
              {{ statusLabel(row.status) }}
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="createdAt" label="Ngày tạo" min-width="150" sortable="custom">
          <template #default="{ row }">
            <span style="font-size: 13px; opacity: 0.8;">{{ fmtDate(row.createdAt) }}</span>
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="Hành động" width="240">
          <template #default="{ row }">
            <div style="display: flex; gap: 6px; flex-wrap: nowrap; align-items: center;">
              <el-button size="small" @click="openEdit(row)">Sửa</el-button>
              <el-button size="small" @click="gotoDetail(row)">Chi tiết</el-button>
              <el-button size="small" type="danger" @click="deleteUser(row)">Xóa</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="table-footer">
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
import { ref, reactive, onMounted, watch, computed, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { userService } from '@/services/user.service'
import { showToast } from '@/utils/toast'
import { showConfirm } from '@/utils/confirm'
import { getAvatarSrc } from '@/utils/avatar'

// Debounce utility for performance (searchUS_26, searchUS_27)
function debounce<T extends (...args: any[]) => any>(fn: T, delay: number) {
  let timeoutId: ReturnType<typeof setTimeout> | null = null
  return (...args: Parameters<T>) => {
    if (timeoutId) clearTimeout(timeoutId)
    timeoutId = setTimeout(() => fn(...args), delay)
  }
}

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
    
    // Handle 403 Forbidden - no permission (searchUS_22)
    if (error?.response?.status === 403) {
      showToast('Bạn không có quyền truy cập trang này', 'error')
      router.push('/admin')
      return
    }
    
    // Handle 401 Unauthorized - session timeout (searchUS_24)
    if (error?.response?.status === 401) {
      showToast('Phiên đăng nhập đã hết hạn, vui lòng đăng nhập lại', 'warning')
      router.push('/login')
      return
    }
    
    showToast(error?.message || 'Không tải được danh sách người dùng', 'error')
  } finally {
    loading.value = false
  }
}

function applyFilters() {
  // Trim search query to handle leading/trailing spaces (searchUS_13)
  query.q = query.q.trim()
  query.page = 1
  pushQuery()
  fetchList()
}

// Debounced search for performance - prevents excessive API calls (searchUS_26, searchUS_27)
const debouncedSearch = debounce(() => {
  applyFilters()
}, 300)
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
    // Validate date range: from must be <= to (searchUS_12)
    const fromDate = new Date(val[0])
    const toDate = new Date(val[1])
    if (fromDate > toDate) {
      showToast('Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc', 'warning')
      return
    }
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
  password: '',
})
const rules = {
  name: [{ required: true, message: 'Nhập họ tên', trigger: 'blur' }],
  username: [{ required: true, message: 'Nhập username', trigger: 'blur' }],
  email: [
    { required: true, message: 'Nhập email', trigger: 'blur' },
    { type: 'email', message: 'Email không hợp lệ', trigger: 'blur' },
  ],
  password: [
    {
      validator: (_rule: any, value: string, callback: (error?: Error) => void) => {
        if (formDialog.mode !== 'create') return callback()
        if (!value) return callback(new Error('Nhập mật khẩu'))
        if (value.length < 6) return callback(new Error('Mật khẩu tối thiểu 6 ký tự'))
        return callback()
      },
      trigger: 'blur',
    },
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
    password: '',
  } as User)
  formDialog.open = true
}
function openEdit(row: User) {
  formDialog.mode = 'edit'
  Object.assign(form, { ...row, password: '' })
  formDialog.open = true
}
async function submitForm() {
  if (formDialog.mode === 'create') {
    const pwd = (form.password || '').trim()
    if (!pwd || pwd.length < 6) {
      showToast('Mật khẩu tối thiểu 6 ký tự', 'error')
      return
    }
  }
  const isValid = await formRef.value?.validate().catch(() => false)
  if (!isValid) {
    showToast('Vui lòng kiểm tra lại thông tin', 'warning')
    return
  }
  saving.value = true
  try {
    if (formDialog.mode === 'create') {
      // Gửi payload tạo tài khoản
      await userService.create({
        username: form.username,
        email: form.email,
        phone: form.phone || undefined,
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
    const data = error?.response?.data || {}
    const detail = data.detail || data.message || error?.message || ''
    const passwordErrors = Array.isArray(data.password) ? data.password.join(' ') : ''
    if (detail.includes('Username already taken')) {
      showToast('Username đã tồn tại', 'error')
    } else if (detail.includes('Email already taken')) {
      showToast('Email đã tồn tại', 'error')
    } else if (detail.includes('Phone already taken')) {
      showToast('Số điện thoại đã tồn tại', 'error')
    } else if (passwordErrors) {
      showToast(passwordErrors, 'error')
    } else if (detail.toLowerCase().includes('password') && detail.includes('6')) {
      showToast('Mật khẩu tối thiểu 6 ký tự', 'error')
    } else {
      showToast(detail || 'Không thể lưu dữ liệu', 'error')
    }
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
.users-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Page Header */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.page-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
}

.page-desc {
  font-size: 14px;
  margin: 4px 0 0;
  opacity: 0.7;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  font-weight: bold;
  margin-right: 4px;
}

/* Filter Card */
.filter-card {
  padding: 16px;
  border-radius: 12px;
  border: 1px solid var(--border-color, rgba(255,255,255,0.08));
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  align-items: end;
}

.filter-search {
  grid-column: span 2;
}

.filter-date {
  width: 100% !important;
}

.filter-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

/* Bulk Bar */
.bulk-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
}

.selection-count {
  font-size: 14px;
  opacity: 0.7;
}

.text-danger {
  color: #ef4444 !important;
}

/* Table Card */
.table-card {
  padding: 16px;
  border-radius: 12px;
  border: 1px solid var(--border-color, rgba(255,255,255,0.08));
}

.table-footer {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.empty-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 12px;
  opacity: 0.4;
}

.empty-title {
  font-size: 14px;
  font-weight: 500;
  margin: 0;
}

.empty-desc {
  font-size: 12px;
  opacity: 0.6;
  margin-top: 4px;
}

/* User Cell */
.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.user-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.user-name {
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email {
  font-size: 12px;
  opacity: 0.7;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.date-text {
  font-size: 13px;
}

.action-btns {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* Responsive */
@media (max-width: 768px) {
  .filter-search {
    grid-column: span 1;
  }
  
  .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .header-actions {
    width: 100%;
  }
}

/* Role Badges */
.role-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.role-admin {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}

.role-instructor {
  background: rgba(251, 191, 36, 0.15);
  color: #f59e0b;
}

.role-student {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
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

.status-active {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.status-locked {
  background: rgba(251, 191, 36, 0.15);
  color: #f59e0b;
}

.status-banned {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
}
</style>
