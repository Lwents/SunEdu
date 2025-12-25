<template>
  <div class="page-wrapper" :class="isDark ? 'dark-mode' : 'light-mode'">
    <div v-if="isDark" class="bg-elements">
      <div class="glow glow-1"></div>
      <div class="glow glow-2"></div>
    </div>

    <div class="page-content">
      <!-- Tabs -->
      <div class="tabs-nav">
        <button type="button" class="tab-btn active">Cá nhân</button>
        <button type="button" class="tab-btn" @click="goChangePwd">Đổi mật khẩu</button>
        <button type="button" class="tab-btn" @click="goParent">Phụ huynh</button>
      </div>

      <!-- Main Card -->
      <div class="profile-card">
        <div class="card-header">
          <h2>Thông tin cá nhân</h2>
          <p>Cập nhật lần cuối: <span>{{ lastUpdated }}</span></p>
        </div>

        <form v-if="ready" class="profile-form" @submit.prevent="saveProfile">
          <!-- Avatar -->
          <div class="form-row">
            <label>Ảnh đại diện</label>
            <div class="avatar-section">
              <button type="button" class="avatar-btn" @click="openFile">
                <img :src="avatarPreview || currentAvatar" alt="Ảnh đại diện" />
                <div class="avatar-overlay">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              </button>
              <p class="hint">Nhấn để đổi ảnh (tối đa 5MB)</p>
              <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onPickFile" />
            </div>
          </div>

          <!-- Username -->
          <div class="form-row">
            <label>Tên đăng nhập</label>
            <div class="input-group">
              <input v-model.trim="form.username" type="text" readonly class="input-readonly" />
              <p class="hint">Không thể thay đổi</p>
            </div>
          </div>

          <!-- Full Name -->
          <div class="form-row">
            <label>Họ và tên <span class="required">*</span></label>
            <div class="input-group">
              <input v-model="fullnameModel" type="text" placeholder="Nhập họ và tên" :maxlength="MAX_FULLNAME_LENGTH" :class="{ error: errors.fullname }" />
              <p v-if="errors.fullname" class="error-text">{{ errors.fullname }}</p>
            </div>
          </div>

          <!-- Date of Birth -->
          <div class="form-row">
            <label>Ngày sinh</label>
            <div class="input-group">
              <div class="dob-selects">
                <select v-model.number="dob.day"><option v-for="d in days" :key="d" :value="d">Ngày {{ d }}</option></select>
                <select v-model.number="dob.month"><option v-for="m in months" :key="m" :value="m">Tháng {{ m }}</option></select>
                <select v-model.number="dob.year"><option v-for="y in years" :key="y" :value="y">Năm {{ y }}</option></select>
              </div>
              <p class="hint">Có thể để trống</p>
            </div>
          </div>

          <!-- Gender -->
          <div class="form-row">
            <label>Giới tính</label>
            <div class="gender-options">
              <label class="gender-option" :class="{ active: form.gender === 'male' }">
                <input type="radio" value="male" v-model="form.gender" /> Nam
              </label>
              <label class="gender-option" :class="{ active: form.gender === 'female' }">
                <input type="radio" value="female" v-model="form.gender" /> Nữ
              </label>
            </div>
          </div>

          <!-- Class -->
          <div class="form-row">
            <label>Lớp học</label>
            <div class="input-group">
              <select v-model="form.className">
                <option value="">Chọn lớp</option>
                <option v-for="c in [1,2,3,4,5]" :key="c" :value="String(c)">Lớp {{ c }}</option>
              </select>
              <p class="hint">Chọn lớp hiện tại của bạn.</p>
            </div>
          </div>

          <!-- Email -->
          <div class="form-row">
            <label>Email</label>
            <div class="input-group">
              <input v-model.trim="form.email" type="email" placeholder="you@example.com" :class="{ error: errors.email }" />
              <p v-if="errors.email" class="error-text">{{ errors.email }}</p>
            </div>
          </div>

          <!-- Email Notifications -->
          <div class="form-row">
            <label>Thông báo email</label>
            <div class="checkbox-group">
              <input id="email-updates" v-model="form.emailUpdates" type="checkbox" />
              <label for="email-updates">Nhận thông báo qua email</label>
            </div>
          </div>

          <!-- Address -->
          <div class="form-row">
            <label>Địa chỉ</label>
            <div class="input-group">
              <textarea v-model.trim="form.address" rows="3" placeholder="Nhập địa chỉ"></textarea>
            </div>
          </div>

          <!-- Province -->
          <div class="form-row">
            <label>Tỉnh/Thành phố</label>
            <div class="input-group">
              <select v-model.number="selectedProvinceCode" :disabled="provincesLoading">
                <option value="">{{ provincesLoading ? 'Đang tải...' : 'Chọn tỉnh/thành phố' }}</option>
                <option v-for="province in provinces" :key="province.code" :value="province.code">{{ province.name }}</option>
              </select>
            </div>
          </div>

          <!-- District -->
          <div class="form-row">
            <label>Quận/Huyện</label>
            <div class="input-group">
              <select v-model.number="selectedDistrictCode" :disabled="!selectedProvinceCode || districtsLoading">
                <option value="">{{ !selectedProvinceCode ? 'Chọn tỉnh/thành phố trước' : districtsLoading ? 'Đang tải...' : 'Chọn quận/huyện' }}</option>
                <option v-for="district in districts" :key="district.code" :value="district.code">{{ district.name }}</option>
              </select>
            </div>
          </div>

          <!-- Ward -->
          <div class="form-row">
            <label>Phường/Xã</label>
            <div class="input-group">
              <select v-model.number="selectedWardCode" :disabled="!selectedDistrictCode || wardsLoading">
                <option value="">{{ !selectedDistrictCode ? 'Chọn quận/huyện trước' : wardsLoading ? 'Đang tải...' : 'Chọn phường/xã' }}</option>
                <option v-for="ward in wards" :key="ward.code" :value="ward.code">{{ ward.name }}</option>
              </select>
            </div>
          </div>

          <!-- Submit Button -->
          <div class="form-actions">
            <p v-if="!isValidInfo" class="action-hint">Vui lòng điền đầy đủ thông tin bắt buộc</p>
            <button type="submit" class="submit-btn" :disabled="saving || !isValidInfo || !isDirty">
              <span v-if="saving" class="spinner"></span>
              {{ saving ? 'Đang cập nhật...' : 'Cập nhật' }}
            </button>
          </div>
        </form>

        <div v-else class="loading-text">Đang tải thông tin…</div>
      </div>
    </div>
  </div>

  <!-- Error Modal -->
  <Transition enter-active-class="transition-opacity duration-200" leave-active-class="transition-opacity duration-200" enter-from-class="opacity-0" leave-to-class="opacity-0">
    <div v-if="limitModal.open" class="modal-overlay" @click.self="closeLimitModal">
      <div class="modal-card" ref="limitCard" tabindex="-1">
        <div class="modal-icon error">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3m0 4h.01M10.29 3.86 1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
          </svg>
        </div>
        <h3>Không thể tải ảnh</h3>
        <p>{{ limitModal.message }}</p>
        <p class="modal-hint">Vui lòng chọn tệp PNG/JPG ≤ 5MB.</p>
        <button type="button" class="modal-btn" @click="closeLimitModal">Đã hiểu</button>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.store'
import { useThemeStore } from '@/store/theme.store'
import { authService, type ProfileUpdatePayload, type ProfileDetails } from '@/services/auth.service'
import { locationService, type DistrictOption, type ProvinceOption, type WardOption } from '@/services/location.service'
import { showToast } from '@/utils/toast'
import { getAvatarSrc } from '@/utils/avatar'

const router = useRouter()
const auth = useAuthStore()
const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)
const ready = ref(false)

const MAX_AVATAR_SIZE = 5 * 1024 * 1024
const MAX_FULLNAME_LENGTH = 25
const OVER_LIMIT_MSG = 'File ảnh vượt quá dung lượng cho phép (5MB)'

const clampFullname = (value: string) => value.trim().slice(0, MAX_FULLNAME_LENGTH)

function goChangePwd() { router.push({ name: 'student-change-password' }) }
function goParent() { router.push({ name: 'student-parent' }) }

const profileDetails = ref<ProfileDetails | null>(null)
const currentAvatar = computed(() => {
  const userAvatar = auth.user?.avatar || profileDetails.value?.avatar || profileDetails.value?.avatar_url
  const gender = auth.user?.gender || profileDetails.value?.gender
  return getAvatarSrc(userAvatar, gender as 'male' | 'female' | 'other' | null | undefined, 'student')
})

const fileInput = ref<HTMLInputElement | null>(null)
const avatarFile = ref<File | null>(null)
const avatarPreview = ref<string>('')

function openFile() { fileInput.value?.click() }

const limitModal = reactive<{ open: boolean; message: string }>({ open: false, message: '' })
const limitCard = ref<HTMLElement | null>(null)

function showLimitModal(msg = OVER_LIMIT_MSG) { limitModal.message = msg; limitModal.open = true; queueMicrotask(() => limitCard.value?.focus()) }
function closeLimitModal() { limitModal.open = false }

function handleEsc(e: KeyboardEvent) { if (e.key === 'Escape' && limitModal.open) { e.stopPropagation(); closeLimitModal() } }
window.addEventListener('keydown', handleEsc)
onBeforeUnmount(() => window.removeEventListener('keydown', handleEsc))

function onPickFile(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  if (file.size > MAX_AVATAR_SIZE) { showLimitModal(); input.value = ''; avatarFile.value = null; avatarPreview.value = ''; return }
  avatarFile.value = file
  const reader = new FileReader()
  reader.onload = () => (avatarPreview.value = String(reader.result || ''))
  reader.readAsDataURL(file)
}

const form = reactive({ username: '', fullname: '', email: '', emailUpdates: true, gender: 'male', className: '', address: '', city: '', district: '', ward: '' })
const fullnameModel = computed({
  get: () => form.fullname,
  set: (value) => {
    const rawValue = String(value ?? '')
    const trimmedValue = rawValue.trim()
    if (trimmedValue.length >= MAX_FULLNAME_LENGTH && form.fullname.length < MAX_FULLNAME_LENGTH) {
      showToast(`Tối đa ${MAX_FULLNAME_LENGTH} ký tự.`, 'warning')
    }
    form.fullname = clampFullname(trimmedValue)
  },
})

const provinces = ref<ProvinceOption[]>([])
const districts = ref<DistrictOption[]>([])
const wards = ref<WardOption[]>([])
const provincesLoading = ref(false)
const districtsLoading = ref(false)
const wardsLoading = ref(false)

const selectedProvinceCode = ref<number | null>(null)
const selectedDistrictCode = ref<number | null>(null)
const selectedWardCode = ref<number | null>(null)
const pendingDistrictName = ref<string | null>(null)
const pendingWardName = ref<string | null>(null)

const dob = reactive({ day: 1, month: 1, year: 2000 })
const days = Array.from({ length: 31 }, (_, i) => i + 1)
const months = Array.from({ length: 12 }, (_, i) => i + 1)
const years = Array.from({ length: 60 }, (_, i) => 1980 + i)

const initialJSON = ref<string>('')
function snapshot() { initialJSON.value = JSON.stringify({ ...form, dob: { ...dob }, avatarPreview: avatarPreview.value }) }

function formatDateTime(value?: string | Date) {
  if (!value) return 'chưa có'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return 'chưa có'
  return new Intl.DateTimeFormat('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' }).format(date)
}

const normalizeName = (value?: string | null) => (value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim()
function findByName<T extends { name: string }>(list: T[], name?: string | null) { if (!name) return undefined; const target = normalizeName(name); return list.find((item) => normalizeName(item.name) === target) }

async function loadProvinces() { provincesLoading.value = true; try { provinces.value = await locationService.listProvinces() } catch { provinces.value = [] } finally { provincesLoading.value = false } }

async function handleProvinceChanged(code: number | null) {
  form.city = ''; form.district = ''; form.ward = ''; districts.value = []; wards.value = []; selectedDistrictCode.value = null; selectedWardCode.value = null
  if (typeof code !== 'number' || Number.isNaN(code)) return
  const province = provinces.value.find((p) => p.code === code); form.city = province?.name || ''
  districtsLoading.value = true; try { districts.value = await locationService.listDistricts(code) } catch { districts.value = [] } finally { districtsLoading.value = false }
  if (pendingDistrictName.value) { const matchDistrict = findByName(districts.value, pendingDistrictName.value); pendingDistrictName.value = null; if (matchDistrict) { selectedDistrictCode.value = matchDistrict.code; return } }
}

async function handleDistrictChanged(code: number | null) {
  form.district = ''; form.ward = ''; wards.value = []; selectedWardCode.value = null
  if (typeof code !== 'number' || Number.isNaN(code)) return
  const district = districts.value.find((d) => d.code === code); form.district = district?.name || ''
  wardsLoading.value = true; try { wards.value = await locationService.listWards(code) } catch { wards.value = [] } finally { wardsLoading.value = false }
  if (pendingWardName.value) { const matchWard = findByName(wards.value, pendingWardName.value); pendingWardName.value = null; if (matchWard) selectedWardCode.value = matchWard.code }
}

function applyProfileToForm(profile?: ProfileDetails | null) {
  if (!profile) return
  form.username = profile.username || profile.name || ''; form.fullname = clampFullname(profile.fullName || profile.name || ''); form.email = profile.email || ''
  form.gender = (profile.gender as any) || form.gender; form.className = profile.class_name || profile.className || ''; form.emailUpdates = profile.email_updates ?? true
  form.address = profile.address || ''; form.city = profile.city || ''; form.district = profile.district || ''; form.ward = profile.ward || ''
  if (profile.dob) { const [year, month, day] = profile.dob.split('-').map(Number); if (year && month && day) { dob.year = year; dob.month = month; dob.day = day } }
  avatarPreview.value = profile.avatar || profile.avatar_url || ''
  if (profile.updatedAt || profile.createdAt) lastUpdated.value = formatDateTime(profile.updatedAt || (profile.createdAt as string))
  snapshot()
}

async function hydrateLocationSelections(profile?: ProfileDetails | null) {
  if (!profile) { selectedProvinceCode.value = null; return }
  pendingDistrictName.value = profile.district || null; pendingWardName.value = profile.ward || null
  const provinceMatch = findByName(provinces.value, profile.city || '')
  if (provinceMatch) selectedProvinceCode.value = provinceMatch.code; else selectedProvinceCode.value = null
}

onMounted(async () => {
  auth.init?.(); await loadProvinces()
  try { await auth.fetchCurrentUser(); const profile = await authService.getProfile(); profileDetails.value = profile; applyProfileToForm(profile); await hydrateLocationSelections(profile)
    const avatarUrl = profile.avatar || profile.avatar_url; if (avatarUrl) auth.setAvatar(avatarUrl)
  } catch { } finally { ready.value = true }
})

const errors = reactive<{ fullname?: string; email?: string }>({})
const isEmail = (v: string) => /^\S+@\S+\.\S+$/.test(v)

watch(
  () => ({ ...form }),
  () => {
    if (!ready.value) return
    const trimmedFullname = form.fullname.trim()
    if (!trimmedFullname) {
      errors.fullname = 'Vui lòng nhập họ và tên.'
    } else if (trimmedFullname.length > MAX_FULLNAME_LENGTH) {
      errors.fullname = `Họ và tên tối đa ${MAX_FULLNAME_LENGTH} ký tự.`
    } else {
      errors.fullname = ''
    }
    errors.email = form.email && !isEmail(form.email) ? 'Email không hợp lệ.' : ''
  },
  { deep: true }
)
watch(selectedProvinceCode, (code) => { const normalized = typeof code === 'number' && !Number.isNaN(code) ? code : null; handleProvinceChanged(normalized) })
watch(selectedDistrictCode, (code) => { const normalized = typeof code === 'number' && !Number.isNaN(code) ? code : null; handleDistrictChanged(normalized) })
watch(selectedWardCode, (code) => { const normalized = typeof code === 'number' && !Number.isNaN(code) ? code : null; if (!normalized) { form.ward = ''; return }; const ward = wards.value.find((w) => w.code === normalized); form.ward = ward?.name || '' })

const isValidInfo = computed(() => !errors.fullname && !errors.email)
const isDirty = computed(() => { const now = JSON.stringify({ ...form, dob: { ...dob }, avatarPreview: avatarPreview.value }); return now !== initialJSON.value })

const saving = ref(false)
const lastUpdated = ref('chưa có')

async function saveProfile() {
  if (!isValidInfo.value) { showToast('Vui lòng kiểm tra lại các trường bắt buộc.', 'error'); return }
  if (!isDirty.value) return
  saving.value = true
  try {
    const payload: ProfileUpdatePayload = { full_name: form.fullname || undefined, email: form.email || undefined, gender: form.gender || undefined,
      avatar_url: avatarPreview.value || profileDetails.value?.avatar || profileDetails.value?.avatar_url, email_updates: form.emailUpdates,
      class_name: form.className || undefined, address: form.address || undefined, city: form.city || undefined, district: form.district || undefined, ward: form.ward || undefined }
    if (dob.year && dob.month && dob.day) payload.dob = `${dob.year}-${String(dob.month).padStart(2, '0')}-${String(dob.day).padStart(2, '0')}`
    const updated = await auth.updateProfile(payload); profileDetails.value = updated; applyProfileToForm(updated)
    lastUpdated.value = formatDateTime(updated.updatedAt || updated.createdAt || new Date()); snapshot()
    avatarFile.value = null; avatarPreview.value = ''; if (fileInput.value) fileInput.value.value = ''
    showToast('Cập nhật hồ sơ thành công!', 'success')
  } catch (e: any) {
    if (e?.response?.status === 200 || e?.response?.status === 201) {
      try { const profile = await authService.getProfile(); profileDetails.value = profile; applyProfileToForm(profile)
        lastUpdated.value = formatDateTime(profile.updatedAt || profile.createdAt || new Date()); snapshot()
        avatarFile.value = null; avatarPreview.value = ''; if (fileInput.value) fileInput.value.value = ''
        showToast('Cập nhật hồ sơ thành công!', 'success')
      } catch { showToast('Cập nhật thành công nhưng không thể tải lại thông tin.', 'warning') }
    } else { showToast(e?.response?.data?.detail || e?.message || 'Cập nhật thất bại.', 'error') }
  } finally { saving.value = false }
}
</script>

<style scoped>
.page-wrapper { min-height: 100vh; position: relative; transition: background-color 0.3s ease; }
.page-wrapper.dark-mode { background: #020617; }
.page-wrapper.light-mode { background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%); }

.bg-elements { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.glow { position: absolute; border-radius: 50%; filter: blur(100px); }
.glow-1 { top: 10%; left: -5%; width: 300px; height: 300px; background: rgba(6, 182, 212, 0.1); }
.glow-2 { bottom: 10%; right: -5%; width: 250px; height: 250px; background: rgba(139, 92, 246, 0.1); }

.page-content { position: relative; z-index: 10; max-width: 800px; margin: 0 auto; padding: 24px; }

.tabs-nav { display: flex; gap: 8px; margin-bottom: 24px; border-bottom: 1px solid; padding-bottom: 12px; }
.dark-mode .tabs-nav { border-color: rgba(255,255,255,0.1); }
.light-mode .tabs-nav { border-color: #e2e8f0; }

.tab-btn { padding: 10px 16px; border-radius: 10px; font-size: 14px; font-weight: 600; background: none; border: none; cursor: pointer; transition: all 0.3s; }
.dark-mode .tab-btn { color: #64748b; }
.light-mode .tab-btn { color: #64748b; }
.tab-btn:hover { }
.dark-mode .tab-btn:hover { color: white; }
.light-mode .tab-btn:hover { color: #1e293b; }
.tab-btn.active { }
.dark-mode .tab-btn.active { color: white; border-bottom: 2px solid #06b6d4; }
.light-mode .tab-btn.active { color: #1e293b; border-bottom: 2px solid #6366f1; }

.profile-card { border-radius: 20px; overflow: hidden; }
.dark-mode .profile-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); }
.light-mode .profile-card { background: white; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }

.card-header { padding: 20px 24px; border-bottom: 1px solid; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; }
.dark-mode .card-header { border-color: rgba(255,255,255,0.08); }
.light-mode .card-header { border-color: #e2e8f0; }
.card-header h2 { font-size: 18px; font-weight: 700; margin: 0; }
.dark-mode .card-header h2 { color: white; }
.light-mode .card-header h2 { color: #1e293b; }
.card-header p { font-size: 12px; margin: 0; }
.dark-mode .card-header p { color: #64748b; }
.light-mode .card-header p { color: #64748b; }
.card-header p span { }
.dark-mode .card-header p span { color: #94a3b8; }
.light-mode .card-header p span { color: #475569; }

.profile-form { padding: 24px; }
.form-row { display: grid; grid-template-columns: 180px 1fr; gap: 16px; margin-bottom: 20px; align-items: start; }
@media (max-width: 640px) { .form-row { grid-template-columns: 1fr; gap: 8px; } }

.form-row > label { font-size: 14px; font-weight: 500; padding-top: 10px; }
.dark-mode .form-row > label { color: #94a3b8; }
.light-mode .form-row > label { color: #475569; }
.required { color: #ef4444; }

.input-group { display: flex; flex-direction: column; gap: 4px; }

input, select, textarea { width: 100%; padding: 10px 14px; border-radius: 10px; font-size: 14px; outline: none; transition: all 0.3s; }
.dark-mode input, .dark-mode select, .dark-mode textarea { background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.1); color: white; }
.light-mode input, .light-mode select, .light-mode textarea { background: white; border: 1px solid #e2e8f0; color: #1e293b; }
/* Fix select options in dark mode */
.dark-mode select option { background: #1e293b; color: white; }
.light-mode select option { background: white; color: #1e293b; }
input:focus, select:focus, textarea:focus { }
.dark-mode input:focus, .dark-mode select:focus, .dark-mode textarea:focus { border-color: #06b6d4; }
.light-mode input:focus, .light-mode select:focus, .light-mode textarea:focus { border-color: #6366f1; }
input.error, select.error, textarea.error { border-color: #ef4444 !important; }
.input-readonly { cursor: not-allowed; }
.dark-mode .input-readonly { background: rgba(255,255,255,0.02); color: #64748b; }
.light-mode .input-readonly { background: #f8fafc; color: #64748b; }

.hint { font-size: 12px; }
.dark-mode .hint { color: #475569; }
.light-mode .hint { color: #94a3b8; }
.error-text { font-size: 12px; color: #ef4444; }

.avatar-section { display: flex; flex-direction: column; gap: 8px; }
.avatar-btn { position: relative; width: 96px; height: 96px; border-radius: 50%; overflow: hidden; border: none; cursor: pointer; padding: 0; }
.dark-mode .avatar-btn { border: 2px solid rgba(255,255,255,0.1); }
.light-mode .avatar-btn { border: 2px solid #e2e8f0; }
.avatar-btn img { width: 100%; height: 100%; object-fit: cover; }
.avatar-overlay { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; background: rgba(0,0,0,0.6); opacity: 0; transition: opacity 0.3s; color: white; }
.avatar-btn:hover .avatar-overlay { opacity: 1; }

.dob-selects { display: flex; gap: 8px; }
.dob-selects select { flex: 1; }

.gender-options { display: flex; gap: 12px; }
.gender-option { display: flex; align-items: center; gap: 8px; padding: 10px 16px; border-radius: 10px; font-size: 14px; cursor: pointer; transition: all 0.3s; }
.dark-mode .gender-option { border: 1px solid rgba(255,255,255,0.1); color: #94a3b8; }
.light-mode .gender-option { border: 1px solid #e2e8f0; color: #64748b; }
.gender-option:hover { }
.dark-mode .gender-option:hover { border-color: rgba(255,255,255,0.2); }
.light-mode .gender-option:hover { border-color: #cbd5e1; }
.gender-option.active { }
.dark-mode .gender-option.active { border-color: #06b6d4; background: rgba(6,182,212,0.1); color: white; }
.light-mode .gender-option.active { border-color: #6366f1; background: rgba(99,102,241,0.1); color: #1e293b; }
.gender-option input { width: 16px; height: 16px; }

.checkbox-group { display: flex; align-items: center; gap: 12px; }
.checkbox-group input { width: 18px; height: 18px; }
.checkbox-group label { font-size: 14px; }
.dark-mode .checkbox-group label { color: #94a3b8; }
.light-mode .checkbox-group label { color: #475569; }

.form-actions { display: flex; justify-content: flex-end; align-items: center; gap: 16px; padding-top: 20px; border-top: 1px solid; margin-top: 20px; }
.dark-mode .form-actions { border-color: rgba(255,255,255,0.08); }
.light-mode .form-actions { border-color: #e2e8f0; }
.action-hint { font-size: 12px; margin-right: auto; }
.dark-mode .action-hint { color: #64748b; }
.light-mode .action-hint { color: #94a3b8; }

.submit-btn { display: inline-flex; align-items: center; gap: 8px; padding: 12px 24px; border-radius: 12px; font-size: 14px; font-weight: 600; border: none; cursor: pointer; transition: all 0.3s; }
.dark-mode .submit-btn { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; }
.light-mode .submit-btn { background: #1e293b; color: white; }
.submit-btn:hover:not(:disabled) { transform: translateY(-2px); }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.loading-text { padding: 40px; text-align: center; font-size: 14px; }
.dark-mode .loading-text { color: #64748b; }
.light-mode .loading-text { color: #64748b; }

.hidden { display: none; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; z-index: 50; display: flex; align-items: center; justify-content: center; padding: 16px; }
.dark-mode .modal-overlay { background: rgba(0,0,0,0.7); }
.light-mode .modal-overlay { background: rgba(0,0,0,0.5); }

.modal-card { width: 100%; max-width: 360px; padding: 24px; border-radius: 16px; text-align: center; outline: none; }
.dark-mode .modal-card { background: #1e293b; border: 1px solid rgba(255,255,255,0.1); }
.light-mode .modal-card { background: white; border: 1px solid #e2e8f0; }

.modal-icon { width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 16px; }
.modal-icon.error { background: rgba(239,68,68,0.1); color: #ef4444; }

.modal-card h3 { font-size: 18px; font-weight: 600; margin: 0 0 12px; }
.dark-mode .modal-card h3 { color: white; }
.light-mode .modal-card h3 { color: #1e293b; }
.modal-card p { font-size: 14px; margin: 0 0 8px; }
.dark-mode .modal-card p { color: #94a3b8; }
.light-mode .modal-card p { color: #64748b; }
.modal-hint { font-size: 12px; }
.dark-mode .modal-hint { color: #64748b; }
.light-mode .modal-hint { color: #94a3b8; }

.modal-btn { width: 100%; padding: 12px; border-radius: 10px; font-size: 14px; font-weight: 600; border: none; cursor: pointer; margin-top: 20px; transition: all 0.3s; }
.dark-mode .modal-btn { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; }
.light-mode .modal-btn { background: #1e293b; color: white; }
.modal-btn:hover { transform: translateY(-2px); }
</style>
