<template>
  <el-dialog
    :model-value="open"
    @update:model-value="$emit('update:open', $event)"
    title="Cài đặt AI (Ẩn)"
    width="480px"
    :close-on-click-modal="false"
    custom-class="ai-settings-dialog"
  >
    <div class="ai-settings-content">
      <!-- Warning Note -->
      <div class="warning-note">
        <svg class="warning-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>Giữ avatar 5 giây để mở cài đặt này</span>
      </div>

      <!-- AI Toggle -->
      <div class="setting-item">
        <div class="setting-label">
          <span class="label-text">Bật/Tắt AI</span>
          <span class="label-desc">Kích hoạt tính năng AI trong hệ thống</span>
        </div>
        <el-switch v-model="settings.aiEnabled" />
      </div>

      <!-- OpenRouter API Key -->
      <div class="setting-item">
        <div class="setting-label">
          <span class="label-text">OPENROUTER_API_KEY</span>
          <span class="label-desc">API key cho OpenRouter</span>
        </div>
        <el-input
          v-model="settings.openrouterApiKey"
          :type="showOpenrouterKey ? 'text' : 'password'"
          placeholder="Nhập API key..."
          class="api-key-input"
        >
          <template #suffix>
            <button class="toggle-visibility" @click="showOpenrouterKey = !showOpenrouterKey">
              <svg v-if="showOpenrouterKey" class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
              <svg v-else class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
          </template>
        </el-input>
      </div>

      <!-- DeepSeek API Key -->
      <div class="setting-item">
        <div class="setting-label">
          <span class="label-text">DEEPSEEK_API_KEY</span>
          <span class="label-desc">API key cho DeepSeek</span>
        </div>
        <el-input
          v-model="settings.deepseekApiKey"
          :type="showDeepseekKey ? 'text' : 'password'"
          placeholder="Nhập API key..."
          class="api-key-input"
        >
          <template #suffix>
            <button class="toggle-visibility" @click="showDeepseekKey = !showDeepseekKey">
              <svg v-if="showDeepseekKey" class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
              <svg v-else class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
          </template>
        </el-input>
      </div>

      <!-- Default Model -->
      <div class="setting-item">
        <div class="setting-label">
          <span class="label-text">Model mặc định</span>
          <span class="label-desc">Chọn model AI sử dụng</span>
        </div>
        <el-select v-model="settings.defaultModel" placeholder="Chọn model" class="model-select">
          <el-option label="GPT-4o" value="openai/gpt-4o" />
          <el-option label="GPT-4o Mini" value="openai/gpt-4o-mini" />
          <el-option label="DeepSeek Chat V3" value="deepseek/deepseek-chat-v3-0324" />
        </el-select>
      </div>
    </div>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="$emit('update:open', false)">Hủy</el-button>
        <el-button type="primary" @click="saveSettings" :loading="saving">
          Lưu cài đặt
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  open: boolean
}>()

const emit = defineEmits<{
  'update:open': [value: boolean]
}>()

const saving = ref(false)
const showOpenrouterKey = ref(false)
const showDeepseekKey = ref(false)

const settings = reactive({
  aiEnabled: false,
  openrouterApiKey: '',
  deepseekApiKey: '',
  defaultModel: 'openai/gpt-4o'
})

// Load settings from localStorage when dialog opens
watch(() => props.open, (isOpen) => {
  if (isOpen) {
    loadSettings()
  }
})

function loadSettings() {
  try {
    const saved = localStorage.getItem('ai_settings')
    if (saved) {
      const parsed = JSON.parse(saved)
      settings.aiEnabled = parsed.aiEnabled ?? false
      settings.openrouterApiKey = parsed.openrouterApiKey ?? ''
      settings.deepseekApiKey = parsed.deepseekApiKey ?? ''
      settings.defaultModel = parsed.defaultModel ?? 'openai/gpt-4o'
    }
  } catch (e) {
    console.error('Failed to load AI settings:', e)
  }
}

async function saveSettings() {
  saving.value = true
  try {
    // Save to localStorage
    localStorage.setItem('ai_settings', JSON.stringify({
      aiEnabled: settings.aiEnabled,
      openrouterApiKey: settings.openrouterApiKey,
      deepseekApiKey: settings.deepseekApiKey,
      defaultModel: settings.defaultModel
    }))
    
    ElMessage.success('Đã lưu cài đặt AI')
    emit('update:open', false)
  } catch (e) {
    console.error('Failed to save AI settings:', e)
    ElMessage.error('Lưu cài đặt thất bại')
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.ai-settings-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.warning-note {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 13px;
}

.warning-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.setting-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.setting-label {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.label-text {
  font-size: 14px;
  font-weight: 600;
}

.label-desc {
  font-size: 12px;
}

.api-key-input {
  width: 100%;
}

.toggle-visibility {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  cursor: pointer;
  background: transparent;
  border: none;
}

.eye-icon {
  width: 18px;
  height: 18px;
}

.model-select {
  width: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>

<!-- Global styles for dark mode -->
<style>
/* Light mode */
.ai-settings-dialog .warning-note {
  background: #fef3c7;
  color: #92400e;
}

.ai-settings-dialog .warning-icon {
  color: #f59e0b;
}

.ai-settings-dialog .label-text {
  color: #1e293b;
}

.ai-settings-dialog .label-desc {
  color: #64748b;
}

.ai-settings-dialog .toggle-visibility {
  color: #64748b;
}

.ai-settings-dialog .toggle-visibility:hover {
  color: #1e293b;
}

/* Dark mode */
html.dark .ai-settings-dialog {
  background: #1e293b !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

html.dark .ai-settings-dialog .el-dialog__header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
}

html.dark .ai-settings-dialog .el-dialog__title {
  color: #fff !important;
}

html.dark .ai-settings-dialog .el-dialog__body {
  color: #e2e8f0 !important;
}

html.dark .ai-settings-dialog .el-dialog__footer {
  border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
}

html.dark .ai-settings-dialog .warning-note {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

html.dark .ai-settings-dialog .warning-icon {
  color: #fbbf24;
}

html.dark .ai-settings-dialog .label-text {
  color: #e2e8f0;
}

html.dark .ai-settings-dialog .label-desc {
  color: #94a3b8;
}

html.dark .ai-settings-dialog .toggle-visibility {
  color: #94a3b8;
}

html.dark .ai-settings-dialog .toggle-visibility:hover {
  color: #e2e8f0;
}
</style>
