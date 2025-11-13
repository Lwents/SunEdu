<template>
  <div v-show="visible" class="absolute bottom-0 left-0 z-50 h-0.5 w-full overflow-hidden bg-cyan-50/30">
    <div
      class="h-full bg-gradient-to-r from-cyan-400 via-cyan-500 to-cyan-600 shadow-sm shadow-cyan-400/40 transition-all duration-300 ease-out"
      :style="{ width: `${progress}%` }"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const progress = ref(0)
const visible = ref(false)
let timer: number | null = null

function tick() {
  if (timer) clearInterval(timer)
  timer = window.setInterval(() => {
    if (progress.value < 95) {
      progress.value += Math.random() * 10
    }
  }, 200)
}

function start() {
  visible.value = true
  progress.value = 10
  tick()
}

function finish(delay = 300) {
  progress.value = 100
  setTimeout(() => {
    visible.value = false
    progress.value = 0
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }, delay)
}

let removeBefore: (() => void) | null = null
let removeAfter: (() => void) | null = null
let removeError: (() => void) | null = null

onMounted(() => {
  removeBefore = router.beforeEach((to, from, next) => {
    if (to.fullPath !== from.fullPath) start()
    next()
  })
  removeAfter = router.afterEach(() => finish())
  removeError = router.onError(() => finish(0))
})

onUnmounted(() => {
  removeBefore?.()
  removeAfter?.()
  removeError?.()
  if (timer) clearInterval(timer)
})
</script>
