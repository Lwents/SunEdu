<template>
  <div class="bulk-create-page">
    <div class="container">
      <section class="form-card">
        <div class="card-header">
          <h2 class="card-title">📋 Tạo tài khoản hàng loạt</h2>
          <p class="card-desc">
            Tạo nhiều tài khoản học sinh theo mã khóa (ví dụ: K72, A23)
          </p>
        </div>

        <form class="form-body" @submit.prevent="onGenerate">
          <div class="form-group">
            <label class="form-label">
              Mã khóa <span class="required">*</span>
            </label>
            <input
              v-model.trim="form.cohortCode"
              type="text"
              placeholder="Ví dụ: K72, A23"
              class="form-input"
              required
            />
            <p class="form-hint">
              Mã khóa sẽ được chuyển thành số đầu tiên. K=72, A=01, B=02, ...
            </p>
          </div>

          <div class="form-group">
            <label class="form-label">
              Số lượng tài khoản <span class="required">*</span>
            </label>
            <input
              v-model.number="form.count"
              type="number"
              min="1"
              max="100"
              placeholder="1-100"
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">Mật khẩu</label>
            <div class="info-box">
              Mỗi tài khoản sẽ được gán <b>ngẫu nhiên 8 ký tự</b> gồm chữ và số. Admin có thể tải file CSV sau khi tạo để gửi cho học sinh.
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Vai trò</label>
            <select v-model="form.role" class="form-input">
              <option value="student">Học sinh</option>
              <option value="teacher">Giáo viên</option>
            </select>
          </div>

          <div class="form-actions">
            <button
              type="submit"
              class="btn-primary"
              :disabled="loading || !isValid"
            >
              {{ loading ? 'Đang tạo...' : 'Tạo tài khoản' }}
            </button>
          </div>

          <div v-if="success" class="success-box">
            <p class="success-title">
              ✓ Đã tạo {{ result.created }} tài khoản thành công!
            </p>
            <div class="success-actions">
              <p class="success-hint">Danh sách kèm mật khẩu. Hãy lưu lại ngay hoặc xuất CSV.</p>
              <button type="button" class="btn-outline-green" @click="exportCsv">
                Xuất CSV
              </button>
              <button type="button" class="btn-outline-blue" @click="handleConfirm">
                Xác nhận
              </button>
              <button
                type="button"
                class="btn-outline-red"
                @click="rollbackAccounts"
                :disabled="rollbacking"
              >
                {{ rollbacking ? 'Đang hủy…' : 'Hủy tạo' }}
              </button>
            </div>
            <div v-if="result.accounts.length" class="accounts-list">
              <p class="list-title">Danh sách tài khoản:</p>
              <div class="table-wrapper">
                <table class="accounts-table">
                  <thead>
                    <tr>
                      <th>Username</th>
                      <th>Email</th>
                      <th>Mật khẩu</th>
                      <th>Vai trò</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="acc in result.accounts" :key="acc.username">
                      <td class="font-mono">{{ acc.username }}</td>
                      <td>{{ acc.email }}</td>
                      <td class="font-mono">{{ acc.password }}</td>
                      <td>{{ acc.role }}</td>
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

<style scoped>
.bulk-create-page {
  padding: 24px;
  min-height: 100%;
}

.container {
  max-width: 700px;
  margin: 0 auto;
}

.form-card {
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(30, 41, 59, 0.6);
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.card-header {
  padding: 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: #fff;
}

.card-desc {
  font-size: 14px;
  color: #94a3b8;
  margin: 8px 0 0;
}

.form-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  font-weight: 500;
  color: #e2e8f0;
}

.required {
  color: #ef4444;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.05);
  color: #e2e8f0;
  font-size: 14px;
  transition: all 0.2s;
}

.form-input::placeholder {
  color: #64748b;
}

.form-input:focus {
  outline: none;
  border-color: #22d3ee;
  box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.15);
}

.form-hint {
  font-size: 12px;
  color: #64748b;
  margin: 0;
}

.info-box {
  padding: 16px;
  border-radius: 10px;
  border: 1px dashed rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.03);
  color: #94a3b8;
  font-size: 14px;
}

.info-box b {
  color: #22d3ee;
}

.form-actions {
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.btn-primary {
  padding: 12px 24px;
  border-radius: 10px;
  background: linear-gradient(135deg, #06b6d4, #8b5cf6);
  color: #fff;
  font-weight: 600;
  font-size: 14px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Success Box */
.success-box {
  padding: 20px;
  border-radius: 12px;
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.success-title {
  font-size: 15px;
  font-weight: 600;
  color: #22c55e;
  margin: 0 0 12px;
}

.success-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.success-hint {
  flex: 1;
  min-width: 200px;
  font-size: 12px;
  color: #86efac;
  margin: 0;
}

.btn-outline-green,
.btn-outline-blue,
.btn-outline-red {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  background: transparent;
}

.btn-outline-green {
  border: 1px solid #22c55e;
  color: #22c55e;
}

.btn-outline-green:hover {
  background: rgba(34, 197, 94, 0.15);
}

.btn-outline-blue {
  border: 1px solid #3b82f6;
  color: #3b82f6;
}

.btn-outline-blue:hover {
  background: rgba(59, 130, 246, 0.15);
}

.btn-outline-red {
  border: 1px solid #ef4444;
  color: #ef4444;
}

.btn-outline-red:hover {
  background: rgba(239, 68, 68, 0.15);
}

.btn-outline-red:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Accounts List */
.accounts-list {
  margin-top: 16px;
}

.list-title {
  font-size: 12px;
  font-weight: 600;
  color: #86efac;
  margin: 0 0 8px;
}

.table-wrapper {
  max-height: 240px;
  overflow-y: auto;
  border-radius: 8px;
  border: 1px solid rgba(34, 197, 94, 0.2);
  background: rgba(0, 0, 0, 0.2);
}

.accounts-table {
  width: 100%;
  font-size: 12px;
  border-collapse: collapse;
}

.accounts-table th,
.accounts-table td {
  padding: 8px 12px;
  text-align: left;
}

.accounts-table th {
  color: #86efac;
  border-bottom: 1px solid rgba(34, 197, 94, 0.2);
  font-weight: 600;
}

.accounts-table td {
  color: #e2e8f0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.accounts-table tr:last-child td {
  border-bottom: none;
}

.font-mono {
  font-family: monospace;
}

/* Native Select Dark Mode */
select.form-input {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2394a3b8'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
  padding-right: 40px;
}

select.form-input option {
  background: #1e293b;
  color: #e2e8f0;
  padding: 8px 12px;
}

/* Number Input Spinner Dark Mode */
input[type="number"].form-input {
  -moz-appearance: textfield;
}

input[type="number"].form-input::-webkit-outer-spin-button,
input[type="number"].form-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Show custom spinner buttons */
.form-group:has(input[type="number"]) {
  position: relative;
}

/* ============================================== */
/* Light Mode Overrides                          */
/* ============================================== */
html:not(.dark) .form-card {
  background: #fff;
  border-color: #e2e8f0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

html:not(.dark) .card-header {
  border-color: #e2e8f0;
}

html:not(.dark) .card-title {
  color: #1e293b;
}

html:not(.dark) .card-desc {
  color: #64748b;
}

html:not(.dark) .form-label {
  color: #334155;
}

html:not(.dark) .form-input {
  background: #f8fafc;
  border-color: #e2e8f0;
  color: #1e293b;
}

html:not(.dark) .form-input::placeholder {
  color: #94a3b8;
}

html:not(.dark) .form-input:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

html:not(.dark) .form-hint {
  color: #64748b;
}

html:not(.dark) .info-box {
  background: #f1f5f9;
  border-color: #cbd5e1;
  color: #475569;
}

html:not(.dark) .info-box b {
  color: #0ea5e9;
}

html:not(.dark) .form-actions {
  border-color: #e2e8f0;
}

html:not(.dark) .btn-primary {
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
}

html:not(.dark) select.form-input option {
  background: #fff;
  color: #1e293b;
}

/* Success box in light mode */
html:not(.dark) .success-box {
  background: rgba(34, 197, 94, 0.08);
  border-color: rgba(34, 197, 94, 0.3);
}

html:not(.dark) .success-title {
  color: #16a34a;
}

html:not(.dark) .success-hint {
  color: #15803d;
}

html:not(.dark) .list-title {
  color: #15803d;
}

html:not(.dark) .table-wrapper {
  background: #f8fafc;
  border-color: rgba(34, 197, 94, 0.2);
}

html:not(.dark) .accounts-table th {
  color: #15803d;
  border-color: rgba(34, 197, 94, 0.2);
}

html:not(.dark) .accounts-table td {
  color: #334155;
  border-color: #e2e8f0;
}
</style>
