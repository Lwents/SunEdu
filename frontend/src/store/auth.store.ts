// src/store/auth.store.ts
import { defineStore } from 'pinia'
import router from '@/router'
import { authService, type Role, type AuthUser, type ProfileUpdatePayload } from '@/services/auth.service'
import { ElMessage } from 'element-plus'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null as string | null,
    user: null as AuthUser | null,
  }),

  // Getters phục vụ Navbar/Profile
  getters: {
    // [ADD]
    isAuthenticated: (state) => !!state.token, // [ADD]
    role: (state): Role | undefined => state.user?.role, // [ADD]
    // ADDluôn có ảnh fallback để Navbar không bị null
    avatar: (state): string => state.user?.avatar || 'https://i.pravatar.cc/80?img=10',
  }, // [ADD]

  actions: {
    async login(identifier: string, password: string, remember = true) {
      try {
        const { token, refresh, user } = await authService.login(identifier, password)
        this.token = token
        this.user = user
        if (remember) {
          localStorage.setItem('auth', JSON.stringify({ token, user }))
          localStorage.setItem('accessToken', token)
          if (refresh) {
            localStorage.setItem('refreshToken', refresh)
          } else {
            localStorage.removeItem('refreshToken')
          }
          sessionStorage.removeItem('accessToken')
          sessionStorage.removeItem('refreshToken')
        } else {
          sessionStorage.setItem('accessToken', token)
          if (refresh) {
            sessionStorage.setItem('refreshToken', refresh)
          } else {
            sessionStorage.removeItem('refreshToken')
          }
          localStorage.removeItem('refreshToken')
        }
        try {
          const profile = await authService.getProfile()
          this.user = {
            ...(this.user as AuthUser),
            name: profile.fullName || profile.name || this.user?.name || '',
            email: profile.email || this.user?.email || '',
            phone: profile.phone || this.user?.phone,
            avatar: profile.avatar || profile.avatar_url || this.user?.avatar,
          }
          this.persist()
        } catch (error) {
          console.warn('Không thể tải profile sau khi đăng nhập:', error)
        }
        this.redirectByRole(user.role)
        return { token, refresh, user }
      } catch (err: any) {
        ElMessage.error(err?.message || 'Đăng nhập thất bại')
        throw err
      }
    },

    // async loginWithGoogle() {
    //   const { token, user } = await authService.loginWithGoogle()
    //   this.token = token
    //   this.user = user
    //   localStorage.setItem('auth', JSON.stringify({ token, user }))
    //   // this.persist() // [ADD-OPTIONAL]
    //   this.redirectByRole(user.role)
    // },

    hydrateFromStorage() {
      const raw = localStorage.getItem('auth')
      if (raw) {
        const parsed = JSON.parse(raw) as { token: string; user: AuthUser }
        this.token = parsed.token
        this.user = parsed.user
      }
    },

    async logout() {
      try {
        await authService.logout()
      } catch (error) {
        console.warn('Logout API error:', error)
      }
      this.token = null
      this.user = null
      localStorage.removeItem('auth')
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      sessionStorage.removeItem('accessToken')
      sessionStorage.removeItem('refreshToken')
      router.push('/')
    },

    redirectByRole(role: Role) {
      if (role === 'admin') {
        router.push('/admin/dashboard')
      } else if (role === 'instructor') {
        router.push('/teacher/dashboard')
      } else {
        router.push('/student/dashboard')
      }
    },

    // Helper lưu/clear localStorage khi cập nhật user/token ngoài luồng login
    persist() {
      if (this.token && this.user) {
        localStorage.setItem('auth', JSON.stringify({ token: this.token, user: this.user }))
      } else {
        localStorage.removeItem('auth')
      }
    },

    // Dùng cho trang Profile để cập nhật hồ sơ người dùng
    async updateProfile(payload: ProfileUpdatePayload) {
      const updated = await authService.updateProfile(payload)
      const prev = this.user
      this.user = {
        ...(prev as AuthUser),
        id: updated.id || prev?.id || 0,
        name: updated.fullName || updated.name || prev?.name || '',
        email: updated.email || prev?.email || '',
        phone: updated.phone || prev?.phone,
        role: (updated.role as Role) || prev?.role || 'student',
        avatar: updated.avatar || updated.avatar_url || prev?.avatar,
      }
      this.persist()
      return updated
    },

    // trang quên đổi mật khẩu
    async forgotPassword(email: string) {
      await authService.forgotPassword(email)
    },
    // trang reset mật khẩu
    async resetPassword(email: string, token: string, newPassword: string) {
      await authService.resetPassword(email, token, newPassword)
    },

    async fetchCurrentUser() {
      try {
        const user = await authService.getCurrentUser()
        this.user = {
          ...(this.user ?? {}),
          ...user,
        }
        this.persist()
        return user
      } catch (error) {
        console.error('Failed to load current user', error)
        throw error
      }
    },

    // [ADD] Dùng cho trang Đổi mật khẩu
    async changePassword(oldPassword: string, newPassword: string) {
      if (typeof authService.changePassword === 'function') {
        await authService.changePassword(oldPassword, newPassword)
      } else {
        return // mock local nếu chưa có API
      }
    },

    // Khởi tạo nhanh khi app load
    init() {
      this.hydrateFromStorage() // [ADD]
    },

    // (Tùy chọn) Cập nhật avatar ngay để UI mượt hơn (optimistic)
    setAvatar(url: string) {
      // [ADD]
      if (this.user) {
        this.user = { ...this.user, avatar: url }
        this.persist()
      }
    },
  },
})
