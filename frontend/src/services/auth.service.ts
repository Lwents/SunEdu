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
  gender?: string
  avatar?: string
  createdAt?: string
  class_name?: string
  className?: string
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
  title?: string
  bio?: string
  dob?: string
  gender?: string
  class_name?: string
  className?: string
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
  class_name?: string
  className?: string
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
  title?: string
  bio?: string
}

function normalizeProfileResponse(data: any): ProfileDetails {
  const metadata = data.metadata || {}
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
    class_name: data.class_name ?? metadata.class_name ?? undefined,
    className: data.class_name ?? metadata.class_name ?? undefined,
    email_updates: data.email_updates ?? metadata.email_updates ?? undefined,
    address: data.address ?? metadata.address ?? undefined,
    city: data.city ?? metadata.city ?? undefined,
    district: data.district ?? metadata.district ?? undefined,
    ward: data.ward ?? metadata.ward ?? undefined,
    parent_name: data.parent_name ?? metadata.parent_name ?? undefined,
    parent_phone: data.parent_phone ?? metadata.parent_phone ?? undefined,
    parent_email: data.parent_email ?? metadata.parent_email ?? undefined,
    parent_relation: data.parent_relation ?? metadata.parent_relation ?? undefined,
    parent_address: data.parent_address ?? metadata.parent_address ?? undefined,
    title: data.title ?? metadata.title ?? undefined,
    bio: data.bio ?? metadata.bio ?? undefined,
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
    // Map frontend fields to backend fields, including title and bio in metadata
    const backendPayload: any = {}
    if (payload.full_name) backendPayload.full_name = payload.full_name
    if (payload.email) backendPayload.email = payload.email
    if (payload.phone !== undefined) backendPayload.phone = payload.phone
    if (payload.avatar_url) backendPayload.avatar_url = payload.avatar_url
    if (payload.dob) backendPayload.dob = payload.dob
    if (payload.gender) backendPayload.gender = payload.gender
    if (payload.class_name || payload.className) backendPayload.class_name = payload.class_name || payload.className
    if (payload.title !== undefined) backendPayload.title = payload.title
    if (payload.bio !== undefined) backendPayload.bio = payload.bio
    // Parent & contact info (backend copies these keys into metadata)
    const copyKeys = [
      'address',
      'city',
      'district',
      'ward',
      'parent_name',
      'parent_phone',
      'parent_email',
      'parent_relation',
      'parent_address',
      'email_updates',
    ] as const
    for (const k of copyKeys) {
      const v = (payload as any)[k]
      if (v !== undefined) backendPayload[k] = v
    }
    try {
    const { data } = await http.patch('/account/profile/', backendPayload)
    return normalizeProfileResponse(data)
    } catch (error: any) {
      // Nếu có response và status code là 200/201, coi như thành công
      // Có thể do timeout hoặc network issue nhưng backend đã lưu thành công
      if (error?.response?.status === 200 || error?.response?.status === 201) {
        // Trả về response data nếu có, hoặc throw lại để caller xử lý
        if (error?.response?.data) {
          return normalizeProfileResponse(error.response.data)
        }
      }
      // Throw lại lỗi để caller xử lý
      throw error
    }
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
