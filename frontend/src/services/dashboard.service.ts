import api from '@/config/axios'

const USE_MOCK = false

export interface DashboardKPIs {
  dau: number
  signups7d: number
  gmvToday: number
  txToday: number
  refundRate7d: number
  approvalsPending: number
}

export interface TopCourse {
  id: string
  title: string
  enrollments: number
}

export interface RecentTransaction {
  id: string
  user: string
  course: string
  amount: number
  gateway: string
  status: string
}

export interface ActiveUsersSummary {
  count: number
  windowMinutes: number
  recent: Array<{
    id: string
    name: string
    email: string
    role: string
    lastActive: string | null
  }>
}

export interface DashboardData {
  kpis: DashboardKPIs
  topCourses: TopCourse[]
  recentTransactions: RecentTransaction[]
  activeUsers: ActiveUsersSummary
  security: {
    failedLogins24h: number
    lockedAccounts: number
    sslDaysToExpire: number
  }
  system: {
    cpuP95: number
    ramP95: number
    disk: number
    backup: {
      lastRun: string
      status: string
    }
  }
}

export const dashboardService = {
  async getDashboard(): Promise<DashboardData> {
    if (!USE_MOCK) {
      const { data } = await api.get('/admin/dashboard/')
      return data
    }
    // Mock data
    return {
      kpis: {
        dau: 0,
        signups7d: 0,
        gmvToday: 0,
        txToday: 0,
        refundRate7d: 0,
        approvalsPending: 0
      },
      topCourses: [],
      recentTransactions: [],
      activeUsers: {
        count: 0,
        windowMinutes: 10,
        recent: []
      },
      security: {
        failedLogins24h: 0,
        lockedAccounts: 0,
        sslDaysToExpire: 30
      },
      system: {
        cpuP95: 0,
        ramP95: 0,
        disk: 0,
        backup: {
          lastRun: '-',
          status: '-'
        }
      }
    }
  },

  async getActiveUsers(): Promise<ActiveUsersSummary> {
    if (!USE_MOCK) {
      const { data } = await api.get('/admin/dashboard/active-users/')
      return data
    }
    return {
      count: 0,
      windowMinutes: 10,
      recent: []
    }
  }
}




