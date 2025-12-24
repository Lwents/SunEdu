<template>
  <div class="config">
    <!-- Header -->
    <div class="config-header">
      <div class="header-info">
        <h1 class="title">⚙️ Cấu hình hệ thống</h1>
        <p class="subtitle">Phiên bản: v{{ form.version }} • {{ form.updatedBy }} • {{ fmt(form.updatedAt) }}</p>
      </div>
      <div class="header-actions">
        <button class="action-btn secondary" @click="load">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Tải lại
        </button>
        <button class="action-btn secondary" :disabled="saving" @click="save">
          {{ saving ? 'Đang lưu...' : 'Lưu nháp' }}
        </button>
        <button class="action-btn primary" :disabled="saving" @click="apply">
          {{ saving ? 'Đang áp dụng...' : 'Áp dụng' }}
        </button>
      </div>
    </div>

    <!-- Tabs -->
    <div class="section-card tabs-card">
      <div class="tabs-header">
        <button v-for="t in tabs" :key="t.key" class="tab-btn" :class="{ active: tab === t.key }" @click="tab = t.key">
          {{ t.icon }} {{ t.label }}
        </button>
      </div>

      <div class="tab-content">
        <!-- Brand Tab -->
        <div v-if="tab === 'brand'" class="form-grid">
          <div class="form-card">
            <div class="form-title">🏷️ Thông tin chung</div>
            <div class="input-group">
              <label>Tên hệ thống</label>
              <input v-model="form.brand.siteName" class="text-input" />
            </div>
            <div class="input-group">
              <label>Ngôn ngữ mặc định</label>
              <select v-model="form.brand.language" class="text-input">
                <option value="vi">Tiếng Việt</option>
                <option value="en">English</option>
              </select>
            </div>
            <div class="input-group">
              <label>Múi giờ</label>
              <input v-model="form.brand.timezone" class="text-input" />
            </div>
            <div class="input-group">
              <label>Tiền tệ</label>
              <input v-model="form.brand.currency" class="text-input" disabled />
            </div>
          </div>
          <div class="form-card">
            <div class="form-title">🖼️ Logo</div>
            <div class="logo-preview" v-if="form.brand.logoUrl">
              <img :src="form.brand.logoUrl" alt="Logo" />
            </div>
            <div class="input-group">
              <label>URL Logo</label>
              <input v-model="form.brand.logoUrl" class="text-input" placeholder="https://..." />
            </div>
          </div>
        </div>

        <!-- Domain & Email Tab -->
        <div v-if="tab === 'email'" class="form-grid">
          <div class="form-card">
            <div class="form-title">🌐 Domain</div>
            <div class="input-group">
              <label>Domain</label>
              <input v-model="form.domainEmail.domain" class="text-input" />
            </div>
            <div class="checkbox-group">
              <label class="checkbox-item">
                <input type="checkbox" v-model="form.domainEmail.forceHttps" />
                <span class="checkmark"></span>
                <span class="checkbox-label">Bắt buộc HTTPS</span>
              </label>
              <label class="checkbox-item">
                <input type="checkbox" v-model="form.domainEmail.hsts" />
                <span class="checkmark"></span>
                <span class="checkbox-label">Bật HSTS</span>
              </label>
            </div>
            <div class="status-tags">
              <span>SPF/DKIM/DMARC:</span>
              <span class="status-tag" :class="badge(form.domainEmail.spf?.status)">{{ form.domainEmail.spf?.status || 'unknown' }}</span>
              <span class="status-tag" :class="badge(form.domainEmail.dkim?.status)">{{ form.domainEmail.dkim?.status || 'unknown' }}</span>
              <span class="status-tag" :class="badge(form.domainEmail.dmarc?.status)">{{ form.domainEmail.dmarc?.status || 'unknown' }}</span>
            </div>
          </div>
          <div class="form-card">
            <div class="form-title">📧 SMTP</div>
            <div class="input-row">
              <div class="input-group">
                <label>Host</label>
                <input v-model="form.domainEmail.smtp.host" class="text-input" />
              </div>
              <div class="input-group" style="max-width: 120px;">
                <label>Port</label>
                <div class="number-input">
                  <button class="num-btn" @click="form.domainEmail.smtp.port = Math.max(1, form.domainEmail.smtp.port - 1)">−</button>
                  <input type="number" v-model.number="form.domainEmail.smtp.port" />
                  <button class="num-btn" @click="form.domainEmail.smtp.port++">+</button>
                </div>
              </div>
            </div>
            <div class="input-group">
              <label>Username</label>
              <input v-model="form.domainEmail.smtp.username" class="text-input" />
            </div>
            <div class="input-group">
              <label>Sender name</label>
              <input v-model="form.domainEmail.smtp.senderName" class="text-input" />
            </div>
            <div class="input-group">
              <label>From email</label>
              <input v-model="form.domainEmail.smtp.fromEmail" class="text-input" />
            </div>
            <div class="password-info">
              <span>Mật khẩu:</span>
              <span class="status-tag info">{{ form.domainEmail.smtp.passwordMasked ? '****** (masked)' : '(chưa thiết lập)' }}</span>
            </div>
            <div class="test-row">
              <input v-model="testMail" class="text-input" placeholder="Email test" />
              <button class="action-btn secondary" :disabled="testingMail" @click="sendTestMail">{{ testingMail ? 'Đang gửi...' : 'Gửi test' }}</button>
            </div>
          </div>
        </div>

        <!-- Auth & Session Tab -->
        <div v-if="tab === 'auth'" class="form-grid">
          <div class="form-card">
            <div class="form-title">🔐 Phiên đăng nhập</div>
            <div class="input-row">
              <div class="input-group">
                <label>Idle timeout (phút)</label>
                <div class="number-input">
                  <button class="num-btn" @click="form.authSession.idleTimeoutMin = Math.max(1, form.authSession.idleTimeoutMin - 1)">−</button>
                  <input type="number" v-model.number="form.authSession.idleTimeoutMin" />
                  <button class="num-btn" @click="form.authSession.idleTimeoutMin++">+</button>
                </div>
              </div>
              <div class="input-group">
                <label>Max session (giờ)</label>
                <div class="number-input">
                  <button class="num-btn" @click="form.authSession.maxSessionHours = Math.max(1, form.authSession.maxSessionHours - 1)">−</button>
                  <input type="number" v-model.number="form.authSession.maxSessionHours" />
                  <button class="num-btn" @click="form.authSession.maxSessionHours++">+</button>
                </div>
              </div>
              <div class="input-group">
                <label>Remember-me (ngày)</label>
                <div class="number-input">
                  <button class="num-btn" @click="form.authSession.rememberMeDays = Math.max(1, form.authSession.rememberMeDays - 1)">−</button>
                  <input type="number" v-model.number="form.authSession.rememberMeDays" />
                  <button class="num-btn" @click="form.authSession.rememberMeDays++">+</button>
                </div>
              </div>
            </div>
            <div class="divider"></div>
            <div class="checkbox-group">
              <label class="checkbox-item">
                <input type="checkbox" v-model="form.authSession.ssoGoogleEnabled" />
                <span class="checkmark"></span>
                <span class="checkbox-label">Bật đăng nhập Google</span>
              </label>
            </div>
            <div class="input-group" v-if="form.authSession.ssoGoogleEnabled">
              <label>Google Client ID</label>
              <input v-model="form.authSession.googleClientId" class="text-input" />
            </div>
            <div class="divider"></div>
            <div class="form-subtitle">2FA bắt buộc</div>
            <div class="checkbox-group horizontal">
              <label class="checkbox-item">
                <input type="checkbox" v-model="form.authSession.twoFAEnforce.admin" />
                <span class="checkmark"></span>
                <span class="checkbox-label">Admin</span>
              </label>
              <label class="checkbox-item">
                <input type="checkbox" v-model="form.authSession.twoFAEnforce.teacher" />
                <span class="checkmark"></span>
                <span class="checkbox-label">Teacher</span>
              </label>
            </div>
            <div class="divider"></div>
            <div class="form-subtitle">Chính sách mật khẩu</div>
            <div class="input-row">
              <div class="input-group">
                <label>Độ dài tối thiểu</label>
                <div class="number-input">
                  <button class="num-btn" @click="form.authSession.passwordPolicy.minLength = Math.max(6, form.authSession.passwordPolicy.minLength - 1)">−</button>
                  <input type="number" v-model.number="form.authSession.passwordPolicy.minLength" />
                  <button class="num-btn" @click="form.authSession.passwordPolicy.minLength++">+</button>
                </div>
              </div>
            </div>
            <div class="switch-group">
              <label class="switch-item"><span>Phải có số</span><label class="switch"><input type="checkbox" v-model="form.authSession.passwordPolicy.requireNumbers" /><span class="slider"></span></label></label>
              <label class="switch-item"><span>Phải có ký tự đặc biệt</span><label class="switch"><input type="checkbox" v-model="form.authSession.passwordPolicy.requireSymbols" /><span class="slider"></span></label></label>
            </div>
            <div class="divider"></div>
            <div class="checkbox-group">
              <label class="checkbox-item">
                <input type="checkbox" v-model="form.authSession.singleDeviceOnly" />
                <span class="checkmark"></span>
                <span class="checkbox-label">Giới hạn 1 thiết bị đăng nhập</span>
              </label>
            </div>
          </div>
          <div class="form-card">
            <div class="form-title">💾 Backup</div>
            <div class="input-row">
              <div class="input-group">
                <label>Lịch backup</label>
                <select v-model="form.backup.schedule" class="text-input">
                  <option value="hourly">Hourly</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                </select>
              </div>
              <div class="input-group">
                <label>Retention (ngày)</label>
                <div class="number-input">
                  <button class="num-btn" @click="form.backup.retentionDays = Math.max(1, form.backup.retentionDays - 1)">−</button>
                  <input type="number" v-model.number="form.backup.retentionDays" />
                  <button class="num-btn" @click="form.backup.retentionDays++">+</button>
                </div>
              </div>
            </div>
            <div class="input-row">
              <div class="input-group">
                <label>RPO (phút)</label>
                <div class="number-input">
                  <button class="num-btn" @click="form.backup.rpoMinutes = Math.max(1, form.backup.rpoMinutes - 1)">−</button>
                  <input type="number" v-model.number="form.backup.rpoMinutes" />
                  <button class="num-btn" @click="form.backup.rpoMinutes++">+</button>
                </div>
              </div>
              <div class="input-group">
                <label>RTO (phút)</label>
                <div class="number-input">
                  <button class="num-btn" @click="form.backup.rtoMinutes = Math.max(1, form.backup.rtoMinutes - 1)">−</button>
                  <input type="number" v-model.number="form.backup.rtoMinutes" />
                  <button class="num-btn" @click="form.backup.rtoMinutes++">+</button>
                </div>
              </div>
            </div>
            <div class="switch-group">
              <label class="switch-item"><span>Mã hoá bản sao lưu</span><label class="switch"><input type="checkbox" v-model="form.backup.encrypted" /><span class="slider"></span></label></label>
            </div>
            <div class="btn-group">
              <button class="action-btn secondary" :disabled="creatingBk" @click="createBackup">{{ creatingBk ? 'Đang tạo...' : 'Tạo backup' }}</button>
              <button class="action-btn secondary" @click="openRestore">Phục hồi</button>
            </div>
          </div>
        </div>

        <!-- Integrations Tab -->
        <div v-if="tab === 'integrations'" class="form-grid">
          <div class="form-card">
            <div class="form-title">💳 Cổng thanh toán</div>
            <div class="checkbox-group horizontal">
              <label class="checkbox-item"><input type="checkbox" v-model="form.integrations.payments.momo" /><span class="checkmark"></span><span class="checkbox-label">Momo</span></label>
              <label class="checkbox-item"><input type="checkbox" v-model="form.integrations.payments.vnpay" /><span class="checkmark"></span><span class="checkbox-label">VNPay</span></label>
              <label class="checkbox-item"><input type="checkbox" v-model="form.integrations.payments.qr" /><span class="checkmark"></span><span class="checkbox-label">QR</span></label>
              <label class="checkbox-item"><input type="checkbox" v-model="form.integrations.payments.bank" /><span class="checkmark"></span><span class="checkbox-label">Ngân hàng</span></label>
            </div>
          </div>
          <div class="form-card">
            <div class="form-title">📊 Analytics & Zoom</div>
            <div class="input-group">
              <label>GA4 Measurement ID</label>
              <input v-model="form.integrations.analytics.ga4MeasurementId" class="text-input" />
            </div>
            <div class="switch-group">
              <label class="switch-item"><span>Zoom</span><label class="switch"><input type="checkbox" v-model="form.integrations.zoom.enabled" /><span class="slider"></span></label></label>
            </div>
          </div>
          <div class="form-card full-width">
            <div class="form-title">☁️ Storage</div>
            <div class="input-row">
              <div class="input-group">
                <label>Provider</label>
                <select v-model="form.integrations.storage.provider" class="text-input">
                  <option value="local">Local</option>
                  <option value="s3">S3</option>
                </select>
              </div>
              <div class="input-group">
                <label>Bucket</label>
                <input v-model="form.integrations.storage.bucket" class="text-input" />
              </div>
              <div class="input-group">
                <label>Region</label>
                <input v-model="form.integrations.storage.region" class="text-input" />
              </div>
            </div>
          </div>
        </div>

        <!-- Logging Tab -->
        <div v-if="tab === 'logging'" class="form-grid">
          <div class="form-card">
            <div class="form-title">📝 Cấu hình Log</div>
            <div class="input-group">
              <label>Mức log</label>
              <select v-model="form.logging.level" class="text-input">
                <option value="info">info</option>
                <option value="warn">warn</option>
                <option value="error">error</option>
              </select>
            </div>
            <div class="input-group">
              <label>Retention (ngày)</label>
              <div class="number-input">
                <button class="num-btn" @click="form.logging.retentionDays = Math.max(7, form.logging.retentionDays - 1)">−</button>
                <input type="number" v-model.number="form.logging.retentionDays" />
                <button class="num-btn" @click="form.logging.retentionDays++">+</button>
              </div>
            </div>
            <div class="switch-group">
              <label class="switch-item"><span>Bật Trace ID</span><label class="switch"><input type="checkbox" v-model="form.logging.traceIdEnabled" /><span class="slider"></span></label></label>
            </div>
          </div>
          <div class="form-card">
            <div class="form-title">📜 Lịch sử chỉnh sửa</div>
            <div class="audit-list">
              <div v-for="a in audits" :key="a.version" class="audit-item">
                <span class="audit-version">v{{ a.version }}</span>
                <span class="audit-key">{{ a.key }}</span>
                <span class="audit-actor">{{ a.actor }}</span>
                <span class="audit-time">{{ fmt(a.at) }}</span>
              </div>
              <div v-if="!audits.length" class="empty-state">Chưa có lịch sử</div>
            </div>
          </div>
          <div class="form-card full-width">
            <div class="form-title">💾 Danh sách backup</div>
            <div class="backup-list">
              <div v-for="b in backups" :key="b.id" class="backup-item">
                <div class="backup-info">
                  <span class="backup-id">{{ b.id }}</span>
                  <span class="backup-time">{{ fmt(b.createdAt) }}</span>
                  <span class="backup-size">{{ b.sizeMB }} MB</span>
                </div>
                <button class="action-btn secondary small" @click="restore(b.id)">Phục hồi</button>
              </div>
              <div v-if="!backups.length" class="empty-state">Chưa có backup</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Restore Dialog -->
    <div v-if="restoreDialog" class="modal-overlay" @click.self="restoreDialog = false">
      <div class="modal-content">
        <div class="modal-header">Phục hồi từ backup</div>
        <select v-model="selectedBackup" class="text-input">
          <option v-for="b in backups" :key="b.id" :value="b.id">{{ b.id }} • {{ fmt(b.createdAt) }}</option>
        </select>
        <div class="modal-actions">
          <button class="action-btn secondary" @click="restoreDialog = false">Huỷ</button>
          <button class="action-btn primary" :disabled="!selectedBackup || restoring" @click="doRestore">{{ restoring ? 'Đang phục hồi...' : 'Phục hồi' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { systemService, type SystemConfig, type BackupItem, type ConfigAuditItem } from '@/services/system.service'
import { showToast } from '@/utils/toast'

const tabs = [
  { key: 'brand', label: 'Tổng quan', icon: '🏷️' },
  { key: 'email', label: 'Domain & Email', icon: '📧' },
  { key: 'auth', label: 'Auth & Session', icon: '🔐' },
  { key: 'integrations', label: 'Tích hợp', icon: '🔗' },
  { key: 'logging', label: 'Logging', icon: '📝' },
]

const tab = ref<string>('brand')
const saving = ref(false)
const creatingBk = ref(false)
const restoring = ref(false)
const testingMail = ref(false)

const form = reactive<SystemConfig>({
  brand: { siteName: '', language: 'vi', timezone: 'Asia/Bangkok', currency: 'VND', logoUrl: '' },
  domainEmail: { domain: '', forceHttps: true, hsts: true, smtp: { host: '', port: 587, username: '', passwordMasked: true, senderName: '', fromEmail: '' } },
  authSession: { idleTimeoutMin: 30, maxSessionHours: 24, rememberMeDays: 14, ssoGoogleEnabled: false, googleClientId: '', twoFAEnforce: { admin: true, teacher: false }, passwordPolicy: { minLength: 8, requireNumbers: true, requireSymbols: true }, singleDeviceOnly: true },
  backup: { schedule: 'daily', retentionDays: 30, rpoMinutes: 15, rtoMinutes: 120, encrypted: true },
  maintenance: { enabled: false, window: { dayOfWeek: 0, start: '01:00', end: '03:00' } },
  integrations: { payments: { momo: true, vnpay: true, qr: true, bank: true }, analytics: {}, zoom: { enabled: false }, storage: { provider: 'local' } },
  logging: { level: 'info', retentionDays: 90, traceIdEnabled: true },
  version: 0, updatedBy: '', updatedAt: new Date().toISOString(),
})

const backups = ref<BackupItem[]>([])
const audits = ref<ConfigAuditItem[]>([])
const restoreDialog = ref(false)
const selectedBackup = ref<string | null>(null)
const testMail = ref('')

function fmt(iso?: string) { return iso ? new Date(iso).toLocaleString('vi-VN') : '' }
function badge(s?: string) { return s === 'pass' ? 'success' : s === 'fail' ? 'danger' : 'info' }

async function load() {
  try {
    const [cfg, bks, ads] = await Promise.all([systemService.getConfig(), systemService.listBackups(), systemService.listConfigAudit()])
    Object.assign(form, cfg); backups.value = bks; audits.value = ads
  } catch (e: any) { showToast(e?.message || 'Không tải được cấu hình', 'error') }
}

async function save() {
  saving.value = true
  try { await systemService.updateConfig(form); showToast('Đã lưu nháp', 'success'); await load() }
  catch (e: any) { showToast(e?.message || 'Không thể lưu', 'error') }
  finally { saving.value = false }
}

async function apply() { await save(); showToast('Đã áp dụng cấu hình', 'success') }

async function createBackup() {
  creatingBk.value = true
  try { await systemService.createBackup('manual'); showToast('Đã tạo backup', 'success'); backups.value = await systemService.listBackups() }
  catch (e: any) { showToast(e?.message || 'Không thể tạo backup', 'error') }
  finally { creatingBk.value = false }
}

function openRestore() { selectedBackup.value = backups.value[0]?.id || null; restoreDialog.value = true }

async function doRestore() {
  if (!selectedBackup.value) return
  restoring.value = true
  try { await systemService.restoreBackup(selectedBackup.value); showToast('Đã gửi yêu cầu phục hồi', 'info'); restoreDialog.value = false }
  catch (e: any) { showToast(e?.message || 'Không thể phục hồi', 'error') }
  finally { restoring.value = false }
}

function restore(id: string) { selectedBackup.value = id; restoreDialog.value = true }

async function sendTestMail() {
  if (!testMail.value) { showToast('Nhập email test', 'warning'); return }
  testingMail.value = true
  try { await systemService.sendTestEmail(testMail.value); showToast('Đã gửi email test', 'success') }
  catch (e: any) { showToast(e?.message || 'Không thể gửi email', 'error') }
  finally { testingMail.value = false }
}

onMounted(load)
</script>

<style scoped>
.config { display: flex; flex-direction: column; gap: 24px; padding-bottom: 24px; }

/* Header */
.config-header { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; flex-wrap: wrap; }
.title { font-size: 24px; font-weight: 700; margin: 0; color: var(--el-text-color-primary); }
.subtitle { font-size: 13px; margin: 4px 0 0; color: var(--el-text-color-secondary); }
.header-actions { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }

/* Buttons */
.action-btn { display: flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: 8px; font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.2s; border: none; }
.action-btn.primary { background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white; }
.action-btn.secondary { background: var(--el-bg-color); border: 1px solid var(--el-border-color); color: var(--el-text-color-primary); }
.action-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); }
.action-btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
.action-btn.small { padding: 6px 12px; font-size: 13px; }

/* Section Card */
.section-card { border-radius: 16px; transition: all 0.3s ease; background: var(--el-bg-color); border: 1px solid var(--el-border-color-light); }

/* Tabs */
.tabs-header { display: flex; gap: 4px; padding: 16px 20px; border-bottom: 1px solid var(--el-border-color-light); flex-wrap: wrap; }
.tab-btn { padding: 10px 16px; border-radius: 8px; font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.2s; border: none; background: transparent; color: var(--el-text-color-secondary); }
.tab-btn:hover { background: rgba(99, 102, 241, 0.1); }
.tab-btn.active { background: linear-gradient(135deg, #6366f1, #8b5cf6); color: white; }
.tab-content { padding: 20px; }

/* Form Grid */
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; }
.form-card { padding: 20px; border-radius: 12px; background: var(--el-fill-color-light); border: 1px solid var(--el-border-color-lighter); }
.form-card.full-width { grid-column: 1 / -1; }
.form-title { font-size: 16px; font-weight: 600; margin-bottom: 16px; color: var(--el-text-color-primary); }
.form-subtitle { font-size: 14px; font-weight: 500; margin-bottom: 12px; color: var(--el-text-color-primary); }

/* Input */
.input-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 16px; }
.input-group label { font-size: 13px; font-weight: 500; color: var(--el-text-color-secondary); }
.input-row { display: flex; gap: 16px; flex-wrap: wrap; }
.input-row .input-group { flex: 1; min-width: 140px; }

.text-input { padding: 10px 14px; border-radius: 8px; font-size: 14px; width: 100%; background: var(--el-bg-color); border: 1px solid var(--el-border-color); color: var(--el-text-color-primary); }
.text-input:focus { outline: none; border-color: #6366f1; }
.text-input:disabled { opacity: 0.6; cursor: not-allowed; }
.text-input::placeholder { color: var(--el-text-color-placeholder); }

/* Number Input */
.number-input { display: flex; align-items: center; border-radius: 8px; overflow: hidden; background: var(--el-bg-color); border: 1px solid var(--el-border-color); }
.num-btn { width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: 500; cursor: pointer; border: none; transition: all 0.2s; background: var(--el-fill-color); color: var(--el-text-color-secondary); }
.num-btn:hover { background: #6366f1; color: white; }
.number-input input { flex: 1; text-align: center; border: none; background: transparent; font-size: 14px; font-weight: 600; padding: 8px; -moz-appearance: textfield; appearance: textfield; color: var(--el-text-color-primary); }
.number-input input::-webkit-outer-spin-button, .number-input input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
</style>

<style scoped>
/* Checkbox */
.checkbox-group { display: flex; flex-direction: column; gap: 12px; margin-bottom: 16px; }
.checkbox-group.horizontal { flex-direction: row; flex-wrap: wrap; gap: 16px; }
.checkbox-item { display: flex; align-items: center; gap: 10px; cursor: pointer; }
.checkbox-item input { display: none; }
.checkmark { width: 20px; height: 20px; border-radius: 6px; border: 2px solid var(--el-border-color); background: var(--el-bg-color); display: flex; align-items: center; justify-content: center; transition: all 0.2s; }
.checkbox-item input:checked + .checkmark { background: #6366f1; border-color: #6366f1; }
.checkbox-item input:checked + .checkmark::after { content: '✓'; color: white; font-size: 12px; }
.checkbox-label { font-size: 14px; color: var(--el-text-color-primary); }

/* Switch */
.switch-group { display: flex; gap: 24px; margin-bottom: 16px; flex-wrap: wrap; }
.switch-item { display: flex; align-items: center; gap: 12px; font-size: 14px; color: var(--el-text-color-primary); }
.switch { position: relative; width: 44px; height: 24px; }
.switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; inset: 0; background: var(--el-border-color); border-radius: 24px; transition: 0.3s; }
.slider::before { content: ''; position: absolute; height: 18px; width: 18px; left: 3px; bottom: 3px; background: white; border-radius: 50%; transition: 0.3s; }
.switch input:checked + .slider { background: #6366f1; }
.switch input:checked + .slider::before { transform: translateX(20px); }

/* Status Tags */
.status-tags { display: flex; align-items: center; gap: 8px; font-size: 12px; flex-wrap: wrap; color: var(--el-text-color-secondary); }
.status-tag { padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }
.status-tag.success { background: rgba(34, 197, 94, 0.15); color: #22c55e; }
.status-tag.danger { background: rgba(239, 68, 68, 0.15); color: #ef4444; }
.status-tag.info { background: rgba(99, 102, 241, 0.15); color: #6366f1; }

/* Divider */
.divider { height: 1px; margin: 16px 0; background: var(--el-border-color-light); }

/* Test Row */
.test-row { display: flex; gap: 12px; margin-top: 16px; }
.test-row .text-input { flex: 1; }

/* Password Info */
.password-info { display: flex; align-items: center; gap: 8px; font-size: 12px; margin-top: 8px; color: var(--el-text-color-secondary); }

/* Logo Preview */
.logo-preview { width: 80px; height: 80px; border-radius: 12px; overflow: hidden; margin-bottom: 16px; background: var(--el-fill-color-light); border: 1px solid var(--el-border-color-light); }
.logo-preview img { width: 100%; height: 100%; object-fit: contain; }

/* Button Group */
.btn-group { display: flex; gap: 12px; margin-top: 16px; }

/* Audit List */
.audit-list { display: flex; flex-direction: column; gap: 8px; max-height: 300px; overflow-y: auto; }
.audit-item { display: flex; gap: 12px; padding: 10px; border-radius: 8px; font-size: 13px; background: var(--el-bg-color); }
.audit-version { font-weight: 600; color: #6366f1; }
.audit-key { flex: 1; color: var(--el-text-color-primary); }
.audit-actor, .audit-time { color: var(--el-text-color-secondary); }

/* Backup List */
.backup-list { display: flex; flex-direction: column; gap: 12px; }
.backup-item { display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border-radius: 10px; background: var(--el-bg-color); }
.backup-info { display: flex; gap: 16px; font-size: 13px; }
.backup-id { font-weight: 600; font-family: monospace; color: #6366f1; }
.backup-time, .backup-size { color: var(--el-text-color-secondary); }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal-content { width: 400px; padding: 24px; border-radius: 16px; background: var(--el-bg-color); }
.modal-header { font-size: 18px; font-weight: 600; margin-bottom: 16px; color: var(--el-text-color-primary); }
.modal-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 20px; }

/* Empty State */
.empty-state { text-align: center; padding: 20px; font-size: 14px; color: var(--el-text-color-secondary); }
</style>
