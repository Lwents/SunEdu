<template>
  <div
    class="min-h-screen bg-gradient-to-br from-slate-50 via-cyan-50/30 to-slate-50 relative overflow-x-hidden"
  >
    <!-- Decorative Background -->
    <div
      class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzE2YTM0YSIgc3Ryb2tlLW9wYWNpdHk9IjAuMDMiIHN0cm9rZS13aWR0aD0iMSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==')] opacity-40"
    ></div>

    <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 pb-20">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 sm:gap-6 mb-8">
        <div class="flex-1">
          <div class="flex items-center gap-3 mb-2">
            <div
              class="w-10 h-10 bg-gradient-to-br from-cyan-500 to-cyan-600 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/30"
            >
              <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"
                />
              </svg>
            </div>
            <h1 class="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
              Thanh toán
            </h1>
          </div>
          <p class="text-slate-600 text-sm sm:text-base ml-13">
            Chọn gói học phù hợp và thanh toán an toàn
          </p>
        </div>

        <button
          @click="loadPlans"
          :disabled="planLoading"
          class="inline-flex items-center gap-2 px-5 py-3 bg-white border-2 border-slate-200 rounded-xl font-semibold text-slate-700 hover:border-cyan-500 dark:border-cyan-600 hover:bg-cyan-50 dark:bg-cyan-900/20 hover:text-cyan-700 dark:text-cyan-300 transition-all duration-300 hover:shadow-lg hover:-translate-y-0.5 disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:translate-y-0 disabled:hover:shadow-none group"
        >
          <svg
            v-if="!planLoading"
            class="w-5 h-5 group-hover:rotate-180 transition-transform duration-500"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            />
          </svg>
          <div
            v-else
            class="w-5 h-5 border-2 border-slate-300 border-t-cyan-600 rounded-full animate-spin"
          ></div>
          <span>{{ planLoading ? 'Đang tải...' : 'Làm mới' }}</span>
        </button>
      </div>

      <!-- Plan Selector (if multiple plans) -->
      <div
        v-if="plans.length > 1"
        class="mb-8 bg-white/80 backdrop-blur-xl border-2 border-white shadow-xl shadow-slate-200/50 rounded-2xl p-6 hover:shadow-2xl transition-all duration-300"
      >
        <div class="flex items-start gap-4 mb-4">
          <div
            class="w-12 h-12 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-xl flex items-center justify-center flex-shrink-0"
          >
            <svg
              class="w-6 h-6 text-blue-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-bold text-slate-900 mb-1">Chọn gói học</h3>
            <p class="text-sm text-slate-600">Tất cả gói đều hỗ trợ học không giới hạn</p>
          </div>
        </div>

        <select
          v-model="selectedPlanId"
          :disabled="planLoading"
          class="w-full px-4 py-3.5 bg-white border-2 border-slate-200 rounded-xl font-semibold text-slate-900 cursor-pointer hover:border-cyan-500 dark:border-cyan-600 focus:border-cyan-500 dark:border-cyan-600 focus:ring-4 focus:ring-cyan-500/30 transition-all duration-200 appearance-none bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMCAyMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNNSA3LjVMMTAgMTIuNUwxNSA3LjUiIHN0cm9rZT0iIzY0NzQ4YiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48L3N2Zz4=')] bg-[length:20px] bg-[position:right_1rem_center] bg-no-repeat pr-12"
        >
          <option v-for="plan in plans" :key="plan.id" :value="plan.id">
            {{ plan.name }} • {{ vnd(plan.price) }} • {{ plan.durationDays }} ngày
          </option>
        </select>
      </div>

      <!-- Payment Methods -->
      <div class="mb-16">
        <div class="flex items-center gap-3 mb-6">
          <div
            class="w-8 h-8 bg-gradient-to-br from-cyan-500 to-cyan-600 rounded-lg flex items-center justify-center"
          >
            <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z"
              />
            </svg>
          </div>
          <h2 class="text-2xl sm:text-3xl font-black text-slate-900">Phương thức thanh toán</h2>
        </div>

        <div class="grid md:grid-cols-2 gap-6">
          <!-- MoMo Payment Method -->
          <div
            class="relative group bg-white/90 backdrop-blur-xl border-2 border-cyan-200 dark:border-cyan-700 shadow-xl shadow-cyan-100/50 rounded-2xl p-6 sm:p-7 hover:shadow-2xl hover:shadow-cyan-200/60 hover:-translate-y-1 transition-all duration-300 overflow-hidden"
          >
            <!-- Recommended Badge -->
            <div class="absolute top-5 right-5 z-10">
              <div
                class="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-amber-400 to-orange-500 rounded-full shadow-lg shadow-amber-500/40"
              >
                <svg class="w-3.5 h-3.5 text-amber-900" viewBox="0 0 20 20" fill="currentColor">
                  <path
                    d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"
                  />
                </svg>
                <span class="text-xs font-black text-amber-900 uppercase tracking-wide"
                  >Phổ biến</span
                >
              </div>
            </div>

            <!-- Gradient Background -->
            <div
              class="absolute inset-0 bg-gradient-to-br from-sky-50 via-cyan-50/50 to-transparent opacity-60 rounded-2xl"
            ></div>

            <!-- Content -->
            <div class="relative z-10">
              <!-- Header -->
              <div class="flex items-center gap-4 mb-5">
                <div
                  class="w-14 h-14 bg-gradient-to-br from-cyan-500 to-cyan-600 rounded-2xl flex items-center justify-center shadow-lg shadow-cyan-500/40 flex-shrink-0"
                >
                  <svg
                    class="w-8 h-8 text-white"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M21 12a2.25 2.25 0 00-2.25-2.25H15a3 3 0 11-6 0H5.25A2.25 2.25 0 003 12m18 0v6a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 18v-6m18 0V9M3 12V9m18 0a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 9m18 0V6a2.25 2.25 0 00-2.25-2.25H5.25A2.25 2.25 0 003 6v3"
                    />
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="text-xl font-black text-slate-900 mb-0.5">Ví MoMo</h3>
                  <p class="text-sm text-slate-600">Thanh toán nhanh chóng & an toàn</p>
                </div>
              </div>

              <!-- Features -->
              <div class="space-y-2.5 mb-5">
                <div class="flex items-center gap-2.5">
                  <div
                    class="w-5 h-5 bg-cyan-100 dark:bg-cyan-900/30 rounded-full flex items-center justify-center flex-shrink-0"
                  >
                    <svg class="w-3 h-3 text-cyan-600 dark:text-cyan-400" viewBox="0 0 20 20" fill="currentColor">
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </div>
                  <span class="text-sm font-medium text-slate-700">Hỗ trợ ví, thẻ, ngân hàng</span>
                </div>
                <div class="flex items-center gap-2.5">
                  <div
                    class="w-5 h-5 bg-cyan-100 dark:bg-cyan-900/30 rounded-full flex items-center justify-center flex-shrink-0"
                  >
                    <svg class="w-3 h-3 text-cyan-600 dark:text-cyan-400" viewBox="0 0 20 20" fill="currentColor">
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </div>
                  <span class="text-sm font-medium text-slate-700">Xử lý tức thì 24/7</span>
                </div>
                <div class="flex items-center gap-2.5">
                  <div
                    class="w-5 h-5 bg-cyan-100 dark:bg-cyan-900/30 rounded-full flex items-center justify-center flex-shrink-0"
                  >
                    <svg class="w-3 h-3 text-cyan-600 dark:text-cyan-400" viewBox="0 0 20 20" fill="currentColor">
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </div>
                  <span class="text-sm font-medium text-slate-700">Bảo mật cao cấp</span>
                </div>
              </div>

              <!-- Payment Summary -->
              <div
                class="bg-gradient-to-br from-slate-50 to-slate-100/50 border-2 border-slate-200 rounded-xl p-4 mb-5"
              >
                <div class="flex justify-between items-center mb-2.5">
                  <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide"
                    >Gói đã chọn</span
                  >
                  <span class="text-sm font-bold text-slate-900">{{ displayPlan.name }}</span>
                </div>
                <div class="flex justify-between items-center pt-2.5 border-t-2 border-slate-200">
                  <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide"
                    >Tổng thanh toán</span
                  >
                  <span class="text-xl font-black text-cyan-600 dark:text-cyan-400">{{
                    vnd(displayPlan.price)
                  }}</span>
                </div>
              </div>

              <!-- Payment Button -->
              <button
                @click="goCheckout('momo')"
                :disabled="loadingMethod === 'momo'"
                class="w-full py-4 px-6 bg-gradient-to-r from-cyan-600 to-cyan-600 hover:from-cyan-700 hover:to-cyan-700 text-white font-bold rounded-xl shadow-lg shadow-cyan-500/40 hover:shadow-xl hover:shadow-cyan-500/50 hover:-translate-y-0.5 transition-all duration-300 flex items-center justify-center gap-3 disabled:opacity-70 disabled:cursor-not-allowed disabled:hover:translate-y-0 group"
              >
                <div
                  v-if="loadingMethod === 'momo'"
                  class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"
                ></div>
                <svg
                  v-else
                  class="w-5 h-5 group-hover:translate-x-1 transition-transform"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                    clip-rule="evenodd"
                  />
                </svg>
                <span>Thanh toán với MoMo</span>
              </button>

              <!-- Security Note -->
              <div
                class="flex items-start gap-2.5 mt-4 px-3 py-2.5 bg-blue-50/50 border border-blue-100 rounded-lg"
              >
                <svg
                  class="w-4 h-4 text-blue-600 mt-0.5 flex-shrink-0"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z"
                    clip-rule="evenodd"
                  />
                </svg>
                <span class="text-xs text-blue-700 leading-relaxed"
                  >Bạn sẽ được chuyển đến cổng thanh toán an toàn của MoMo</span
                >
              </div>
            </div>
          </div>

          <!-- Bank Transfer Method (Disabled) -->
          <div
            class="relative group bg-white/60 backdrop-blur-xl border-2 border-slate-200 shadow-lg rounded-2xl p-6 sm:p-7 overflow-hidden opacity-75"
          >
            <!-- Coming Soon Badge -->
            <div class="absolute top-5 right-5 z-10">
              <div
                class="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-orange-400 to-amber-500 rounded-full shadow-lg"
              >
                <svg class="w-3.5 h-3.5 text-orange-900" viewBox="0 0 20 20" fill="currentColor">
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                    clip-rule="evenodd"
                  />
                </svg>
                <span class="text-xs font-black text-orange-900 uppercase tracking-wide"
                  >Sắp ra mắt</span
                >
              </div>
            </div>

            <!-- Disabled Overlay -->
            <div class="absolute inset-0 bg-white/40 backdrop-blur-[2px] z-10 rounded-2xl"></div>

            <!-- Content -->
            <div class="relative">
              <!-- Header -->
              <div class="flex items-center gap-4 mb-5">
                <div
                  class="w-14 h-14 bg-gradient-to-br from-blue-400 to-indigo-500 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-400/30 flex-shrink-0"
                >
                  <svg
                    class="w-8 h-8 text-white"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M8 14v3m4-3v3m4-3v3M3 21h18M3 10h18M3 7l9-4 9 4M4 10h16v11H4V10z"
                    />
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="text-xl font-black text-slate-900 mb-0.5">Chuyển khoản VietQR</h3>
                  <p class="text-sm text-slate-600">Quét mã QR ngân hàng NAPAS 247</p>
                </div>
              </div>

              <!-- Features -->
              <div class="space-y-2.5 mb-5">
                <div class="flex items-center gap-2.5">
                  <div
                    class="w-5 h-5 bg-slate-100 rounded-full flex items-center justify-center flex-shrink-0"
                  >
                    <svg class="w-3 h-3 text-slate-500" viewBox="0 0 20 20" fill="currentColor">
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </div>
                  <span class="text-sm font-medium text-slate-600">Hỗ trợ mọi ngân hàng</span>
                </div>
                <div class="flex items-center gap-2.5">
                  <div
                    class="w-5 h-5 bg-slate-100 rounded-full flex items-center justify-center flex-shrink-0"
                  >
                    <svg class="w-3 h-3 text-slate-500" viewBox="0 0 20 20" fill="currentColor">
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </div>
                  <span class="text-sm font-medium text-slate-600">Tự động xác nhận</span>
                </div>
                <div class="flex items-center gap-2.5">
                  <div
                    class="w-5 h-5 bg-slate-100 rounded-full flex items-center justify-center flex-shrink-0"
                  >
                    <svg class="w-3 h-3 text-slate-500" viewBox="0 0 20 20" fill="currentColor">
                      <path
                        fill-rule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clip-rule="evenodd"
                      />
                    </svg>
                  </div>
                  <span class="text-sm font-medium text-slate-600">Phí 0đ</span>
                </div>
              </div>

              <!-- Payment Summary -->
              <div
                class="bg-gradient-to-br from-slate-50 to-slate-100/50 border-2 border-slate-200 rounded-xl p-4 mb-5"
              >
                <div class="flex justify-between items-center mb-2.5">
                  <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide"
                    >Gói đã chọn</span
                  >
                  <span class="text-sm font-bold text-slate-700">{{ displayPlan.name }}</span>
                </div>
                <div class="flex justify-between items-center pt-2.5 border-t-2 border-slate-200">
                  <span class="text-xs font-semibold text-slate-500 uppercase tracking-wide"
                    >Tổng thanh toán</span
                  >
                  <span class="text-xl font-black text-slate-700">{{
                    vnd(displayPlan.price)
                  }}</span>
                </div>
              </div>

              <!-- Disabled Button -->
              <button
                disabled
                class="w-full py-4 px-6 bg-slate-300 text-slate-500 font-bold rounded-xl cursor-not-allowed flex items-center justify-center gap-3"
              >
                <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                    clip-rule="evenodd"
                  />
                </svg>
                <span>Đang nâng cấp</span>
              </button>

              <!-- Security Note -->
              <div
                class="flex items-start gap-2.5 mt-4 px-3 py-2.5 bg-amber-50/50 border border-amber-100 rounded-lg"
              >
                <svg
                  class="w-4 h-4 text-amber-600 mt-0.5 flex-shrink-0"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                    clip-rule="evenodd"
                  />
                </svg>
                <span class="text-xs text-amber-700 leading-relaxed"
                  >Tính năng sẽ sớm quay lại với nhiều tiện ích hơn</span
                >
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Transaction History -->
      <HistoryList :limit="5" :showHeader="false" :showViewAll="true" />
      <div v-if="false">
        <!-- Section Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
          <div class="flex items-center gap-3">
            <div
              class="w-8 h-8 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-lg flex items-center justify-center"
            >
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900">Lịch sử thanh toán</h2>
          </div>

          <select
            v-model="statusFilter"
            class="px-4 py-3 bg-white border-2 border-slate-200 rounded-xl font-semibold text-slate-700 cursor-pointer hover:border-purple-500 focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all appearance-none bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHZpZXdCb3g9IjAgMCAyMCAyMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNNSA3LjVMMTAgMTIuNUwxNSA3LjUiIHN0cm9rZT0iIzY0NzQ4YiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48L3N2Zz4=')] bg-[length:18px] bg-[position:right_1rem_center] bg-no-repeat pr-12 min-w-[200px]"
          >
            <option value="">Tất cả trạng thái</option>
            <option value="success">✓ Thành công</option>
            <option value="pending">⌛ Đang xử lý</option>
            <option value="failed">✕ Thất bại</option>
          </select>

          <RouterLink
            class="px-4 py-3 bg-white border-2 border-slate-200 rounded-xl font-extrabold text-slate-700 hover:border-purple-500 hover:text-purple-700 transition"
            to="/student/payments/history"
          >
            Xem tất cả
          </RouterLink>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 sm:gap-5 mb-6">
          <!-- Total Success -->
          <div
            class="bg-white/90 backdrop-blur-xl border-2 border-white shadow-xl shadow-slate-200/50 rounded-2xl p-5 sm:p-6 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300"
          >
            <div class="flex items-center gap-4">
              <div
                class="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-cyan-100 to-cyan-100 rounded-xl flex items-center justify-center flex-shrink-0"
              >
                <svg
                  class="w-6 sm:w-7 h-6 sm:h-7 text-cyan-600 dark:text-cyan-400"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8 8.114 8 8c0-.114.07-.34.433-.582zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.433.468.433.582 0 .114-.07.34-.433.582a2.305 2.305 0 01-.567.267z"
                  />
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a1 1 0 10-2 0v.092a4.535 4.535 0 00-1.676.662C6.602 6.234 6 7.009 6 8c0 .99.602 1.765 1.324 2.246.48.32 1.054.545 1.676.662v1.941c-.391-.127-.68-.317-.843-.504a1 1 0 10-1.51 1.31c.562.649 1.413 1.076 2.353 1.253V15a1 1 0 102 0v-.092a4.535 4.535 0 001.676-.662C13.398 13.766 14 12.991 14 12c0-.99-.602-1.765-1.324-2.246A4.535 4.535 0 0011 9.092V7.151c.391.127.68.317.843.504a1 1 0 101.511-1.31c-.563-.649-1.413-1.076-2.354-1.253V5z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-2xl sm:text-3xl font-black text-slate-900 mb-0.5 truncate">
                  {{ vnd(totalSuccess) }}
                </div>
                <div class="text-xs sm:text-sm text-slate-600 font-medium">Tổng thanh toán</div>
              </div>
            </div>
          </div>

          <!-- Pending Count -->
          <div
            class="bg-white/90 backdrop-blur-xl border-2 border-white shadow-xl shadow-slate-200/50 rounded-2xl p-5 sm:p-6 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300"
          >
            <div class="flex items-center gap-4">
              <div
                class="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-amber-100 to-orange-100 rounded-xl flex items-center justify-center flex-shrink-0"
              >
                <svg
                  class="w-6 sm:w-7 h-6 sm:h-7 text-amber-600"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-2xl sm:text-3xl font-black text-slate-900 mb-0.5">
                  {{ pendingCount }}
                </div>
                <div class="text-xs sm:text-sm text-slate-600 font-medium">Đang xử lý</div>
              </div>
            </div>
          </div>

          <!-- Success Count -->
          <div
            class="bg-white/90 backdrop-blur-xl border-2 border-white shadow-xl shadow-slate-200/50 rounded-2xl p-5 sm:p-6 hover:shadow-2xl hover:-translate-y-1 transition-all duration-300"
          >
            <div class="flex items-center gap-4">
              <div
                class="w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-purple-100 to-indigo-100 rounded-xl flex items-center justify-center flex-shrink-0"
              >
                <svg
                  class="w-6 sm:w-7 h-6 sm:h-7 text-purple-600"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <div class="text-2xl sm:text-3xl font-black text-slate-900 mb-0.5">
                  {{ successCount }}
                </div>
                <div class="text-xs sm:text-sm text-slate-600 font-medium">
                  Giao dịch thành công
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Desktop Table -->
        <div
          class="hidden lg:block bg-white/90 backdrop-blur-xl border-2 border-white shadow-xl shadow-slate-200/50 rounded-2xl overflow-hidden"
        >
          <div v-if="filteredTransactions.length > 0" class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gradient-to-r from-slate-50 to-slate-100">
                <tr>
                  <th
                    class="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider"
                  >
                    Mã đơn
                  </th>
                  <th
                    class="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider"
                  >
                    Gói học
                  </th>
                  <th
                    class="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider"
                  >
                    Số tiền
                  </th>
                  <th
                    class="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider"
                  >
                    Phương thức
                  </th>
                  <th
                    class="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider"
                  >
                    Ngày
                  </th>
                  <th
                    class="px-6 py-4 text-left text-xs font-black text-slate-600 uppercase tracking-wider"
                  >
                    Trạng thái
                  </th>
                  <th
                    class="px-6 py-4 text-center text-xs font-black text-slate-600 uppercase tracking-wider"
                  >
                    Thao tác
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-100">
                <tr
                  v-for="item in filteredTransactions"
                  :key="item.id"
                  class="hover:bg-slate-50/50 transition-colors"
                >
                  <td class="px-6 py-4">
                    <span class="font-mono text-sm font-bold text-slate-900">{{
                      item.orderId
                    }}</span>
                  </td>
                  <td class="px-6 py-4">
                    <span class="text-sm font-semibold text-slate-900">{{ item.plan }}</span>
                  </td>
                  <td class="px-6 py-4">
                    <span class="text-sm font-black text-cyan-600 dark:text-cyan-400">{{ vnd(item.amount) }}</span>
                  </td>
                  <td class="px-6 py-4">
                    <div class="inline-flex items-center gap-2 px-3 py-1.5 bg-slate-100 rounded-lg">
                      <svg class="w-4 h-4 text-slate-600" viewBox="0 0 20 20" fill="currentColor">
                        <path
                          fill-rule="evenodd"
                          d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z"
                          clip-rule="evenodd"
                        />
                      </svg>
                      <span class="text-xs font-semibold text-slate-700">{{ item.method }}</span>
                    </div>
                  </td>
                  <td class="px-6 py-4">
                    <span class="text-sm text-slate-600 font-medium">{{
                      formatDate(item.date)
                    }}</span>
                  </td>
                  <td class="px-6 py-4">
                    <span
                      :class="[
                        'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wide',
                        item.status === 'success' ? 'bg-cyan-100 dark:bg-cyan-900/30 text-cyan-700 dark:text-cyan-300' : '',
                        item.status === 'pending' ? 'bg-amber-100 text-amber-700' : '',
                        item.status === 'failed' ? 'bg-red-100 text-red-700' : '',
                      ]"
                    >
                      <span
                        :class="[
                          'w-1.5 h-1.5 rounded-full',
                          item.status === 'success' ? 'bg-cyan-50 dark:bg-cyan-900/200' : '',
                          item.status === 'pending' ? 'bg-amber-500' : '',
                          item.status === 'failed' ? 'bg-red-500' : '',
                        ]"
                      ></span>
                      {{ statusText(item.status) }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-center">
                    <button
                      @click="viewDetail(item)"
                      class="inline-flex items-center justify-center w-9 h-9 bg-white border-2 border-slate-200 rounded-lg text-slate-600 hover:border-purple-500 hover:bg-purple-50 hover:text-purple-600 transition-all duration-200 hover:scale-110"
                      title="Xem chi tiết"
                    >
                      <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                        <path
                          fill-rule="evenodd"
                          d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                          clip-rule="evenodd"
                        />
                      </svg>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Empty State (Desktop) -->
          <div v-else class="py-16 text-center">
            <div
              class="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <svg
                class="w-10 h-10 text-slate-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
                />
              </svg>
            </div>
            <h3 class="text-lg font-bold text-slate-900 mb-2">Chưa có giao dịch nào</h3>
            <p class="text-sm text-slate-600">Lịch sử thanh toán của bạn sẽ hiển thị ở đây</p>
          </div>
        </div>

        <!-- Mobile Cards -->
        <div class="lg:hidden space-y-4">
          <div
            v-for="item in filteredTransactions"
            :key="'mobile-' + item.id"
            class="bg-white/90 backdrop-blur-xl border-2 border-white shadow-lg rounded-2xl p-5 hover:shadow-xl transition-all duration-300"
          >
            <!-- Header -->
            <div class="flex items-center justify-between mb-4 pb-4 border-b-2 border-slate-100">
              <span class="font-mono text-sm font-bold text-slate-900">{{ item.orderId }}</span>
              <span
                :class="[
                  'inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold uppercase',
                  item.status === 'success' ? 'bg-cyan-100 dark:bg-cyan-900/30 text-cyan-700 dark:text-cyan-300' : '',
                  item.status === 'pending' ? 'bg-amber-100 text-amber-700' : '',
                  item.status === 'failed' ? 'bg-red-100 text-red-700' : '',
                ]"
              >
                <span
                  :class="[
                    'w-1.5 h-1.5 rounded-full',
                    item.status === 'success' ? 'bg-cyan-50 dark:bg-cyan-900/200' : '',
                    item.status === 'pending' ? 'bg-amber-500' : '',
                    item.status === 'failed' ? 'bg-red-500' : '',
                  ]"
                ></span>
                {{ statusText(item.status) }}
              </span>
            </div>

            <!-- Body -->
            <div class="space-y-3 mb-4">
              <div class="flex justify-between items-center">
                <span class="text-xs text-slate-500 font-semibold uppercase">Gói học</span>
                <span class="text-sm font-bold text-slate-900">{{ item.plan }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-xs text-slate-500 font-semibold uppercase">Số tiền</span>
                <span class="text-base font-black text-cyan-600 dark:text-cyan-400">{{ vnd(item.amount) }}</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-xs text-slate-500 font-semibold uppercase">Phương thức</span>
                <div class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-slate-100 rounded-lg">
                  <svg class="w-3.5 h-3.5 text-slate-600" viewBox="0 0 20 20" fill="currentColor">
                    <path
                      fill-rule="evenodd"
                      d="M4 4a2 2 0 00-2 2v4a2 2 0 002 2V6h10a2 2 0 00-2-2H4zm2 6a2 2 0 012-2h8a2 2 0 012 2v4a2 2 0 01-2 2H8a2 2 0 01-2-2v-4zm6 4a2 2 0 100-4 2 2 0 000 4z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  <span class="text-xs font-semibold text-slate-700">{{ item.method }}</span>
                </div>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-xs text-slate-500 font-semibold uppercase">Ngày</span>
                <span class="text-sm text-slate-700 font-medium">{{ formatDate(item.date) }}</span>
              </div>
            </div>

            <!-- Footer -->
            <button
              @click="viewDetail(item)"
              class="w-full py-3 px-4 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-bold rounded-xl shadow-lg shadow-purple-500/30 hover:shadow-xl hover:shadow-purple-500/40 transition-all duration-300 flex items-center justify-center gap-2"
            >
              <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                <path
                  fill-rule="evenodd"
                  d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z"
                  clip-rule="evenodd"
                />
              </svg>
              <span>Xem chi tiết</span>
            </button>
          </div>

          <!-- Empty State (Mobile) -->
          <div
            v-if="filteredTransactions.length === 0"
            class="bg-white/90 backdrop-blur-xl border-2 border-white shadow-lg rounded-2xl p-12 text-center"
          >
            <div
              class="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <svg
                class="w-10 h-10 text-slate-400"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
                />
              </svg>
            </div>
            <h3 class="text-lg font-bold text-slate-900 mb-2">Chưa có giao dịch nào</h3>
            <p class="text-sm text-slate-600">Lịch sử thanh toán của bạn sẽ hiển thị ở đây</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import { paymentService, type SubscriptionPlan } from '@/services/payment.service'
import HistoryList from '@/components/payments/HistoryList.vue'

const router = useRouter()

const plans = ref<SubscriptionPlan[]>([])
const planLoading = ref(false)
const selectedPlanId = ref<string>('')
const fallbackPlan: SubscriptionPlan = {
  id: '',
  name: 'Thanh toán tuỳ chỉnh',
  price: 0,
  durationDays: 0,
  features: [],
}
const selectedPlan = computed(() => plans.value.find((p) => p.id === selectedPlanId.value) || null)
const displayPlan = computed(() => selectedPlan.value ?? fallbackPlan)
const loadingMethod = ref<'momo' | 'bank' | ''>('')

onMounted(() => {
  loadPlans()
  loadHistory()
  import('@/pages/student/payments/Checkout.vue')
})

async function loadPlans() {
  planLoading.value = true
  try {
    const data = await paymentService.listPlans()
    plans.value = data
    if (!selectedPlanId.value && data.length) {
      selectedPlanId.value = data[0].id
    }
  } catch (err: any) {
    console.error(err)
    ElMessage.error(err?.message || 'Không tải được danh sách gói')
  } finally {
    planLoading.value = false
  }
}

async function goCheckout(method: 'momo' | 'bank') {
  if (loadingMethod.value) return
  const plan = displayPlan.value
  if (!plan.id && method === 'bank') {
    ElMessage.info('Phương thức VietQR đang nâng cấp')
    return
  }
  loadingMethod.value = method
  try {
    const query: Record<string, string> = {
      plan: plan.name,
      method,
      flow: 'pay_with_method',
    }
    if (plan.id) {
      query.planId = plan.id
    }
    if (plan.price) {
      query.amount = String(Math.round(plan.price))
    }
    await router.push({
      name: 'student-payments-checkout',
      query,
    })
  } finally {
    loadingMethod.value = ''
  }
}

type Transaction = {
  id: string
  orderId: string
  plan: string
  amount: number
  method: string
  date: string
  status: 'success' | 'pending' | 'failed'
}
const transactions = ref<Transaction[]>([])
const loadingHistory = ref(false)

async function loadHistory() {
  loadingHistory.value = true
  try {
    const { items } = await paymentService.listMyPayments()
    transactions.value = items as unknown as Transaction[]
  } catch (err) {
    console.error(err)
  } finally {
    loadingHistory.value = false
  }
}

const statusFilter = ref('')

const filteredTransactions = computed(() => {
  if (!statusFilter.value) return transactions.value
  return transactions.value.filter((t) => t.status === statusFilter.value)
})

const totalSuccess = computed(() =>
  transactions.value.filter((t) => t.status === 'success').reduce((s, t) => s + t.amount, 0),
)
const pendingCount = computed(() => transactions.value.filter((t) => t.status === 'pending').length)
const successCount = computed(() => transactions.value.filter((t) => t.status === 'success').length)

function vnd(n: number) {
  return n.toLocaleString('vi-VN') + 'đ'
}
function formatDate(s: string) {
  const d = new Date(s)
  return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}/${d.getFullYear()}`
}
function statusText(st: string) {
  return ({ success: 'Thành công', pending: 'Đang xử lý', failed: 'Thất bại' } as any)[st] || st
}
function viewDetail(item: Transaction) {
  alert(`Chi tiết: ${item.orderId}`)
}
</script>
