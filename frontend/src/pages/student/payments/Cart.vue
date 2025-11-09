<template>
  <div class="student-shell">
    <div class="student-container">
      <div class="mb-4">
        <p class="student-section-title">Thanh toán</p>
        <h1 class="text-3xl font-black text-brand-deep">Giỏ hàng</h1>
      </div>

      <div v-if="items.length" class="student-card space-y-6">
        <div class="overflow-hidden rounded-2xl border border-slate-100">
          <table class="min-w-full divide-y divide-slate-100 text-sm">
            <thead class="bg-slate-50 text-xs font-semibold uppercase tracking-wide text-brand-muted">
              <tr>
                <th class="px-4 py-3 text-left">Khoá học</th>
                <th class="px-4 py-3 text-right">Giá</th>
                <th class="px-4 py-3 text-center">Hành động</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              <tr v-for="it in items" :key="it.id" class="bg-white/80">
                <td class="px-4 py-3 font-semibold text-brand-deep">{{ it.name }}</td>
                <td class="px-4 py-3 text-right font-semibold text-brand-deep">{{ vnd(it.price) }}</td>
                <td class="px-4 py-3 text-center">
                  <button
                    type="button"
                    class="inline-flex items-center rounded-xl border border-slate-200 px-3 py-1.5 text-xs font-semibold text-brand-muted transition hover:bg-slate-50"
                    @click="remove(it.id)"
                  >
                    Xoá
                  </button>
                </td>
              </tr>
            </tbody>
            <tfoot class="bg-slate-50 text-sm font-bold text-brand-deep">
              <tr>
                <td class="px-4 py-3">Tổng cộng</td>
                <td class="px-4 py-3 text-right">{{ vnd(total) }}</td>
                <td></td>
              </tr>
            </tfoot>
          </table>
        </div>

        <div class="flex justify-end">
          <button
            type="button"
            class="inline-flex items-center justify-center rounded-2xl border border-transparent bg-brand-500 px-5 py-3 text-sm font-extrabold uppercase tracking-wide text-white shadow-lg shadow-emerald-200 transition hover:bg-brand-600 disabled:cursor-not-allowed disabled:border-slate-200 disabled:bg-slate-200 disabled:text-slate-500"
            :disabled="!items.length"
            @click="goCheckout"
          >
            Thanh toán
          </button>
        </div>
      </div>

      <div
        v-else
        class="student-card flex flex-col items-center justify-center text-center text-sm text-brand-muted"
      >
        Giỏ hàng trống.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Demo data - thay bằng dữ liệu thật của bạn
const items = reactive([
  { id: 1, name: 'Khoá học Standard', price: 199000 },
  // { id: 2, name: 'Khoá học Pro', price: 299000 },
])

const total = computed(() => items.reduce((s, i) => s + i.price, 0))
function vnd(n: number) { return n.toLocaleString('vi-VN') + 'đ' }

function remove(id: number) {
  const idx = items.findIndex(i => i.id === id)
  if (idx >= 0) items.splice(idx, 1)
}

function goCheckout() {
  router.push({
    name: 'student-payments-checkout',
    query: { amount: String(total.value), plan: items[0]?.name || 'Thanh toán' }
  })
}
</script>
