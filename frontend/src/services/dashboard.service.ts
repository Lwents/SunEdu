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

export interface PendingApproval {
  id: string
  title: string
  teacher: string
  submittedAt: string
}

export interface DashboardData {
  kpis: DashboardKPIs
  topCourses: TopCourse[]
  recentTransactions: RecentTransaction[]
  pendingApprovals: PendingApproval[]
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
      const { data } = await api.get('/api/admin/dashboard/')
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
      pendingApprovals: [],
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
  }
}




