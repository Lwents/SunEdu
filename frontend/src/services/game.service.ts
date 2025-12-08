import api from '@/config/axios'

export interface GameQuestion {
  id: number
  question: string
  options: string[]
  correct: number
  // For word match
  left?: string
  right?: string
}

export interface Game {
  id: string
  title: string
  description: string
  game_type: string
  game_type_display: string
  difficulty: string
  difficulty_display?: string
  subject: string
  grade_level: number | null
  question_count: number
  play_count: number
  user_best_score?: number
  user_play_count?: number
  questions?: GameQuestion[]
  settings?: Record<string, any>
  is_published?: boolean
}

export interface GameSession {
  session_id: string
  game_id: string
  questions: GameQuestion[]
  max_score: number
}

export interface GameResult {
  session_id: string
  score: number
  max_score: number
  time_spent: number
  percentage: number
  rank: number
  total_players: number
}

export interface LeaderboardEntry {
  rank: number
  player_name: string
  score: number
  time_spent: number
  is_current_user: boolean
}

// Student APIs
export const gameService = {
  // List all games
  async list(params?: { type?: string; subject?: string; grade?: number }) {
    const { data } = await api.get('/student/games/', { params })
    return data
  },

  // Get game details
  async detail(gameId: string) {
    const { data } = await api.get(`/student/games/${gameId}/`)
    return data as Game
  },

  // Start game session
  async start(gameId: string): Promise<GameSession> {
    const { data } = await api.post(`/student/games/${gameId}/start/`)
    return data
  },

  // Submit game results
  async submit(gameId: string, payload: {
    session_id?: string
    score: number
    time_spent: number
    answers: any[]
  }): Promise<GameResult> {
    const { data } = await api.post(`/student/games/${gameId}/submit/`, payload)
    return data
  },

  // Get leaderboard
  async leaderboard(gameId: string) {
    const { data } = await api.get(`/student/games/${gameId}/leaderboard/`)
    return data as { leaderboard: LeaderboardEntry[] }
  },
}

// Teacher APIs
export const teacherGameService = {
  // List teacher's games
  async list() {
    const { data } = await api.get('/teacher/games/')
    return data
  },

  // Get game details
  async detail(gameId: string) {
    const { data } = await api.get(`/teacher/games/${gameId}/`)
    return data
  },

  // Create game
  async create(payload: {
    title: string
    description?: string
    game_type: string
    difficulty?: string
    questions: GameQuestion[]
    settings?: Record<string, any>
    subject?: string
    grade_level?: number
    is_published?: boolean
  }) {
    const { data } = await api.post('/teacher/games/', payload)
    return data
  },

  // Update game
  async update(gameId: string, payload: Partial<{
    title: string
    description: string
    game_type: string
    difficulty: string
    questions: GameQuestion[]
    settings: Record<string, any>
    subject: string
    grade_level: number
    is_published: boolean
  }>) {
    const { data } = await api.put(`/teacher/games/${gameId}/`, payload)
    return data
  },

  // Delete game
  async delete(gameId: string) {
    const { data } = await api.delete(`/teacher/games/${gameId}/`)
    return data
  },

  // Get game stats
  async stats(gameId: string) {
    const { data } = await api.get(`/teacher/games/${gameId}/stats/`)
    return data
  },

  // Generate questions with AI
  async generateWithAI(payload: {
    game_type: string
    title?: string
    subject?: string
    grade_level?: number
    count?: number
    hint?: string
  }) {
    const { data } = await api.post('/teacher/games/ai-generate/', payload)
    return data
  },
}
