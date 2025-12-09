<template>
  <Teleport to="body">
    <Transition name="celebration-fade">
      <div
        v-if="show"
        class="fixed inset-0 z-[9999] flex items-center justify-center"
        @click="close"
      >
        <!-- Fireworks Canvas - Hiện ngay lập tức -->
        <canvas
          ref="canvasRef"
          class="absolute inset-0 pointer-events-none z-20"
        />
        
        <!-- Overlay -->
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" />
        
        <!-- Content - Delay hiển thị sau pháo hoa -->
        <Transition name="content-slide">
          <div
            v-if="showContent"
            class="relative z-10 text-center px-6 py-10 max-w-lg mx-4"
            @click.stop
          >
          <!-- Trophy Icon -->
          <div class="mb-6 animate-trophy">
            <div class="inline-flex items-center justify-center w-32 h-32 rounded-full bg-gradient-to-br from-yellow-400 via-amber-500 to-orange-500 shadow-2xl shadow-amber-500/50">
              <span class="text-6xl">🏆</span>
            </div>
          </div>
          
          <!-- Congratulations Text -->
          <h1 class="text-4xl md:text-5xl font-bold text-white mb-4 animate-text-glow">
            🎉 Chúc mừng! 🎉
          </h1>
          
          <h2 class="text-2xl md:text-3xl font-semibold text-amber-300 mb-6">
            Hoàn thành khóa học
          </h2>
          
          <p class="text-xl text-white/90 mb-2 font-medium">
            {{ courseTitle }}
          </p>
          
          <!-- Praise Message -->
          <div class="mt-6 p-4 rounded-2xl bg-white/10 backdrop-blur-sm border border-white/20">
            <p class="text-lg text-white/95 leading-relaxed">
              {{ praiseMessage }}
            </p>
          </div>
          
          <!-- Stars -->
          <div class="flex justify-center gap-2 mt-6 mb-8">
            <span v-for="i in 5" :key="i" class="text-4xl animate-star" :style="{ animationDelay: `${i * 0.1}s` }">⭐</span>
          </div>
          
          <!-- Close Button -->
          <button
            class="px-8 py-3 bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-600 hover:to-teal-600 text-white font-semibold rounded-full shadow-lg shadow-emerald-500/30 transition-all duration-300 hover:scale-105"
            @click="close"
          >
            Tuyệt vời! 🚀
          </button>
        </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, onUnmounted } from 'vue'

const props = defineProps<{
  show: boolean
  courseTitle: string
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const canvasRef = ref<HTMLCanvasElement | null>(null)
const showContent = ref(false)
let animationId: number | null = null
let particles: Particle[] = []
let contentTimer: ReturnType<typeof setTimeout> | null = null

const praiseMessages = [
  'Bạn thật xuất sắc! Kiến thức đã được nạp đầy, sẵn sàng chinh phục những thử thách mới! 💪',
  'Tuyệt vời! Bạn đã hoàn thành xuất sắc khóa học. Hãy tự hào về bản thân mình nhé! 🌟',
  'Chăm chỉ và kiên trì - đó là bí quyết thành công của bạn! Tiếp tục phát huy nhé! 🎯',
  'Bạn là ngôi sao sáng nhất! Mỗi bài học là một bước tiến, và bạn đã đi được cả chặng đường! ⭐',
  'Phi thường! Bạn đã chứng minh rằng không có gì là không thể khi có quyết tâm! 🏆',
]

const praiseMessage = ref(praiseMessages[Math.floor(Math.random() * praiseMessages.length)])

interface Particle {
  x: number
  y: number
  vx: number
  vy: number
  color: string
  size: number
  life: number
  maxLife: number
  type: 'spark' | 'trail'
}

const colors = [
  '#ff0000', '#ff7700', '#ffff00', '#00ff00', '#00ffff', 
  '#0077ff', '#7700ff', '#ff00ff', '#ff0077', '#ffffff',
  '#ffd700', '#ff69b4', '#00ff7f', '#ff4500', '#9400d3'
]

function createFirework(x: number, y: number) {
  const particleCount = 80 + Math.random() * 40
  const color = colors[Math.floor(Math.random() * colors.length)]
  
  for (let i = 0; i < particleCount; i++) {
    const angle = (Math.PI * 2 * i) / particleCount + Math.random() * 0.2
    const speed = 2 + Math.random() * 4
    const life = 60 + Math.random() * 40
    
    particles.push({
      x,
      y,
      vx: Math.cos(angle) * speed,
      vy: Math.sin(angle) * speed,
      color: Math.random() > 0.3 ? color : colors[Math.floor(Math.random() * colors.length)],
      size: 2 + Math.random() * 3,
      life,
      maxLife: life,
      type: 'spark'
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
  
  // Clear with fade effect
  ctx.fillStyle = 'rgba(0, 0, 0, 0.15)'
  ctx.fillRect(0, 0, canvas.width, canvas.height)
  
  // Update and draw particles
  particles = particles.filter(p => {
    p.x += p.vx
    p.y += p.vy
    p.vy += 0.05 // gravity
    p.vx *= 0.99 // friction
    p.life--
    
    if (p.life <= 0) return false
    
    const alpha = p.life / p.maxLife
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.size * alpha, 0, Math.PI * 2)
    ctx.fillStyle = p.color + Math.floor(alpha * 255).toString(16).padStart(2, '0')
    ctx.fill()
    
    // Glow effect
    ctx.shadowBlur = 10
    ctx.shadowColor = p.color
    
    return true
  })
  
  ctx.shadowBlur = 0
  
  animationId = requestAnimationFrame(animate)
}

function launchFireworks() {
  const canvas = canvasRef.value
  if (!canvas) return
  
  const w = window.innerWidth
  const h = window.innerHeight
  
  // Initial burst
  for (let i = 0; i < 5; i++) {
    setTimeout(() => {
      createFirework(
        w * 0.2 + Math.random() * w * 0.6,
        h * 0.2 + Math.random() * h * 0.3
      )
    }, i * 200)
  }
  
  // Continuous fireworks
  const interval = setInterval(() => {
    if (!props.show) {
      clearInterval(interval)
      return
    }
    createFirework(
      w * 0.1 + Math.random() * w * 0.8,
      h * 0.15 + Math.random() * h * 0.35
    )
  }, 400)
  
  // Stop after 10 seconds
  setTimeout(() => clearInterval(interval), 10000)
}

function close() {
  emit('close')
}

watch(() => props.show, (newVal) => {
  if (newVal) {
    praiseMessage.value = praiseMessages[Math.floor(Math.random() * praiseMessages.length)]
    particles = []
    showContent.value = false // Ẩn content trước
    
    // Bắt đầu pháo hoa ngay lập tức
    setTimeout(() => {
      animate()
      launchFireworks()
    }, 100)
    
    // Delay 1.5s rồi mới hiện content (sau khi pháo hoa đã bắn)
    contentTimer = setTimeout(() => {
      showContent.value = true
    }, 1500)
  } else {
    // Reset khi đóng
    showContent.value = false
    if (contentTimer) {
      clearTimeout(contentTimer)
      contentTimer = null
    }
    if (animationId) {
      cancelAnimationFrame(animationId)
      animationId = null
    }
    particles = []
  }
})

onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  if (contentTimer) {
    clearTimeout(contentTimer)
  }
})
</script>

<style scoped>
.celebration-fade-enter-active,
.celebration-fade-leave-active {
  transition: opacity 0.5s ease;
}

.celebration-fade-enter-from,
.celebration-fade-leave-to {
  opacity: 0;
}

/* Content slide up animation - hiện sau pháo hoa */
.content-slide-enter-active {
  transition: all 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.content-slide-leave-active {
  transition: all 0.3s ease-out;
}

.content-slide-enter-from {
  opacity: 0;
  transform: translateY(60px) scale(0.8);
}

.content-slide-leave-to {
  opacity: 0;
  transform: translateY(-30px) scale(0.9);
}

@keyframes bounce-in {
  0% {
    transform: scale(0.3);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.animate-bounce-in {
  animation: bounce-in 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

@keyframes trophy {
  0%, 100% {
    transform: rotate(-5deg) scale(1);
  }
  25% {
    transform: rotate(5deg) scale(1.1);
  }
  50% {
    transform: rotate(-5deg) scale(1);
  }
  75% {
    transform: rotate(5deg) scale(1.1);
  }
}

.animate-trophy {
  animation: trophy 2s ease-in-out infinite;
}

@keyframes text-glow {
  0%, 100% {
    text-shadow: 0 0 20px rgba(255, 215, 0, 0.8), 0 0 40px rgba(255, 215, 0, 0.4);
  }
  50% {
    text-shadow: 0 0 40px rgba(255, 215, 0, 1), 0 0 80px rgba(255, 215, 0, 0.6);
  }
}

.animate-text-glow {
  animation: text-glow 1.5s ease-in-out infinite;
}

@keyframes star {
  0%, 100% {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
  50% {
    transform: scale(1.3) rotate(15deg);
    opacity: 0.8;
  }
}

.animate-star {
  animation: star 1s ease-in-out infinite;
}
</style>
