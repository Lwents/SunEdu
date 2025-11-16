// Confirm Dialog Utility
// Usage: const confirmed = await showConfirm('Message here', { title: 'Title', type: 'danger' })

import { createApp, h } from 'vue'
import ConfirmDialog from '@/components/shared/ConfirmDialog.vue'

export interface ConfirmOptions {
  title?: string
  message: string
  type?: 'danger' | 'warning' | 'info'
  confirmText?: string
  cancelText?: string
}

export function showConfirm(options: ConfirmOptions | string): Promise<boolean> {
  return new Promise((resolve) => {
    // Normalize options
    const opts: ConfirmOptions =
      typeof options === 'string'
        ? { message: options }
        : options

    // Create a temporary container
    const container = document.createElement('div')
    document.body.appendChild(container)

    // Create app instance
    const app = createApp({
      setup() {
        const handleConfirm = () => {
          app.unmount()
          container.remove()
          resolve(true)
        }

        const handleCancel = () => {
          app.unmount()
          container.remove()
          resolve(false)
        }

        return () =>
          h(ConfirmDialog, {
            title: opts.title,
            message: opts.message,
            type: opts.type || 'info',
            confirmText: opts.confirmText,
            cancelText: opts.cancelText,
            onConfirm: handleConfirm,
            onCancel: handleCancel
          })
      }
    })

    app.mount(container)
  })
}

