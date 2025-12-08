// src/store/exam.store.ts
import { defineStore } from 'pinia'
import { examService, type ExamSummary, type Level } from '@/services/exam.service'

/** ========= Types ========= */
export type ExamLevel = 'basic' | 'advanced'

export interface Exam {
  id: string | number
  title: string
  level: ExamLevel
  durationSec: number
  passCount: number
  questionsCount: number
  done?: boolean
  attemptId?: string | number
}

// Helper to convert backend Level to ExamLevel
function mapLevel(level: Level | string): ExamLevel {
  // Map 'Khối 1-2' to 'basic', 'Khối 3-5' to 'advanced'
  const levelStr = String(level || '').toLowerCase()
  if (levelStr.includes('1') || levelStr.includes('2') || levelStr === 'basic' || levelStr === 'cơ bản') {
    return 'basic'
  }
  return 'advanced'
}

/** ========= Store ========= */
export const useExamStore = defineStore('exam', {
  state: () => ({
    // list/paging
    exams: [] as Exam[],
    total: 0,
    page: 1,
    pageSize: 12,

    // filters
    q: '' as string,
    level: '' as '' | ExamLevel,

    // ui
    loading: false,
    error: '' as string,
  }),

  getters: {
    pages(state): number {
      return Math.max(1, Math.ceil(state.total / state.pageSize))
    },
  },

  actions: {
    /** Lấy 1 trang dữ liệu từ API – KHÔNG dùng default param với this */
    async fetchExamsPage(page?: number, pageSize?: number) {
      // gán mặc định bên trong để tránh lỗi this chưa bind
      page = page ?? this.page
      pageSize = pageSize ?? this.pageSize

      this.loading = true
      this.error = ''
      try {
        // Build API params
        const params: any = {
          page,
          pageSize,
          status: 'published', // Only fetch published exams for students
        }
        
        if (this.q) {
          params.q = this.q
        }

        // Call API
        const { items, total: totalItems } = await examService.list(params)
        
        // Filter by level on frontend (map backend level to frontend level)
        let filteredItems = items || []
        if (this.level) {
          filteredItems = filteredItems.filter((ex: ExamSummary) => {
            const examLevel = mapLevel(ex.level)
            return examLevel === this.level
          })
        }

        // Map ExamSummary to Exam format
        // passCount: number of questions needed to pass (based on passScore percentage)
        const mappedExams: Exam[] = filteredItems.map((ex: any) => {
          // Calculate passCount: if passScore is percentage, convert to count
          // Otherwise, if passScore is already a count, use it directly
          // For now, assume passScore is a minimum score, convert to count
          const passCount = ex.passScore <= ex.questionsCount 
            ? Math.ceil(ex.passScore) 
            : Math.ceil((ex.passScore / 100) * ex.questionsCount) || Math.ceil(ex.questionsCount * 0.6)
          
          return {
            id: ex.id,
            title: ex.title,
            level: mapLevel(ex.level),
            durationSec: ex.durationSec,
            passCount,
            questionsCount: ex.questionsCount,
            done: !!ex.done,
            attemptId: ex.attemptId,
          }
        })

        // Set state
        this.exams = mappedExams
        this.total = this.level ? filteredItems.length : totalItems
        this.page = page
        this.pageSize = pageSize
      } catch (e: any) {
        this.error = e?.message || String(e)
        console.error('Error fetching exams:', e)
        this.exams = []
        this.total = 0
      } finally {
        this.loading = false
      }
    },

    /** Tiện ích tải theo state hiện tại */
    async fetchExams() {
      await this.fetchExamsPage()
    },

    /** Lấy exam theo id từ danh sách hiện tại hoặc fetch từ API */
    getById(id: number | string): Exam | undefined {
      // First check current list
      const found = this.exams.find((x) => String(x.id) === String(id))
      if (found) return found
      
      // If not found, try to fetch from API (async)
      // For now, return undefined and let the detail page handle fetching
      return undefined
    },

    /** Đảm bảo exam có trong danh sách hiện tại (tiện cho trang detail vào trực tiếp) */
    ensureExam(id: number) {
      const item = this.getById(id)
      if (!item) return
      if (!this.exams.find((x) => x.id === item.id)) {
        // chèn lên đầu list để UI có dữ liệu ngay
        this.exams = [item, ...this.exams]
      }
    },

    /** Thay đổi filter rồi nạp lại trang 1 */
    async applyFilters({ q, level }: { q?: string; level?: '' | ExamLevel }) {
      if (typeof q === 'string') this.q = q
      if (typeof level !== 'undefined') this.level = level
      await this.fetchExamsPage(1, this.pageSize)
    },

    /** Chuyển trang */
    async goTo(page: number) {
      const target = Math.min(Math.max(1, page), this.pages)
      await this.fetchExamsPage(target, this.pageSize)
    },
  },
})
