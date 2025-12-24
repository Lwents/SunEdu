<template>
  <div class="security">
    <!-- Header -->
    <div class="security-header">
      <div class="header-info">
        <h1 class="title">🔒 Bảo mật hệ thống</h1>
        <p class="subtitle">Quản lý chính sách bảo mật, IP và phiên đăng nhập</p>
      </div>
      <div class="header-actions">
        <button class="action-btn secondary" @click="load">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Tải lại
        </button>
        <button class="action-btn primary" :disabled="saving" @click="savePolicy">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          {{ saving ? 'Đang lưu...' : 'Lưu chính sách' }}
        </button>
      </div>
    </div>

    <!-- Tabs -->
    <div class="section-card tabs-card">
      <div class="tabs-header">
        <button 
          v-for="t in tabs" 
          :key="t.key" 
          class="tab-btn" 
          :class="{ active: tab === t.key }"
          @click="tab = t.key"
        >
          {{ t.icon }} {{ t.label }}
        </button>
      </div>

      <div class="tab-content">
        <!-- Policy Tab -->
        <div v-if="tab === 'policy'" class="policy-grid">
          <div class="policy-card">
            <div class="policy-title">🔐 Xác thực 2 lớp (2FA)</div>
            <div class="checkbox-group">
              <label class="checkbox-item">
                <input type="checkbox" v-model="policy.twoFA.enforceAdmin" />
                <span class="checkmark"></span>
                <span class="checkbox-label">Bắt buộc cho Admin</span>
              </label>
              <label class="checkbox-item">
                <input type="checkbox" v-model="policy.twoFA.enforceTeacher" />
                <span class="checkmark"></span>
                <span class="checkbox-label">Bắt buộc cho Teacher</span>
              </label>
            </div>
            <p class="policy-note">HS có thể bật tự nguyện.</p>
          </div>

          <div class="policy-card">
            <div class="policy-title">⚡ Rate limit & Lockout</div>
            <div class="input-grid">
              <div class="input-group">
                <label>Login sai (lần)</label>
                <div class="number-input">
                  <button class="num-btn" @click="policy.rateLimit.loginFailures = Math.max(3, policy.rateLimit.loginFailures - 1)">−</button>
                  <input type="number" v-model.number="policy.rateLimit.loginFailures" min="3" />
                  <button class="num-btn" @click="policy.rateLimit.loginFailures++">+</button>
                </div>
              </div>
              <div class="input-group">
                <label>Trong (phút)</label>
                <div class="number-input">
                  <button class="num-btn" @click="policy.rateLimit.windowMin = Math.max(1, policy.rateLimit.windowMin - 1)">−</button>
                  <input type="number" v-model.number="policy.rateLimit.windowMin" min="1" />
                  <button class="num-btn" @click="policy.rateLimit.windowMin++">+</button>
                </div>
              </div>
              <div class="input-group">
                <label>Ngưỡng lockout (lần)</label>
                <div class="number-input">
                  <button class="num-btn" @click="policy.lockout.attempts = Math.max(3, policy.lockout.attempts - 1)">−</button>
                  <input type="number" v-model.number="policy.lockout.attempts" min="3" />
                  <button class="num-btn" @click="policy.lockout.attempts++">+</button>
                </div>
              </div>
              <div class="input-group">
                <label>Khoá (phút)</label>
                <div class="number-input">
                  <button class="num-btn" @click="policy.lockout.lockMinutes = Math.max(1, policy.lockout.lockMinutes - 1)">−</button>
                  <input type="number" v-model.number="policy.lockout.lockMinutes" min="1" />
                  <button class="num-btn" @click="policy.lockout.lockMinutes++">+</button>
                </div>
              </div>
              <div class="input-group full-width">
                <label>Ban vĩnh viễn sau (lần)</label>
                <div class="number-input">
                  <button class="num-btn" @click="policy.lockout.banStrikes = Math.max(3, policy.lockout.banStrikes - 1)">−</button>
                  <input type="number" v-model.number="policy.lockout.banStrikes" min="3" />
                  <button class="num-btn" @click="policy.lockout.banStrikes++">+</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- IP Tab -->
        <div v-if="tab === 'ip'" class="ip-section">
          <div class="ip-form">
            <input v-model="cidr" placeholder="203.0.113.0/24" class="text-input" />
            <input v-model="ipNote" placeholder="Ghi chú" class="text-input" />
            <button class="action-btn primary" @click="addIp">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              Thêm IP
            </button>
          </div>
          <div class="ip-list">
            <div v-for="ip in ipList" :key="ip.id" class="ip-item">
              <div class="ip-info">
                <span class="ip-cidr">{{ ip.cidr }}</span>
                <span class="ip-note">{{ ip.note }}</span>
              </div>
              <div class="ip-meta">
                <span class="ip-status" :class="ip.active ? 'active' : ''">{{ ip.active ? 'Active' : 'Off' }}</span>
                <span class="ip-by">{{ ip.createdBy }}</span>
                <span class="ip-time">{{ fmt(ip.createdAt) }}</span>
              </div>
              <button class="delete-btn" @click="removeIp(ip.id)">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
            <div v-if="!ipList.length" class="empty-state">Chưa có IP nào trong danh sách</div>
          </div>
        </div>

        <!-- TLS Tab -->
        <div v-if="tab === 'tls'" class="tls-grid">
          <div class="policy-card">
            <div class="policy-title">📜 Trạng thái chứng chỉ</div>
            <div class="cert-info">
              <div class="cert-row"><span class="cert-label">Issuer:</span><span class="cert-value">{{ cert.issuer }}</span></div>
              <div class="cert-row"><span class="cert-label">Valid:</span><span class="cert-value">{{ fmt(cert.validFrom) }} → {{ fmt(cert.validTo) }}</span></div>
              <div class="cert-row"><span class="cert-label">Còn lại:</span><span class="cert-value highlight">{{ cert.daysRemaining }} ngày</span></div>
              <div class="cert-row"><span class="cert-label">Auto-renew:</span><span class="cert-status" :class="cert.autoRenew ? 'on' : 'off'">{{ cert.autoRenew ? 'ON' : 'OFF' }}</span></div>
              <div class="cert-row" v-if="cert.grade"><span class="cert-label">SSL Labs:</span><span class="cert-value highlight">{{ cert.grade }}</span></div>
            </div>
            <button class="action-btn secondary mt-4" :disabled="renewing" @click="renewCert">
              {{ renewing ? 'Đang gia hạn...' : 'Gia hạn (mock)' }}
            </button>
          </div>

          <div class="policy-card">
            <div class="policy-title">🔔 Alerting</div>
            <div class="input-grid">
              <div class="input-group">
                <label>CPU threshold %</label>
                <div class="number-input">
                  <button class="num-btn" @click="alertPolicy.cpuThreshold = Math.max(10, alertPolicy.cpuThreshold - 5)">−</button>
                  <input type="number" v-model.number="alertPolicy.cpuThreshold" min="10" max="100" />
                  <button class="num-btn" @click="alertPolicy.cpuThreshold = Math.min(100, alertPolicy.cpuThreshold + 5)">+</button>
                </div>
              </div>
              <div class="input-group">
                <label>Error rate %</label>
                <div class="number-input">
                  <button class="num-btn" @click="alertPolicy.errorRateThreshold = Math.max(0, alertPolicy.errorRateThreshold - 1)">−</button>
                  <input type="number" v-model.number="alertPolicy.errorRateThreshold" min="0" max="100" />
                  <button class="num-btn" @click="alertPolicy.errorRateThreshold = Math.min(100, alertPolicy.errorRateThreshold + 1)">+</button>
                </div>
              </div>
            </div>
            <div class="switch-group">
              <label class="switch-item">
                <span>Kênh Email</span>
                <label class="switch"><input type="checkbox" v-model="alertPolicy.channels.email" /><span class="slider"></span></label>
              </label>
              <label class="switch-item">
                <span>Kênh SMS</span>
                <label class="switch"><input type="checkbox" v-model="alertPolicy.channels.sms" /><span class="slider"></span></label>
              </label>
            </div>
            <div class="input-group full-width mt-3">
              <label>On-call</label>
              <input v-model="alertPolicy.onCall" class="text-input" placeholder="Email hoặc số điện thoại" />
            </div>
            <div class="btn-group mt-4">
              <button class="action-btn secondary" :disabled="savingAlerts" @click="saveAlerts">{{ savingAlerts ? 'Đang lưu...' : 'Lưu Alert' }}</button>
              <button class="action-btn primary" :disabled="testingAlert" @click="testAlert">{{ testingAlert ? 'Đang gửi...' : 'Test Alert' }}</button>
            </div>
          </div>
        </div>

        <!-- Sessions Tab -->
        <div v-if="tab === 'sessions'" class="sessions-section">
          <div class="session-filter">
            <input v-model="filterUser" placeholder="Lọc theo User ID" class="text-input" />
            <button class="action-btn secondary" @click="loadSessions">Tải danh sách</button>
          </div>
          <div class="session-list">
            <div v-for="s in sessions" :key="s.jti" class="session-item">
              <div class="session-main">
                <div class="session-user">
                  <span class="user-name">{{ s.userName }}</span>
                  <span class="user-role">{{ s.role }}</span>
                </div>
                <div class="session-device">{{ s.device }} • {{ s.ip }}</div>
              </div>
              <div class="session-meta">
                <span class="session-time">{{ fmt(s.lastActiveAt) }}</span>
                <span class="session-location">{{ s.location }}</span>
              </div>
              <button class="delete-btn" @click="revoke(s.jti)" title="Thu hồi phiên">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                </svg>
              </button>
            </div>
            <div v-if="!sessions.length" class="empty-state">Không có phiên đăng nhập nào</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import {
  securityService,
  type SecurityPolicy,
  type IpAllowItem,
  type SessionItem,
  type CertStatus,
  type AlertPolicy,
} from '@/services/security.service'
import { showToast } from '@/utils/toast'

const tabs = [
  { key: 'policy', label: 'Chính sách', icon: '📋' },
  { key: 'ip', label: 'IP Allowlist', icon: '🌐' },
  { key: 'tls', label: 'Chứng chỉ & TLS', icon: '🔐' },
  { key: 'sessions', label: 'Phiên đăng nhập', icon: '👤' },
]

const tab = ref<string>('policy')
const saving = ref(false)
const savingAlerts = ref(false)
const renewing = ref(false)
const testingAlert = ref(false)

const policy = reactive<SecurityPolicy>({
  twoFA: { enforceAdmin: false, enforceTeacher: false },
  rateLimit: { loginFailures: 5, windowMin: 10 },
  lockout: { attempts: 5, lockMinutes: 30, banStrikes: 5 },
  rbacNote: '',
})
const ipList = ref<IpAllowItem[]>([])
const sessions = ref<SessionItem[]>([])
const cert = reactive<CertStatus>({ issuer: '', validFrom: '', validTo: '', daysRemaining: 0, autoRenew: true })
const alertPolicy = reactive<AlertPolicy>({ cpuThreshold: 90, errorRateThreshold: 2, channels: { email: true, sms: true }, onCall: '' })

const cidr = ref('')
const ipNote = ref('')
const filterUser = ref<string>('')

function fmt(iso?: string) { return iso ? new Date(iso).toLocaleString('vi-VN') : '' }

async function load() {
  try {
    const [p, ips, c, ap] = await Promise.all([
      securityService.getPolicy(), securityService.listIpAllow(), securityService.getCertStatus(), securityService.getAlertPolicy(),
    ])
    Object.assign(policy, p)
    ipList.value = ips
    Object.assign(cert, c)
    Object.assign(alertPolicy, ap)
  } catch (error: any) { showToast(error?.message || 'Không tải được dữ liệu', 'error') }
}

async function savePolicy() {
  saving.value = true
  try { await securityService.updatePolicy(policy); showToast('Đã lưu chính sách', 'success') }
  catch (error: any) { showToast(error?.message || 'Không thể lưu', 'error') }
  finally { saving.value = false }
}

async function addIp() {
  if (!cidr.value) { showToast('Nhập CIDR', 'warning'); return }
  try { await securityService.addIpAllow(cidr.value, ipNote.value); cidr.value = ''; ipNote.value = ''; ipList.value = await securityService.listIpAllow(); showToast('Đã thêm IP', 'success') }
  catch (error: any) { showToast(error?.message || 'Không thể thêm IP', 'error') }
}

async function removeIp(id: string) {
  try { await securityService.removeIpAllow(id); ipList.value = await securityService.listIpAllow(); showToast('Đã xoá IP', 'info') }
  catch (error: any) { showToast(error?.message || 'Không thể xoá IP', 'error') }
}

async function loadSessions() {
  const uid = filterUser.value ? Number(filterUser.value) : undefined
  try { sessions.value = await securityService.listSessions(uid) }
  catch (error: any) { showToast(error?.message || 'Không tải được danh sách phiên', 'error') }
}

async function revoke(jti: string) {
  try { await securityService.revokeSession(jti); await loadSessions(); showToast('Đã thu hồi phiên', 'success') }
  catch (error: any) { showToast(error?.message || 'Không thu hồi được phiên', 'error') }
}

async function renewCert() {
  renewing.value = true
  try { await securityService.renewCert(); Object.assign(cert, await securityService.getCertStatus()); showToast('Đã gửi yêu cầu gia hạn', 'info') }
  catch (error: any) { showToast(error?.message || 'Không thể gia hạn', 'error') }
  finally { renewing.value = false }
}

async function saveAlerts() {
  savingAlerts.value = true
  try { await securityService.updateAlertPolicy(alertPolicy); showToast('Đã lưu cấu hình alert', 'success') }
  catch (error: any) { showToast(error?.message || 'Không thể lưu alert', 'error') }
  finally { savingAlerts.value = false }
}

async function testAlert() {
  testingAlert.value = true
  try { await securityService.alertTest(); showToast('Đã gửi test alert', 'info') }
  catch (error: any) { showToast(error?.message || 'Không gửi được test alert', 'error') }
  finally { testingAlert.value = false }
}

onMounted(() => { load(); loadSessions() })
</script>

<style scoped>
.security {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding-bottom: 24px;
}

/* Header */
.security-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  flex-wrap: wrap;
}

.title { font-size: 24px; font-weight: 700; margin: 0; color: var(--el-text-color-primary); }
.subtitle { font-size: 14px; margin: 4px 0 0; color: var(--el-text-color-secondary); }

.header-actions { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }

/* Buttons */
.action-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.action-btn.primary { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; }
.action-btn.secondary { 
  background: var(--el-bg-color); 
  border: 1px solid var(--el-border-color); 
  color: var(--el-text-color-primary); 
}
.action-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); }
.action-btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }

/* Section Card */
.section-card { 
  border-radius: 16px; 
  transition: all 0.3s ease; 
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color-light);
}

/* Tabs */
.tabs-header { 
  display: flex; 
  gap: 4px; 
  padding: 16px 20px; 
  border-bottom: 1px solid var(--el-border-color-light); 
  flex-wrap: wrap; 
}

.tab-btn {
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  background: transparent;
  color: var(--el-text-color-secondary);
}

.tab-btn:hover { background: rgba(99, 102, 241, 0.1); }
.tab-btn.active { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; }

.tab-content { padding: 20px; }

/* Policy Grid */
.policy-grid, .tls-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }

.policy-card { 
  padding: 20px; 
  border-radius: 12px; 
  background: var(--el-fill-color-light);
  border: 1px solid var(--el-border-color-lighter);
}

.policy-title { font-size: 16px; font-weight: 600; margin-bottom: 16px; color: var(--el-text-color-primary); }
.policy-note { font-size: 12px; margin-top: 12px; color: var(--el-text-color-secondary); }

/* Checkbox */
.checkbox-group { display: flex; flex-direction: column; gap: 12px; }
.checkbox-item { display: flex; align-items: center; gap: 10px; cursor: pointer; }
.checkbox-item input { display: none; }
.checkmark {
  width: 20px; height: 20px; border-radius: 6px; 
  border: 2px solid var(--el-border-color);
  background: var(--el-bg-color);
  display: flex; align-items: center; justify-content: center; transition: all 0.2s;
}
.checkbox-item input:checked + .checkmark { background: #6366f1; border-color: #6366f1; }
.checkbox-item input:checked + .checkmark::after { content: '✓'; color: white; font-size: 12px; }
.checkbox-label { font-size: 14px; color: var(--el-text-color-primary); }
</style>

<style scoped>
/* Input Grid */
.input-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.input-group { display: flex; flex-direction: column; gap: 6px; }
.input-group.full-width { grid-column: span 2; }
.input-group label { font-size: 13px; font-weight: 500; color: var(--el-text-color-secondary); }

/* Number Input */
.number-input {
  display: flex;
  align-items: center;
  border-radius: 8px;
  overflow: hidden;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color);
}

.num-btn {
  width: 36px; height: 36px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; font-weight: 500;
  cursor: pointer; border: none; transition: all 0.2s;
  background: var(--el-fill-color);
  color: var(--el-text-color-secondary);
}
.num-btn:hover { background: #6366f1; color: white; }

.number-input input {
  flex: 1; text-align: center; border: none; background: transparent;
  font-size: 14px; font-weight: 600; padding: 8px;
  -moz-appearance: textfield;
  appearance: textfield;
  color: var(--el-text-color-primary);
}
.number-input input::-webkit-outer-spin-button,
.number-input input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }

/* Text Input */
.text-input {
  padding: 10px 14px; border-radius: 8px; font-size: 14px; width: 100%;
  background: var(--el-bg-color);
  border: 1px solid var(--el-border-color);
  color: var(--el-text-color-primary);
}
.text-input:focus { outline: none; border-color: #6366f1; }
.text-input::placeholder { color: var(--el-text-color-placeholder); }

/* Switch */
.switch-group { display: flex; gap: 24px; margin-top: 16px; flex-wrap: wrap; }
.switch-item { display: flex; align-items: center; gap: 12px; font-size: 14px; color: var(--el-text-color-primary); }

.switch { position: relative; width: 44px; height: 24px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider {
  position: absolute; cursor: pointer; inset: 0;
  background: var(--el-border-color); border-radius: 24px; transition: 0.3s;
}
.slider::before {
  content: ''; position: absolute; height: 18px; width: 18px;
  left: 3px; bottom: 3px; background: white; border-radius: 50%; transition: 0.3s;
}
.switch input:checked + .slider { background: #6366f1; }
.switch input:checked + .slider::before { transform: translateX(20px); }

/* Button Group */
.btn-group { display: flex; gap: 12px; }
.mt-3 { margin-top: 12px; }
.mt-4 { margin-top: 16px; }

/* IP Section */
.ip-form { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 20px; }
.ip-form .text-input { width: 200px; }

.ip-list { display: flex; flex-direction: column; gap: 12px; }
.ip-item { 
  display: flex; align-items: center; gap: 16px; padding: 16px; border-radius: 12px; 
  background: var(--el-fill-color-light);
}

.ip-info { flex: 1; display: flex; flex-direction: column; gap: 4px; }
.ip-cidr { font-size: 14px; font-weight: 600; font-family: monospace; color: #6366f1; }
.ip-note { font-size: 13px; color: var(--el-text-color-secondary); }

.ip-meta { display: flex; gap: 16px; align-items: center; font-size: 12px; color: var(--el-text-color-secondary); }

.ip-status { padding: 4px 10px; border-radius: 6px; font-weight: 600; background: var(--el-fill-color); color: var(--el-text-color-secondary); }
.ip-status.active { background: rgba(34, 197, 94, 0.15); color: #22c55e; }

.delete-btn {
  width: 36px; height: 36px; border-radius: 8px; border: none;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all 0.2s;
  background: rgba(239, 68, 68, 0.1); color: #ef4444;
}
.delete-btn:hover { background: #ef4444; color: white; }

/* Cert Info */
.cert-info { display: flex; flex-direction: column; gap: 10px; }
.cert-row { display: flex; gap: 8px; font-size: 14px; }
.cert-label { min-width: 80px; color: var(--el-text-color-secondary); }
.cert-value { font-weight: 500; color: var(--el-text-color-primary); }
.cert-value.highlight { color: #22d3ee; }

.cert-status { padding: 2px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }
.cert-status.on { background: rgba(34, 197, 94, 0.15); color: #22c55e; }
.cert-status.off { background: var(--el-fill-color); color: var(--el-text-color-secondary); }

/* Sessions */
.session-filter { display: flex; gap: 12px; margin-bottom: 20px; }
.session-filter .text-input { width: 200px; }

.session-list { display: flex; flex-direction: column; gap: 12px; }
.session-item { 
  display: flex; align-items: center; gap: 16px; padding: 16px; border-radius: 12px; 
  background: var(--el-fill-color-light);
}

.session-main { flex: 1; }
.session-user { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.user-name { font-size: 14px; font-weight: 600; color: var(--el-text-color-primary); }
.user-role { padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; background: rgba(99, 102, 241, 0.15); color: #6366f1; }
.session-device { font-size: 13px; color: var(--el-text-color-secondary); }

.session-meta { display: flex; flex-direction: column; align-items: flex-end; gap: 4px; font-size: 12px; color: var(--el-text-color-secondary); }

/* Empty State */
.empty-state { text-align: center; padding: 40px 20px; font-size: 14px; color: var(--el-text-color-secondary); }

@media (max-width: 768px) {
  .input-grid { grid-template-columns: 1fr; }
  .input-group.full-width { grid-column: span 1; }
  .ip-form .text-input { width: 100%; }
}
</style>
