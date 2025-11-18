<template>
  <div class="min-h-screen bg-slate-50 p-4 sm:p-6">
    <div class="mx-auto max-w-4xl">
      <section class="rounded-xl border border-slate-200 bg-white shadow-sm">
        <div class="border-b border-slate-200 p-6">
          <h2 class="text-xl font-bold text-slate-800">Tạo tài khoản hàng loạt</h2>
          <p class="mt-1 text-sm text-slate-500">
            Tạo nhiều tài khoản học sinh theo mã khóa (ví dụ: K72, A23)
          </p>
        </div>

        <form class="space-y-6 p-6" @submit.prevent="onGenerate">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">
                Mã khóa <span class="text-red-500">*</span>
              </label>
              <input
                v-model.trim="form.cohortCode"
                type="text"
                placeholder="Ví dụ: K72, A23"
                class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
                required
              />
              <p class="mt-1 text-xs text-slate-500">
                Mã khóa sẽ được chuyển thành số đầu tiên. K=72, A=01, B=02, ...
              </p>
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">
                Số lượng tài khoản <span class="text-red-500">*</span>
              </label>
              <input
                v-model.number="form.count"
                type="number"
                min="1"
                max="100"
                placeholder="1-100"
                class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">
                Mật khẩu
              </label>
              <div class="rounded-lg border border-dashed border-slate-300 bg-slate-50 p-3 text-sm text-slate-600">
                Mỗi tài khoản sẽ được gán <b>ngẫu nhiên 8 ký tự</b> gồm chữ và số. Admin có thể tải file CSV sau khi tạo để gửi cho học sinh.
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">
                Vai trò
              </label>
              <select
                v-model="form.role"
                class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
              >
                <option value="student">Học sinh</option>
                <option value="teacher">Giáo viên</option>
              </select>
            </div>
          </div>

          <div class="flex flex-wrap items-center gap-3 pt-4 border-t border-slate-200">
            <button
              type="submit"
              class="rounded-lg bg-blue-600 px-6 py-2.5 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="loading || !isValid"
            >
              {{ loading ? 'Đang tạo...' : 'Tạo tài khoản' }}
            </button>
          </div>

          <div v-if="success" class="rounded-lg bg-green-50 border border-green-200 p-4 space-y-3">
            <p class="text-sm font-medium text-green-800">
              ✓ Đã tạo {{ result.created }} tài khoản thành công!
            </p>
          <div class="flex items-center gap-3 flex-wrap">
            <p class="text-xs text-green-700 flex-1 min-w-[200px]">Danh sách kèm mật khẩu. Hãy lưu lại ngay hoặc xuất CSV.</p>
                <button
                  type="button"
                  class="rounded border border-green-500 px-3 py-1 text-xs font-semibold text-green-700 hover:bg-green-100"
                  @click="exportCsv"
                >
                  Xuất CSV
                </button>
                <button
                  type="button"
                  class="rounded border border-blue-500 px-3 py-1 text-xs font-semibold text-blue-700 hover:bg-blue-50"
                  @click="handleConfirm"
                >
                  Xác nhận
                </button>
                <button
                  type="button"
                  class="rounded border border-rose-500 px-3 py-1 text-xs font-semibold text-rose-600 hover:bg-rose-50"
                  @click="rollbackAccounts"
                  :disabled="rollbacking"
                >
                  {{ rollbacking ? 'Đang hủy…' : 'Hủy tạo' }}
                </button>
              </div>
            <div v-if="result.accounts.length" class="mt-3 space-y-3">
              <p class="text-xs font-medium text-green-700 mb-2">Danh sách tài khoản:</p>
              <div class="max-h-60 overflow-y-auto bg-white rounded border border-green-200 p-3">
                <table class="w-full text-xs">
                  <thead>
                    <tr class="border-b border-green-100">
                      <th class="text-left py-1 px-2">Username</th>
                      <th class="text-left py-1 px-2">Email</th>
                      <th class="text-left py-1 px-2">Mật khẩu</th>
                      <th class="text-left py-1 px-2">Vai trò</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="acc in result.accounts" :key="acc.username" class="border-b border-green-50">
                      <td class="py-1 px-2 font-mono">{{ acc.username }}</td>
                      <td class="py-1 px-2">{{ acc.email }}</td>
                      <td class="py-1 px-2 font-mono">{{ acc.password }}</td>
                      <td class="py-1 px-2">{{ acc.role }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted } from 'vue'
import api from '@/config/axios'
import { showToast } from '@/utils/toast'
import { showConfirm } from '@/utils/confirm'

const form = reactive({
  cohortCode: '',
  count: 10,
  role: 'student' as 'student' | 'teacher'
})

const STORAGE_KEY = 'admin_bulk_last_batch'

const loading = ref(false)
const rollbacking = ref(false)
const success = ref(false)
const result = reactive({
  created: 0,
  accounts: [] as Array<{ username: string; email: string; role: string; password: string }>
})

const isValid = computed(() => {
  return form.cohortCode.length > 0 && form.count > 0 && form.count <= 100
})

async function onGenerate() {
  if (!isValid.value || loading.value) return

  loading.value = true
  success.value = false
  result.created = 0
  result.accounts = []

  try {
    const { data } = await api.post('/admin/users/bulk-create/', {
      cohort_code: form.cohortCode,
      count: form.count,
      role: form.role
    })

    result.created = data.created || 0
    result.accounts = data.accounts || []
    success.value = true
    localStorage.setItem(STORAGE_KEY, JSON.stringify(result.accounts))
    showToast(`Đã tạo ${result.created} tài khoản thành công`, 'success')
  } catch (e: any) {
    console.error('Bulk create error:', e)
    showToast(e?.response?.data?.detail || e?.message || 'Không thể tạo tài khoản', 'error')
  } finally {
    loading.value = false
  }
}

async function rollbackNewAccounts() {
  if (!result.accounts.length) return true
  rollbacking.value = true
  try {
    const usernames = result.accounts.map((acc) => acc.username)
    const { data } = await api.post('/admin/users/bulk-create/rollback/', { usernames })
    showToast(`Đã hủy ${data.deleted || usernames.length} tài khoản vừa tạo`, 'info')
    result.created = 0
    result.accounts = []
    success.value = false
    localStorage.removeItem(STORAGE_KEY)
    return true
  } catch (e: any) {
    console.error('Rollback bulk create error:', e)
    showToast(e?.response?.data?.detail || e?.message || 'Không thể hủy các tài khoản vừa tạo', 'error')
    return false
  } finally {
    rollbacking.value = false
  }
}

async function rollbackAccounts() {
  await rollbackNewAccounts()
}

async function handleConfirm() {
  const confirmed = await showConfirm({
    title: 'Xác nhận',
    message: 'Bạn đã lưu thông tin tài khoản và mật khẩu chưa? Sau khi xác nhận, thông báo này sẽ không hiển thị lại khi tải lại trang.',
    type: 'info',
    confirmText: 'Đã lưu',
    cancelText: 'Hủy'
  })
  
  if (confirmed) {
    // Xóa localStorage để không hiển thị lại khi reload
    localStorage.removeItem(STORAGE_KEY)
    // Đóng thông báo thành công
    success.value = false
    result.created = 0
    result.accounts = []
    showToast('Đã xác nhận. Thông báo sẽ không hiển thị lại khi tải lại trang.', 'success')
  }
}

function exportCsv() {
  if (!result.accounts.length) return

  const headers = ['Username', 'Email', 'Password', 'Role']
  const rows = result.accounts.map((acc) => [acc.username, acc.email, acc.password, acc.role])

  const escape = (value: string) => `"${value.replace(/"/g, '""')}"`
  const csv = [headers, ...rows]
    .map((row) => row.map((cell) => escape(String(cell))).join(','))
    .join('\n')

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `accounts-${new Date().toISOString().slice(0, 10)}.csv`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

onMounted(() => {
  const cached = localStorage.getItem(STORAGE_KEY)
  if (cached) {
    try {
      const accounts = JSON.parse(cached)
      if (Array.isArray(accounts) && accounts.length) {
        result.accounts = accounts
        result.created = accounts.length
        success.value = true
      }
    } catch (err) {
      console.warn('Invalid cached bulk data', err)
      localStorage.removeItem(STORAGE_KEY)
    }
  }
})
</script>
