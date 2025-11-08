<template>
  <div class="font-sans text-gray-900 bg-white overflow-x-hidden">
    <!-- Modern Header with Glassmorphism - Optimized Height -->
    <header
      class="fixed top-0 left-0 right-0 z-50 backdrop-blur-lg bg-white/80 border-b border-gray-200/50 shadow-sm"
    >
      <div class="max-w-7xl mx-auto px-6 py-3 flex justify-between items-center">
        <LogoSmartEdu :size="70" />
        <nav class="hidden lg:flex items-center space-x-8">
          <a
            href="#home"
            class="text-gray-700 hover:text-indigo-600 font-medium transition-colors"
            >Trang chủ</a
          >
          <a
            href="#features"
            class="text-gray-700 hover:text-indigo-600 font-medium transition-colors"
            >Tính năng</a
          >
          <a
            href="#courses"
            class="text-gray-700 hover:text-indigo-600 font-medium transition-colors"
            >Khóa học</a
          >
          <a
            href="#testimonials"
            class="text-gray-700 hover:text-indigo-600 font-medium transition-colors"
            >Đánh giá</a
          >
        </nav>
        <div class="flex items-center">
          <router-link to="/auth/login">
            <button
              class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-2.5 rounded-xl font-semibold hover:shadow-xl hover:scale-105 transition-all duration-300 flex items-center space-x-2"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
              </svg>
              <span>Đăng nhập</span>
            </button>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Hero Section with Modern Gradient -->
    <section
      id="home"
      class="pt-28 pb-20 px-6 bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 relative overflow-hidden"
    >
      <div class="absolute top-0 right-0 w-96 h-96 bg-purple-300 rounded-full blur-3xl opacity-20"></div>
      <div class="absolute bottom-0 left-0 w-96 h-96 bg-indigo-300 rounded-full blur-3xl opacity-20"></div>
      
      <div class="max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center relative z-10">
        <div class="space-y-6">
          <div class="inline-block px-4 py-2 bg-indigo-100 rounded-full">
            <span class="text-indigo-700 font-semibold text-sm">✨ Nền tảng học tập #1 cho trẻ em</span>
          </div>
          <h1
            class="text-5xl md:text-6xl font-bold leading-tight bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent"
          >
            Học tập thông minh cùng SMARTEDU
          </h1>
          <p class="text-xl text-gray-600 leading-relaxed">
            Khám phá hành trình học tập đầy màu sắc với hơn 10,000+ bài học tương tác, trò chơi giáo dục và video sinh động được thiết kế riêng cho học sinh tiểu học.
          </p>
          <div class="flex flex-wrap gap-4 pt-4">
            <router-link to="/auth/login">
              <button
                class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-4 rounded-2xl font-bold text-lg hover:shadow-2xl hover:scale-105 transition-all duration-300"
              >
                Bắt đầu học ngay
              </button>
            </router-link>
            <button
              class="bg-white text-gray-700 px-8 py-4 rounded-2xl font-bold text-lg border-2 border-gray-200 hover:border-indigo-300 hover:shadow-lg transition-all duration-300"
            >
              Xem video giới thiệu
            </button>
          </div>
          <div class="flex items-center space-x-8 pt-6">
            <div>
              <div class="text-3xl font-bold text-indigo-600">50K+</div>
              <div class="text-sm text-gray-600">Học sinh</div>
            </div>
            <div>
              <div class="text-3xl font-bold text-purple-600">10K+</div>
              <div class="text-sm text-gray-600">Bài học</div>
            </div>
            <div>
              <div class="text-3xl font-bold text-pink-600">4.9⭐</div>
              <div class="text-sm text-gray-600">Đánh giá</div>
            </div>
          </div>
        </div>
        <div class="relative">
          <div class="relative z-10">
            <img
              src="https://images.pexels.com/photos/8422252/pexels-photo-8422252.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
              alt="Happy children learning"
              class="rounded-3xl shadow-2xl"
            />
          </div>
          <div class="absolute -bottom-6 -left-6 w-64 h-64 bg-gradient-to-r from-yellow-300 to-orange-300 rounded-3xl -z-10"></div>
          <div class="absolute -top-6 -right-6 w-48 h-48 bg-gradient-to-r from-green-300 to-teal-300 rounded-3xl -z-10"></div>
        </div>
      </div>
    </section>

    <!-- Stats Bar -->
    <section class="py-12 bg-white border-y border-gray-100">
      <div class="max-w-7xl mx-auto px-6">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div v-for="stat in stats" :key="stat.label" class="space-y-2">
            <div class="text-4xl">{{ stat.icon }}</div>
            <div class="text-2xl font-bold text-gray-900">{{ stat.value }}</div>
            <div class="text-sm text-gray-600">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section with Modern Cards -->
    <section id="features" class="py-24 px-6 bg-gray-50">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <div class="inline-block px-4 py-2 bg-purple-100 rounded-full mb-4">
            <span class="text-purple-700 font-semibold text-sm">Tính năng nổi bật</span>
          </div>
          <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Tại sao chọn SMARTEDU?
          </h2>
          <p class="text-xl text-gray-600 max-w-2xl mx-auto">
            Nền tảng học tập toàn diện với công nghệ AI và phương pháp giáo dục hiện đại
          </p>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div
            v-for="(feature, index) in features"
            :key="index"
            class="group bg-white rounded-3xl p-8 shadow-sm hover:shadow-2xl transition-all duration-500 hover:-translate-y-2 border border-gray-100"
          >
            <div
              class="w-16 h-16 rounded-2xl mb-6 flex items-center justify-center text-3xl transition-transform duration-500 group-hover:scale-110"
              :class="feature.bgColor"
            >
              {{ feature.icon }}
            </div>
            <h3 class="text-xl font-bold text-gray-900 mb-3">{{ feature.title }}</h3>
            <p class="text-gray-600 leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Courses Section with Bento Grid -->
    <section id="courses" class="py-24 px-6 bg-white">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <div class="inline-block px-4 py-2 bg-green-100 rounded-full mb-4">
            <span class="text-green-700 font-semibold text-sm">Khóa học đa dạng</span>
          </div>
          <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Khám phá thế giới kiến thức
          </h2>
        </div>

        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="(course, index) in modernCourses"
            :key="index"
            class="group relative overflow-hidden rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-500 hover:-translate-y-2"
          >
            <div class="absolute inset-0 bg-gradient-to-br opacity-90" :class="course.gradient"></div>
            <div class="relative p-8 text-white h-full flex flex-col justify-between min-h-[280px]">
              <div>
                <div class="text-5xl mb-4">{{ course.icon }}</div>
                <h3 class="text-2xl font-bold mb-3">{{ course.title }}</h3>
                <p class="text-white/90 mb-4">{{ course.description }}</p>
                <div class="flex items-center space-x-4 text-sm">
                  <span>📚 {{ course.lessons }} bài học</span>
                  <span>⏱️ {{ course.duration }}</span>
                </div>
              </div>
              <router-link to="/auth/login">
                <button
                  class="mt-6 bg-white/20 backdrop-blur-sm text-white px-6 py-3 rounded-xl font-semibold hover:bg-white/30 transition-all duration-300 w-full"
                >
                  Khám phá ngay
                </button>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Interactive Learning Section -->
    <section class="py-24 px-6 bg-gradient-to-br from-blue-50 to-indigo-50">
      <div class="max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center">
        <div class="space-y-6">
          <div class="inline-block px-4 py-2 bg-blue-100 rounded-full">
            <span class="text-blue-700 font-semibold text-sm">🎮 Học qua chơi</span>
          </div>
          <h2 class="text-4xl md:text-5xl font-bold text-gray-900">
            Học tập tương tác với trò chơi giáo dục
          </h2>
          <p class="text-xl text-gray-600 leading-relaxed">
            Hơn 500+ trò chơi giáo dục được thiết kế để giúp trẻ học mà chơi, chơi mà học. Mỗi trò chơi đều kết hợp kiến thức và kỹ năng tư duy logic.
          </p>
          <ul class="space-y-4">
            <li v-for="benefit in interactiveBenefits" :key="benefit" class="flex items-start space-x-3">
              <div class="flex-shrink-0 w-6 h-6 rounded-full bg-green-500 flex items-center justify-center text-white text-sm mt-1">
                ✓
              </div>
              <span class="text-gray-700 text-lg">{{ benefit }}</span>
            </li>
          </ul>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <img
            src="https://images.pexels.com/photos/8422147/pexels-photo-8422147.jpeg?auto=compress&cs=tinysrgb&w=600"
            alt="Interactive learning"
            class="rounded-2xl shadow-xl"
          />
          <img
            src="https://images.pexels.com/photos/8422177/pexels-photo-8422177.jpeg?auto=compress&cs=tinysrgb&w=600"
            alt="Educational games"
            class="rounded-2xl shadow-xl mt-8"
          />
          <img
            src="https://images.pexels.com/photos/8422144/pexels-photo-8422144.jpeg?auto=compress&cs=tinysrgb&w=600"
            alt="Children learning"
            class="rounded-2xl shadow-xl -mt-8"
          />
          <img
            src="https://images.pexels.com/photos/8422143/pexels-photo-8422143.jpeg?auto=compress&cs=tinysrgb&w=600"
            alt="Fun education"
            class="rounded-2xl shadow-xl"
          />
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section id="testimonials" class="py-24 px-6 bg-white">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <div class="inline-block px-4 py-2 bg-yellow-100 rounded-full mb-4">
            <span class="text-yellow-700 font-semibold text-sm">💬 Đánh giá</span>
          </div>
          <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Phụ huynh nói gì về chúng tôi?
          </h2>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div
            v-for="(testimonial, index) in testimonials"
            :key="index"
            class="bg-gradient-to-br from-gray-50 to-white rounded-3xl p-8 border border-gray-100 hover:shadow-xl transition-all duration-300"
          >
            <div class="flex items-center space-x-1 mb-4">
              <span v-for="star in 5" :key="star" class="text-yellow-400 text-xl">★</span>
            </div>
            <p class="text-gray-700 text-lg mb-6 leading-relaxed">"{{ testimonial.text }}"</p>
            <div class="flex items-center space-x-4">
              <div
                class="w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold text-white"
                :class="testimonial.avatarBg"
              >
                {{ testimonial.initial }}
              </div>
              <div>
                <div class="font-bold text-gray-900">{{ testimonial.name }}</div>
                <div class="text-sm text-gray-600">{{ testimonial.role }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-24 px-6 bg-gradient-to-r from-indigo-600 to-purple-600 text-white relative overflow-hidden">
      <div class="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 left-0 w-96 h-96 bg-white/10 rounded-full blur-3xl"></div>
      
      <div class="max-w-4xl mx-auto text-center relative z-10">
        <h2 class="text-4xl md:text-5xl font-bold mb-6">
          Sẵn sàng bắt đầu hành trình học tập?
        </h2>
        <p class="text-xl mb-8 text-white/90">
          Tham gia cùng hàng nghìn phụ huynh và học sinh đã tin tưởng SMARTEDU
        </p>
        <div class="flex flex-wrap justify-center gap-4">
          <router-link to="/auth/login">
            <button
              class="bg-white text-indigo-600 px-10 py-4 rounded-2xl font-bold text-lg hover:shadow-2xl hover:scale-105 transition-all duration-300"
            >
              Đăng nhập ngay
            </button>
          </router-link>
          <button
            class="bg-white/20 backdrop-blur-sm text-white px-10 py-4 rounded-2xl font-bold text-lg hover:bg-white/30 transition-all duration-300"
          >
            Tư vấn ngay
          </button>
        </div>
        <p class="text-sm text-white/70 mt-6">
          Không cần thẻ tín dụng • Hủy bất cứ lúc nào
        </p>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-gray-300 py-16 px-6">
      <div class="max-w-7xl mx-auto">
        <div class="grid md:grid-cols-4 gap-12 mb-12">
          <div class="space-y-4">
            <LogoSmartEdu :size="70" />
            <p class="text-sm leading-relaxed">
              Nền tảng học tập trực tuyến hàng đầu cho học sinh tiểu học Việt Nam
            </p>
          </div>
          <div>
            <h4 class="text-white font-bold text-lg mb-4">Sản phẩm</h4>
            <ul class="space-y-2">
              <li><a href="#" class="hover:text-white transition-colors">Khóa học</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Trò chơi</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Video</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Bài tập</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-white font-bold text-lg mb-4">Công ty</h4>
            <ul class="space-y-2">
              <li><a href="#" class="hover:text-white transition-colors">Giới thiệu</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Blog</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Tuyển dụng</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Liên hệ</a></li>
            </ul>
          </div>
          <div>
            <h4 class="text-white font-bold text-lg mb-4">Kết nối</h4>
            <div class="flex space-x-3 mb-4">
              <a
                href="https://www.facebook.com/tu.chu.46680?locale=vi_VN"
                class="w-10 h-10 bg-gray-800 hover:bg-blue-600 rounded-xl flex items-center justify-center transition-colors"
                target="_blank"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
              </a>
              <a
                href="https://www.instagram.com/tustar.k72/"
                class="w-10 h-10 bg-gray-800 hover:bg-pink-600 rounded-xl flex items-center justify-center transition-colors"
                target="_blank"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                </svg>
              </a>
              <a
                href="https://www.youtube.com/@T%C3%BANguy%E1%BB%85nanh-tuna2004/featured"
                class="w-10 h-10 bg-gray-800 hover:bg-red-600 rounded-xl flex items-center justify-center transition-colors"
                target="_blank"
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
              </a>
            </div>
            <p class="text-sm">Email: anhtu105182@gmail.com</p>
            <p class="text-sm">Hotline: 0383137092</p>
          </div>
        </div>
        <div class="border-t border-gray-800 pt-8 text-center text-sm">
          <p>© 2025 SMARTEDU. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import LogoSmartEdu from '@/components/ui/LogoSmartEdu.vue'

const stats = ref([
  { icon: '👨‍👩‍👧‍👦', value: '50,000+', label: 'Học sinh' },
  { icon: '📚', value: '10,000+', label: 'Bài học' },
  { icon: '🎮', value: '500+', label: 'Trò chơi' },
  { icon: '⭐', value: '4.9/5', label: 'Đánh giá' }
])

const features = ref([
  {
    icon: '🤖',
    title: 'AI cá nhân hóa',
    description: 'Hệ thống AI thông minh tạo lộ trình học phù hợp với khả năng và tiến độ của từng bé',
    bgColor: 'bg-gradient-to-br from-blue-100 to-indigo-100'
  },
  {
    icon: '🎯',
    title: 'Học qua chơi',
    description: 'Trò chơi giáo dục thú vị giúp bé học tập một cách tự nhiên và hiệu quả nhất',
    bgColor: 'bg-gradient-to-br from-purple-100 to-pink-100'
  },
  {
    icon: '📊',
    title: 'Theo dõi tiến độ',
    description: 'Dashboard chi tiết giúp phụ huynh nắm bắt hoàn toàn quá trình học của con',
    bgColor: 'bg-gradient-to-br from-green-100 to-teal-100'
  },
  {
    icon: '🎨',
    title: 'Nội dung đa dạng',
    description: 'Video hoạt hình, bài tập tương tác và quiz thú vị cho mọi môn học',
    bgColor: 'bg-gradient-to-br from-yellow-100 to-orange-100'
  },
  {
    icon: '🏆',
    title: 'Hệ thống phần thưởng',
    description: 'Huy hiệu, điểm số và bảng xếp hạng giúp tạo động lực học tập mỗi ngày',
    bgColor: 'bg-gradient-to-br from-red-100 to-pink-100'
  },
  {
    icon: '👨‍👩‍👧',
    title: 'An toàn tuyệt đối',
    description: 'Môi trường học tập an toàn, không quảng cáo và được kiểm duyệt kỹ lưỡng',
    bgColor: 'bg-gradient-to-br from-indigo-100 to-purple-100'
  }
])

const modernCourses = ref([
  {
    icon: '🔢',
    title: 'Toán học',
    description: 'Từ đếm số đến giải toán nâng cao một cách vui vẻ',
    gradient: 'from-blue-500 to-indigo-600',
    lessons: '2,500',
    duration: '15-20 phút'
  },
  {
    icon: '📝',
    title: 'Tiếng Việt',
    description: 'Đọc hiểu, chính tả và viết văn sáng tạo',
    gradient: 'from-purple-500 to-pink-600',
    lessons: '2,000',
    duration: '10-15 phút'
  },
  {
    icon: '🌍',
    title: 'Tiếng Anh',
    description: 'Học từ vựng và giao tiếp qua trò chơi tương tác',
    gradient: 'from-green-500 to-teal-600',
    lessons: '1,800',
    duration: '15-20 phút'
  },
  {
    icon: '🔬',
    title: 'Khoa học',
    description: 'Khám phá thế giới tự nhiên qua thí nghiệm ảo',
    gradient: 'from-yellow-500 to-orange-600',
    lessons: '1,200',
    duration: '20-25 phút'
  },
  {
    icon: '🎨',
    title: 'Mỹ thuật',
    description: 'Phát triển óc sáng tạo và kỹ năng nghệ thuật',
    gradient: 'from-pink-500 to-red-600',
    lessons: '800',
    duration: '10-15 phút'
  },
  {
    icon: '💻',
    title: 'Tin học',
    description: 'Lập trình Scratch và kỹ năng số cơ bản',
    gradient: 'from-indigo-500 to-blue-600',
    lessons: '600',
    duration: '15-20 phút'
  }
])

const interactiveBenefits = ref([
  'Học tập cá nhân hóa với AI thông minh',
  'Trò chơi giáo dục hấp dẫn và phù hợp lứa tuổi',
  'Video hoạt hình chất lượng cao',
  'Bài tập tương tác giúp ghi nhớ lâu dài',
  'Theo dõi tiến độ chi tiết theo thời gian thực'
])

const testimonials = ref([
  {
    name: 'Chị Ngọc Anh',
    role: 'Phụ huynh bé Minh Anh - Lớp 3',
    text: 'Con tôi rất thích học trên SMARTEDU. Điểm Toán của con đã cải thiện rõ rệt chỉ sau 2 tháng sử dụng!',
    initial: 'N',
    avatarBg: 'bg-gradient-to-br from-blue-500 to-indigo-600'
  },
  {
    name: 'Anh Tuấn Minh',
    role: 'Phụ huynh bé Hà My - Lớp 4',
    text: 'Giao diện đẹp, nội dung chất lượng. Con tự giác học mỗi ngày mà không cần nhắc nhở. Rất đáng đầu tư!',
    initial: 'T',
    avatarBg: 'bg-gradient-to-br from-purple-500 to-pink-600'
  },
  {
    name: 'Cô Thanh Hương',
    role: 'Giáo viên tiểu học - 15 năm kinh nghiệm',
    text: 'SMARTEDU là công cụ hỗ trợ tuyệt vời cho việc giảng dạy. Nội dung sát chương trình và rất sinh động!',
    initial: 'H',
    avatarBg: 'bg-gradient-to-br from-green-500 to-teal-600'
  }
])
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}
</style>
