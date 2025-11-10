<template>
  <div class="font-sans text-gray-900 bg-white overflow-x-hidden">
    <!-- Modern Header with Glassmorphism -->
    <header
      ref="header"
      class="fixed top-0 left-0 right-0 z-50 backdrop-blur-lg bg-white/80 border-b border-gray-200/50 shadow-sm"
    >
      <div class="max-w-7xl mx-auto px-3 sm:px-6 py-2 sm:py-3 flex justify-between items-center">
        <LogoSmartEdu :size="50" class="sm:w-[70px]" />
        <nav class="hidden lg:flex items-center space-x-8">
          <a
            href="#home"
            class="text-gray-700 hover:text-indigo-600 font-medium transition-colors"
            @click.prevent="scrollToSection('home')"
            >Trang chủ</a
          >
          <a
            href="#features"
            class="text-gray-700 hover:text-indigo-600 font-medium transition-colors"
            @click.prevent="scrollToSection('features')"
            >Tính năng</a
          >
          <a
            href="#courses"
            class="text-gray-700 hover:text-indigo-600 font-medium transition-colors"
            @click.prevent="scrollToSection('courses')"
            >Khóa học</a
          >
          <a
            href="#testimonials"
            class="text-gray-700 hover:text-indigo-600 font-medium transition-colors"
            @click.prevent="scrollToSection('testimonials')"
            >Đánh giá</a
          >
        </nav>
        <div class="flex items-center">
          <router-link to="/auth/login">
            <button
              class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-4 py-2 sm:px-8 sm:py-2.5 rounded-lg sm:rounded-xl text-sm sm:text-base font-semibold hover:shadow-xl hover:scale-105 transition-all duration-300 flex items-center space-x-1.5 sm:space-x-2 whitespace-nowrap"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4 sm:h-5 sm:w-5"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
                  clip-rule="evenodd"
                />
              </svg>
              <span>Đăng nhập</span>
            </button>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section
      id="home"
      ref="heroSection"
      class="pt-20 sm:pt-28 pb-12 sm:pb-20 px-3 sm:px-6 bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 relative overflow-hidden"
    >
      <div
        class="absolute top-0 right-0 w-64 h-64 sm:w-96 sm:h-96 bg-purple-300 rounded-full blur-3xl opacity-20 animate-float"
      ></div>
      <div
        class="absolute bottom-0 left-0 w-64 h-64 sm:w-96 sm:h-96 bg-indigo-300 rounded-full blur-3xl opacity-20 animate-float-delayed"
      ></div>

      <div class="max-w-7xl mx-auto grid lg:grid-cols-2 gap-8 sm:gap-12 items-center relative z-10">
        <div class="space-y-4 sm:space-y-6 opacity-0 -translate-x-12 animate-fade-in-left">
          <div class="inline-block px-3 py-1.5 sm:px-4 sm:py-2 bg-indigo-100 rounded-full">
            <span class="text-indigo-700 font-semibold text-xs sm:text-sm"
              >✨ Nền tảng học tập #1 cho trẻ em</span
            >
          </div>
          <h1
            class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold leading-tight bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent"
          >
            Học tập thông minh cùng SMARTEDU
          </h1>
          <p class="text-base sm:text-lg md:text-xl text-gray-600 leading-relaxed">
            Khám phá hành trình học tập đầy màu sắc với hơn 10,000+ bài học tương tác, trò chơi giáo
            dục và video sinh động được thiết kế riêng cho học sinh tiểu học.
          </p>
          <div class="flex flex-wrap gap-3 sm:gap-4 pt-2 sm:pt-4">
            <router-link to="/auth/login">
              <button
                class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-5 py-3 sm:px-8 sm:py-4 rounded-xl sm:rounded-2xl font-bold text-sm sm:text-base md:text-lg hover:shadow-2xl hover:scale-105 transition-all duration-300"
              >
                Bắt đầu học ngay
              </button>
            </router-link>
            <button
              class="bg-white text-gray-700 px-5 py-3 sm:px-8 sm:py-4 rounded-xl sm:rounded-2xl font-bold text-sm sm:text-base md:text-lg border-2 border-gray-200 hover:border-indigo-300 hover:shadow-lg transition-all duration-300"
            >
              Xem video giới thiệu
            </button>
          </div>
          <div class="flex items-center space-x-4 sm:space-x-8 pt-4 sm:pt-6">
            <div class="counter-item">
              <div
                class="text-xl sm:text-2xl md:text-3xl font-bold text-indigo-600"
                data-target="50000"
              >
                0
              </div>
              <div class="text-xs sm:text-sm text-gray-600">Học sinh</div>
            </div>
            <div class="counter-item">
              <div
                class="text-xl sm:text-2xl md:text-3xl font-bold text-purple-600"
                data-target="10000"
              >
                0
              </div>
              <div class="text-xs sm:text-sm text-gray-600">Bài học</div>
            </div>
            <div>
              <div class="text-xl sm:text-2xl md:text-3xl font-bold text-pink-600">4.9⭐</div>
              <div class="text-xs sm:text-sm text-gray-600">Đánh giá</div>
            </div>
          </div>
        </div>
        <div class="relative opacity-0 translate-x-12 animate-fade-in-right mt-8 lg:mt-0">
          <div class="relative z-10">
            <img
              src="https://images.pexels.com/photos/8422252/pexels-photo-8422252.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
              alt="Happy children learning"
              class="rounded-2xl sm:rounded-3xl shadow-2xl"
            />
          </div>
          <div
            class="absolute -bottom-4 -left-4 sm:-bottom-6 sm:-left-6 w-48 h-48 sm:w-64 sm:h-64 bg-gradient-to-r from-yellow-300 to-orange-300 rounded-2xl sm:rounded-3xl -z-10"
          ></div>
          <div
            class="absolute -top-4 -right-4 sm:-top-6 sm:-right-6 w-32 h-32 sm:w-48 sm:h-48 bg-gradient-to-r from-green-300 to-teal-300 rounded-2xl sm:rounded-3xl -z-10"
          ></div>
        </div>
      </div>
    </section>

    <!-- Stats Bar -->
    <section class="py-8 sm:py-12 bg-white border-y border-gray-100">
      <div class="max-w-7xl mx-auto px-3 sm:px-6">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-8 text-center">
          <div
            v-for="(stat, index) in stats"
            :key="stat.label"
            class="space-y-1 sm:space-y-2 opacity-0 scale-75 transition-all duration-600"
            :class="{ 'opacity-100 scale-100': statsVisible }"
            :style="{ transitionDelay: `${index * 100}ms` }"
          >
            <div class="text-2xl sm:text-3xl md:text-4xl">{{ stat.icon }}</div>
            <div class="text-lg sm:text-xl md:text-2xl font-bold text-gray-900">
              {{ stat.value }}
            </div>
            <div class="text-xs sm:text-sm text-gray-600">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="py-12 sm:py-16 md:py-24 px-3 sm:px-6 bg-gray-50">
      <div class="max-w-7xl mx-auto">
        <div
          class="text-center mb-8 sm:mb-12 md:mb-16 opacity-0 translate-y-8 transition-all duration-800"
          :class="{ 'opacity-100 translate-y-0': featuresVisible }"
        >
          <div class="inline-block px-4 py-2 bg-purple-100 rounded-full mb-4">
            <span class="text-purple-700 font-semibold text-sm">Tính năng nổi bật</span>
          </div>
          <h2
            class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-3 sm:mb-4"
          >
            Tại sao chọn SMARTEDU?
          </h2>
          <p class="text-base sm:text-lg md:text-xl text-gray-600 max-w-2xl mx-auto px-4">
            Nền tảng học tập toàn diện với công nghệ AI và phương pháp giáo dục hiện đại
          </p>
        </div>

        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 md:gap-8">
          <div
            v-for="(feature, index) in features"
            :key="index"
            class="group bg-white rounded-2xl sm:rounded-3xl p-5 sm:p-6 md:p-8 shadow-sm hover:shadow-2xl transition-all duration-500 hover:-translate-y-2 border border-gray-100 opacity-0 translate-y-8"
            :class="{ 'opacity-100 translate-y-0': featuresVisible }"
            :style="{ transitionDelay: `${index * 100}ms`, transitionDuration: '800ms' }"
          >
            <div
              class="w-12 h-12 sm:w-14 sm:h-14 md:w-16 md:h-16 rounded-xl sm:rounded-2xl mb-4 sm:mb-5 md:mb-6 flex items-center justify-center text-2xl sm:text-3xl transition-all duration-500 group-hover:scale-110 group-hover:rotate-6"
              :class="feature.bgColor"
            >
              {{ feature.icon }}
            </div>
            <h3 class="text-lg sm:text-xl font-bold text-gray-900 mb-2 sm:mb-3">
              {{ feature.title }}
            </h3>
            <p class="text-sm sm:text-base text-gray-600 leading-relaxed">
              {{ feature.description }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Courses Section -->
    <section id="courses" class="py-12 sm:py-16 md:py-24 px-3 sm:px-6 bg-white">
      <div class="max-w-7xl mx-auto">
        <div
          class="text-center mb-8 sm:mb-12 md:mb-16 opacity-0 translate-y-8 transition-all duration-800"
          :class="{ 'opacity-100 translate-y-0': coursesVisible }"
        >
          <div
            class="inline-block px-3 py-1.5 sm:px-4 sm:py-2 bg-green-100 rounded-full mb-3 sm:mb-4"
          >
            <span class="text-green-700 font-semibold text-xs sm:text-sm">Khóa học đa dạng</span>
          </div>
          <h2
            class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900 mb-3 sm:mb-4"
          >
            Khám phá thế giới kiến thức
          </h2>
        </div>

        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 md:gap-8">
          <div
            v-for="(course, index) in modernCourses"
            :key="index"
            class="group relative overflow-hidden rounded-2xl sm:rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-500 hover:-translate-y-2 opacity-0 translate-y-8"
            :class="{ 'opacity-100 translate-y-0': coursesVisible }"
            :style="{ transitionDelay: `${index * 100}ms`, transitionDuration: '800ms' }"
          >
            <div
              class="absolute inset-0 bg-gradient-to-br opacity-90"
              :class="course.gradient"
            ></div>
            <div
              class="relative p-5 sm:p-6 md:p-8 text-white h-full flex flex-col justify-between min-h-[240px] sm:min-h-[280px]"
            >
              <div>
                <div
                  class="text-3xl sm:text-4xl md:text-5xl mb-3 sm:mb-4 transition-all duration-500 group-hover:scale-110 group-hover:rotate-6"
                >
                  {{ course.icon }}
                </div>
                <h3 class="text-lg sm:text-xl md:text-2xl font-bold mb-2 sm:mb-3">
                  {{ course.title }}
                </h3>
                <p class="text-white/90 mb-3 sm:mb-4 text-sm sm:text-base">
                  {{ course.description }}
                </p>
                <div class="flex items-center space-x-3 sm:space-x-4 text-xs sm:text-sm">
                  <span>📚 {{ course.lessons }} bài học</span>
                  <span>⏱️ {{ course.duration }}</span>
                </div>
              </div>
              <router-link to="/auth/login">
                <button
                  class="mt-4 sm:mt-6 bg-white/20 backdrop-blur-sm text-white px-4 py-2.5 sm:px-6 sm:py-3 rounded-lg sm:rounded-xl text-sm sm:text-base font-semibold w-full"
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
    <section
      class="py-12 sm:py-16 md:py-24 px-3 sm:px-6 bg-gradient-to-br from-blue-50 to-indigo-50"
    >
      <div class="max-w-7xl mx-auto grid lg:grid-cols-2 gap-8 sm:gap-12 items-center">
        <div
          class="space-y-4 sm:space-y-6 opacity-0 -translate-x-12 transition-all duration-1000"
          :class="{ 'opacity-100 translate-x-0': interactiveVisible }"
        >
          <div class="inline-block px-3 py-1.5 sm:px-4 sm:py-2 bg-blue-100 rounded-full">
            <span class="text-blue-700 font-semibold text-xs sm:text-sm">🎮 Học qua chơi</span>
          </div>
          <h2 class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-gray-900">
            Học tập tương tác với trò chơi
          </h2>
          <p class="text-base sm:text-lg md:text-xl text-gray-600 leading-relaxed">
            500+ trò chơi giáo dục giúp trẻ học mà chơi, chơi mà học.
          </p>
          <ul class="space-y-3 sm:space-y-4">
            <li
              v-for="(benefit, index) in interactiveBenefits"
              :key="benefit"
              class="flex items-start space-x-2 sm:space-x-3 opacity-0 -translate-x-8 transition-all duration-600"
              :class="{ 'opacity-100 translate-x-0': interactiveVisible }"
              :style="{ transitionDelay: `${index * 100}ms` }"
            >
              <div
                class="flex-shrink-0 w-5 h-5 sm:w-6 sm:h-6 rounded-full bg-green-500 flex items-center justify-center text-white text-xs sm:text-sm mt-0.5 sm:mt-1"
              >
                ✓
              </div>
              <span class="text-gray-700 text-sm sm:text-base md:text-lg leading-relaxed">{{
                benefit
              }}</span>
            </li>
          </ul>
        </div>
        <!-- Mobile: Show 1 image, Desktop: 2x2 grid with offset -->
        <div
          class="opacity-0 translate-x-12 transition-all duration-1000 delay-200"
          :class="{ 'opacity-100 translate-x-0': interactiveVisible }"
        >
          <!-- Mobile: Single centered image -->
          <div class="lg:hidden">
            <img
              src="https://images.pexels.com/photos/8422147/pexels-photo-8422147.jpeg?auto=compress&cs=tinysrgb&w=600"
              alt="Interactive learning"
              class="rounded-2xl shadow-xl w-full h-[280px] sm:h-[320px] object-cover mx-auto"
            />
          </div>
          <!-- Desktop: 2x2 grid with offset -->
          <div class="hidden lg:grid grid-cols-2 gap-4">
            <img
              src="https://images.pexels.com/photos/8422147/pexels-photo-8422147.jpeg?auto=compress&cs=tinysrgb&w=600"
              alt="Interactive learning"
              class="rounded-2xl shadow-xl hover:scale-105 transition-transform duration-300"
            />
            <img
              src="https://images.pexels.com/photos/8422177/pexels-photo-8422177.jpeg?auto=compress&cs=tinysrgb&w=600"
              alt="Educational games"
              class="rounded-2xl shadow-xl mt-8 hover:scale-105 transition-transform duration-300"
            />
            <img
              src="https://images.pexels.com/photos/8422144/pexels-photo-8422144.jpeg?auto=compress&cs=tinysrgb&w=600"
              alt="Children learning"
              class="rounded-2xl shadow-xl -mt-8 hover:scale-105 transition-transform duration-300"
            />
            <img
              src="https://images.pexels.com/photos/8422143/pexels-photo-8422143.jpeg?auto=compress&cs=tinysrgb&w=600"
              alt="Fun education"
              class="rounded-2xl shadow-xl hover:scale-105 transition-transform duration-300"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- TESTIMONIALS SECTION - ĐÃ FIX HOÀN TOÀN -->
    <section
      id="testimonials"
      class="py-12 sm:py-16 md:py-24 px-3 sm:px-6 bg-gradient-to-br from-gray-50 via-white to-indigo-50 overflow-hidden"
    >
      <div class="max-w-full">
        <!-- Header -->
        <div
          class="text-center mb-8 sm:mb-12 md:mb-16 px-3 sm:px-6 opacity-0 translate-y-8 transition-all duration-800"
          :class="{ 'opacity-100 translate-y-0': testimonialsVisible }"
        >
          <div
            class="inline-block px-3 py-1.5 sm:px-4 sm:py-2 bg-yellow-100 rounded-full mb-3 sm:mb-4"
          >
            <span class="text-yellow-700 font-semibold text-xs sm:text-sm"
              >💬 Đánh giá từ phụ huynh</span
            >
          </div>
          <h2
            class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-bold text-gray-900 mb-3 sm:mb-4"
          >
            Phụ huynh nói gì về chúng tôi?
          </h2>
          <p
            class="text-base sm:text-lg md:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed px-4"
          >
            Hơn
            <span class="font-bold text-indigo-600 text-lg sm:text-xl md:text-2xl">18,547+</span>
            đánh giá tích cực từ phụ huynh và giáo viên khắp Việt Nam
          </p>
        </div>

        <!-- Stats Grid -->
        <div class="max-w-7xl mx-auto px-3 sm:px-6 mb-8 sm:mb-12 md:mb-16">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4 md:gap-6">
            <div
              v-for="(stat, index) in testimonialStats"
              :key="index"
              class="rounded-2xl sm:rounded-3xl p-3 sm:p-4 md:p-6 text-center border-2 hover:scale-105 transition-all duration-300 hover:shadow-xl opacity-0 scale-75"
              :class="[stat.className, { 'opacity-100 scale-100': testimonialsVisible }]"
              :style="{ transitionDelay: `${index * 100}ms`, transitionDuration: '600ms' }"
            >
              <div
                class="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-black mb-2 sm:mb-3"
                :class="stat.textClass"
              >
                {{ stat.value }}
              </div>
              <div v-if="stat.showStars" class="flex justify-center mb-2 sm:mb-3 space-x-0.5">
                <span
                  v-for="star in 5"
                  :key="star"
                  class="text-yellow-400 text-base sm:text-lg md:text-xl lg:text-2xl"
                  >★</span
                >
              </div>
              <div v-else class="text-xl sm:text-2xl md:text-3xl mb-1 sm:mb-2">
                {{ stat.emoji }}
              </div>
              <div class="text-xs sm:text-sm font-semibold text-gray-700">{{ stat.label }}</div>
              <div class="text-[10px] sm:text-xs text-gray-500 mt-0.5 sm:mt-1">
                {{ stat.sublabel }}
              </div>
            </div>
          </div>
        </div>

        <!-- First Row - Scroll Right (SEAMLESS LOOP) -->
        <div class="mb-6 sm:mb-8">
          <div class="overflow-x-hidden overflow-y-visible relative py-3 sm:py-4">
            <div class="flex gap-4 sm:gap-6 animate-scroll-right-seamless">
              <!-- Duplicate để tạo seamless loop -->
              <template v-for="n in 2" :key="'row1-set' + n">
                <div
                  v-for="(testimonial, index) in testimonialsRow1"
                  :key="`row1-${n}-${index}`"
                  class="w-[280px] sm:w-[350px] md:w-[400px] bg-white rounded-2xl sm:rounded-3xl p-5 sm:p-6 md:p-8 transition-all duration-300 border-2 border-transparent flex-shrink-0 testimonial-card"
                  :class="testimonial.borderColor"
                >
                  <div class="flex items-center space-x-4 mb-5">
                    <div
                      class="w-14 h-14 rounded-full flex items-center justify-center text-xl font-bold text-white shadow-md"
                      :class="testimonial.avatarBg"
                    >
                      {{ testimonial.initial }}
                    </div>
                    <div class="flex-1">
                      <div class="font-bold text-gray-900 text-lg flex items-center space-x-2">
                        <span>{{ testimonial.name }}</span>
                        <svg
                          v-if="testimonial.verified"
                          class="w-5 h-5 text-blue-500"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path
                            fill-rule="evenodd"
                            d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                            clip-rule="evenodd"
                          />
                        </svg>
                      </div>
                      <div class="text-sm text-gray-600">{{ testimonial.role }}</div>
                    </div>
                  </div>
                  <div class="flex items-center space-x-1 mb-4">
                    <span
                      v-for="star in testimonial.rating"
                      :key="star"
                      class="text-yellow-400 text-xl"
                      >★</span
                    >
                    <span
                      v-for="star in 5 - testimonial.rating"
                      :key="'empty-' + star"
                      class="text-gray-300 text-xl"
                      >★</span
                    >
                  </div>
                  <p class="text-gray-700 text-base leading-relaxed mb-4">
                    "{{ testimonial.text }}"
                  </p>
                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="tag in testimonial.tags"
                      :key="tag"
                      class="px-3 py-1 text-xs font-medium rounded-full"
                      :class="testimonial.tagClass"
                    >
                      {{ tag }}
                    </span>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>

        <!-- Second Row - Scroll Left (SEAMLESS LOOP) -->
        <div>
          <div class="overflow-x-hidden overflow-y-visible relative py-3 sm:py-4">
            <div class="flex gap-4 sm:gap-6 animate-scroll-left-seamless">
              <!-- Duplicate để tạo seamless loop -->
              <template v-for="n in 2" :key="'row2-set' + n">
                <div
                  v-for="(testimonial, index) in testimonialsRow2"
                  :key="`row2-${n}-${index}`"
                  class="w-[280px] sm:w-[350px] md:w-[400px] bg-white rounded-2xl sm:rounded-3xl p-5 sm:p-6 md:p-8 transition-all duration-300 border-2 border-transparent flex-shrink-0 testimonial-card"
                  :class="testimonial.borderColor"
                >
                  <div class="flex items-center space-x-4 mb-5">
                    <div
                      class="w-14 h-14 rounded-full flex items-center justify-center text-xl font-bold text-white shadow-md"
                      :class="testimonial.avatarBg"
                    >
                      {{ testimonial.initial }}
                    </div>
                    <div class="flex-1">
                      <div class="font-bold text-gray-900 text-lg flex items-center space-x-2">
                        <span>{{ testimonial.name }}</span>
                        <svg
                          v-if="testimonial.verified"
                          class="w-5 h-5 text-blue-500"
                          fill="currentColor"
                          viewBox="0 0 20 20"
                        >
                          <path
                            fill-rule="evenodd"
                            d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                            clip-rule="evenodd"
                          />
                        </svg>
                      </div>
                      <div class="text-sm text-gray-600">{{ testimonial.role }}</div>
                    </div>
                  </div>
                  <div class="flex items-center space-x-1 mb-4">
                    <span
                      v-for="star in testimonial.rating"
                      :key="star"
                      class="text-yellow-400 text-xl"
                      >★</span
                    >
                    <span
                      v-for="star in 5 - testimonial.rating"
                      :key="'empty-' + star"
                      class="text-gray-300 text-xl"
                      >★</span
                    >
                  </div>
                  <p class="text-gray-700 text-base leading-relaxed mb-4">
                    "{{ testimonial.text }}"
                  </p>
                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="tag in testimonial.tags"
                      :key="tag"
                      class="px-3 py-1 text-xs font-medium rounded-full"
                      :class="testimonial.tagClass"
                    >
                      {{ tag }}
                    </span>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>

        <!-- CTA -->
        <div class="mt-8 sm:mt-12 md:mt-16 text-center px-3 sm:px-6">
          <div
            class="inline-block bg-white rounded-2xl sm:rounded-3xl p-6 sm:p-8 md:p-10 border-2 border-indigo-200 shadow-xl hover:shadow-2xl transition-all duration-300 max-w-3xl opacity-0 translate-y-8"
            :class="{ 'opacity-100 translate-y-0': testimonialsVisible }"
          >
            <div class="text-3xl sm:text-4xl md:text-5xl mb-3 sm:mb-4">✍️</div>
            <h3 class="text-xl sm:text-2xl md:text-3xl font-bold text-gray-900 mb-3 sm:mb-4">
              Bạn đã trải nghiệm SMARTEDU?
            </h3>
            <p class="text-sm sm:text-base md:text-lg text-gray-600 mb-4 sm:mb-6">
              Chia sẻ câu chuyện của bạn để giúp hàng ngàn phụ huynh khác đưa ra quyết định đúng
              đắn!
            </p>
            <div class="flex flex-wrap justify-center gap-4">
              <button
                class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-10 py-4 rounded-2xl font-bold text-lg hover:shadow-xl hover:scale-105 transition-all duration-300"
              >
                Viết đánh giá ngay
              </button>
              <button
                class="bg-gray-100 text-gray-700 px-10 py-4 rounded-2xl font-bold text-lg hover:bg-gray-200 transition-all duration-300"
              >
                Xem thêm đánh giá
              </button>
            </div>
            <p class="text-sm text-gray-500 mt-4">
              🎁 Nhận voucher giảm 20% khi viết đánh giá chi tiết
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section
      class="py-24 px-6 bg-gradient-to-r from-indigo-600 to-purple-600 text-white relative overflow-hidden"
    >
      <div
        class="absolute top-0 right-0 w-96 h-96 bg-white/10 rounded-full blur-3xl animate-float"
      ></div>
      <div
        class="absolute bottom-0 left-0 w-96 h-96 bg-white/10 rounded-full blur-3xl animate-float-delayed"
      ></div>

      <div
        class="max-w-4xl mx-auto text-center relative z-10 opacity-0 translate-y-8 transition-all duration-800"
        :class="{ 'opacity-100 translate-y-0': ctaVisible }"
      >
        <h2 class="text-4xl md:text-5xl font-bold mb-6">Sẵn sàng bắt đầu hành trình học tập?</h2>
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
            class="bg-white/20 backdrop-blur-sm text-white px-10 py-4 rounded-2xl font-bold text-lg hover:bg-white/30 transition-all"
          >
            Tư vấn ngay
          </button>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-gray-300 py-8 sm:py-12 md:py-16 px-3 sm:px-6">
      <div class="max-w-7xl mx-auto">
        <!-- Logo + Description (Full width on all screens) -->
        <div
          class="mb-6 sm:mb-8 md:mb-12 opacity-0 translate-y-8 transition-all duration-800 text-center"
          :class="{ 'opacity-100 translate-y-0': footerVisible }"
        >
          <LogoSmartEdu :size="60" class="sm:w-[70px] mx-auto mb-3" />
          <p class="text-xs sm:text-sm leading-relaxed max-w-2xl mx-auto">
            Nền tảng học tập trực tuyến hàng đầu cho học sinh tiểu học Việt Nam
          </p>
        </div>

        <!-- 3 columns: Mobile horizontal (3 cols), Tablet (3 cols), Desktop (3 cols) -->
        <div class="grid grid-cols-3 gap-4 sm:gap-8 md:gap-12 mb-8 sm:mb-12">
          <!-- Sản phẩm -->
          <div
            class="opacity-0 translate-y-8 transition-all duration-800 delay-100 text-center"
            :class="{ 'opacity-100 translate-y-0': footerVisible }"
          >
            <h4 class="text-white font-bold text-sm sm:text-base md:text-lg mb-2 sm:mb-3 md:mb-4">
              Sản phẩm
            </h4>
            <ul class="space-y-1 sm:space-y-1.5 md:space-y-2 text-xs sm:text-sm md:text-base">
              <li><a href="#" class="hover:text-white transition-colors">Khóa học</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Trò chơi</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Video</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Bài tập</a></li>
            </ul>
          </div>

          <!-- Công ty -->
          <div
            class="opacity-0 translate-y-8 transition-all duration-800 delay-200 text-center"
            :class="{ 'opacity-100 translate-y-0': footerVisible }"
          >
            <h4 class="text-white font-bold text-sm sm:text-base md:text-lg mb-2 sm:mb-3 md:mb-4">
              Công ty
            </h4>
            <ul class="space-y-1 sm:space-y-1.5 md:space-y-2 text-xs sm:text-sm md:text-base">
              <li><a href="#" class="hover:text-white transition-colors">Giới thiệu</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Blog</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Tuyển dụng</a></li>
              <li><a href="#" class="hover:text-white transition-colors">Liên hệ</a></li>
            </ul>
          </div>

          <!-- Kết nối -->
          <div
            class="opacity-0 translate-y-8 transition-all duration-800 delay-300 text-center"
            :class="{ 'opacity-100 translate-y-0': footerVisible }"
          >
            <h4 class="text-white font-bold text-sm sm:text-base md:text-lg mb-2 sm:mb-3 md:mb-4">
              Kết nối
            </h4>
            <div
              class="flex justify-center space-x-1.5 sm:space-x-2 md:space-x-3 mb-2 sm:mb-3 md:mb-4"
            >
              <a
                href="https://www.facebook.com/vulekien2004/?locale=vi_VN"
                class="w-8 h-8 sm:w-9 sm:h-9 md:w-10 md:h-10 bg-gray-800 hover:bg-blue-600 rounded-lg sm:rounded-xl flex items-center justify-center transition-all duration-300 hover:scale-110"
                target="_blank"
              >
                <svg
                  class="w-3.5 h-3.5 sm:w-4 sm:h-4 md:w-5 md:h-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"
                  />
                </svg>
              </a>
              <a
                href="https://www.instagram.com/ne_kinn/"
                class="w-8 h-8 sm:w-9 sm:h-9 md:w-10 md:h-10 bg-gray-800 hover:bg-pink-600 rounded-lg sm:rounded-xl flex items-center justify-center transition-all duration-300 hover:scale-110"
                target="_blank"
              >
                <svg
                  class="w-3.5 h-3.5 sm:w-4 sm:h-4 md:w-5 md:h-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"
                  />
                </svg>
              </a>
              <a
                href=""
                class="w-8 h-8 sm:w-9 sm:h-9 md:w-10 md:h-10 bg-gray-800 hover:bg-red-600 rounded-lg sm:rounded-xl flex items-center justify-center transition-all duration-300 hover:scale-110"
                target="_blank"
              >
                <svg
                  class="w-3.5 h-3.5 sm:w-4 sm:h-4 md:w-5 md:h-5"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"
                  />
                </svg>
              </a>
            </div>
            <p class="text-[10px] sm:text-xs md:text-sm leading-tight">
              Email: kiritovn777@gmail.com
            </p>
            <p class="text-[10px] sm:text-xs md:text-sm leading-tight">Hotline: 0966148388</p>
          </div>
        </div>
        <div class="border-t border-gray-800 pt-4 sm:pt-6 md:pt-8 text-center">
          <p class="text-[10px] sm:text-xs md:text-sm text-gray-400">
            © 2025 SMARTEDU. All rights reserved.
          </p>
        </div>
      </div>
    </footer>

    <!-- Scroll to Top Button -->
    <transition
      enter-active-class="transition-opacity duration-300"
      leave-active-class="transition-opacity duration-300"
      enter-from-class="opacity-0"
      leave-to-class="opacity-0"
    >
      <button
        v-if="showScrollTop"
        @click="scrollToTop"
        class="fixed bottom-8 right-8 z-50 bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-4 rounded-full shadow-2xl hover:shadow-3xl hover:scale-110 transition-all duration-300"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 10l7-7m0 0l7 7m-7-7v18"
          />
        </svg>
      </button>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import LogoSmartEdu from '@/components/ui/LogoSmartEdu.vue'

// Visibility states
const showScrollTop = ref(false)
const statsVisible = ref(false)
const featuresVisible = ref(false)
const coursesVisible = ref(false)
const interactiveVisible = ref(false)
const testimonialsVisible = ref(false)
const ctaVisible = ref(false)
const footerVisible = ref(false)

// Data
const stats = ref([
  { icon: '👨‍👩‍👧‍👦', value: '50,000+', label: 'Học sinh' },
  { icon: '📚', value: '10,000+', label: 'Bài học' },
  { icon: '🎮', value: '500+', label: 'Trò chơi' },
  { icon: '⭐', value: '4.9/5', label: 'Đánh giá' },
])

const features = ref([
  {
    icon: '🤖',
    title: 'AI cá nhân hóa',
    description:
      'Hệ thống AI thông minh tạo lộ trình học phù hợp với khả năng và tiến độ của từng bé',
    bgColor: 'bg-gradient-to-br from-blue-100 to-indigo-100',
  },
  {
    icon: '📊',
    title: 'Theo dõi tiến độ',
    description: 'Dashboard chi tiết giúp phụ huynh nắm bắt hoàn toàn quá trình học của con',
    bgColor: 'bg-gradient-to-br from-green-100 to-teal-100',
  },
  {
    icon: '🎨',
    title: 'Nội dung đa dạng',
    description: 'Video hoạt hình, bài tập tương tác và quiz thú vị cho mọi môn học',
    bgColor: 'bg-gradient-to-br from-yellow-100 to-orange-100',
  },
])

const modernCourses = ref([
  {
    icon: '🔢',
    title: 'Toán học',
    description: 'Từ đếm số đến giải toán nâng cao một cách vui vẻ',
    gradient: 'from-blue-500 to-indigo-600',
    lessons: '2,500',
    duration: '15-20 phút',
  },
  {
    icon: '📝',
    title: 'Tiếng Việt',
    description: 'Đọc hiểu, chính tả và viết văn sáng tạo',
    gradient: 'from-purple-500 to-pink-600',
    lessons: '2,000',
    duration: '10-15 phút',
  },
  {
    icon: '🌍',
    title: 'Tiếng Anh',
    description: 'Học từ vựng và giao tiếp qua trò chơi tương tác',
    gradient: 'from-green-500 to-teal-600',
    lessons: '1,800',
    duration: '15-20 phút',
  },
  {
    icon: '🔬',
    title: 'Khoa học',
    description: 'Khám phá thế giới tự nhiên qua thí nghiệm ảo',
    gradient: 'from-yellow-500 to-orange-600',
    lessons: '1,200',
    duration: '20-25 phút',
  },
  {
    icon: '🎨',
    title: 'Mỹ thuật',
    description: 'Phát triển óc sáng tạo và kỹ năng nghệ thuật',
    gradient: 'from-pink-500 to-red-600',
    lessons: '800',
    duration: '10-15 phút',
  },
  {
    icon: '💻',
    title: 'Tin học',
    description: 'Lập trình Scratch và kỹ năng số cơ bản',
    gradient: 'from-indigo-500 to-blue-600',
    lessons: '600',
    duration: '15-20 phút',
  },
])

const interactiveBenefits = ref([
  'AI cá nhân hóa việc học',
  'Trò chơi hấp dẫn phù hợp lứa tuổi',
  'Video hoạt hình chất lượng cao',
  'Bài tập giúp ghi nhớ lâu dài',
  'Theo dõi tiến độ chi tiết',
])

const testimonialStats = ref([
  {
    value: '4.9',
    label: 'Đánh giá trung bình',
    sublabel: 'Từ 18,547 đánh giá',
    showStars: true,
    className: 'bg-gradient-to-br from-yellow-50 via-yellow-100 to-orange-50 border-yellow-200',
    textClass: 'text-yellow-600',
  },
  {
    value: '98%',
    label: 'Phụ huynh hài lòng',
    sublabel: 'Sẽ giới thiệu cho bạn bè',
    emoji: '😊',
    className: 'bg-gradient-to-br from-green-50 via-green-100 to-emerald-50 border-green-200',
    textClass: 'text-green-600',
  },
  {
    value: '18K+',
    label: 'Lượt đánh giá',
    sublabel: 'Tăng 120% năm 2024',
    emoji: '💬',
    className: 'bg-gradient-to-br from-blue-50 via-blue-100 to-indigo-50 border-blue-200',
    textClass: 'text-blue-600',
  },
  {
    value: '52K+',
    label: 'Gia đình tin tưởng',
    sublabel: 'Đang hoạt động hàng ngày',
    emoji: '👨‍👩‍👧‍👦',
    className: 'bg-gradient-to-br from-purple-50 via-purple-100 to-pink-50 border-purple-200',
    textClass: 'text-purple-600',
  },
])

const testimonialsRow1 = ref([
  {
    name: 'Chị Ngọc Anh',
    role: 'Phụ huynh bé Minh Anh - Lớp 3',
    text: 'Con tôi rất thích học trên SMARTEDU. Điểm Toán của con đã cải thiện rõ rệt chỉ sau 2 tháng sử dụng!',
    initial: 'N',
    avatarBg: 'bg-gradient-to-br from-blue-500 to-indigo-600',
    borderColor: 'hover:border-blue-300',
    tagClass: 'bg-blue-50 text-blue-700',
    rating: 5,
    verified: true,
    tags: ['Toán học', 'Tiến bộ nhanh'],
  },
  {
    name: 'Anh Tuấn Minh',
    role: 'Phụ huynh bé Hà My - Lớp 4',
    text: 'Giao diện đẹp, nội dung chất lượng. Con tự giác học mỗi ngày mà không cần nhắc nhở. Rất đáng đầu tư!',
    initial: 'T',
    avatarBg: 'bg-gradient-to-br from-purple-500 to-pink-600',
    borderColor: 'hover:border-purple-300',
    tagClass: 'bg-purple-50 text-purple-700',
    rating: 5,
    verified: true,
    tags: ['Tự giác', 'Chất lượng cao'],
  },
  {
    name: 'Cô Thanh Hương',
    role: 'Giáo viên tiểu học - 15 năm kinh nghiệm',
    text: 'SMARTEDU là công cụ hỗ trợ tuyệt vời cho việc giảng dạy. Nội dung sát chương trình và rất sinh động!',
    initial: 'H',
    avatarBg: 'bg-gradient-to-br from-green-500 to-teal-600',
    borderColor: 'hover:border-green-300',
    tagClass: 'bg-green-50 text-green-700',
    rating: 5,
    verified: true,
    tags: ['Giáo viên', 'Sát CT'],
  },
  {
    name: 'Chị Mai Lan',
    role: 'Phụ huynh bé Bảo An - Lớp 2',
    text: 'Con học rất vui, các trò chơi giáo dục hấp dẫn. Tiếng Anh của bé tiến bộ nhanh chóng. Rất hài lòng!',
    initial: 'M',
    avatarBg: 'bg-gradient-to-br from-pink-500 to-rose-600',
    borderColor: 'hover:border-pink-300',
    tagClass: 'bg-pink-50 text-pink-700',
    rating: 5,
    verified: true,
    tags: ['Tiếng Anh', 'Game hay'],
  },
  {
    name: 'Anh Đức Thành',
    role: 'Phụ huynh bé Minh Quân - Lớp 5',
    text: 'Nền tảng tuyệt vời! Con học được nhiều kiến thức bổ ích. Hệ thống theo dõi tiến độ rất chi tiết.',
    initial: 'Đ',
    avatarBg: 'bg-gradient-to-br from-amber-500 to-orange-600',
    borderColor: 'hover:border-amber-300',
    tagClass: 'bg-amber-50 text-amber-700',
    rating: 5,
    verified: true,
    tags: ['Lớp 5', 'Theo dõi tốt'],
  },
  {
    name: 'Chị Phương Anh',
    role: 'Phụ huynh bé Khánh Linh - Lớp 3',
    text: 'Chương trình học khoa học, phù hợp với lứa tuổi. Con rất thích các video hoạt hình sinh động.',
    initial: 'P',
    avatarBg: 'bg-gradient-to-br from-teal-500 to-cyan-600',
    borderColor: 'hover:border-teal-300',
    tagClass: 'bg-teal-50 text-teal-700',
    rating: 5,
    verified: true,
    tags: ['Video đẹp', 'Khoa học'],
  },
])

const testimonialsRow2 = ref([
  {
    name: 'Anh Hoàng Nam',
    role: 'Phụ huynh bé Gia Bảo - Lớp 4',
    text: 'Đầu tư xứng đáng! Con học đều đặn mỗi ngày, điểm số ở trường cũng tăng lên đáng kể.',
    initial: 'H',
    avatarBg: 'bg-gradient-to-br from-indigo-500 to-violet-600',
    borderColor: 'hover:border-indigo-300',
    tagClass: 'bg-indigo-50 text-indigo-700',
    rating: 5,
    verified: true,
    tags: ['Điểm cao', 'Đầu tư tốt'],
  },
  {
    name: 'Chị Thu Hà',
    role: 'Phụ huynh bé Minh Châu - Lớp 1',
    text: 'Nội dung phong phú, dễ hiểu. Con học chữ và đếm số rất nhanh. Giao diện thân thiện với trẻ em.',
    initial: 'T',
    avatarBg: 'bg-gradient-to-br from-rose-500 to-pink-600',
    borderColor: 'hover:border-rose-300',
    tagClass: 'bg-rose-50 text-rose-700',
    rating: 5,
    verified: true,
    tags: ['Lớp 1', 'Học chữ'],
  },
  {
    name: 'Anh Quang Minh',
    role: 'Phụ huynh bé Thiên Phúc - Lớp 5',
    text: 'Hệ thống bài tập đa dạng, giúp con rèn luyện tốt. Tính năng AI cá nhân hóa rất thông minh.',
    initial: 'Q',
    avatarBg: 'bg-gradient-to-br from-sky-500 to-blue-600',
    borderColor: 'hover:border-sky-300',
    tagClass: 'bg-sky-50 text-sky-700',
    rating: 5,
    verified: true,
    tags: ['AI thông minh', 'Đa dạng'],
  },
  {
    name: 'Chị Hương Giang',
    role: 'Phụ huynh bé Ánh Dương - Lớp 2',
    text: 'Con thích học Toán qua game. Điểm Toán của con tăng từ 7 lên 9 chỉ sau 3 tháng. Tuyệt vời!',
    initial: 'H',
    avatarBg: 'bg-gradient-to-br from-orange-500 to-red-600',
    borderColor: 'hover:border-orange-300',
    tagClass: 'bg-orange-50 text-orange-700',
    rating: 5,
    verified: true,
    tags: ['Toán game', 'Tăng điểm'],
  },
  {
    name: 'Anh Việt Anh',
    role: 'Phụ huynh bé Nam Anh - Lớp 4',
    text: 'Platform rất ổn định, không bị lag hay lỗi. Con có thể học bất cứ lúc nào trên cả máy tính và tablet.',
    initial: 'V',
    avatarBg: 'bg-gradient-to-br from-cyan-500 to-blue-600',
    borderColor: 'hover:border-cyan-300',
    tagClass: 'bg-cyan-50 text-cyan-700',
    rating: 5,
    verified: true,
    tags: ['Ổn định', 'Đa thiết bị'],
  },
  {
    name: 'Chị Thanh Tâm',
    role: 'Phụ huynh bé Gia Hân - Lớp 3',
    text: 'Con từ chỗ không thích học giờ đã tự giác. Các bài học được thiết kế rất bắt mắt và dễ hiểu.',
    initial: 'T',
    avatarBg: 'bg-gradient-to-br from-violet-500 to-purple-600',
    borderColor: 'hover:border-violet-300',
    tagClass: 'bg-violet-50 text-violet-700',
    rating: 5,
    verified: true,
    tags: ['Thay đổi', 'Thiết kế đẹp'],
  },
])

// Methods
const scrollToSection = (id) => {
  const element = document.getElementById(id)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handleScroll = () => {
  const scrollY = window.scrollY
  showScrollTop.value = scrollY > 500

  if (scrollY > 200) statsVisible.value = true
  if (scrollY > 500) featuresVisible.value = true
  if (scrollY > 1000) coursesVisible.value = true
  if (scrollY > 1500) interactiveVisible.value = true
  if (scrollY > 2200) testimonialsVisible.value = true
  if (scrollY > 3000) ctaVisible.value = true
  if (scrollY > 3500) footerVisible.value = true
}

const animateCounter = (el) => {
  const target = parseInt(el.getAttribute('data-target'))
  const increment = target / 100
  let current = 0

  const updateCounter = () => {
    current += increment
    if (current < target) {
      el.textContent = Math.ceil(current).toLocaleString() + '+'
      requestAnimationFrame(updateCounter)
    } else {
      el.textContent = target.toLocaleString() + '+'
    }
  }

  updateCounter()
}

const setupCounters = () => {
  const counterElements = document.querySelectorAll('.counter-item div[data-target]')

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && entry.target.textContent === '0') {
          animateCounter(entry.target)
        }
      })
    },
    { threshold: 0.5 },
  )

  counterElements.forEach((el) => observer.observe(el))
}

onMounted(() => {
  setupCounters()
  window.addEventListener('scroll', handleScroll)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
html {
  scroll-behavior: smooth;
}

/* Float animations */
@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

@keyframes float-delayed {
  0%,
  100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-30px);
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

.animate-float-delayed {
  animation: float-delayed 8s ease-in-out infinite;
}

/* Initial page load animations */
@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.animate-fade-in-left {
  animation: fadeInLeft 1s ease-out forwards;
}

.animate-fade-in-right {
  animation: fadeInRight 1s ease-out 0.2s forwards;
}

/* SEAMLESS LOOP: Carousel animations - FIXED */
@keyframes scrollRightSeamless {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-50%);
  }
}

@keyframes scrollLeftSeamless {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-50%);
  }
}

.animate-scroll-right-seamless {
  animation: scrollRightSeamless 50s linear infinite;
  display: flex;
  width: fit-content;
}

.animate-scroll-left-seamless {
  animation: scrollLeftSeamless 50s linear infinite;
  animation-direction: reverse;
  display: flex;
  width: fit-content;
}

/* Pause on hover */
.animate-scroll-right-seamless:hover,
.animate-scroll-left-seamless:hover {
  animation-play-state: paused;
}

/* Testimonial card - Simple shadow only */
.testimonial-card {
  box-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06),
    0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

/* Responsive overrides for testimonial cards */
.testimonial-card :deep(.flex.items-center) {
  font-size: 0.875rem;
}

@media (min-width: 640px) {
  .testimonial-card :deep(.flex.items-center) {
    font-size: 1rem;
  }
}

@media (min-width: 768px) {
  .testimonial-card :deep(.flex.items-center) {
    font-size: 1.125rem;
  }
}

/* Hide scrollbar for horizontal scroll on mobile */
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

/* Smooth scroll snap */
.snap-x {
  scroll-snap-type: x mandatory;
  scroll-behavior: smooth;
}

.snap-center {
  scroll-snap-align: center;
}
</style>
