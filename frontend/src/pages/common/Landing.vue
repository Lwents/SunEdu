<template>
  <div class="font-sans text-gray-900 bg-slate-950 overflow-x-hidden">
    <!-- Floating 3D Elements Background -->
    <div class="fixed inset-0 pointer-events-none overflow-hidden z-0">
      <div class="absolute top-20 left-10 w-32 h-32 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 rounded-3xl transform rotate-12 animate-float-slow"></div>
      <div class="absolute top-40 right-20 w-24 h-24 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-2xl transform -rotate-12 animate-float-medium"></div>
      <div class="absolute bottom-40 left-1/4 w-20 h-20 bg-gradient-to-br from-yellow-500/20 to-orange-500/20 rounded-xl transform rotate-45 animate-float-fast"></div>
    </div>

    <!-- Header -->
    <header class="fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-slate-950/70 border-b border-white/10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 py-3 sm:py-4 flex justify-between items-center">
        <LogoSmartEdu :size="64" class="w-16 sm:w-[90px]" />
        <nav class="hidden lg:flex items-center space-x-8">
          <a v-for="item in navItems" :key="item.id" :href="'#' + item.id"
            class="text-gray-300 hover:text-white font-medium transition-all duration-300 hover:scale-105"
            @click.prevent="scrollToSection(item.id)">{{ item.label }}</a>
        </nav>
        <router-link to="/auth/login">
          <button class="px-6 py-2.5 sm:px-8 sm:py-3 rounded-xl font-semibold text-sm sm:text-base bg-gradient-to-r from-cyan-500 via-purple-500 to-pink-500 text-white hover:scale-105 transition-all duration-300 flex items-center gap-2">
            <svg class="w-4 h-4 sm:w-5 sm:h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"/>
            </svg>
            Đăng nhập
          </button>
        </router-link>
      </div>
    </header>

    <!-- Hero Section -->
    <section id="home" class="min-h-screen pt-24 sm:pt-32 pb-16 px-4 sm:px-6 relative overflow-hidden">
      <div class="absolute top-1/4 -left-32 w-96 h-96 bg-cyan-500/30 rounded-full blur-[128px] animate-pulse"></div>
      <div class="absolute bottom-1/4 -right-32 w-96 h-96 bg-purple-500/30 rounded-full blur-[128px] animate-pulse"></div>

      <div class="max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center relative z-10">
        <div class="space-y-6 sm:space-y-8">
          <div class="inline-flex items-center gap-2 px-4 py-2 bg-cyan-500/10 border border-cyan-500/20 rounded-full">
            <span class="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></span>
            <span class="text-cyan-400 font-medium text-sm">Nền tảng học tập #1 cho trẻ em</span>
          </div>
          
          <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-black leading-tight">
            <span class="text-white">Học tập</span><br>
            <span class="bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">thông minh</span><br>
            <span class="text-white">cùng SMARTEDU</span>
          </h1>
          
          <p class="text-lg sm:text-xl text-gray-400 leading-relaxed max-w-xl">
            Khám phá hành trình học tập đầy màu sắc với hơn <span class="text-cyan-400 font-semibold">10,000+</span> bài học tương tác.
          </p>

          <div class="flex flex-wrap gap-4 pt-4">
            <router-link to="/auth/login">
              <button class="px-8 py-4 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-2xl font-bold text-lg text-white hover:scale-105 hover:shadow-[0_0_40px_rgba(6,182,212,0.5)] transition-all duration-300 flex items-center gap-2">
                Bắt đầu học ngay
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                </svg>
              </button>
            </router-link>
            <button class="px-8 py-4 border-2 border-white/20 hover:border-cyan-400/50 rounded-2xl font-bold text-lg text-white hover:bg-white/5 transition-all duration-300 flex items-center gap-2">
              <div class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center">
                <svg class="w-5 h-5 text-cyan-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z"/>
                </svg>
              </div>
              Xem video
            </button>
          </div>

          <div class="flex items-center gap-8 pt-8">
            <div v-for="stat in heroStats" :key="stat.label" class="text-center">
              <div class="text-2xl sm:text-3xl font-black bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">{{ stat.value }}</div>
              <div class="text-sm text-gray-500">{{ stat.label }}</div>
            </div>
          </div>
        </div>

        <div class="relative">
          <div class="relative w-full aspect-square max-w-lg mx-auto flex items-center justify-center">
            <div class="isometric-container">
              <div class="isometric-card bg-gradient-to-br from-cyan-500 to-purple-600 w-64 h-64 rounded-3xl shadow-2xl flex items-center justify-center p-1">
                <img src="https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=600&h=600&fit=crop" alt="Happy children learning" class="w-full h-full object-cover rounded-2xl"/>
              </div>
              <div class="absolute -top-8 -right-8 w-20 h-20 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-2xl shadow-xl shadow-orange-500/30 flex items-center justify-center text-3xl animate-bounce-slow">🎮</div>
              <div class="absolute -bottom-6 -left-6 w-16 h-16 bg-gradient-to-br from-green-400 to-emerald-500 rounded-xl shadow-xl shadow-green-500/30 flex items-center justify-center text-2xl animate-bounce-slow">📚</div>
              <div class="absolute top-1/2 -right-12 w-14 h-14 bg-gradient-to-br from-pink-400 to-rose-500 rounded-lg shadow-xl shadow-pink-500/30 flex items-center justify-center text-xl animate-bounce-slow">⭐</div>
              <div class="absolute -top-4 left-1/4 w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg shadow-xl shadow-cyan-500/30 flex items-center justify-center text-lg animate-bounce-slow">🏆</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-16 relative z-10">
      <div class="max-w-7xl mx-auto px-4 sm:px-6">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div v-for="stat in stats" :key="stat.label" class="p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm hover:border-cyan-500/50 hover:scale-105 transition-all duration-500">
            <div class="text-center">
              <div class="text-4xl mb-3">{{ stat.icon }}</div>
              <div class="text-2xl sm:text-3xl font-black text-white mb-1">{{ stat.value }}</div>
              <div class="text-sm text-gray-400">{{ stat.label }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-20 sm:py-32 px-4 sm:px-6 relative">
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-purple-500/20 rounded-full blur-[150px]"></div>
      <div class="max-w-7xl mx-auto relative z-10">
        <div class="text-center mb-16">
          <div class="inline-flex items-center gap-2 px-4 py-2 bg-purple-500/10 border border-purple-500/20 rounded-full mb-6">
            <span class="text-purple-400 font-medium text-sm">✨ Tính năng nổi bật</span>
          </div>
          <h2 class="text-3xl sm:text-4xl md:text-5xl font-black text-white mb-4">
            Tại sao chọn <span class="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">SMARTEDU</span>?
          </h2>
          <p class="text-lg text-gray-400 max-w-2xl mx-auto">Nền tảng học tập toàn diện với công nghệ AI</p>
        </div>

        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 sm:gap-8">
          <div v-for="feature in features" :key="feature.title" class="group p-8 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-sm hover:border-cyan-500/30 hover:-translate-y-2 transition-all duration-500">
            <div class="w-16 h-16 rounded-2xl mb-6 flex items-center justify-center text-3xl group-hover:scale-110 group-hover:rotate-6 transition-all duration-500" :class="feature.iconBg">{{ feature.icon }}</div>
            <h3 class="text-xl font-bold text-white mb-3">{{ feature.title }}</h3>
            <p class="text-gray-400 leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Courses Section -->
    <section id="courses" class="py-20 sm:py-32 px-4 sm:px-6 relative">
      <div class="absolute bottom-0 right-0 w-[600px] h-[400px] bg-cyan-500/20 rounded-full blur-[150px]"></div>
      <div class="max-w-7xl mx-auto relative z-10">
        <div class="text-center mb-16">
          <div class="inline-flex items-center gap-2 px-4 py-2 bg-green-500/10 border border-green-500/20 rounded-full mb-6">
            <span class="text-green-400 font-medium text-sm">📚 Khóa học đa dạng</span>
          </div>
          <h2 class="text-3xl sm:text-4xl md:text-5xl font-black text-white mb-4">
            Khám phá <span class="bg-gradient-to-r from-green-400 to-cyan-400 bg-clip-text text-transparent">thế giới kiến thức</span>
          </h2>
        </div>

        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="course in modernCourses" :key="course.title" class="group relative overflow-hidden rounded-3xl hover:-translate-y-2 hover:shadow-[0_0_60px_rgba(6,182,212,0.3)] transition-all duration-500">
            <div class="absolute inset-0 bg-gradient-to-br opacity-90" :class="course.gradient"></div>
            <div class="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-colors duration-500"></div>
            <div class="relative p-8 h-full flex flex-col justify-between min-h-[300px]">
              <div>
                <div class="text-5xl mb-4 group-hover:scale-110 group-hover:rotate-12 transition-all duration-500">{{ course.icon }}</div>
                <h3 class="text-2xl font-bold text-white mb-3">{{ course.title }}</h3>
                <p class="text-white/80 mb-4">{{ course.description }}</p>
                <div class="flex items-center gap-4 text-sm text-white/70">
                  <span>📚 {{ course.lessons }} bài</span>
                  <span>⏱️ {{ course.duration }}</span>
                </div>
              </div>
              <router-link to="/auth/login" class="mt-6">
                <button class="w-full py-3 bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-xl font-semibold text-white transition-all duration-300">Khám phá ngay</button>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Interactive Learning -->
    <section class="py-20 sm:py-32 px-4 sm:px-6 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950"></div>
      <div class="absolute top-1/2 left-0 w-[500px] h-[500px] bg-blue-500/20 rounded-full blur-[150px] -translate-y-1/2"></div>
      <div class="max-w-7xl mx-auto relative z-10">
        <div class="grid lg:grid-cols-2 gap-12 items-center">
          <div class="space-y-6">
            <div class="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/10 border border-blue-500/20 rounded-full">
              <span class="text-blue-400 font-medium text-sm">🎮 Học qua chơi</span>
            </div>
            <h2 class="text-3xl sm:text-4xl md:text-5xl font-black text-white">
              Học tập tương tác với <span class="bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">trò chơi</span>
            </h2>
            <p class="text-lg text-gray-400 leading-relaxed">500+ trò chơi giáo dục giúp trẻ học mà chơi, chơi mà học.</p>
            <ul class="space-y-4">
              <li v-for="benefit in interactiveBenefits" :key="benefit" class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center text-white text-sm font-bold shadow-lg shadow-cyan-500/30">✓</div>
                <span class="text-gray-300 text-lg">{{ benefit }}</span>
              </li>
            </ul>
          </div>
          <div class="relative">
            <div class="grid grid-cols-2 gap-4">
              <div class="space-y-4">
                <div class="overflow-hidden rounded-2xl hover:scale-105 transition-all duration-500 border-2 border-cyan-500/30 shadow-lg shadow-cyan-500/20">
                  <img src="https://images.unsplash.com/photo-1588072432836-e10032774350?w=400&h=300&fit=crop" alt="Learning" class="w-full h-48 object-cover"/>
                </div>
                <div class="overflow-hidden rounded-2xl hover:scale-105 transition-all duration-500 translate-y-8 border-2 border-purple-500/30 shadow-lg shadow-purple-500/20">
                  <img src="https://images.unsplash.com/photo-1497486751825-1233686d5d80?w=400&h=350&fit=crop" alt="Children" class="w-full h-56 object-cover"/>
                </div>
              </div>
              <div class="space-y-4 pt-8">
                <div class="overflow-hidden rounded-2xl hover:scale-105 transition-all duration-500 border-2 border-pink-500/30 shadow-lg shadow-pink-500/20">
                  <img src="https://images.unsplash.com/photo-1509062522246-3755977927d7?w=400&h=350&fit=crop" alt="Games" class="w-full h-56 object-cover"/>
                </div>
                <div class="overflow-hidden rounded-2xl hover:scale-105 transition-all duration-500 border-2 border-yellow-500/30 shadow-lg shadow-yellow-500/20">
                  <img src="https://images.unsplash.com/photo-1544776193-352d25ca82cd?w=400&h=300&fit=crop" alt="Fun" class="w-full h-48 object-cover"/>
                </div>
              </div>
            </div>
            <div class="absolute -bottom-4 left-1/2 -translate-x-1/2 px-6 py-3 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full shadow-xl shadow-cyan-500/30 animate-bounce-slow">
              <span class="text-white font-bold">500+ Trò chơi</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials -->
    <section id="testimonials" class="py-20 sm:py-32 px-4 sm:px-6 relative overflow-hidden">
      <div class="absolute top-1/2 right-0 w-[600px] h-[600px] bg-purple-500/20 rounded-full blur-[150px] -translate-y-1/2"></div>
      <div class="max-w-7xl mx-auto relative z-10">
        <div class="text-center mb-16">
          <div class="inline-flex items-center gap-2 px-4 py-2 bg-yellow-500/10 border border-yellow-500/20 rounded-full mb-6">
            <span class="text-yellow-400 font-medium text-sm">💬 Đánh giá từ phụ huynh</span>
          </div>
          <h2 class="text-3xl sm:text-4xl md:text-5xl font-black text-white mb-4">
            Phụ huynh nói gì về <span class="bg-gradient-to-r from-yellow-400 to-orange-400 bg-clip-text text-transparent">chúng tôi</span>?
          </h2>
          <p class="text-lg text-gray-400">Hơn <span class="text-yellow-400 font-bold">18,547+</span> đánh giá tích cực</p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
          <div v-for="stat in testimonialStats" :key="stat.label" class="p-6 rounded-2xl border border-white/10 backdrop-blur-sm text-center hover:scale-105 hover:border-cyan-500/30 transition-all duration-300" :class="stat.bgClass">
            <div class="text-3xl sm:text-4xl font-black mb-2" :class="stat.textClass">{{ stat.value }}</div>
            <div v-if="stat.showStars" class="flex justify-center gap-1 mb-2">
              <span v-for="star in 5" :key="star" class="text-yellow-400 text-lg">★</span>
            </div>
            <div v-else class="text-2xl mb-2">{{ stat.emoji }}</div>
            <div class="text-sm text-gray-300 font-medium">{{ stat.label }}</div>
          </div>
        </div>

        <div class="space-y-6 overflow-hidden">
          <div class="flex gap-6 animate-scroll-right">
            <template v-for="n in 2" :key="'row1-' + n">
              <div v-for="t in testimonialsRow1" :key="t.name + n" class="flex-shrink-0 w-[350px] sm:w-[400px] p-6 rounded-2xl bg-gradient-to-br from-white/10 to-white/5 border border-white/10 backdrop-blur-sm hover:border-cyan-500/30 transition-all duration-300">
                <div class="flex items-center gap-4 mb-4">
                  <div class="w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold text-white shadow-lg" :class="t.avatarBg">{{ t.initial }}</div>
                  <div>
                    <div class="font-bold text-white flex items-center gap-2">
                      {{ t.name }}
                      <svg class="w-4 h-4 text-cyan-400" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                    </div>
                    <div class="text-sm text-gray-400">{{ t.role }}</div>
                  </div>
                </div>
                <div class="flex gap-1 mb-3">
                  <span v-for="star in t.rating" :key="star" class="text-yellow-400 text-lg">★</span>
                </div>
                <p class="text-gray-300 leading-relaxed">"{{ t.text }}"</p>
              </div>
            </template>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 sm:py-32 px-4 sm:px-6 relative overflow-hidden">
      <div class="absolute inset-0 bg-gradient-to-r from-slate-900 via-purple-900 to-slate-900"></div>
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-cyan-500/20 via-transparent to-transparent"></div>
      <div class="absolute top-10 left-10 w-20 h-20 bg-cyan-500/20 rounded-full blur-xl animate-float-slow"></div>
      <div class="absolute bottom-10 right-10 w-32 h-32 bg-purple-500/20 rounded-full blur-xl animate-float-medium"></div>
      <div class="absolute top-1/2 left-1/4 w-24 h-24 bg-pink-500/20 rounded-full blur-xl animate-float-fast"></div>
      <div class="max-w-4xl mx-auto text-center relative z-10">
        <h2 class="text-3xl sm:text-4xl md:text-5xl font-black text-white mb-6">Sẵn sàng bắt đầu hành trình học tập?</h2>
        <p class="text-xl text-gray-300 mb-10">Tham gia cùng hàng nghìn phụ huynh và học sinh đã tin tưởng SMARTEDU</p>
        <div class="flex flex-wrap justify-center gap-4">
          <router-link to="/auth/login">
            <button class="px-10 py-4 bg-gradient-to-r from-cyan-500 to-purple-500 text-white rounded-2xl font-bold text-lg hover:shadow-[0_0_40px_rgba(6,182,212,0.5)] hover:scale-105 transition-all duration-300">Đăng nhập ngay</button>
          </router-link>
          <button class="px-10 py-4 bg-white/10 backdrop-blur-sm text-white border border-white/20 rounded-2xl font-bold text-lg hover:bg-white/20 hover:border-cyan-400/50 transition-all duration-300">Tư vấn ngay</button>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-16 px-4 sm:px-6 bg-slate-950 border-t border-white/10">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
          <div class="col-span-2 md:col-span-1">
            <LogoSmartEdu :size="64" class="mb-4" />
            <p class="text-gray-400 text-sm">Nền tảng học tập trực tuyến hàng đầu dành cho học sinh tiểu học.</p>
          </div>
          <div>
            <h4 class="text-white font-bold mb-4">Sản phẩm</h4>
            <ul class="space-y-2 text-sm text-gray-400">
              <li><a href="#" class="hover:text-cyan-400 transition-colors">Khóa học</a></li>
              <li><a href="#" class="hover:text-cyan-400 transition-colors">Trò chơi</a></li>
              <li><a href="#" class="hover:text-cyan-400 transition-colors">Video</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-white font-bold mb-4">Công ty</h4>
            <ul class="space-y-2 text-sm text-gray-400">
              <li><a href="#" class="hover:text-cyan-400 transition-colors">Giới thiệu</a></li>
              <li><a href="#" class="hover:text-cyan-400 transition-colors">Blog</a></li>
              <li><a href="#" class="hover:text-cyan-400 transition-colors">Liên hệ</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-white font-bold mb-4">Kết nối</h4>
            <div class="flex gap-3 mb-4">
              <a href="https://www.facebook.com/vulekien2004" target="_blank" class="w-10 h-10 rounded-xl bg-white/5 hover:bg-blue-500 flex items-center justify-center text-gray-400 hover:text-white transition-all duration-300">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
              </a>
              <a href="https://www.instagram.com/ne_kinn" target="_blank" class="w-10 h-10 rounded-xl bg-white/5 hover:bg-pink-500 flex items-center justify-center text-gray-400 hover:text-white transition-all duration-300">
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
              </a>
            </div>
            <p class="text-gray-400 text-sm">kiritovn777@gmail.com</p>
            <p class="text-gray-400 text-sm">0966148388</p>
          </div>
        </div>
        <div class="border-t border-white/10 pt-8 text-center">
          <p class="text-gray-500 text-sm">© 2025 SMARTEDU. All rights reserved.</p>
        </div>
      </div>
    </footer>

    <!-- Scroll to Top -->
    <button v-if="showScrollTop" @click="scrollToTop" class="fixed bottom-8 right-8 z-50 w-14 h-14 bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full shadow-lg flex items-center justify-center text-white hover:scale-110 transition-all duration-300">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18"/></svg>
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import LogoSmartEdu from '@/components/ui/LogoSmartEdu.vue'

const showScrollTop = ref(false)

const navItems = [
  { id: 'home', label: 'Trang chủ' },
  { id: 'features', label: 'Tính năng' },
  { id: 'courses', label: 'Khóa học' },
  { id: 'testimonials', label: 'Đánh giá' },
]

const heroStats = [
  { value: '5,000+', label: 'Học sinh' },
  { value: '1,000+', label: 'Bài học' },
  { value: '4.9⭐', label: 'Đánh giá' },
]

const stats = ref([
  { icon: '👨‍👩‍👧‍👦', value: '5,000+', label: 'Học sinh' },
  { icon: '📚', value: '1,000+', label: 'Bài học' },
  { icon: '🎮', value: '500+', label: 'Trò chơi' },
  { icon: '⭐', value: '4.9/5', label: 'Đánh giá' },
])

const features = ref([
  { icon: '🤖', title: 'AI cá nhân hóa', description: 'Hệ thống AI thông minh tạo lộ trình học phù hợp với khả năng của từng bé', iconBg: 'bg-gradient-to-br from-cyan-500/20 to-blue-500/20' },
  { icon: '📊', title: 'Theo dõi tiến độ', description: 'Dashboard chi tiết giúp phụ huynh nắm bắt quá trình học của con', iconBg: 'bg-gradient-to-br from-green-500/20 to-teal-500/20' },
  { icon: '🎨', title: 'Nội dung đa dạng', description: 'Video hoạt hình, bài tập tương tác và quiz thú vị cho mọi môn học', iconBg: 'bg-gradient-to-br from-yellow-500/20 to-orange-500/20' },
  { icon: '🎮', title: 'Học qua trò chơi', description: '500+ trò chơi giáo dục giúp trẻ học mà chơi, chơi mà học', iconBg: 'bg-gradient-to-br from-purple-500/20 to-pink-500/20' },
  { icon: '🏆', title: 'Hệ thống phần thưởng', description: 'Huy hiệu, điểm thưởng và bảng xếp hạng tạo động lực học tập', iconBg: 'bg-gradient-to-br from-amber-500/20 to-red-500/20' },
  { icon: '👨‍👩‍👧', title: 'Kết nối gia đình', description: 'Phụ huynh có thể theo dõi và tham gia vào quá trình học của con', iconBg: 'bg-gradient-to-br from-rose-500/20 to-pink-500/20' },
])

const modernCourses = ref([
  { icon: '🔢', title: 'Toán học', description: 'Từ đếm số đến giải toán nâng cao', gradient: 'from-blue-500 to-indigo-600', lessons: '2,500', duration: '15-20 phút' },
  { icon: '📝', title: 'Tiếng Việt', description: 'Đọc hiểu, chính tả và viết văn sáng tạo', gradient: 'from-purple-500 to-pink-600', lessons: '2,000', duration: '10-15 phút' },
  { icon: '🌍', title: 'Tiếng Anh', description: 'Học từ vựng và giao tiếp qua trò chơi', gradient: 'from-green-500 to-teal-600', lessons: '1,800', duration: '15-20 phút' },
  { icon: '🔬', title: 'Khoa học', description: 'Khám phá thế giới tự nhiên qua thí nghiệm', gradient: 'from-yellow-500 to-orange-600', lessons: '1,200', duration: '20-25 phút' },
  { icon: '🎨', title: 'Mỹ thuật', description: 'Phát triển óc sáng tạo và kỹ năng nghệ thuật', gradient: 'from-pink-500 to-red-600', lessons: '800', duration: '10-15 phút' },
  { icon: '💻', title: 'Tin học', description: 'Lập trình Scratch và kỹ năng số cơ bản', gradient: 'from-cyan-500 to-blue-600', lessons: '600', duration: '15-20 phút' },
])

const interactiveBenefits = ref([
  'AI cá nhân hóa việc học',
  'Trò chơi hấp dẫn phù hợp lứa tuổi',
  'Video hoạt hình chất lượng cao',
  'Bài tập giúp ghi nhớ lâu dài',
  'Theo dõi tiến độ chi tiết',
])

const testimonialStats = ref([
  { value: '4.9', label: 'Đánh giá trung bình', showStars: true, bgClass: 'bg-gradient-to-br from-yellow-500/20 to-orange-500/10', textClass: 'text-yellow-400' },
  { value: '98%', label: 'Phụ huynh hài lòng', emoji: '😊', bgClass: 'bg-gradient-to-br from-green-500/20 to-emerald-500/10', textClass: 'text-green-400' },
  { value: '18K+', label: 'Lượt đánh giá', emoji: '💬', bgClass: 'bg-gradient-to-br from-cyan-500/20 to-blue-500/10', textClass: 'text-cyan-400' },
  { value: '52K+', label: 'Gia đình tin tưởng', emoji: '👨‍👩‍👧‍👦', bgClass: 'bg-gradient-to-br from-purple-500/20 to-pink-500/10', textClass: 'text-purple-400' },
])

const testimonialsRow1 = ref([
  { name: 'Chị Ngọc Anh', role: 'Phụ huynh bé Minh Anh - Lớp 3', text: 'Con tôi rất thích học trên SMARTEDU. Điểm Toán của con đã cải thiện rõ rệt!', initial: 'N', avatarBg: 'bg-gradient-to-br from-cyan-500 to-blue-600 shadow-cyan-500/30', rating: 5 },
  { name: 'Anh Tuấn Minh', role: 'Phụ huynh bé Hà My - Lớp 4', text: 'Giao diện đẹp, nội dung chất lượng. Con tự giác học mỗi ngày.', initial: 'T', avatarBg: 'bg-gradient-to-br from-purple-500 to-pink-600 shadow-purple-500/30', rating: 5 },
  { name: 'Cô Thanh Hương', role: 'Giáo viên tiểu học', text: 'SMARTEDU là công cụ hỗ trợ tuyệt vời cho việc giảng dạy!', initial: 'H', avatarBg: 'bg-gradient-to-br from-green-500 to-emerald-600 shadow-green-500/30', rating: 5 },
  { name: 'Chị Mai Lan', role: 'Phụ huynh bé Bảo An - Lớp 2', text: 'Con học rất vui, các trò chơi giáo dục hấp dẫn.', initial: 'M', avatarBg: 'bg-gradient-to-br from-pink-500 to-rose-600 shadow-pink-500/30', rating: 5 },
])

const scrollToSection = (id) => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
const scrollToTop = () => window.scrollTo({ top: 0, behavior: 'smooth' })
const handleScroll = () => { showScrollTop.value = window.scrollY > 500 }

onMounted(() => window.addEventListener('scroll', handleScroll))
onUnmounted(() => window.removeEventListener('scroll', handleScroll))
</script>

<style scoped>
@keyframes float-slow { 0%, 100% { transform: translateY(0) rotate(12deg); } 50% { transform: translateY(-20px) rotate(12deg); } }
@keyframes float-medium { 0%, 100% { transform: translateY(0) rotate(-12deg); } 50% { transform: translateY(-15px) rotate(-12deg); } }
@keyframes float-fast { 0%, 100% { transform: translateY(0) rotate(45deg); } 50% { transform: translateY(-10px) rotate(45deg); } }
@keyframes bounce-slow { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
@keyframes scroll-right { from { transform: translateX(0); } to { transform: translateX(-50%); } }

.animate-float-slow { animation: float-slow 6s ease-in-out infinite; }
.animate-float-medium { animation: float-medium 5s ease-in-out infinite; }
.animate-float-fast { animation: float-fast 4s ease-in-out infinite; }
.animate-bounce-slow { animation: bounce-slow 3s ease-in-out infinite; }
.animate-scroll-right { animation: scroll-right 40s linear infinite; display: flex; width: fit-content; }

.isometric-container { transform: perspective(1000px) rotateX(10deg) rotateY(-10deg); transform-style: preserve-3d; }
.isometric-card { transform: translateZ(20px); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 0 0 60px rgba(6, 182, 212, 0.2); }

:global(html) { scroll-behavior: smooth; }
</style>
