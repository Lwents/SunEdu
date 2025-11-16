// src/config/axios.ts
import axios from 'axios'

// Default to the SmartEdu public API when no env override is provided.
const DEFAULT_API_URL = 'https://api.smartedu.click'
const rawApiUrl = (import.meta.env.VITE_API_URL ?? '').toString().trim()
const apiUrl = (rawApiUrl || DEFAULT_API_URL).replace(/\/+$/, '')

const normalizePrefix = (value?: string) => {
  const cleaned = (value ?? '').trim().replace(/^\/+|\/+$/g, '')
  return cleaned || 'api'
}

const apiPrefix = `/${normalizePrefix(import.meta.env.VITE_API_PREFIX)}`

const http = axios.create({
  baseURL: `${apiUrl}${apiPrefix}`,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
})

let isRefreshing = false
let refreshQueue: Array<(token: string) => void> = []

function enqueueRefresh(cb: (token: string) => void) {
  refreshQueue.push(cb)
}

function resolveRefreshQueue(token: string) {
  refreshQueue.forEach((cb) => cb(token))
  refreshQueue = []
}

function getAccessToken() {
  return localStorage.getItem('accessToken') || sessionStorage.getItem('accessToken')
}

http.interceptors.response.use(
  (response) => {
    console.log('Response Data:', response.data)
    return response
  },
  (error) => Promise.reject(error)
)

/*=============backend có phần nào sửa lại như này nhé để fortend dịch=========*/
function translateMessage(message: string): string {
  const translations: Record<string, string> = {
    // Login errors
    'Invalid credentials': 'Tài khoản hoặc mật khẩu không chính xác',
    'Invalid email or password': 'Tài khoản hoặc mật khẩu không chính xác',
    'Unable to log in with provided credentials.': 'Tài khoản hoặc mật khẩu không chính xác',
    'Email not found': 'Tài khoản không tồn tại',
    'User not found': 'Tài khoản không tồn tại',

    // Register errors
    'Username already taken': 'Username đã tồn tại',
    'Email already taken': 'Email đã tồn tại',
    'Email already exists': 'Email đã tồn tại',
    'Phone already taken': 'Số điện thoại đã được sử dụng',
    'Invalid email': 'Email không hợp lệ',
    'Password is too weak': 'Mật khẩu quá yếu',
    'Password must be at least 6 characters': 'Mật khẩu phải ít nhất 6 ký tự',
  }
  return translations[message] || message
}

// Interceptor để thêm token vào tất cả các request
http.interceptors.request.use(
  (config) => {
    const token = getAccessToken()
    if (config.url && !config.url.includes('/login') && !config.url.includes('/register')) {
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`
      }
    }
    
    // Nếu data là FormData, để axios tự động set Content-Type là multipart/form-data
    // Không set Content-Type thủ công để browser tự thêm boundary
    if (config.data instanceof FormData) {
      // Xóa Content-Type để browser tự động set với boundary
      if (config.headers) {
        delete config.headers['Content-Type']
      }
    }
    
    return config
  },
  (error) => Promise.reject(error)
)

http.interceptors.response.use(
  (response) => response,
  async (error: any) => {
    const originalRequest = error.config
    const status = error.response?.status

    const isAuthEndpoint =
      originalRequest?.url?.includes('/login') || originalRequest?.url?.includes('/register')

    if (status === 401 && !originalRequest._retry && !isAuthEndpoint) {
      if (isRefreshing) {
        return new Promise((resolve) => {
          enqueueRefresh((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            resolve(http(originalRequest))
          })
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const refresh =
          localStorage.getItem('refreshToken') || sessionStorage.getItem('refreshToken')
        if (!refresh) throw new Error('No refresh token')

        const { data } = await http.post('/account/refresh/', { refresh })
        const newAccess = data.access || data.access_token
        const newRefresh = data.refresh || data.refresh_token
        if (!newAccess) throw new Error('No access token')

        localStorage.setItem('accessToken', newAccess)
        if (newRefresh) localStorage.setItem('refreshToken', newRefresh)
        originalRequest.headers.Authorization = `Bearer ${newAccess}`
        resolveRefreshQueue(newAccess)
        return http(originalRequest)
      } catch (refreshError) {
        refreshQueue = []
        localStorage.removeItem('auth')
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        sessionStorage.removeItem('accessToken')
        sessionStorage.removeItem('refreshToken')
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    let message = 'Có lỗi xảy ra'

    if (error.response) {
      const data = error.response.data
      if (typeof data === 'string' && data.trim()) {
        message = data
      } else if (data?.message) {
        message = data.message
      } else if (data?.error) {
        message = data.error
      } else if (data?.detail) {
        message = data.detail
      } else if (data && typeof data === 'object') {
        const firstKey = Object.keys(data)[0]
        const firstValue = data[firstKey]
        if (Array.isArray(firstValue) && firstValue[0]) {
          message = String(firstValue[0])
        } else if (typeof firstValue === 'string') {
          message = firstValue
        }
      }

      if (!message || message === 'Có lỗi xảy ra') {
        if (status === 401) {
          message = 'Phiên đăng nhập đã hết hạn'
        } else if (status === 400) {
          message = 'Yêu cầu không hợp lệ'
        } else if (status === 500) {
          message = 'Lỗi máy chủ'
        }
      }

      message = translateMessage(message)
    } else if (!error.response) {
      message = 'Lỗi kết nối. Kiểm tra internet'
    }

    const enhancedError = error || new Error(message)
    if (enhancedError instanceof Error) {
      enhancedError.message = message
      ;(enhancedError as any).status = status
      ;(enhancedError as any).data = error?.response?.data
    }
    return Promise.reject(enhancedError)
  }
)

export default http
