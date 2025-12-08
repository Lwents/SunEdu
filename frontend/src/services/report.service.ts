import api from '@/config/axios'

export type ID = string | number
type Granularity = 'day' | 'week' | 'month'

// ===== Types =====
export interface DateRange { from?: string; to?: string; granularity?: Granularity }

export interface RevenuePoint { date: string; gross: number; net: number; refunds: number }
export interface RevenueByGateway { gateway: string; amount: number }
export interface RevenueTopCourse { courseId: ID; title: string; teacher: string; gross: number; net: number; orders: number }

export interface UserKPIs { dau: number; mau: number; newUsers: number; activeUsers: number }
export interface UserSeriesPoint { date: string; dau: number; newUsers: number }
export interface UserByRole { role: 'admin' | 'teacher' | 'student'; count: number }

export interface LearningKPIs { avgCompletion: number; avgScore: number; avgTimeSpentMin: number }
export interface CompletionPoint { date: string; completion: number }
export interface ScoreBySubject { subject: string; avgScore: number }
export interface AtRiskRow { userId: ID; name: string; className?: string; progress: number; lastActiveAt?: string }

export interface ContentKPIs { totalPublished: number; totalEnrollments: number; avgRating: number }
export interface ViewsBySubject { subject: string; views: number }
export interface TopContentRow { courseId: ID; title: string; views: number; enrollments: number; rating: number }

function buildCsv(header: string, rows: string[]) {
  return new Blob([header + '\n' + rows.join('\n')], { type: 'text/csv;charset=utf-8;' })
}

// ===== Service =====
export const reportService = {
  // ---------- Revenue ----------
  async revenueTimeseries(params: DateRange): Promise<RevenuePoint[]> {
    const { data } = await api.get('/admin/reports/revenue/', {
      params: { ...params, type: 'timeseries' },
    })
    return data
  },

  async revenueByGateway(params: DateRange): Promise<RevenueByGateway[]> {
    const { data } = await api.get('/admin/reports/revenue/', {
      params: { ...params, type: 'by-gateway' },
    })
    return data
  },

  async revenueTopCourses(params: DateRange): Promise<RevenueTopCourse[]> {
    const { data } = await api.get('/admin/reports/revenue/', {
      params: { ...params, type: 'top-courses' },
    })
    return data
  },

  async exportRevenueCsv(params: DateRange): Promise<Blob> {
    const rows = await this.revenueTimeseries(params)
    const payload = rows.map((r) => `${r.date},${r.gross},${r.net},${r.refunds}`)
    return buildCsv('date,gross,net,refunds', payload)
  },

  // ---------- Users ----------
  async userKpis(params: DateRange): Promise<UserKPIs> {
    const { data } = await api.get('/admin/reports/users/', { params: { ...params, type: 'kpis' } })
    return data
  },
  async userSeries(params: DateRange): Promise<UserSeriesPoint[]> {
    const { data } = await api.get('/admin/reports/users/', { params: { ...params, type: 'timeseries' } })
    return data
  },
  async userByRole(params: DateRange): Promise<UserByRole[]> {
    const { data } = await api.get('/admin/reports/users/', { params: { ...params, type: 'by-role' } })
    return data
  },
  async exportUsersCsv(params: DateRange): Promise<Blob> {
    const series = await this.userSeries(params)
    const payload = series.map((r) => `${r.date},${r.dau},${r.newUsers}`)
    return buildCsv('date,dau,newUsers', payload)
  },

  // ---------- Learning ----------
  async learningKpis(params: DateRange): Promise<LearningKPIs> {
    const { data } = await api.get('/admin/reports/learning/', { params: { ...params, type: 'kpis' } })
    return data
  },
  async completionSeries(params: DateRange): Promise<CompletionPoint[]> {
    const { data } = await api.get('/admin/reports/learning/', {
      params: { ...params, type: 'completion' },
    })
    return data
  },
  async scoreBySubject(params: DateRange): Promise<ScoreBySubject[]> {
    const { data } = await api.get('/admin/reports/learning/', {
      params: { ...params, type: 'score-by-subject' },
    })
    return data
  },
  async atRiskStudents(params: DateRange): Promise<AtRiskRow[]> {
    const { data } = await api.get('/admin/reports/learning/', {
      params: { ...params, type: 'at-risk' },
    })
    return data
  },
  async exportLearningCsv(params: DateRange): Promise<Blob> {
    const series = await this.completionSeries(params)
    const payload = series.map((r) => `${r.date},${r.completion}`)
    return buildCsv('date,completion', payload)
  },

  // ---------- Content ----------
  async contentKpis(params: DateRange): Promise<ContentKPIs> {
    const { data } = await api.get('/admin/reports/content/', { params: { ...params, type: 'kpis' } })
    return data
  },
  async viewsBySubject(params: DateRange): Promise<ViewsBySubject[]> {
    const { data } = await api.get('/admin/reports/content/', {
      params: { ...params, type: 'views-by-subject' },
    })
    return data
  },
  async topContents(params: DateRange): Promise<TopContentRow[]> {
    const { data } = await api.get('/admin/reports/content/', { params: { ...params, type: 'top' } })
    return data
  },
  async exportContentCsv(params: DateRange): Promise<Blob> {
    const list = await this.topContents(params)
    const payload = list.map((r) => `${r.courseId},"${r.title}",${r.views},${r.enrollments},${r.rating}`)
    return buildCsv('courseId,title,views,enrollments,rating', payload)
  },
}
