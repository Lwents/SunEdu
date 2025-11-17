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
                Mật khẩu mặc định <span class="text-red-500">*</span>
              </label>
              <input
                v-model.trim="form.defaultPassword"
                type="text"
                placeholder="Mật khẩu chung cho tất cả tài khoản"
                class="w-full rounded-lg border border-slate-300 px-4 py-2 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200"
                required
              />
              <p class="mt-1 text-xs text-slate-500">
                Học sinh có thể đổi mật khẩu sau khi đăng nhập
              </p>
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

          <div class="flex items-center gap-3 pt-4 border-t border-slate-200">
            <button
              type="submit"
              class="rounded-lg bg-blue-600 px-6 py-2.5 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="loading || !isValid"
            >
              {{ loading ? 'Đang tạo...' : 'Tạo tài khoản' }}
            </button>

            <button
              type="button"
              class="rounded-lg border border-slate-300 px-6 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50"
              @click="resetForm"
              :disabled="loading"
            >
              Đặt lại
            </button>
          </div>

          <div v-if="error" class="rounded-lg bg-red-50 border border-red-200 p-4">
            <p class="text-sm text-red-800">{{ error }}</p>
          </div>

          <div v-if="success" class="rounded-lg bg-green-50 border border-green-200 p-4">
            <p class="text-sm font-medium text-green-800">
              ✓ Đã tạo {{ result.created }} tài khoản thành công!
            </p>
            <div v-if="result.accounts.length" class="mt-3">
              <p class="text-xs font-medium text-green-700 mb-2">Danh sách tài khoản:</p>
              <div class="max-h-60 overflow-y-auto bg-white rounded border border-green-200 p-3">
                <table class="w-full text-xs">
                  <thead>
                    <tr class="border-b border-green-100">
                      <th class="text-left py-1 px-2">Username</th>
                      <th class="text-left py-1 px-2">Email</th>
                      <th class="text-left py-1 px-2">Vai trò</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="acc in result.accounts" :key="acc.username" class="border-b border-green-50">
                      <td class="py-1 px-2 font-mono">{{ acc.username }}</td>
                      <td class="py-1 px-2">{{ acc.email }}</td>
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
import { ref, computed, reactive } from 'vue'
import api from '@/config/axios'

const form = reactive({
  cohortCode: '',
  count: 10,
  defaultPassword: 'Student@123',
  role: 'student' as 'student' | 'teacher'
})

const loading = ref(false)
const error = ref('')
const success = ref(false)
const result = reactive({
  created: 0,
  accounts: [] as Array<{ username: string; email: string; role: string }>
})

const isValid = computed(() => {
  return form.cohortCode.length > 0 && form.count > 0 && form.count <= 100 && form.defaultPassword.length >= 6
})

function resetForm() {
  form.cohortCode = ''
  form.count = 10
  form.defaultPassword = 'Student@123'
  form.role = 'student'
  error.value = ''
  success.value = false
  result.created = 0
  result.accounts = []
}

async function onGenerate() {
  if (!isValid.value || loading.value) return

  loading.value = true
  error.value = ''
  success.value = false
  result.created = 0
  result.accounts = []

  try {
    const { data } = await api.post('/admin/users/bulk-create/', {
      cohort_code: form.cohortCode,
      count: form.count,
      default_password: form.defaultPassword,
      role: form.role
    })

    result.created = data.created || 0
    result.accounts = data.accounts || []
    success.value = true
  } catch (e: any) {
    console.error('Bulk create error:', e)
    error.value = e?.response?.data?.detail || e?.message || 'Không thể tạo tài khoản'
  } finally {
    loading.value = false
  }
}
</script>
