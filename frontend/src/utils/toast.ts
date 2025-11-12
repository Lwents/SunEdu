// Toast Notification Utility - Fade Slide Up from Bottom Right
// Usage: showToast('Message here', 'success')

export type ToastType = 'success' | 'error' | 'warning' | 'info'

let toastContainer: HTMLElement | null = null
let toastCount = 0
let isHovering = false
let closingToasts = new Set<HTMLElement>()

function getToastContainer() {
  if (!toastContainer) {
    toastContainer = document.createElement('div')
    toastContainer.className = 'toast-container-custom'
    toastContainer.style.cssText = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      z-index: 99999;
      display: flex;
      flex-direction: column;
      gap: 0;
      pointer-events: none;
      max-width: 420px;
    `
    document.body.appendChild(toastContainer)
  }
  return toastContainer
}

const toastIcons = {
  success: `<svg fill="currentColor" viewBox="0 0 20 20" style="width: 24px; height: 24px;"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>`,
  error: `<svg fill="currentColor" viewBox="0 0 20 20" style="width: 24px; height: 24px;"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/></svg>`,
  warning: `<svg fill="currentColor" viewBox="0 0 20 20" style="width: 24px; height: 24px;"><path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>`,
  info: `<svg fill="currentColor" viewBox="0 0 20 20" style="width: 24px; height: 24px;"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/></svg>`
}

const toastColors = {
  success: { border: '#10b981', icon: '#10b981' },
  error: { border: '#ef4444', icon: '#ef4444' },
  warning: { border: '#f59e0b', icon: '#f59e0b' },
  info: { border: '#3b82f6', icon: '#3b82f6' }
}

export function showToast(message: string, type: ToastType = 'info') {
  const container = getToastContainer()
  const colors = toastColors[type]
  toastCount++
  
  const toast = document.createElement('div')
  toast.className = 'toast-item'
  toast.dataset.index = String(toastCount)
  
  toast.style.cssText = `
    min-width: 320px;
    max-width: 420px;
    background: white;
    padding: 16px 20px;
    border-radius: 12px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    display: flex;
    align-items: center;
    gap: 15px;
    pointer-events: auto;
    position: absolute;
    bottom: 0;
    right: 0;
    border-left: 5px solid ${colors.border};
    transform: translateY(100px);
    opacity: 0;
    transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    z-index: ${100 + toastCount};
  `
  
  toast.innerHTML = `
    <div style="color: ${colors.icon}; flex-shrink: 0;">
      ${toastIcons[type]}
    </div>
    <div style="flex: 1; font-size: 14px; color: #1f2937; line-height: 1.5; font-weight: 500;">
      ${message}
    </div>
    <button class="toast-close-btn" style="
      background: none;
      border: none;
      color: #9ca3af;
      cursor: pointer;
      font-size: 20px;
      padding: 0;
      width: 24px;
      height: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      transition: color 0.2s;
    " aria-label="Close">×</button>
  `
  
  const closeBtn = toast.querySelector('.toast-close-btn') as HTMLElement
  closeBtn?.addEventListener('click', () => closeToast(toast, container))
  closeBtn?.addEventListener('mouseenter', () => {
    closeBtn.style.color = '#4b5563'
    closeBtn.style.transform = 'scale(1.2)'
  })
  closeBtn?.addEventListener('mouseleave', () => {
    closeBtn.style.color = '#9ca3af'
    closeBtn.style.transform = 'scale(1)'
  })
  
  // Add to container
  container.appendChild(toast)
  
  // Hover only on individual toast to expand
  toast.addEventListener('mouseenter', () => {
    if (!closingToasts.has(toast)) {
      isHovering = true
      expandToasts(container)
    }
  })
  
  container.addEventListener('mouseleave', () => {
    isHovering = false
    collapseToasts(container)
  })
  
  // Animate in
  requestAnimationFrame(() => {
    toast.style.transform = 'translateY(0)'
    toast.style.opacity = '1'
    updateToastPositions(container)
  })
  
  // Auto close
  setTimeout(() => {
    closeToast(toast, container)
  }, 4000)
}

function updateToastPositions(container: HTMLElement) {
  if (isHovering) return // Don't update positions while hovering
  
  const toasts = Array.from(container.children).filter(t => !closingToasts.has(t as HTMLElement)) as HTMLElement[]
  const maxVisible = 3
  const toastHeight = 68 // Height of one toast
  
  toasts.forEach((toast, index) => {
    if (closingToasts.has(toast)) return // Skip closing toasts
    
    if (index < maxVisible) {
      // Visible toasts - stack them from bottom
      const offset = index * 8 // Small offset for stacking effect
      const scale = 1 - (index * 0.05)
      const opacity = 1 - (index * 0.15)
      
      toast.style.bottom = `${offset}px`
      toast.style.transform = `translateY(0) scale(${scale})`
      toast.style.opacity = String(opacity)
      toast.style.zIndex = String(100 - index)
    } else {
      // Hidden toasts
      toast.style.bottom = '0'
      toast.style.opacity = '0'
      toast.style.transform = 'translateY(20px) scale(0.85)'
    }
  })
}

function expandToasts(container: HTMLElement) {
  const toasts = Array.from(container.children) as HTMLElement[]
  const toastHeight = 68 // Height of one toast
  const gap = 12 // Gap between expanded toasts
  
  toasts.forEach((toast, index) => {
    if (closingToasts.has(toast)) return // Skip closing toasts
    
    // Calculate position from bottom, spreading upwards
    const bottomPosition = index * (toastHeight + gap)
    
    toast.style.bottom = `${bottomPosition}px`
    toast.style.transform = 'translateY(0) scale(1)'
    toast.style.opacity = '1'
    toast.style.zIndex = String(100 + index) // Higher z-index for toasts on top
  })
}

function collapseToasts(container: HTMLElement) {
  updateToastPositions(container)
}

function closeToast(toast: HTMLElement, container: HTMLElement) {
  // Mark as closing to prevent position updates
  closingToasts.add(toast)
  
  // Disable pointer events to prevent hover during closing
  toast.style.pointerEvents = 'none'
  
  // Slide out to the right (not down)
  toast.style.transform = 'translateX(450px) scale(0.9)'
  toast.style.opacity = '0'
  
  setTimeout(() => {
    closingToasts.delete(toast)
    toast.remove()
    
    if (container.children.length === 0) {
      container.remove()
      toastContainer = null
      toastCount = 0
      closingToasts.clear()
      isHovering = false
    } else {
      // Smooth transition for remaining toasts
      if (!isHovering) {
        updateToastPositions(container)
      }
    }
  }, 600)
}
