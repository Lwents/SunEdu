<!-- src/components/shared/AdminSidebar.vue -->
<template>
  <aside class="sidebar" :class="isDark ? 'dark' : 'light'">
    <!-- Brand -->
    <div class="brand">
      <button class="close-btn" aria-label="Đóng menu" @click="$emit('close')">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
      <RouterLink to="/admin/dashboard" class="logo-link">
        <LogoSunnyEdu :size="70" />
      </RouterLink>
    </div>

    <!-- Nav -->
    <nav class="nav-area">
      <template v-for="(group, gi) in groups" :key="gi">
        <div class="group-label">{{ group.label }}</div>
        <ul class="nav-list">
          <li v-for="item in group.items" :key="item.to">
            <RouterLink :to="item.to" v-slot="{ isActive }" class="nav-link-wrapper">
              <div class="nav-item" :class="{ active: isActive }">
                <component :is="item.icon" class="nav-icon" />
                <span class="nav-text">{{ item.label }}</span>
              </div>
            </RouterLink>
          </li>
        </ul>
      </template>
    </nav>

    <!-- Footer -->
    <div class="sidebar-footer">© {{ year }} SunnyEdu</div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
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
import LogoSunnyEdu from '@/components/ui/LogoSunnyEdu.vue'
import { useThemeStore } from '@/store/theme.store'

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)
const year = new Date().getFullYear()

type NavItem = { to: string; label: string; icon: any }
type NavGroup = { label: string; items: NavItem[] }

const groups: NavGroup[] = [
  {
    label: 'Tổng quan',
    items: [{ to: '/admin/dashboard', label: 'Dashboard', icon: LayoutDashboard }],
  },
  {
    label: 'Quản trị',
    items: [
      { to: '/admin/users', label: 'Người dùng', icon: Users },
      { to: '/admin/users/bulk-create', label: 'Tạo TK hàng loạt', icon: Users },
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
</script>

<style scoped>
.sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.sidebar.dark {
  background: rgba(15, 23, 42, 0.95);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
}

.sidebar.light {
  background: #ffffff;
  border-right: 1px solid #e2e8f0;
}

/* Brand */
.brand {
  height: 60px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 16px;
  border-bottom: 1px solid;
}

.sidebar.dark .brand {
  border-color: rgba(255, 255, 255, 0.08);
}

.sidebar.light .brand {
  border-color: #e2e8f0;
}

.close-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s;
}

@media (min-width: 768px) {
  .close-btn {
    display: none;
  }
}

.sidebar.dark .close-btn {
  color: #94a3b8;
}

.sidebar.dark .close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.sidebar.light .close-btn {
  color: #64748b;
}

.sidebar.light .close-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.logo-link {
  display: flex;
  align-items: center;
  flex: 1;
}

/* Nav */
.nav-area {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.group-label {
  padding: 12px 12px 8px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.sidebar.dark .group-label {
  color: #64748b;
}

.sidebar.light .group-label {
  color: #94a3b8;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0 0 8px;
}

.nav-link-wrapper {
  display: block;
  text-decoration: none;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
}

.sidebar.dark .nav-item {
  color: #94a3b8;
}

.sidebar.dark .nav-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #e2e8f0;
}

.sidebar.dark .nav-item.active {
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(139, 92, 246, 0.2));
  color: #22d3ee;
  border: 1px solid rgba(6, 182, 212, 0.3);
}

.sidebar.light .nav-item {
  color: #64748b;
}

.sidebar.light .nav-item:hover {
  background: #f8fafc;
  color: #1e293b;
}

.sidebar.light .nav-item.active {
  background: #eff6ff;
  color: #2563eb;
  border: 1px solid #bfdbfe;
}

.nav-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.nav-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Footer */
.sidebar-footer {
  padding: 12px 16px;
  font-size: 11px;
  text-align: center;
  border-top: 1px solid;
}

.sidebar.dark .sidebar-footer {
  color: #475569;
  border-color: rgba(255, 255, 255, 0.08);
}

.sidebar.light .sidebar-footer {
  color: #94a3b8;
  border-color: #e2e8f0;
}
</style>
