<template>
  <canvas
    ref="canvasRef"
    class="fixed inset-0 pointer-events-none z-50"
  />
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'

const props = defineProps<{
  active: boolean
  intensity?: 'low' | 'medium' | 'high'
}>()

const canvasRef = ref<HTMLCanvasElement | null>(null)
let animationId: number | null = null
let particles: Particle[] = []
let fireworkInterval: ReturnType<typeof setInterval> | null = null

interface Particle {
  x: number
  y: number
  vx: number
  vy: number
  color: string
  size: number
  life: number
  maxLife: number
  alpha: number
}

const colors = [
  '#FFD700', '#FFA500', '#FF6347', '#FF69B4', '#00CED1',
  '#7B68EE', '#32CD32', '#FF4500', '#9400D3', '#00FF7F',
  '#FF1493', '#00BFFF', '#ADFF2F', '#FF8C00', '#E6E6FA'
]

function createFirework(x: number, y: number) {
  const particleCount = 60 + Math.random() * 30
  const color = colors[Math.floor(Math.random() * colors.length)]
  
  for (let i = 0; i < particleCount; i++) {
    const angle = (Math.PI * 2 * i) / particleCount + Math.random() * 0.3
    const speed = 2 + Math.random() * 3
    const life = 50 + Math.random() * 30
    
    particles.push({
      x,
      y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      color: Math.random() > 0.4 ? color : colors[Math.floor(Math.random() * colors.length)],
      size: 2 + Math.random() * 2,
      life,
      maxLife: life,
      alpha: 1
    })
  }
}

function animate() {
  const canvas = canvasRef.value
  if (!canvas) return
  
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  
  canvas.width = window.innerWidth
  canvas.height = window.innerHeight
  
  // Clear with fade
  ctx.fillStyle = 'rgba(0, 0, 0, 0.1)'
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  // Update and draw particles
  particles = particles.filter(p => {
    p.x += p.vx
    p.y += p.vy
    p.vy += 0.06 // gravity
    p.vx *= 0.98 // friction
    p.life--
    p.alpha = p.life / p.maxLife
    
    if (p.life <= 0) return false
    
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.size * p.alpha, 0, Math.PI * 2)
    ctx.fillStyle = p.color
    ctx.globalAlpha = p.alpha
    ctx.fill()
    
    // Glow
    ctx.shadowBlur = 8
    ctx.shadowColor = p.color
    
    return true
  })
  
  ctx.globalAlpha = 1
  ctx.shadowBlur = 0
  
  if (props.active) {
    animationId = requestAnimationFrame(animate)
  }
}

function launchFireworks() {
  if (!props.active) return
  
  const w = window.innerWidth
  const h = window.innerHeight
  
  // Initial burst - nhiều pháo hoa hơn
  for (let i = 0; i < 8; i++) {
    setTimeout(() => {
      if (!props.active) return
      createFirework(
        w * 0.1 + Math.random() * w * 0.8,
        h * 0.1 + Math.random() * h * 0.4
      )
    }, i * 150)
  }
  
  // Continuous fireworks
  const intervalTime = props.intensity === 'high' ? 300 : props.intensity === 'medium' ? 500 : 800
  fireworkInterval = setInterval(() => {
    if (!props.active) {
      if (fireworkInterval) clearInterval(fireworkInterval)
      return
    }
    createFirework(
      w * 0.1 + Math.random() * w * 0.8,
      h * 0.1 + Math.random() * h * 0.4
    )
  }, intervalTime)
}

function start() {
  particles = []
  animate()
  launchFireworks()
}

function stop() {
  if (animationId) {
    cancelAnimationFrame(animationId)
    animationId = null
  }
  if (fireworkInterval) {
    clearInterval(fireworkInterval)
    fireworkInterval = null
  }
  particles = []
  
  // Clear canvas
  const canvas = canvasRef.value
  if (canvas) {
    const ctx = canvas.getContext('2d')
    if (ctx) {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
    }
  }
}

watch(() => props.active, (newVal) => {
  if (newVal) {
    start()
  } else {
    stop()
  }
})

onMounted(() => {
  if (props.active) {
    start()
  }
})

onUnmounted(() => {
  stop()
})
</script>
