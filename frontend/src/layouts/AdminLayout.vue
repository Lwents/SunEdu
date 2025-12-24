<template>
  <div class="admin-layout" :class="isDark ? 'dark' : 'light'">
    <!-- Sidebar -->
    <aside class="sidebar" :class="{ collapsed: isCollapsed, 'mobile-open': isMobileOpen }">
      <!-- Logo -->
      <div class="sidebar-header">
        <RouterLink v-if="!isCollapsed" to="/admin/dashboard" class="logo-link">
          <LogoSunnyEdu :size="55" />
        </RouterLink>
        <button class="collapse-btn desktop-only" @click="isCollapsed = !isCollapsed">
          <svg class="w-5 h-5" :class="{ rotated: isCollapsed }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
          </svg>
        </button>
        <button class="close-btn mobile-only" @click="isMobileOpen = false">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Navigation -->
      <nav class="sidebar-nav">
        <template v-for="(group, gi) in navGroups" :key="gi">
          <div v-if="!isCollapsed" class="nav-group-label">{{ group.label }}</div>
          <div v-else class="nav-divider"></div>
          <ul class="nav-list">
            <li v-for="item in group.items" :key="item.to">
              <RouterLink :to="item.to" v-slot="{ isActive }" class="nav-link">
                <div class="nav-item" :class="{ active: isActive }" :title="isCollapsed ? item.label : ''">
                  <component :is="item.icon" class="nav-icon" />
                  <span v-if="!isCollapsed" class="nav-text">{{ item.label }}</span>
                </div>
              </RouterLink>
            </li>
          </ul>
        </template>
      </nav>

    </aside>

    <!-- Mobile Overlay -->
    <div v-if="isMobileOpen" class="mobile-overlay" @click="isMobileOpen = false"></div>

    <!-- Main Content -->
    <div class="main-wrapper">
      <!-- Top Header -->
      <header class="top-header">
        <div class="header-left">
          <button class="menu-btn mobile-only" @click="isMobileOpen = true">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <div class="breadcrumb">
            <span class="breadcrumb-icon">📊</span>
            <h1 class="page-title">{{ pageTitle }}</h1>
          </div>
        </div>
        
        <div class="header-right">
          <!-- Theme Toggle Switch -->
          <button class="theme-switch" @click="toggleTheme" :title="isDark ? 'Chế độ sáng' : 'Chế độ tối'">
            <div class="switch-track">
              <svg class="switch-icon sun" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 7a5 5 0 100 10 5 5 0 000-10zM12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
              </svg>
              <svg class="switch-icon moon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/>
              </svg>
              <div class="switch-thumb" :class="{ active: isDark }"></div>
            </div>
          </button>
          
          <NotificationBell :user-id="auth.user?.id" role="admin" />
          
          <div class="user-dropdown" @click="showUserMenu = !showUserMenu">
            <img 
              class="user-avatar" 
              :src="avatarSrc" 
              alt="avatar" 
              @error="handleAvatarError"
              @mousedown="startLongPress"
              @mouseup="cancelLongPress"
              @mouseleave="cancelLongPress"
              @touchstart.prevent="startLongPress"
              @touchend="cancelLongPress"
              @touchcancel="cancelLongPress"
            />
            <div class="user-info desktop-only">
              <span class="user-name">{{ user?.name || 'Admin' }}</span>
              <span class="user-role">Quản trị viên</span>
            </div>
            <svg class="w-4 h-4 desktop-only" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
            
            <!-- Dropdown Menu -->
            <div v-if="showUserMenu" class="dropdown-menu">
              <div class="dropdown-header">
                <img class="dropdown-avatar" :src="avatarSrc" alt="avatar" />
                <div>
                  <div class="dropdown-name">{{ user?.name || 'Admin' }}</div>
                  <div class="dropdown-email">{{ user?.email }}</div>
                </div>
              </div>
              <div class="dropdown-divider"></div>
              <button class="dropdown-item" @click="showConfirm = true">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
                Đăng xuất
              </button>
            </div>
          </div>
        </div>
      </header>

      <!-- Content Area -->
      <main class="content-area">
        <router-view />
      </main>
    </div>

    <ConfirmLogout :open="showConfirm" @update:open="showConfirm = $event" @confirm="handleLogout" />
    
    <!-- AI Settings Dialog (Hidden) -->
    <AISettingsDialog v-model:open="showAISettings" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth.store'
import { useThemeStore } from '@/store/theme.store'
import LogoSunnyEdu from '@/components/ui/LogoSunnyEdu.vue'
import NotificationBell from '@/components/shared/NotificationBell.vue'
import ConfirmLogout from '@/components/ui/ConfirmLogout.vue'
import AISettingsDialog from '@/components/admin/AISettingsDialog.vue'
import { getAvatarSrc } from '@/utils/avatar'
import {
  LayoutDashboard,
  Users,
  BookOpen,
  CreditCard,
  BarChart3,
  ShieldCheck,
  FileText,
  History,
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const themeStore = useThemeStore()

const isDark = computed(() => themeStore.isDark)
const user = computed(() => auth.user)

const isCollapsed = ref(false)
const isMobileOpen = ref(false)
const showUserMenu = ref(false)
const showConfirm = ref(false)
const showAISettings = ref(false)

// Long press for AI Settings (5 seconds)
let longPressTimer: ReturnType<typeof setTimeout> | null = null
const LONG_PRESS_DURATION = 5000 // 5 seconds

function startLongPress() {
  cancelLongPress()
  longPressTimer = setTimeout(() => {
    showAISettings.value = true
    showUserMenu.value = false
  }, LONG_PRESS_DURATION)
}

function cancelLongPress() {
  if (longPressTimer) {
    clearTimeout(longPressTimer)
    longPressTimer = null
  }
}

onUnmounted(() => {
  cancelLongPress()
})

const toggleTheme = () => themeStore.toggleTheme()

const avatarSrc = computed(() => {
  return getAvatarSrc(
    auth.user?.avatar,
    auth.user?.gender as 'male' | 'female' | 'other' | null | undefined,
    'admin'
  )
})

const pageTitle = computed(() => {
  const matched = [...route.matched].reverse().find((r) => r.meta?.title) as any
  const raw = matched?.meta?.title
  const title = typeof raw === 'function' ? raw(route) : raw
  return title || 'Dashboard'
})

type NavItem = { to: string; label: string; icon: any }
type NavGroup = { label: string; items: NavItem[] }

const navGroups: NavGroup[] = [
  {
    label: 'Tổng quan',
    items: [{ to: '/admin/dashboard', label: 'Dashboard', icon: LayoutDashboard }],
  },
  {
    label: 'Quản trị',
    items: [
      { to: '/admin/users', label: 'Người dùng', icon: Users },
      { to: '/admin/courses', label: 'Khóa học', icon: BookOpen },
      { to: '/admin/transactions', label: 'Giao dịch', icon: CreditCard },
    ],
  },
  {
    label: 'Báo cáo',
    items: [
      { to: '/admin/reports/revenue', label: 'Doanh thu', icon: BarChart3 },
      { to: '/admin/reports/users', label: 'Người dùng', icon: FileText },
      { to: '/admin/reports/learning', label: 'Học tập', icon: FileText },
      { to: '/admin/reports/content', label: 'Nội dung', icon: FileText },
    ],
  },
  {
    label: 'Hệ thống',
    items: [
      { to: '/admin/system', label: 'Cấu hình', icon: ShieldCheck },
      { to: '/admin/system/security', label: 'Bảo mật', icon: ShieldCheck },
      { to: '/admin/system/activity', label: 'Log hoạt động', icon: History },
    ],
  },
]

function handleAvatarError(event: Event) {
  const img = event.target as HTMLImageElement
  img.src = getAvatarSrc(null, auth.user?.gender as 'male' | 'female' | 'other' | null | undefined, 'admin')
}

async function handleLogout() {
  try {
    if (typeof auth.logout === 'function') {
      await auth.logout()
    }
    await router.push('/auth/login')
  } catch {
    await router.push('/auth/login')
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  transition: background-color 0.3s ease;
}

.admin-layout.dark { background: #0f172a; }
.admin-layout.light { background: #f1f5f9; }

/* Sidebar */
.sidebar {
  width: 260px;
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  z-index: 100;
  flex-shrink: 0;
}

.sidebar.collapsed { width: 72px; }

.admin-layout.dark .sidebar {
  background: rgba(15, 23, 42, 0.98);
  border-right: 1px solid rgba(255, 255, 255, 0.06);
}

.admin-layout.light .sidebar {
  background: #ffffff;
  border-right: 1px solid #e2e8f0;
}

/* Mobile Sidebar */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    transform: translateX(-100%);
    width: 280px;
    box-shadow: 4px 0 20px rgba(0, 0, 0, 0.3);
  }
  
  .sidebar.mobile-open {
    transform: translateX(0);
  }
  
  .sidebar.collapsed {
    width: 280px;
  }
}

.mobile-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 99;
}

@media (min-width: 769px) {
  .mobile-overlay { display: none; }
}

/* Sidebar Header */
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  height: 70px;
  border-bottom: 1px solid;
}

.admin-layout.dark .sidebar-header { border-color: rgba(255, 255, 255, 0.06); }
.admin-layout.light .sidebar-header { border-color: #e2e8f0; }

.logo-link {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s;
}

.admin-layout.dark .logo-icon { 
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(139, 92, 246, 0.2));
  color: #22d3ee;
}
.admin-layout.dark .logo-icon:hover { 
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.3), rgba(139, 92, 246, 0.3));
}
.admin-layout.light .logo-icon { 
  background: #eff6ff;
  color: #2563eb;
}
.admin-layout.light .logo-icon:hover { 
  background: #dbeafe;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
}

.admin-layout.dark .logo-text { color: white; }
.admin-layout.light .logo-text { color: #1e293b; }

.collapse-btn, .close-btn {
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s;
}

.admin-layout.dark .collapse-btn, .admin-layout.dark .close-btn { color: #64748b; }
.admin-layout.dark .collapse-btn:hover, .admin-layout.dark .close-btn:hover { background: rgba(255, 255, 255, 0.1); color: white; }
.admin-layout.light .collapse-btn, .admin-layout.light .close-btn { color: #94a3b8; }
.admin-layout.light .collapse-btn:hover, .admin-layout.light .close-btn:hover { background: #f1f5f9; color: #1e293b; }

.collapse-btn svg { transition: transform 0.3s ease; }
.collapse-btn svg.rotated { transform: rotate(180deg); }

.desktop-only { display: flex; }
.mobile-only { display: none; }

@media (max-width: 768px) {
  .desktop-only { display: none; }
  .mobile-only { display: flex; }
}

/* Sidebar Nav */
.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 12px 8px;
}

.nav-group-label {
  padding: 12px 12px 8px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.admin-layout.dark .nav-group-label { color: #475569; }
.admin-layout.light .nav-group-label { color: #94a3b8; }

.nav-divider {
  height: 1px;
  margin: 8px 12px;
}

.admin-layout.dark .nav-divider { background: rgba(255, 255, 255, 0.06); }
.admin-layout.light .nav-divider { background: #e2e8f0; }

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0 0 8px;
}

.nav-link { text-decoration: none; display: block; }

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 14px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
}

.sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 12px;
}

.admin-layout.dark .nav-item { color: #94a3b8; }
.admin-layout.dark .nav-item:hover { background: rgba(255, 255, 255, 0.05); color: white; }
.admin-layout.dark .nav-item.active {
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(139, 92, 246, 0.15));
  color: #22d3ee;
}

.admin-layout.light .nav-item { color: #64748b; }
.admin-layout.light .nav-item:hover { background: #f8fafc; color: #1e293b; }
.admin-layout.light .nav-item.active {
  background: #eff6ff;
  color: #2563eb;
}

.nav-icon { width: 20px; height: 20px; flex-shrink: 0; }
.nav-text { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* Main Wrapper */
.main-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow: hidden;
}

/* Top Header */
.top-header {
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  flex-shrink: 0;
}

.admin-layout.dark .top-header {
  background: rgba(15, 23, 42, 0.8);
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.admin-layout.light .top-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.menu-btn {
  padding: 8px;
  border-radius: 8px;
}

.admin-layout.dark .menu-btn { color: #94a3b8; }
.admin-layout.dark .menu-btn:hover { background: rgba(255, 255, 255, 0.1); }
.admin-layout.light .menu-btn { color: #64748b; }
.admin-layout.light .menu-btn:hover { background: #f1f5f9; }

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 10px;
}

.breadcrumb-icon { font-size: 20px; }

.page-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.admin-layout.dark .page-title { color: white; }
.admin-layout.light .page-title { color: #1e293b; }

/* Header Right */
.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* Theme Switch */
.theme-switch {
  padding: 4px;
  border-radius: 20px;
  cursor: pointer;
  background: transparent;
  border: none;
}

.switch-track {
  width: 52px;
  height: 28px;
  border-radius: 14px;
  position: relative;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 6px;
}

.admin-layout.dark .switch-track {
  background: linear-gradient(135deg, #1e3a5f, #0f172a);
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.4);
}

.admin-layout.light .switch-track {
  background: linear-gradient(135deg, #87ceeb, #60a5fa);
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.switch-icon {
  width: 14px;
  height: 14px;
  z-index: 1;
  transition: all 0.3s;
}

.switch-icon.sun {
  color: #fbbf24;
}

.admin-layout.dark .switch-icon.sun {
  opacity: 0.4;
}

.admin-layout.light .switch-icon.sun {
  opacity: 1;
}

.switch-icon.moon {
  color: #e2e8f0;
}

.admin-layout.dark .switch-icon.moon {
  opacity: 1;
}

.admin-layout.light .switch-icon.moon {
  opacity: 0.4;
}

.switch-thumb {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  position: absolute;
  top: 3px;
  left: 3px;
  transition: all 0.3s cubic-bezier(0.68, -0.15, 0.27, 1.15);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.admin-layout.light .switch-thumb {
  background: linear-gradient(135deg, #fff, #fef3c7);
}

.admin-layout.dark .switch-thumb {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
}

.switch-thumb.active {
  left: 27px;
}

/* User Dropdown */
.user-dropdown {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 12px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}

.admin-layout.dark .user-dropdown:hover { background: rgba(255, 255, 255, 0.05); }
.admin-layout.light .user-dropdown:hover { background: #f8fafc; }

.user-avatar {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  object-fit: cover;
}

.admin-layout.dark .user-avatar { border: 2px solid rgba(255, 255, 255, 0.1); }
.admin-layout.light .user-avatar { border: 2px solid #e2e8f0; }

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  line-height: 1.2;
}

.admin-layout.dark .user-name { color: white; }
.admin-layout.light .user-name { color: #1e293b; }

.user-role {
  font-size: 12px;
  line-height: 1.2;
}

.admin-layout.dark .user-role { color: #64748b; }
.admin-layout.light .user-role { color: #94a3b8; }

.admin-layout.dark .user-dropdown svg { color: #64748b; }
.admin-layout.light .user-dropdown svg { color: #94a3b8; }

/* Dropdown Menu */
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  width: 240px;
  border-radius: 12px;
  overflow: hidden;
  z-index: 200;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-8px); }
  to { opacity: 1; transform: translateY(0); }
}

.admin-layout.dark .dropdown-menu {
  background: #1e293b;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
}

.admin-layout.light .dropdown-menu {
  background: white;
  border: 1px solid #e2e8f0;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
}

.dropdown-avatar {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  object-fit: cover;
}

.dropdown-name {
  font-size: 14px;
  font-weight: 600;
}

.admin-layout.dark .dropdown-name { color: white; }
.admin-layout.light .dropdown-name { color: #1e293b; }

.dropdown-email {
  font-size: 12px;
  margin-top: 2px;
}

.admin-layout.dark .dropdown-email { color: #64748b; }
.admin-layout.light .dropdown-email { color: #94a3b8; }

.dropdown-divider {
  height: 1px;
  margin: 0 12px;
}

.admin-layout.dark .dropdown-divider { background: rgba(255, 255, 255, 0.08); }
.admin-layout.light .dropdown-divider { background: #e2e8f0; }

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 12px 16px;
  font-size: 14px;
  transition: all 0.2s;
  color: #ef4444;
}

.dropdown-item:hover {
  background: rgba(239, 68, 68, 0.1);
}

/* Content Area */
.content-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

@media (max-width: 640px) {
  .content-area { padding: 16px; }
  .top-header { padding: 0 16px; }
}

/* ============================================== */
/* Global Admin Dark Mode Overrides              */
/* ============================================== */

/* Text colors */
.admin-layout.dark .content-area {
  color: #e2e8f0;
}

.admin-layout.dark .text-gray-800,
.admin-layout.dark .text-gray-700 {
  color: #e2e8f0 !important;
}

.admin-layout.dark .text-gray-600 {
  color: #94a3b8 !important;
}

.admin-layout.dark .text-gray-500,
.admin-layout.dark .text-gray-400 {
  color: #64748b !important;
}

/* Background overrides */
.admin-layout.dark .bg-white {
  background: rgba(30, 41, 59, 0.8) !important;
  border-color: rgba(255, 255, 255, 0.08) !important;
}

.admin-layout.dark .bg-gray-50,
.admin-layout.dark .bg-gray-100 {
  background: rgba(255, 255, 255, 0.03) !important;
}

.admin-layout.dark .ring-black\/5 {
  --tw-ring-color: rgba(255, 255, 255, 0.08) !important;
}

/* Element Plus - Input */
.admin-layout.dark :deep(.el-input__wrapper),
.admin-layout.dark :deep(.el-textarea__inner) {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  box-shadow: none !important;
}

.admin-layout.dark :deep(.el-input__inner),
.admin-layout.dark :deep(.el-textarea__inner) {
  color: #e2e8f0 !important;
}

.admin-layout.dark :deep(.el-input__inner)::placeholder,
.admin-layout.dark :deep(.el-textarea__inner)::placeholder {
  color: #64748b !important;
}

/* Element Plus - Select */
.admin-layout.dark :deep(.el-select__wrapper) {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  box-shadow: none !important;
}

.admin-layout.dark :deep(.el-select__placeholder) {
  color: #64748b !important;
}

.admin-layout.dark :deep(.el-select__selected-item) {
  color: #e2e8f0 !important;
}

/* Element Plus - Table */
.admin-layout.dark :deep(.el-table) {
  --el-table-bg-color: transparent !important;
  --el-table-tr-bg-color: transparent !important;
  --el-table-header-bg-color: rgba(255, 255, 255, 0.03) !important;
  --el-table-row-hover-bg-color: rgba(255, 255, 255, 0.05) !important;
  --el-table-border-color: rgba(255, 255, 255, 0.08) !important;
  --el-table-text-color: #e2e8f0 !important;
  --el-table-header-text-color: #94a3b8 !important;
}

.admin-layout.dark :deep(.el-table th.el-table__cell) {
  background: rgba(255, 255, 255, 0.03) !important;
}

.admin-layout.dark :deep(.el-table__empty-text) {
  color: #64748b !important;
}

/* Element Plus - Button (default) */
.admin-layout.dark :deep(.el-button--default) {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.15) !important;
  color: #e2e8f0 !important;
}

.admin-layout.dark :deep(.el-button--default:hover) {
  background: rgba(255, 255, 255, 0.1) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
}

/* Element Plus - Dialog */
.admin-layout.dark :deep(.el-dialog) {
  background: #1e293b !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.admin-layout.dark :deep(.el-dialog__header) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.admin-layout.dark :deep(.el-dialog__title) {
  color: #fff !important;
}

.admin-layout.dark :deep(.el-dialog__footer) {
  border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
}

/* Element Plus - Form */
.admin-layout.dark :deep(.el-form-item__label) {
  color: #94a3b8 !important;
}

/* Element Plus - Pagination */
.admin-layout.dark :deep(.el-pagination) {
  --el-pagination-bg-color: transparent !important;
  --el-pagination-text-color: #94a3b8 !important;
  --el-pagination-button-bg-color: rgba(255, 255, 255, 0.05) !important;
  --el-pagination-button-color: #e2e8f0 !important;
  --el-pagination-hover-color: #22d3ee !important;
}

.admin-layout.dark :deep(.el-pager li) {
  background: rgba(255, 255, 255, 0.05) !important;
  color: #94a3b8 !important;
}

.admin-layout.dark :deep(.el-pager li.is-active) {
  background: linear-gradient(135deg, #06b6d4, #8b5cf6) !important;
  color: #fff !important;
}

/* Element Plus - Dropdown */
.admin-layout.dark :deep(.el-dropdown-menu) {
  background: #1e293b !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.admin-layout.dark :deep(.el-dropdown-menu__item) {
  color: #e2e8f0 !important;
}

.admin-layout.dark :deep(.el-dropdown-menu__item:hover) {
  background: rgba(255, 255, 255, 0.05) !important;
}

/* Element Plus - DatePicker */
.admin-layout.dark :deep(.el-date-editor) {
  --el-input-bg-color: rgba(255, 255, 255, 0.05) !important;
  --el-input-border-color: rgba(255, 255, 255, 0.1) !important;
  --el-input-text-color: #e2e8f0 !important;
}

/* Element Plus - Loading */
.admin-layout.dark :deep(.el-loading-mask) {
  background: rgba(15, 23, 42, 0.8) !important;
}

/* Cards and containers */
.admin-layout.dark .rounded-lg {
  border-color: rgba(255, 255, 255, 0.08) !important;
}
</style>

<!-- Global styles for admin dark mode (NOT scoped) -->
<style>
/* Text colors for admin dark mode */
.admin-layout.dark .text-gray-800,
.admin-layout.dark .text-gray-700 {
  color: #e2e8f0 !important;
}

.admin-layout.dark .text-gray-600 {
  color: #94a3b8 !important;
}

.admin-layout.dark .text-gray-500,
.admin-layout.dark .text-gray-400,
.admin-layout.dark .text-gray-300 {
  color: #64748b !important;
}

/* Background colors for admin dark mode */
.admin-layout.dark .bg-white {
  background: rgba(30, 41, 59, 0.9) !important;
}

.admin-layout.dark .bg-gray-50,
.admin-layout.dark .bg-gray-100 {
  background: rgba(255, 255, 255, 0.03) !important;
}

/* Ring color */
.admin-layout.dark .ring-black\/5,
.admin-layout.dark [class*="ring-black"] {
  --tw-ring-color: rgba(255, 255, 255, 0.08) !important;
}

/* Element Plus Input */
.admin-layout.dark .el-input__wrapper,
.admin-layout.dark .el-textarea__inner {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  box-shadow: none !important;
}

.admin-layout.dark .el-input__inner {
  color: #e2e8f0 !important;
  -webkit-text-fill-color: #e2e8f0 !important;
  background: transparent !important;
}

.admin-layout.dark .el-input__inner::placeholder {
  color: #64748b !important;
  -webkit-text-fill-color: #64748b !important;
}

/* Element Plus Select */
.admin-layout.dark .el-select__wrapper {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  box-shadow: none !important;
}

.admin-layout.dark .el-select__placeholder,
.admin-layout.dark .el-select .el-input__inner::placeholder {
  color: #64748b !important;
}

.admin-layout.dark .el-select__selected-item,
.admin-layout.dark .el-select .el-input__inner {
  color: #e2e8f0 !important;
}

/* Element Plus Table */
.admin-layout.dark .el-table {
  --el-table-bg-color: transparent !important;
  --el-table-tr-bg-color: transparent !important;
  --el-table-header-bg-color: rgba(255, 255, 255, 0.03) !important;
  --el-table-row-hover-bg-color: rgba(255, 255, 255, 0.05) !important;
  --el-table-border-color: rgba(255, 255, 255, 0.08) !important;
  --el-table-text-color: #e2e8f0 !important;
  --el-table-header-text-color: #94a3b8 !important;
  background: transparent !important;
}

.admin-layout.dark .el-table th.el-table__cell {
  background: rgba(255, 255, 255, 0.03) !important;
}

.admin-layout.dark .el-table td.el-table__cell {
  border-color: rgba(255, 255, 255, 0.06) !important;
}

.admin-layout.dark .el-table__empty-text {
  color: #64748b !important;
}

.admin-layout.dark .el-table--enable-row-hover .el-table__body tr:hover > td {
  background: rgba(255, 255, 255, 0.05) !important;
}

/* Element Plus Button default */
.admin-layout.dark .el-button--default:not(.el-button--primary):not(.el-button--success):not(.el-button--warning):not(.el-button--danger) {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: rgba(255, 255, 255, 0.15) !important;
  color: #e2e8f0 !important;
}

.admin-layout.dark .el-button--default:not(.el-button--primary):not(.el-button--success):not(.el-button--warning):not(.el-button--danger):hover {
  background: rgba(255, 255, 255, 0.1) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
}

/* Element Plus Dialog */
.admin-layout.dark .el-dialog {
  background: #1e293b !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.admin-layout.dark .el-dialog__header {
  border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
}

.admin-layout.dark .el-dialog__title {
  color: #fff !important;
}

.admin-layout.dark .el-dialog__body {
  color: #e2e8f0 !important;
}

.admin-layout.dark .el-dialog__footer {
  border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
}

/* Element Plus Form */
.admin-layout.dark .el-form-item__label {
  color: #94a3b8 !important;
}

/* Element Plus Pagination */
.admin-layout.dark .el-pagination {
  --el-pagination-bg-color: transparent !important;
  --el-pagination-text-color: #94a3b8 !important;
  --el-pagination-button-bg-color: rgba(255, 255, 255, 0.05) !important;
  --el-pagination-button-color: #e2e8f0 !important;
}

.admin-layout.dark .el-pager li {
  background: rgba(255, 255, 255, 0.05) !important;
  color: #94a3b8 !important;
}

.admin-layout.dark .el-pager li.is-active {
  background: linear-gradient(135deg, #06b6d4, #8b5cf6) !important;
  color: #fff !important;
}

.admin-layout.dark .el-pagination button {
  background: rgba(255, 255, 255, 0.05) !important;
  color: #94a3b8 !important;
}

.admin-layout.dark .el-pagination__total,
.admin-layout.dark .el-pagination__sizes .el-input__inner {
  color: #94a3b8 !important;
}

/* Element Plus Dropdown */
.admin-layout.dark .el-dropdown-menu {
  background: #1e293b !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.admin-layout.dark .el-dropdown-menu__item {
  color: #e2e8f0 !important;
}

.admin-layout.dark .el-dropdown-menu__item:hover {
  background: rgba(255, 255, 255, 0.05) !important;
}

/* Element Plus DatePicker */
.admin-layout.dark .el-date-editor .el-input__wrapper {
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  box-shadow: none !important;
}

.admin-layout.dark .el-date-editor .el-input__inner {
  color: #e2e8f0 !important;
}

/* Element Plus Loading */
.admin-layout.dark .el-loading-mask {
  background: rgba(15, 23, 42, 0.8) !important;
}

/* Element Plus Tag */
.admin-layout.dark .el-tag {
  border-color: transparent !important;
}

/* Element Plus Card */
.admin-layout.dark .el-card {
  background: rgba(30, 41, 59, 0.9) !important;
  border-color: rgba(255, 255, 255, 0.08) !important;
}

.admin-layout.dark .el-card__header {
  border-color: rgba(255, 255, 255, 0.08) !important;
}

/* Tabs */
.admin-layout.dark .el-tabs__item {
  color: #94a3b8 !important;
}

.admin-layout.dark .el-tabs__item.is-active {
  color: #22d3ee !important;
}

.admin-layout.dark .el-tabs__active-bar {
  background: linear-gradient(90deg, #06b6d4, #8b5cf6) !important;
}

/* ============================================== */
/* Popup/Popovers rendered in body (outside layout) */
/* Uses html.dark which is set by theme store */
/* ============================================== */

/* Date Picker Popup */
html.dark .el-picker__popper,
html.dark .el-date-picker,
html.dark .el-date-range-picker {
  background: #1e293b !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

html.dark .el-picker-panel {
  background: #1e293b !important;
  color: #e2e8f0 !important;
}

html.dark .el-date-picker__header,
html.dark .el-date-range-picker__header {
  color: #e2e8f0 !important;
}

html.dark .el-date-picker__header-label {
  color: #e2e8f0 !important;
}

html.dark .el-picker-panel__icon-btn {
  color: #94a3b8 !important;
}

html.dark .el-date-table th {
  color: #64748b !important;
  border-color: rgba(255, 255, 255, 0.06) !important;
}

html.dark .el-date-table td {
  color: #94a3b8 !important;
}

html.dark .el-date-table td.available:hover {
  color: #22d3ee !important;
}

html.dark .el-date-table td.today span {
  color: #22d3ee !important;
}

html.dark .el-date-table td.current:not(.disabled) span {
  background: linear-gradient(135deg, #06b6d4, #8b5cf6) !important;
  color: #fff !important;
}

html.dark .el-date-table td.in-range div {
  background: rgba(6, 182, 212, 0.2) !important;
}

html.dark .el-date-table td.start-date span,
html.dark .el-date-table td.end-date span {
  background: linear-gradient(135deg, #06b6d4, #8b5cf6) !important;
  color: #fff !important;
}

html.dark .el-date-table td.disabled div {
  color: #475569 !important;
}

html.dark .el-picker-panel__body-wrapper {
  background: #1e293b !important;
}

html.dark .el-picker-panel__sidebar {
  background: rgba(255, 255, 255, 0.03) !important;
  border-color: rgba(255, 255, 255, 0.08) !important;
}

html.dark .el-picker-panel__shortcut {
  color: #94a3b8 !important;
}

html.dark .el-picker-panel__shortcut:hover {
  color: #22d3ee !important;
}

html.dark .el-date-range-picker__content {
  border-color: rgba(255, 255, 255, 0.08) !important;
}

html.dark .el-picker-panel__link-btn {
  color: #22d3ee !important;
}

html.dark .el-time-spinner__item {
  color: #94a3b8 !important;
}

html.dark .el-time-spinner__item.is-active {
  color: #fff !important;
}

html.dark .el-time-panel {
  background: #1e293b !important;
  border-color: rgba(255, 255, 255, 0.08) !important;
}

/* Select Dropdown Popup */
html.dark .el-select__popper,
html.dark .el-select-dropdown {
  background: #1e293b !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

html.dark .el-select-dropdown__item {
  color: #e2e8f0 !important;
}

html.dark .el-select-dropdown__item:hover {
  background: rgba(255, 255, 255, 0.05) !important;
}

html.dark .el-select-dropdown__item.is-selected {
  color: #22d3ee !important;
  background: rgba(6, 182, 212, 0.1) !important;
}

html.dark .el-select-dropdown__item.is-disabled {
  color: #475569 !important;
}

/* Popper Arrow */
html.dark .el-popper.is-dark {
  background: #1e293b !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

html.dark .el-popper .el-popper__arrow::before {
  background: #1e293b !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
}

/* Message Box */
html.dark .el-message-box {
  background: #1e293b !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

html.dark .el-message-box__title {
  color: #fff !important;
}

html.dark .el-message-box__content {
  color: #e2e8f0 !important;
}

/* Popover */
html.dark .el-popover.el-popper {
  background: #1e293b !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: #e2e8f0 !important;
}

html.dark .el-popover__title {
  color: #fff !important;
}
</style>
