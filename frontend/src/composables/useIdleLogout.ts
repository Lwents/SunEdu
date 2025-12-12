import { ref, onMounted, onBeforeUnmount } from 'vue'

type Options = {
    timeout?: number // ms
    warningTime?: number // ms before logout to show warning
    autoStart?: boolean // start tracking immediately on mount (default: false)
    onLogout: () => void
    onWarn?: (remainingMs: number) => void
    onActive?: () => void // called when activity is detected (useful to hide warning)
}

const STORAGE_KEY = 'app-last-activity'

export function useIdleLogout(opts: Options) {
    const timeout = opts.timeout ?? 10 * 60 * 1000 // default 10 minutes
    const warningTime = opts.warningTime ?? 60 * 1000 // default 1 minute
    const autoStart = opts.autoStart ?? false
    const isWarning = ref(false)
    const remaining = ref<number>(timeout)

    let started = false
    let idleTimer: ReturnType<typeof setTimeout> | null = null
    let warnTimer: ReturnType<typeof setTimeout> | null = null
    const visibilityHandler = () => {
        if (!started) return
        if (!document.hidden) updateLastActivity(true)
    }

    function updateLastActivity(force = false) {
        if (!started && !force) return
        // Khi đang cảnh báo, chỉ cho phép reset nếu force=true (bấm nút giữ phiên)
        if (isWarning.value && !force) return
        // Clear warning trạng thái khi đã xác nhận tiếp tục
        if (isWarning.value) {
            isWarning.value = false
            opts.onActive?.()
        }
        const now = Date.now()
        try {
            localStorage.setItem(STORAGE_KEY, String(now))
        } catch {
            // ignore (privacy modes)
        }
        resetTimers()
    }

    function handleStorageEvent(e: StorageEvent) {
        if (!started) return
        if (e.key === STORAGE_KEY) {
            resetTimers()
        }
    }

    function clearTimers() {
        if (idleTimer) {
            clearTimeout(idleTimer)
            idleTimer = null
        }
        if (warnTimer) {
            clearTimeout(warnTimer)
            warnTimer = null
        }
        isWarning.value = false
    }

    function resetTimers() {
        if (!started) return
        clearTimers()
        const last = Number(localStorage.getItem(STORAGE_KEY) || Date.now())
        const elapsed = Date.now() - last
        const timeLeft = Math.max(0, timeout - elapsed)
        remaining.value = timeLeft

        if (timeLeft <= 0) {
            // already expired
            opts.onLogout()
            return
        }

        // schedule warning
        const warnIn = Math.max(0, timeLeft - warningTime)
        warnTimer = setTimeout(() => {
            isWarning.value = true
            opts.onWarn?.(warningTime)
        }, warnIn)

        // schedule logout
        idleTimer = setTimeout(() => {
            clearTimers()
            opts.onLogout()
        }, timeLeft)
    }

    function onActivity() {
        updateLastActivity()
    }

    function addListeners() {
        const events = ['mousemove', 'keydown', 'click', 'touchstart', 'scroll']
        events.forEach((ev) => window.addEventListener(ev, onActivity, { passive: true }))
        document.addEventListener('visibilitychange', visibilityHandler)
        window.addEventListener('storage', handleStorageEvent)
        // Cho phép nơi khác phát sự kiện giữ phiên
        window.addEventListener('idle-keepalive', () => updateLastActivity(true))
    }

    function removeListeners() {
        const events = ['mousemove', 'keydown', 'click', 'touchstart', 'scroll']
        events.forEach((ev) => window.removeEventListener(ev, onActivity))
        window.removeEventListener('storage', handleStorageEvent)
        document.removeEventListener('visibilitychange', visibilityHandler)
        clearTimers()
    }

    function start() {
        if (started) {
            updateLastActivity(true)
            return
        }
        started = true
        addListeners()
        updateLastActivity(true)
    }

    function stop() {
        if (!started) {
            clearTimers()
            return
        }
        started = false
        removeListeners()
    }

    onMounted(() => {
        if (autoStart) {
            start()
        }
    })

    onBeforeUnmount(() => {
        stop()
    })

    // Expose manual controls
    return {
        isWarning,
        remaining,
        reset: () => updateLastActivity(true),
        stop,
        start,
    }
}
