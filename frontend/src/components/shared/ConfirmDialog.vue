<template>
  <Teleport to="body">
    <Transition name="fade">
      <div
        v-if="isOpen"
        class="fixed inset-0 z-[99999] flex items-center justify-center bg-black/50 p-4"
        @click.self="handleCancel"
      >
        <Transition name="scale">
          <div
            v-if="isOpen"
            class="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl"
            @click.stop
          >
            <!-- Icon -->
            <div class="mb-4 flex justify-center">
              <div
                class="flex h-12 w-12 items-center justify-center rounded-full"
                :class="iconClass"
              >
                <svg
                  v-if="type === 'danger'"
                  class="h-6 w-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
                <svg
                  v-else
                  class="h-6 w-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
            </div>

            <!-- Title -->
            <h3 class="mb-2 text-center text-lg font-bold text-gray-900">
              {{ title }}
            </h3>

            <!-- Message -->
            <p class="mb-6 text-center text-sm text-gray-600">
              {{ message }}
            </p>

            <!-- Actions -->
            <div class="flex justify-end gap-3">
              <button
                type="button"
                class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
                @click="handleCancel"
              >
                {{ cancelText }}
              </button>
              <button
                type="button"
                class="rounded-lg px-4 py-2 text-sm font-medium text-white transition"
                :class="confirmButtonClass"
                @click="handleConfirm"
              >
                {{ confirmText }}
              </button>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

type ConfirmType = 'danger' | 'warning' | 'info'

interface Props {
  title?: string
  message: string
  type?: ConfirmType
  confirmText?: string
  cancelText?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: 'Xác nhận',
  type: 'info',
  confirmText: 'Xác nhận',
  cancelText: 'Hủy'
})

const emit = defineEmits<{
  confirm: []
  cancel: []
}>()

const isOpen = ref(true)

const iconClass = computed(() => {
  switch (props.type) {
    case 'danger':
      return 'bg-rose-100 text-rose-600'
    case 'warning':
      return 'bg-amber-100 text-amber-600'
    default:
      return 'bg-blue-100 text-blue-600'
  }
})

const confirmButtonClass = computed(() => {
  switch (props.type) {
    case 'danger':
      return 'bg-rose-600 hover:bg-rose-700'
    case 'warning':
      return 'bg-amber-600 hover:bg-amber-700'
    default:
      return 'bg-cyan-600 hover:bg-cyan-700'
  }
})

function handleConfirm() {
  isOpen.value = false
  emit('confirm')
}

function handleCancel() {
  isOpen.value = false
  emit('cancel')
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.scale-enter-active,
.scale-leave-active {
  transition: all 0.2s;
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>

