<template>
  <div class="space-y-4">
    <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="text-lg font-semibold">Sức khỏe hệ thống</div>
          <p class="text-xs text-gray-500">Theo dõi CPU/RAM/Disk và biểu đồ Grafana. Tự cập nhật mỗi 5s.</p>
        </div>
        <div class="flex flex-wrap gap-2">
          <el-button type="primary" :disabled="!grafanaLink" @click="openGrafana">
            Mở Grafana
          </el-button>
        </div>
      </div>
    </div>

    <div class="grid gap-4 md:grid-cols-4">
      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="text-xs text-gray-500">CPU hiện tại</div>
        <div class="mt-2 text-2xl font-semibold">{{ fmtPercent(health.cpu.current) }}</div>
        <div class="mt-1 text-xs text-gray-500">p95: {{ fmtPercent(health.cpu.p95) }}</div>
      </div>

      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="text-xs text-gray-500">RAM hiện tại</div>
        <div class="mt-2 text-2xl font-semibold">{{ fmtPercent(health.ram.current) }}</div>
        <div class="mt-1 text-xs text-gray-500">p95: {{ fmtPercent(health.ram.p95) }}</div>
      </div>

      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="text-xs text-gray-500">Disk đang dùng</div>
        <div class="mt-2 text-2xl font-semibold">{{ fmtPercent(health.disk.current) }}</div>
        <div class="mt-1 text-xs text-gray-500">Tổng quan lưu trữ</div>
      </div>

      <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
        <div class="text-xs text-gray-500">Backup gần nhất</div>
        <div class="mt-2 text-base font-semibold">{{ backupTimeLabel }}</div>
        <div class="mt-2">
          <el-tag size="small" :type="backupStatus.type">{{ backupStatus.label }}</el-tag>
        </div>
      </div>
    </div>

    <el-alert
      v-if="!grafanaBase"
      type="warning"
      :closable="false"
      title="Chưa cấu hình Grafana URL"
      description="Thiết lập VITE_GRAFANA_URL để nhúng dashboard Grafana vào trang này."
    />

    <div class="rounded-lg bg-white p-4 ring-1 ring-black/5">
      <div class="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div class="font-medium">Biểu đồ hệ thống</div>
        <a
          v-if="grafanaLink"
          :href="grafanaLink"
          target="_blank"
          rel="noopener"
          class="text-sm text-blue-600 hover:text-blue-700"
        >
          Mở toàn màn
        </a>
      </div>

      <div v-if="grafanaBase" class="grid gap-4 lg:grid-cols-2">
        <div class="h-[260px] overflow-hidden rounded border bg-gray-50">
          <iframe :src="panelUrls.cpu" class="h-full w-full" frameborder="0" allowfullscreen />
        </div>
        <div class="h-[260px] overflow-hidden rounded border bg-gray-50">
          <iframe :src="panelUrls.ram" class="h-full w-full" frameborder="0" allowfullscreen />
        </div>
        <div class="h-[300px] overflow-hidden rounded border bg-gray-50 lg:col-span-2">
          <iframe :src="panelUrls.disk" class="h-full w-full" frameborder="0" allowfullscreen />
        </div>
      </div>
      <div v-else class="text-sm text-gray-500">
        Không có URL Grafana để hiển thị.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { systemService } from '@/services/system.service'
import { showToast } from '@/utils/toast'

const loading = ref(false)
const health = reactive({
  cpu: { current: 0, p95: 0 },
  ram: { current: 0, p95: 0 },
  disk: { current: 0 },
  backup: { status: '', lastBackup: '' },
})

const grafanaBase = (import.meta.env.VITE_GRAFANA_URL ?? (import.meta.env.DEV ? 'http://localhost:3000' : ''))
  .toString()
  .trim()
  .replace(/\/+$/, '')

const grafanaLink = computed(() =>
  grafanaBase ? `${grafanaBase}/d/system-health/system-health?orgId=1` : ''
)
const panelUrls = computed(() => {
  if (!grafanaBase) {
    return { cpu: '', ram: '', disk: '' }
  }
  const base = `${grafanaBase}/d-solo/system-health/system-health?orgId=1&refresh=5s&theme=light`
  return {
    cpu: `${base}&panelId=1`,
    ram: `${base}&panelId=2`,
    disk: `${base}&panelId=3`,
  }
})

const backupStatus = computed(() => {
  switch (health.backup.status) {
    case 'success':
      return { label: 'Thành công', type: 'success' as const }
    case 'no_backup':
      return { label: 'Chưa backup', type: 'info' as const }
    case 'failed':
      return { label: 'Lỗi', type: 'danger' as const }
    default:
      return { label: 'Không rõ', type: 'warning' as const }
  }
})

const backupTimeLabel = computed(() => {
  if (!health.backup.lastBackup) return 'Chưa có'
  const date = new Date(health.backup.lastBackup)
  if (Number.isNaN(date.getTime())) return health.backup.lastBackup
  return date.toLocaleString('vi-VN', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
})

function fmtPercent(value: number) {
  if (Number.isNaN(value) || !Number.isFinite(value)) return '--'
  return `${value.toFixed(1)}%`
}

async function loadHealth() {
  if (loading.value) return
  loading.value = true
  try {
    const data = await systemService.getHealth()
    health.cpu.current = data.cpu.current
    health.cpu.p95 = data.cpu.p95
    health.ram.current = data.ram.current
    health.ram.p95 = data.ram.p95
    health.disk.current = data.disk.current
    health.backup.status = data.backup.status
    health.backup.lastBackup = data.backup.lastBackup
  } catch (error: any) {
    showToast(error?.message || 'Không tải được sức khỏe hệ thống', 'error')
  } finally {
    loading.value = false
  }
}

function openGrafana() {
  if (!grafanaLink.value) return
  window.open(grafanaLink.value, '_blank', 'noopener')
}

let refreshTimer: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  loadHealth()
  refreshTimer = setInterval(() => {
    loadHealth()
  }, 5000)
})

onBeforeUnmount(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
})
</script>
