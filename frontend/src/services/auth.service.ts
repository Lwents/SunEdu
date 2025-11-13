//frontend/src/services/auth.service.ts

import http from '@/config/axios'
import { jwtDecode } from 'jwt-decode'

export type Role = 'admin' | 'instructor' | 'student'

export const getRoleFromToken = (token: string): Role | null => {
  if (!token) return null
  try {
    const raw = token.startsWith('Bearer ') ? token.slice(7) : token
    const decoded: any = jwtDecode(raw)

    const maybeRole =
      decoded.role ||
      decoded.roles ||
      decoded.user?.role ||
      (Array.isArray(decoded.roles) && decoded.roles[0]) ||
      null

    if (!maybeRole) return null

    const r = String(maybeRole).toLowerCase()
    if (r === 'admin') return 'admin'
    if (r === 'instructor') return 'instructor'
    return 'student'
  } catch (error) {
    console.error('Invalid token:', error)
    return null
  }
}

export interface AuthUser {
  id: number
  name: string
  email: string
  role: Role
  phone?: string
  title?: string
  bio?: string
  avatar?: string
  createdAt?: string
}

export interface AuthPayload {
  token: string
  refresh?: string
  user: AuthUser
}

export interface ProfileUpdatePayload {
  username?: string
  full_name?: string
  phone?: string
  email?: string
  avatar_url?: string
  dob?: string
  gender?: string
  email_updates?: boolean
  address?: string
  city?: string
  district?: string
  ward?: string
  parent_name?: string
  parent_phone?: string
  parent_email?: string
  parent_relation?: string
  parent_address?: string
}

export interface ProfileDetails extends AuthUser {
  username?: string
  fullName?: string
  avatar_url?: string
  dob?: string
  gender?: string
  email_updates?: boolean
  address?: string
  city?: string
  district?: string
  ward?: string
  updatedAt?: string
  parent_name?: string
  parent_phone?: string
  parent_email?: string
  parent_relation?: string
  parent_address?: string
}

function normalizeProfileResponse(data: any): ProfileDetails {
  return {
    id: Number(data.id ?? 0),
    name: data.full_name ?? data.username ?? 'User',
    username: data.username ?? undefined,
    email: data.email ?? '',
    phone: data.phone ?? undefined,
    role: (data.role as Role) || 'student',
    avatar: data.avatar_url ?? undefined,
    avatar_url: data.avatar_url ?? undefined,
    fullName: data.full_name ?? undefined,
    dob: data.dob ?? undefined,
    gender: data.gender ?? undefined,
    email_updates: data.email_updates ?? undefined,
    address: data.address ?? undefined,
    city: data.city ?? undefined,
    district: data.district ?? undefined,
    ward: data.ward ?? undefined,
    parent_name: data.parent_name ?? undefined,
    parent_phone: data.parent_phone ?? undefined,
    parent_email: data.parent_email ?? undefined,
    parent_relation: data.parent_relation ?? undefined,
    parent_address: data.parent_address ?? undefined,
    createdAt: data.created_on ?? data.createdAt,
    updatedAt: data.updated_on ?? data.updatedAt,
  }
}

export const authService = {
  async login(identifier: string, password: string): Promise<AuthPayload> {
    if (!identifier || !password) throw new Error('Thiếu thông tin đăng nhập')

    const isEmail = /\S+@\S+\.\S+/.test(identifier)
    const body = isEmail ? { email: identifier, password } : { username: identifier, password }

    const { data } = await http.post('/account/login/', body)

    const token = (data.access || data.access_token || data.token) as string
    if (!token) throw new Error('Không nhận được token từ server')
    const refresh = (data.refresh || data.refresh_token) as string | undefined

    const role = (getRoleFromToken(token) || (data.user?.role as Role) || 'student') as Role

    const user: AuthUser = {
      id: Number(data.user?.id ?? data.user_id ?? 0),
      name: data.user?.username ?? data.user?.name ?? 'User',
      email: data.user?.email ?? '',
      role,
    }

    localStorage.setItem('access', token)
    localStorage.setItem('accessToken', token)
    return { token, refresh, user }
  },

  // Nếu backend hỗ trợ social login bằng token từ client
  // async loginWithGoogle(googleToken: string): Promise<AuthPayload> {
  //   const { data } = await http.post('/account/social/google/', { token: googleToken })
  //   const token = (data.access || data.access_token || data.token) as string
  //   if (!token) throw new Error('Không nhận được token từ server')

  //   const role = (getRoleFromToken(token) || (data.user?.role as Role) || 'student') as Role
  //   const user: AuthUser = {
  //     id: Number(data.user?.id ?? 0),
  //     name: data.user?.username ?? data.user?.name ?? 'User',
  //     email: data.user?.email ?? '',
  //     role,
  //   }

  //   localStorage.setItem('access', token)
  //   localStorage.setItem('accessToken', token)
  //   if (data.refresh) localStorage.setItem('refresh', data.refresh)

  //   return { token, user }
  // },

  async register(payload: {
    username: string
    email: string
    phone: string
    password: string
  }): Promise<{ ok: boolean }> {
    const body = {
      username: payload.username,
      email: payload.email,
      password: payload.password,
      phone: payload.phone,
    }

    await http.post('/account/register/', body)

    return { ok: true }
  },

  async updateProfile(payload: ProfileUpdatePayload): Promise<ProfileDetails> {
    const { data } = await http.patch('/account/profile/', payload)
    return normalizeProfileResponse(data)
  },

  async getCurrentUser(): Promise<AuthUser> {
    const { data } = await http.get('/account/user/')
    const user: AuthUser = {
      id: Number(data.id ?? 0),
      name: data.username ?? data.full_name ?? data.name ?? 'User',
      email: data.email ?? '',
      role: (data.role as Role) || 'student',
      phone: data.phone ?? undefined,
      createdAt: data.created_on ?? data.createdAt,
    }
    return user
  },

  async getProfile(): Promise<ProfileDetails> {
    const { data } = await http.get('/account/profile/')
    return normalizeProfileResponse(data)
  },

  async changePassword(oldPassword: string, newPassword: string): Promise<{ ok: boolean }> {
    if (!oldPassword || !newPassword) throw new Error('Thiếu mật khẩu')
    await http.post('/account/password/change/', {
      old_password: oldPassword,
      new_password: newPassword,
    })
    return { ok: true }
  },

  async requestPasswordChangeOtp(
    currentPassword: string,
  ): Promise<{ detail?: string; email?: string }> {
    if (!currentPassword) throw new Error('Vui lòng nhập mật khẩu hiện tại')
    const { data } = await http.post('/account/password/change/request-otp/', {
      current_password: currentPassword,
    })
    return data
  },

  async changePasswordWithOtp(otp: string, newPassword: string): Promise<{ ok: boolean }> {
    if (!otp || !newPassword) throw new Error('Thiếu OTP hoặc mật khẩu mới')
    await http.post('/account/password/change/confirm-otp/', {
      otp,
      new_password: newPassword,
    })
    return { ok: true }
  },

  async forgotPassword(email: string): Promise<void> {
    if (!email) throw new Error('Vui lòng nhập email')
    await http.post('/account/password/reset/', { email })
  },

  async resetPassword(email: string, token: string, newPassword: string): Promise<void> {
    if (!email || !token || !newPassword) throw new Error('Thiếu thông tin cập nhật mật khẩu')
    await http.post('/account/password/reset/confirm/', {
      email,
      reset_token: token,
      new_password: newPassword,
    })
  },

  async logout(): Promise<void> {
    const refresh = localStorage.getItem('refreshToken') || sessionStorage.getItem('refreshToken')
    try {
      await http.post('/account/logout/', refresh ? { refresh } : {})
    } catch (error: any) {
      const status = error?.response?.status
      if (status && [400, 401].includes(status)) {
        return
      }
      throw error
    }
  },

  async refreshToken(): Promise<{ access: string; refresh?: string }> {
    const refresh = localStorage.getItem('refreshToken') || sessionStorage.getItem('refreshToken')
    if (!refresh) {
      throw new Error('Thiếu refresh token')
    }
    const { data } = await http.post('/account/refresh/', { refresh })
    const access = data.access || data.access_token
    const newRefresh = data.refresh || data.refresh_token
    if (!access) {
      throw new Error('Không nhận được access token mới')
    }
    localStorage.setItem('accessToken', access)
    if (newRefresh) {
      localStorage.setItem('refreshToken', newRefresh)
    }
    return { access, refresh: newRefresh }
  },
}
