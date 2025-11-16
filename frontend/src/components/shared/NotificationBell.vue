<!-- src/components/shared/NotificationBell.vue -->
<template>
  <div class="relative" ref="notificationRef">
    <!-- Bell Button -->
    <button
      @click="toggleDropdown"
      class="relative rounded-lg p-2 text-slate-600 hover:bg-slate-100 transition focus:outline-none focus:ring-2 focus:ring-slate-200"
      aria-label="Thông báo"
    >
      <!-- Bell Icon -->
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-5 w-5"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
        stroke-width="2"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 10-12 0v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
        />
      </svg>

      <!-- Badge -->
      <span v-if="unreadCount > 0" class="absolute top-1 right-1 flex items-center justify-center">
        <span class="h-2 w-2 rounded-full bg-red-500 border border-white"></span>
      </span>
    </button>

    <!-- Dropdown Notification Panel -->
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isOpen"
        class="absolute left-1/2 z-50 mt-2 w-[min(20rem,calc(100vw-2rem))] -translate-x-1/2 rounded-lg border border-slate-200 bg-white shadow-lg overflow-hidden sm:left-auto sm:right-0 sm:w-96 sm:translate-x-0"
      >
        <!-- Header -->
        <div class="px-4 py-3 bg-slate-50 border-b border-slate-200">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-semibold text-slate-900">Thông báo {{ roleLabel }}</h3>
            <span
              v-if="unreadCount > 0"
              class="px-2 py-1 text-xs font-medium text-slate-700 bg-slate-200 rounded-full"
            >
              {{ unreadCount }} mới
            </span>
          </div>
        </div>

        <!-- Notification List -->
        <div class="max-h-80 overflow-y-auto">
          <!-- Loading State -->
          <div v-if="loading" class="flex items-center justify-center py-8">
            <div class="h-6 w-6 border-2 border-slate-300 border-t-slate-900 rounded-full animate-spin"></div>
          </div>

          <!-- Empty State -->
          <div
            v-else-if="displayedNotifications.length === 0"
            class="px-4 py-8 text-center text-slate-500"
          >
            <svg
              class="mx-auto h-12 w-12 text-slate-400 mb-2"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
              />
            </svg>
            <p class="text-sm">Không có thông báo nào</p>
          </div>

          <!-- Notification Items -->
          <div v-else class="divide-y divide-slate-100">
            <div
              v-for="notification in displayedNotifications"
              :key="notification.id"
              @click="handleNotificationClick(notification)"
              class="px-4 py-3 hover:bg-slate-50 transition-colors cursor-pointer"
              :class="{ 'bg-blue-50/50': !notification.is_read }"
            >
              <div class="flex gap-3">
                <!-- Icon -->
                <div
                  class="w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0"
                  :class="getNotificationIconClass(notification.type)"
                >
                  <svg
                    class="w-5 h-5"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      :d="getNotificationIconPath(notification.type)"
                    />
                  </svg>
                </div>

                <!-- Content -->
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-slate-900 line-clamp-2">
                    {{ notification.title }}
                  </p>
                  <p class="text-xs text-slate-600 mt-0.5 line-clamp-2">
                    {{ notification.message }}
                  </p>
                  <p class="text-xs text-slate-500 mt-1">
                    {{ formatTime(notification.created_at) }}
                  </p>
                </div>

                <!-- Unread Indicator -->
                <div v-if="!notification.is_read" class="flex-shrink-0">
                  <span class="block w-2 h-2 rounded-full bg-blue-600"></span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div
          v-if="displayedNotifications.length > 0"
          class="px-4 py-3 bg-slate-50 border-t border-slate-200"
        >
          <button
            v-if="hasUnread"
            @click="markAllAsRead"
            class="w-full px-3 py-2 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition"
          >
            Đánh dấu tất cả đã đọc
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { onClickOutside } from '@vueuse/core'

// ===== TYPES =====
interface Notification {
  id: string | number
  title: string
  message: string
  type: 'info' | 'success' | 'warning' | 'error'
  is_read: boolean
  created_at: string
  category?: string
}

interface Props {
  userId?: number | string
  role?: 'student' | 'teacher' | 'admin'
}

// ===== PROPS =====
const props = withDefaults(defineProps<Props>(), {
  role: 'student',
})

// ===== STATE =====
const isOpen = ref(false)
const loading = ref(false)
const notifications = ref<Notification[]>([])
const notificationRef = ref<HTMLElement | null>(null)
const maxNotifications = 20

// ===== COMPUTED =====
const displayedNotifications = computed(() => {
  const sorted = [...notifications.value].sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
  )
  return sorted.slice(0, maxNotifications)
})

const unreadCount = computed(() => displayedNotifications.value.filter((n) => !n.is_read).length)

const hasUnread = computed(() => unreadCount.value > 0)

const roleLabel = computed(() => {
  const labels = {
    student: '',
    teacher: '',
    admin: '(Admin)',
  }
  return labels[props.role] || ''
})

const apiEndpoint = computed(() => {
  const endpoints = {
    student: '/api/student/notifications',
    teacher: '/api/teacher/notifications',
    admin: '/api/admin/notifications',
  }
  return endpoints[props.role] || '/api/notifications'
})

// ===== METHODS =====
function toggleDropdown() {
  isOpen.value = !isOpen.value
  if (isOpen.value && notifications.value.length === 0) {
    fetchNotifications()
  }
}

async function fetchNotifications() {
  loading.value = true
  try {
    // Use axios instead of fetch for consistency
    const api = (await import('@/config/axios')).default
    const response = await api.get(apiEndpoint.value, {
      params: { limit: maxNotifications * 2 }
    })
    
    // Backend returns { notifications: [...] }
    const data = response.data || {}
    notifications.value = data.notifications || []
  } catch (error) {
    console.error('Failed to fetch notifications:', error)
    // Only use mock if API completely fails
    notifications.value = []
  } finally {
    loading.value = false
  }
}

function getMockNotificationsByRole(): Notification[] {
  const generateNotifications = (baseId: number, count: number): Notification[] => {
    return Array.from({ length: count }, (_, i) => ({
      id: baseId + i,
      title: 'demo',
      message: 'demo',
      type: ['info', 'success', 'warning', 'error'][i % 4] as any,
      is_read: i % 3 === 0,
      created_at: new Date(Date.now() - i * 3600000).toISOString(),
    }))
  }

  const mockData = {
    student: [
      {
        id: 1,
        title: 'demo',
        message: 'demo',
        type: 'info' as const,
        is_read: false,
        created_at: new Date(Date.now() - 3600000).toISOString(),
      },
      {
        id: 2,
        title: 'demo',
        message: 'demo',
        type: 'success' as const,
        is_read: false,
        created_at: new Date(Date.now() - 7200000).toISOString(),
      },
      {
        id: 3,
        title: 'demo',
        message: 'demo',
        type: 'info' as const,
        is_read: true,
        created_at: new Date(Date.now() - 86400000).toISOString(),
      },
      {
        id: 4,
        title: 'demo',
        message: 'demo',
        type: 'warning' as const,
        is_read: true,
        created_at: new Date(Date.now() - 172800000).toISOString(),
      },
      ...generateNotifications(5, 8),
    ],
    teacher: [
      {
        id: 101,
        title: 'demo',
        message: 'demo',
        type: 'info' as const,
        is_read: false,
        created_at: new Date(Date.now() - 1800000).toISOString(),
      },
      {
        id: 102,
        title: 'demo',
        message: 'demo',
        type: 'warning' as const,
        is_read: false,
        created_at: new Date(Date.now() - 5400000).toISOString(),
      },
      {
        id: 103,
        title: 'demo',
        message: 'demo',
        type: 'success' as const,
        is_read: true,
        created_at: new Date(Date.now() - 86400000).toISOString(),
      },
      ...generateNotifications(104, 12),
    ],
    admin: [
      {
        id: 201,
        title: 'demo',
        message: 'demo',
        type: 'info' as const,
        is_read: false,
        created_at: new Date(Date.now() - 3600000).toISOString(),
      },
      {
        id: 202,
        title: 'demo',
        message: 'demo',
        type: 'error' as const,
        is_read: false,
        created_at: new Date(Date.now() - 1800000).toISOString(),
      },
      {
        id: 203,
        title: 'demo',
        message: 'demo',
        type: 'success' as const,
        is_read: true,
        created_at: new Date(Date.now() - 86400000).toISOString(),
      },
      ...generateNotifications(204, 10),
    ],
  }

  return mockData[props.role] || []
}

async function handleNotificationClick(notification: Notification) {
  if (!notification.is_read) {
    await markAsRead(notification.id)
  }
}

async function markAsRead(notificationId: number | string) {
  try {
    const api = (await import('@/config/axios')).default
    await api.patch(`${apiEndpoint.value}/${notificationId}/read/`)
    
    const notification = notifications.value.find((n) => String(n.id) === String(notificationId))
    if (notification) {
      notification.is_read = true
    }
  } catch (error) {
    console.error('Failed to mark as read:', error)
  }
}

async function markAllAsRead() {
  try {
    const api = (await import('@/config/axios')).default
    await api.patch(`${apiEndpoint.value}/read-all/`)
    
    displayedNotifications.value.forEach((n) => (n.is_read = true))
  } catch (error) {
    console.error('Failed to mark all as read:', error)
  }
}

function formatTime(dateString: string): string {
  try {
    const date = new Date(dateString)
    const now = new Date()
    const diff = now.getTime() - date.getTime()
    const minutes = Math.floor(diff / 60000)
    const hours = Math.floor(minutes / 60)
    const days = Math.floor(hours / 24)
    const weeks = Math.floor(days / 7)
    const months = Math.floor(days / 30)

    if (minutes < 1) return 'Vừa xong'
    if (minutes < 60) return `${minutes} phút trước`
    if (hours < 24) return `${hours} giờ trước`
    if (days < 7) return `${days} ngày trước`
    if (weeks < 4) return `${weeks} tuần trước`
    if (months < 12) return `${months} tháng trước`

    return date.toLocaleDateString('vi-VN', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    })
  } catch {
    return dateString
  }
}

function getNotificationIconClass(type: string): string {
  const classes = {
    info: 'bg-blue-100 text-blue-600',
    success: 'bg-green-100 text-green-600',
    warning: 'bg-amber-100 text-amber-600',
    error: 'bg-red-100 text-red-600',
  }
  return classes[type as keyof typeof classes] || classes.info
}

function getNotificationIconPath(type: string): string {
  const paths = {
    info: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    success: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
    warning:
      'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z',
    error: 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z',
  }
  return paths[type as keyof typeof paths] || paths.info
}

onClickOutside(notificationRef, () => {
  isOpen.value = false
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
