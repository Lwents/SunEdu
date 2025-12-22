export function resolveMediaUrl(input?: string | null): string {
  if (!input) return ''

  const trimmed = String(input).trim()
  if (!trimmed) return ''

  if (trimmed.startsWith('http://') || trimmed.startsWith('https://') || trimmed.startsWith('data:')) {
    return trimmed
  }

  const configuredMediaBase = import.meta.env.VITE_MEDIA_BASE_URL?.toString().trim()
  let mediaBase = configuredMediaBase?.replace(/\/+$/, '')

  if (!mediaBase) {
    const defaultApiBase = import.meta.env.DEV ? 'http://localhost:8000' : ''
    const apiBaseRaw = (import.meta.env.VITE_API_URL ?? defaultApiBase)?.toString().trim()
    try {
      // Lấy origin để tránh dính /api ở cuối URL
      mediaBase = apiBaseRaw ? new URL(apiBaseRaw, window.location.origin).origin : window.location.origin
    } catch {
      mediaBase = window.location.origin
    }
  }

  if (!mediaBase) {
    mediaBase = window.location.origin
  }

  const normalized = trimmed.replace(/^\/+/, '')
  const apiPrefix = (import.meta.env.VITE_API_PREFIX ?? '').toString().trim().replace(/^\/+|\/+$/g, '') || 'api'
  const isLocal =
    mediaBase.includes('localhost') ||
    mediaBase.includes('127.0.0.1') ||
    mediaBase.includes('0.0.0.0')

  if (isLocal) {
    const streamPath = normalized.replace(/^api\//, '').replace(/^media\//, '')
    return `${mediaBase}/${apiPrefix}/media/stream/${streamPath}`
  }

  if (trimmed.startsWith('/')) {
    return `${mediaBase}${trimmed}`
  }

  if (normalized.startsWith('api/media/')) {
    return `${mediaBase}/${normalized.replace(/^api\//, '')}`
  }
  if (normalized.startsWith('media/')) {
    return `${mediaBase}/${normalized}`
  }

  return `${mediaBase}/media/${normalized}`
}
