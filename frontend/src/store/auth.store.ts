// src/store/auth.store.ts
import { defineStore } from 'pinia'
import router from '@/router'
import {
  authService,
  type Role,
  type AuthUser,
  type ProfileUpdatePayload,
  type ProfileDetails,
} from '@/services/auth.service'
import { ElMessage } from 'element-plus'
import { getAvatarSrc } from '@/utils/avatar'

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
    // Avatar với fallback dựa vào gender và role
    avatar: (state): string => {
      if (!state.user) return '/boy.webp'
      return getAvatarSrc(
        state.user.avatar,
        state.user.gender as 'male' | 'female' | 'other' | null | undefined,
        state.user.role
      )
    },
  }, // [ADD]

  actions: {
    async login(identifier: string, password: string, remember = true) {
      try {
        const { token, refresh, user } = await authService.login(identifier, password)
        this.token = token
        this.user = user
        if (remember) {
          // Không lưu avatar base64 vào localStorage
          const userToStore = { ...user }
          if (userToStore.avatar && (
            userToStore.avatar.startsWith('data:') || 
            userToStore.avatar.length > 1000
          )) {
            userToStore.avatar = userToStore.avatar.startsWith('http') ? userToStore.avatar : undefined
          }
          try {
            localStorage.setItem('auth', JSON.stringify({ token, user: userToStore }))
          } catch (e: any) {
            if (e.name === 'QuotaExceededError') {
              console.warn('LocalStorage quota exceeded during login')
              localStorage.removeItem('auth')
            }
          }
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
          localStorage.removeItem('accessToken')
          localStorage.removeItem('auth')
        }
        try {
          const profile = await authService.getProfile()
          this.user = {
            ...(this.user as AuthUser),
            id: (this.user as AuthUser)?.id ?? (profile as any)?.id ?? user.id,
            name: profile.fullName || profile.name || this.user?.name || '',
            email: profile.email || this.user?.email || '',
            phone: profile.phone || this.user?.phone,
            avatar: profile.avatar || profile.avatar_url || this.user?.avatar,
            gender: profile.gender ?? this.user?.gender,
            title: profile.title ?? this.user?.title,
            bio: profile.bio ?? this.user?.bio,
            class_name: (profile as any).class_name || (profile as any).className || (this.user as any)?.class_name,
          }
          this.persist()
        } catch (error) {
          console.warn('Không thể tải profile sau khi đăng nhập:', error)
        }
        this.redirectByRole(user.role)
        return { token, refresh, user }
      } catch (err: any) {
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
      // Clear state trước
      this.token = null
      this.user = null
      localStorage.removeItem('auth')
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      sessionStorage.removeItem('accessToken')
      sessionStorage.removeItem('refreshToken')
      // Đảm bảo luôn quay về trang đăng nhập ngay cả khi API lỗi hoặc token hết hạn
      try {
        await router.replace('/auth/login')
      } catch (_) {
        /* ignore */
      }
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
        // Không lưu avatar base64 vào localStorage để tránh QuotaExceededError
        // Chỉ lưu URL nếu avatar là URL, không lưu base64 string
        const userToStore = { ...this.user }
        if (userToStore.avatar && (
          userToStore.avatar.startsWith('data:') || 
          userToStore.avatar.length > 1000
        )) {
          // Nếu avatar là base64 hoặc quá dài, không lưu vào localStorage
          // Chỉ lưu URL hoặc để undefined
          userToStore.avatar = userToStore.avatar.startsWith('http') ? userToStore.avatar : undefined
        }
        try {
          localStorage.setItem('auth', JSON.stringify({ token: this.token, user: userToStore }))
        } catch (e: any) {
          // Nếu vẫn lỗi quota, thử xóa một số keys cũ hoặc chỉ lưu token
          if (e.name === 'QuotaExceededError') {
            console.warn('LocalStorage quota exceeded, clearing old data')
            try {
              // Xóa auth cũ và chỉ lưu token
              localStorage.removeItem('auth')
              localStorage.setItem('accessToken', this.token)
              // Không lưu user vào localStorage nếu quá lớn
            } catch (e2) {
              console.error('Failed to save to localStorage:', e2)
            }
          }
        }
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
        gender: updated.gender ?? prev?.gender,
        title: updated.title ?? prev?.title,
        bio: updated.bio ?? prev?.bio,
        class_name: (updated as any).class_name ?? (updated as any).className ?? (prev as any)?.class_name,
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

    async requestPasswordOtp(currentPassword: string) {
      return authService.requestPasswordChangeOtp(currentPassword)
    },
    async changePasswordWithOtp(otp: string, newPassword: string) {
      return authService.changePasswordWithOtp(otp, newPassword)
    },

    // Khởi tạo nhanh khi app load, đồng bộ avatar từ profile để tránh fallback boy/girl
    async init() {
      this.hydrateFromStorage()
      if (this.token) {
        await this.refreshProfile().catch((err) => {
          console.warn('Không thể tải profile khi khởi tạo:', err)
        })
      }
    },

    async refreshProfile(force = false): Promise<ProfileDetails | null> {
      if (force) {
        this.hydrateFromStorage()
      }
      if (!this.token) {
        return null
      }
          const profile = await authService.getProfile()
          this.user = {
            ...(this.user as AuthUser | null),
        id: profile.id || this.user?.id || 0,
            name: profile.fullName || profile.name || this.user?.name || '',
            email: profile.email || this.user?.email || '',
            phone: profile.phone || this.user?.phone,
        role: this.user?.role || (profile.role as Role) || 'student',
            avatar: profile.avatar || profile.avatar_url || this.user?.avatar,
            gender: profile.gender ?? this.user?.gender,
            title: profile.title ?? this.user?.title,
            bio: profile.bio ?? this.user?.bio,
        class_name: profile.class_name || profile.className || (this.user as any)?.class_name,
          }
          this.persist()
      return profile
    },

    // (Tùy chọn) Cập nhật avatar ngay để UI mượt hơn (optimistic)
    setAvatar(url: string) {
      if (this.user) {
        this.user = { ...this.user, avatar: url }
        this.persist()
      }
    },
  },
})
