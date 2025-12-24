<template>
  <div class="auth-layout">
    <!-- Animated Background -->
    <div class="bg-wrapper">
      <div class="gradient-sphere sphere-1"></div>
      <div class="gradient-sphere sphere-2"></div>
      <div class="gradient-sphere sphere-3"></div>
      <div class="particles">
        <div v-for="n in 20" :key="n" class="particle" :style="getParticleStyle(n)"></div>
      </div>
      <div class="grid-overlay"></div>
    </div>

    <!-- Home Button -->
    <router-link to="/" class="home-btn">
      <div class="home-icon">
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
        </svg>
      </div>
      <span>Trang chủ</span>
    </router-link>

    <!-- Main Content -->
    <div class="auth-content">
      <!-- Glass Card -->
      <div class="auth-card">
        <!-- Left Side - Branding -->
        <div class="brand-side">
          <div class="brand-content">
            <!-- Logo Animation -->
            <div class="logo-wrapper">
              <div class="logo-glow"></div>
              <div class="logo-icon">
                <svg viewBox="0 0 48 48" fill="none">
                  <defs>
                    <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stop-color="#06b6d4" />
                      <stop offset="100%" stop-color="#8b5cf6" />
                    </linearGradient>
                  </defs>
                  <path d="M24 4L4 14v20l20 10 20-10V14L24 4z" fill="url(#logoGrad)" opacity="0.2"/>
                  <path d="M24 4L4 14l20 10 20-10L24 4z" fill="url(#logoGrad)"/>
                  <path d="M4 14v20l20 10V24L4 14z" fill="url(#logoGrad)" opacity="0.7"/>
                  <path d="M44 14v20l-20 10V24l20-10z" fill="url(#logoGrad)" opacity="0.5"/>
                </svg>
              </div>
            </div>

            <h1 class="brand-title">SunnyEdu</h1>
            <p class="brand-tagline">Nền tảng học tập thông minh</p>

            <!-- Features -->
            <div class="features">
              <div class="feature-item">
                <div class="feature-icon">📚</div>
                <span>Khóa học chất lượng</span>
              </div>
              <div class="feature-item">
                <div class="feature-icon">🎯</div>
                <span>Học theo lộ trình</span>
              </div>
              <div class="feature-item">
                <div class="feature-icon">🤖</div>
                <span>AI thông minh</span>
              </div>
            </div>
          </div>

          <!-- Decorative Elements -->
          <div class="brand-decoration">
            <div class="deco-circle deco-1"></div>
            <div class="deco-circle deco-2"></div>
            <div class="deco-line deco-3"></div>
          </div>
        </div>

        <!-- Right Side - Form -->
        <div class="form-side">
          <div class="form-container">
            <!-- Form Header -->
            <div class="form-header">
              <h2 class="form-title">{{ pageTitle }}</h2>
              <p class="form-subtitle">{{ pageSubtitle }}</p>
            </div>

            <!-- Dynamic Form Content -->
            <div class="form-content">
              <router-view />
            </div>

            <!-- Forgot Password Link (only on login) -->
            <div v-if="isLoginPage" class="forgot-link">
              <router-link to="/auth/forgot-password" class="link-button">
                <svg class="link-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"/>
                </svg>
                <span>Quên mật khẩu?</span>
              </router-link>
            </div>

          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const isLoginPage = computed(() => route.path === '/auth/login')

const pageTitle = computed(() => {
  switch (route.path) {
    case '/auth/login': return 'Đăng nhập'
    case '/auth/register': return 'Đăng ký'
    case '/auth/forgot-password': return 'Quên mật khẩu'
    case '/auth/reset-password': return 'Đặt lại mật khẩu'
    default: return route.meta.title || 'Xác thực'
  }
})

const pageSubtitle = computed(() => {
  switch (route.path) {
    case '/auth/login': return 'Chào mừng trở lại! Tiếp tục hành trình học tập'
    case '/auth/register': return 'Tạo tài khoản để bắt đầu học tập'
    case '/auth/forgot-password': return 'Nhập email để khôi phục mật khẩu'
    case '/auth/reset-password': return 'Tạo mật khẩu mới cho tài khoản'
    default: return ''
  }
})

function getParticleStyle(n: number) {
  const size = Math.random() * 4 + 2
  const left = Math.random() * 100
  const delay = Math.random() * 5
  const duration = Math.random() * 10 + 10
  return {
    width: `${size}px`,
    height: `${size}px`,
    left: `${left}%`,
    animationDelay: `${delay}s`,
    animationDuration: `${duration}s`
  }
}
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0a0e1a;
  position: relative;
  overflow: hidden;
  padding: 2rem;
}

/* Background */
.bg-wrapper {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.gradient-sphere {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
}

.sphere-1 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(6, 182, 212, 0.4) 0%, transparent 70%);
  top: -200px;
  left: -200px;
  animation: pulse 8s ease-in-out infinite;
}

.sphere-2 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(139, 92, 246, 0.4) 0%, transparent 70%);
  bottom: -150px;
  right: -150px;
  animation: pulse 10s ease-in-out infinite reverse;
}

.sphere-3 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(236, 72, 153, 0.3) 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: pulse 12s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.1); }
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image: 
    linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size: 50px 50px;
  mask-image: radial-gradient(ellipse at center, black 0%, transparent 70%);
}

.particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  background: rgba(6, 182, 212, 0.6);
  border-radius: 50%;
  bottom: -10px;
  animation: float-up linear infinite;
}

@keyframes float-up {
  0% { transform: translateY(0) rotate(0deg); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(-100vh) rotate(720deg); opacity: 0; }
}

/* Home Button */
.home-btn {
  position: fixed;
  top: 2rem;
  left: 2rem;
  z-index: 100;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.25rem;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 100px;
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.home-btn:hover {
  background: rgba(6, 182, 212, 0.2);
  border-color: rgba(6, 182, 212, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 10px 40px rgba(6, 182, 212, 0.2);
}

.home-icon {
  width: 20px;
  height: 20px;
}

.home-icon svg {
  width: 100%;
  height: 100%;
}

/* Main Content */
.auth-content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 1100px;
}

/* Auth Card */
.auth-card {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 650px;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(40px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 32px;
  overflow: hidden;
  box-shadow: 
    0 0 0 1px rgba(255, 255, 255, 0.05) inset,
    0 25px 80px rgba(0, 0, 0, 0.5),
    0 0 100px rgba(6, 182, 212, 0.1);
  animation: card-appear 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes card-appear {
  from {
    opacity: 0;
    transform: translateY(40px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Brand Side */
.brand-side {
  position: relative;
  background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.brand-content {
  position: relative;
  z-index: 1;
  text-align: center;
}

.logo-wrapper {
  position: relative;
  width: 100px;
  height: 100px;
  margin: 0 auto 2rem;
}

.logo-glow {
  position: absolute;
  inset: -20px;
  background: radial-gradient(circle, rgba(6, 182, 212, 0.4) 0%, transparent 70%);
  filter: blur(20px);
  animation: glow-pulse 3s ease-in-out infinite;
}

@keyframes glow-pulse {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.2); }
}

.logo-icon {
  position: relative;
  width: 100%;
  height: 100%;
  animation: float 4s ease-in-out infinite;
}

.logo-icon svg {
  width: 100%;
  height: 100%;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.brand-title {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #06b6d4 0%, #8b5cf6 50%, #ec4899 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.brand-tagline {
  color: rgba(255, 255, 255, 0.6);
  font-size: 1rem;
  margin-bottom: 3rem;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.feature-item:hover {
  background: rgba(6, 182, 212, 0.1);
  border-color: rgba(6, 182, 212, 0.2);
  transform: translateX(5px);
}

.feature-icon {
  font-size: 1.5rem;
}

/* Brand Decoration */
.brand-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.deco-circle {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.deco-1 {
  width: 300px;
  height: 300px;
  top: -100px;
  right: -100px;
  animation: spin 30s linear infinite;
}

.deco-2 {
  width: 200px;
  height: 200px;
  bottom: -50px;
  left: -50px;
  animation: spin 20s linear infinite reverse;
}

.deco-line {
  position: absolute;
  background: linear-gradient(90deg, transparent, rgba(6, 182, 212, 0.3), transparent);
  height: 1px;
}

.deco-3 {
  width: 100%;
  bottom: 30%;
  animation: slide 5s ease-in-out infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@keyframes slide {
  0%, 100% { opacity: 0.3; transform: translateX(-20%); }
  50% { opacity: 0.8; transform: translateX(20%); }
}

/* Form Side */
.form-side {
  padding: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(10, 14, 26, 0.8);
}

.form-container {
  width: 100%;
  max-width: 380px;
}

.form-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.form-title {
  font-size: 2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #fff 0%, rgba(255,255,255,0.8) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.75rem;
}

.form-subtitle {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.95rem;
}

.form-content {
  animation: form-fade 0.5s ease;
}

@keyframes form-fade {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Forgot Password Link */
.forgot-link {
  margin-top: 2rem;
  text-align: center;
}

.link-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(139, 92, 246, 0.1);
  border: 1px solid rgba(139, 92, 246, 0.2);
  border-radius: 100px;
  color: #a78bfa;
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s ease;
}

.link-button:hover {
  background: rgba(139, 92, 246, 0.2);
  border-color: rgba(139, 92, 246, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(139, 92, 246, 0.2);
}

.link-icon {
  width: 18px;
  height: 18px;
}

/* Bottom Wave */
.bottom-wave {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 120px;
  pointer-events: none;
}

.bottom-wave svg {
  width: 100%;
  height: 100%;
}

/* Responsive */
@media (max-width: 900px) {
  .auth-card {
    grid-template-columns: 1fr;
    max-width: 480px;
    margin: 0 auto;
  }

  .brand-side {
    display: none;
  }

  .form-side {
    padding: 2.5rem;
  }
}

@media (max-width: 480px) {
  .auth-layout {
    padding: 1rem;
  }

  .auth-card {
    border-radius: 24px;
  }

  .form-side {
    padding: 2rem 1.5rem;
  }

  .home-btn {
    top: 1rem;
    left: 1rem;
    padding: 0.5rem 1rem;
  }

  .home-btn span {
    display: none;
  }
}
</style>
