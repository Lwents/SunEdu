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
    const apiBaseRaw = import.meta.env.VITE_API_URL?.toString().trim()
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

  if (trimmed.startsWith('/')) {
    return `${mediaBase}${trimmed}`
  }

  return `${mediaBase}/media/${trimmed}`
}
