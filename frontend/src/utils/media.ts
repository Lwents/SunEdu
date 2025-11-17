export function resolveMediaUrl(input?: string | null): string {
  if (!input) return ''

  const trimmed = String(input).trim()
  if (!trimmed) return ''

  if (trimmed.startsWith('http://') || trimmed.startsWith('https://') || trimmed.startsWith('data:')) {
    return trimmed
  }

  const apiBaseRaw = (import.meta.env.VITE_API_URL ?? window.location.origin).toString().trim()
  const apiBase = apiBaseRaw.replace(/\/+$/, '') || window.location.origin

  if (trimmed.startsWith('/')) {
    return `${apiBase}${trimmed}`
  }

  return `${apiBase}/media/${trimmed}`
}
