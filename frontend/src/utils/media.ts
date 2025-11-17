export function resolveMediaUrl(input?: string | null): string {
  if (!input) return ''

  const trimmed = String(input).trim()
  if (!trimmed) return ''

  if (trimmed.startsWith('http://') || trimmed.startsWith('https://') || trimmed.startsWith('data:')) {
    return trimmed
  }

  const mediaBaseRaw = (import.meta.env.VITE_MEDIA_BASE_URL
    ?? import.meta.env.VITE_API_URL
    ?? window.location.origin).toString().trim()
  const mediaBase = mediaBaseRaw.replace(/\/+$/, '') || window.location.origin

  if (trimmed.startsWith('/')) {
    return `${mediaBase}${trimmed}`
  }

  return `${mediaBase}/media/${trimmed}`
}
