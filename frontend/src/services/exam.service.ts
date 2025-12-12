// src/services/exam.service.ts
import api from '@/config/axios'

// Helper to avoid lost `this` when functions are destructured
async function fetchExamStats(examId: ID): Promise<{ submissions: number; avgScore: number; passRate: number }> {
  try {
    const { data } = await api.get(`/activities/exercises/${examId}/stats/`)
    return {
      submissions: data.submissions || data.total_attempts || 0,
      avgScore: data.avgScore || data.avg_score || 0,
      passRate: data.passRate || data.pass_rate || 0,
    }
  } catch (e: any) {
    console.error('Load stats error:', e)
    return { submissions: 0, avgScore: 0, passRate: 0 }
  }
}

export type ID = string | number
export type Level = 'Khối 1' | 'Khối 2' | 'Khối 3' | 'Khối 4' | 'Khối 5'
export type ExamStatus = 'draft' | 'scheduled' | 'published' | 'archived'

export type QType = 'single' | 'multi' | 'boolean' | 'fill' | 'match' | 'order'

export interface Choice { id: string; text: string }
export interface MatchPair { left: string; right: string } // cho 'match'
export interface QuestionBase {
  id: ID
  type: QType
  text: string
  score: number
  // hiển thị phụ
  image?: string
  hint?: string
}

export type Question =
  | (QuestionBase & { type: 'single' | 'multi'; choices: Choice[]; answer: string[] })
  | (QuestionBase & { type: 'boolean'; answer: boolean })
  | (QuestionBase & { type: 'fill'; blanks: number; answer: string[] })
  | (QuestionBase & { type: 'match'; pairs: MatchPair[] }) // chấm điểm theo đúng mapping
  | (QuestionBase & { type: 'order'; items: string[]; answer: string[] })

export interface ExamSummary {
  id: ID
  title: string
  level: Level
  durationSec: number
  passScore: number // điểm đạt tối thiểu
  questionsCount: number
  status: ExamStatus
  updatedAt: string
  maxAttempts?: number
  courseId?: ID
}

export interface ExamDetail extends ExamSummary {
  description?: string
  shuffleQuestions?: boolean
  shuffleChoices?: boolean
  questions: Question[]
  scheduledAt?: string // ISO datetime string for scheduled publishing
  endAt?: string // ISO datetime string for exam closing time
  maxAttempts?: number
  submissions?: number
  avgScore?: number
  passRate?: number
  courseId?: ID
}

export interface AttemptQuestion {
  id: ID
  type: QType
  text: string
  score: number
  choices?: Choice[]
  blanks?: number
  pairs?: MatchPair[]
  items?: string[]
}

export interface Attempt {
  id: string
  examId: ID
  startedAt: string
  deadlineAt: string // = started + duration
  questions: AttemptQuestion[]
  // bài làm (tối giản)
  answers: Record<string, any>
}

export interface AttemptResult {
  attemptId: string
  examId: ID
  totalScore: number
  maxScore: number
  correctCount: number
  totalCount: number
  passed: boolean
  detail: Array<{ qid: ID; score: number; max: number }>
  // Optional flags to control answer visibility
  can_show_answers?: boolean
  show_answers?: string
}

const USE_MOCK = false

// ========= MOCK BANK GENERATOR =========
function randPick<T>(arr: T[], n: number): T[] {
  const a = arr.slice()
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a.slice(0, n)
}

function makeId(prefix: string, i: number) {
  return `${prefix}_${i}_${Math.random().toString(36).slice(2, 7)}`
}

function makeSingle(i: number): Question {
  const choices = Array.from({ length: 4 }, (_, k) => ({ id: `c${k + 1}`, text: `Phương án ${k + 1}` }))
  const ans = [choices[i % 4].id]
  return { id: makeId('qS', i), type: 'single', text: `Câu đơn #${i}`, score: 1, choices, answer: ans }
}

function makeMulti(i: number): Question {
  const choices = Array.from({ length: 5 }, (_, k) => ({ id: `c${k + 1}`, text: `Đáp án ${k + 1}` }))
  const answer = choices.filter((_, idx) => (i + idx) % 2 === 0).map(c => c.id) // vài đáp án đúng
  return { id: makeId('qM', i), type: 'multi', text: `Chọn nhiều #${i}`, score: 2, choices, answer }
}

function makeBoolean(i: number): Question {
  return { id: makeId('qB', i), type: 'boolean', text: `Đúng / Sai #${i}`, score: 1, answer: i % 2 === 0 }
}

function makeFill(i: number): Question {
  const blanks = 2
  const answer = [`kw${i}`, `ans${i}`]
  return { id: makeId('qF', i), type: 'fill', text: `Điền từ #${i}`, score: 2, blanks, answer }
}

function makeMatch(i: number): Question {
  const pairs: MatchPair[] = [
    { left: 'Hà Nội', right: 'Việt Nam' },
    { left: 'Tokyo', right: 'Nhật Bản' },
    { left: 'Bangkok', right: 'Thái Lan' },
  ]
  return { id: makeId('qX', i), type: 'match', text: `Nối cặp #${i}`, score: 3, pairs }
}

function makeOrder(i: number): Question {
  const items = ['B1', 'B2', 'B3', 'B4']
  const answer = items.slice() // đúng thứ tự
  return { id: makeId('qO', i), type: 'order', text: `Sắp xếp #${i}`, score: 2, items, answer }
}

function buildMockExam(id: number, level: Level): ExamDetail {
  const bank: Question[] = [
    ...Array.from({ length: 10 }, (_, i) => makeSingle(i)),
    ...Array.from({ length: 6 }, (_, i) => makeMulti(i)),
    ...Array.from({ length: 6 }, (_, i) => makeBoolean(i)),
    ...Array.from({ length: 4 }, (_, i) => makeFill(i)),
    ...Array.from({ length: 3 }, (_, i) => makeMatch(i)),
    ...Array.from({ length: 3 }, (_, i) => makeOrder(i)),
  ]
  const questions = randPick(bank, 18)
  // Default duration based on level
  const durationSec = ['Khối 1', 'Khối 2'].includes(level) ? 20 * 60 : 30 * 60

  return {
    id,
    title: `Đề luyện tập #${id} – ${level}`,
    level,
    durationSec,
    passScore: 10, // ví dụ
    questionsCount: questions.length,
    status: 'published',
    updatedAt: new Date().toISOString(),
    description: 'Đề mock sinh ngẫu nhiên nhiều dạng câu.',
    shuffleQuestions: true,
    shuffleChoices: true,
    questions,
  }
}

const MOCK_EXAMS: ExamDetail[] = [
  buildMockExam(101, 'Khối 1'),
  buildMockExam(102, 'Khối 2'),
  buildMockExam(201, 'Khối 3'),
  buildMockExam(202, 'Khối 4'),
  buildMockExam(203, 'Khối 5'),
]

// ========= HELPERS =========
function toSummary(d: ExamDetail): ExamSummary {
  return {
    id: d.id,
    title: d.title,
    level: d.level,
    durationSec: d.durationSec,
    passScore: d.passScore,
    questionsCount: d.questionsCount,
    status: d.status,
    updatedAt: d.updatedAt,
  }
}

function scoreQuestion(q: Question, ans: any): number {
  switch (q.type) {
    case 'single': {
      const ok = Array.isArray(ans) ? ans[0] : ans
      return q.answer.includes(String(ok)) ? q.score : 0
    }
    case 'multi': {
      const a = new Set((ans as string[]) || [])
      const gold = new Set(q.answer)
      const correctAll = q.answer.every(x => a.has(x)) && a.size === gold.size
      // có thể thêm partial credit nếu muốn
      return correctAll ? q.score : 0
    }
    case 'boolean':
      return (ans === true || ans === false) && ans === q.answer ? q.score : 0
    case 'fill': {
      const given = (ans as string[]) || []
      let c = 0
      for (let i = 0; i < q.blanks; i++) {
        if ((given[i] || '').trim().toLowerCase() === (q.answer[i] || '').toLowerCase()) c++
      }
      // partial: mỗi blank 1/n điểm
      return (c / q.blanks) * q.score
    }
    case 'match': {
      // ans là array right theo thứ tự left
      const given = (ans as string[]) || []
      const gold = q.pairs.map(p => p.right)
      let c = 0
      for (let i = 0; i < gold.length; i++) if (given[i] === gold[i]) c++
      return (c / gold.length) * q.score
    }
    case 'order': {
      const given = (ans as string[]) || []
      const gold = q.answer
      let c = 0
      for (let i = 0; i < gold.length; i++) if (given[i] === gold[i]) c++
      return (c / gold.length) * q.score
    }
  }
}

// ========= SERVICE API =========
export const examService = {
  async list(params?: { level?: Level; q?: string; status?: ExamStatus; page?: number; pageSize?: number; includeStats?: boolean; excludeLessons?: boolean; studentView?: boolean }): Promise<{ items: ExamSummary[]; total: number }> {
    try {
     const apiParams: any = {}
      if (params?.q) apiParams.q = params.q
      if (params?.level) apiParams.level = params.level
      if (params?.status) apiParams.status = params.status
      if (params?.page) apiParams.page = params.page
      if (params?.pageSize) apiParams.pageSize = params.pageSize
      if (params?.includeStats) apiParams.include_stats = 'true'
      if (params?.studentView) apiParams.student_view = 'true'
      // yêu cầu backend gửi kèm attempt của user nếu đã đăng nhập
      apiParams.include_my_attempt = 'true'
      
      const { data } = await api.get('/activities/exercises/', { params: apiParams })
      
        // Map backend exercise to frontend exam format
        const exercises = Array.isArray(data) ? data : (data.results || data.items || [])
      const total = data.total || data.count || exercises.length
      
      // Filter by status if needed (only published for students)
      let filteredExercises = exercises
      if (params?.status === 'published') {
        filteredExercises = exercises.filter((ex: any) => ex.published === true)
      }
      // Tùy chọn loại bỏ bài tập gắn với bài học (nếu cần)
      if (params?.excludeLessons) {
        filteredExercises = filteredExercises.filter((ex: any) => !ex.lesson)
      }
      // Loại bỏ bài luyện tập AI (không hiển thị trong danh sách bài kiểm tra)
      filteredExercises = filteredExercises.filter((ex: any) => {
        const title = ex.title || ''
        const isAIPractice = title.startsWith('AI Practice') || ex.metadata?.type === 'ai_practice'
        return !isAIPractice
      })
      
      // Map exercises to ExamSummary format
      const items = filteredExercises.map((ex: any) => ({
          id: ex.id,
          title: ex.title || 'Đề thi',
        level: ex.settings?.level || ex.metadata?.level || ex.level || 'Khối 1',
        durationSec: ex.settings?.duration_seconds || ex.duration_seconds || 1800,
        passScore: ex.settings?.pass_score || ex.pass_score || 10,
        questionsCount: ex.questions?.length || ex.questions_count || 0,
        status: ex.published ? 'published' : (ex.settings?.scheduled_at ? 'scheduled' : 'draft'),
        scheduledAt: ex.settings?.scheduled_at,
        maxAttempts: ex.settings?.max_attempts ?? ex.max_attempts ?? 1,
        courseId: ex.settings?.course_id || ex.course_id || ex.course?.id || ex.metadata?.course_id,
          updatedAt: ex.updated_at || ex.updatedAt || new Date().toISOString(),
        // Stats from backend if include_stats was true
        submissions: ex.stats?.total_attempts || ex.submissions || 0,
        avgScore: ex.stats?.avg_score || ex.avgScore || ex.avg_score || 0,
        passRate: ex.stats?.pass_rate || ex.passRate || ex.pass_rate || 0,
        // attempt info per-user (backend attaches when authenticated)
        done: !!ex.done || (!!ex.my_attempt && !!ex.my_attempt.finished_at),
        attemptId: ex.my_attempt?.id || ex.my_attempt?.attempt_id,
        }))
      
      return { items, total: params?.status === 'published' ? filteredExercises.length : total }
      } catch (e: any) {
        console.error('Load exams error:', e)
      throw new Error('Không thể tải danh sách bài kiểm tra: ' + (e.response?.data?.detail || e.message))
    }
  },
  
  // New method to get stats for a single exam
  async getStats(examId: ID): Promise<{ submissions: number; avgScore: number; passRate: number }> {
    return fetchExamStats(examId)
  },

  async detail(id: ID): Promise<ExamDetail> {
    try {
      const [examRes, stats] = await Promise.all([
        api.get(`/activities/exercises/${id}/`),
        fetchExamStats(id).catch(() => ({ submissions: 0, avgScore: 0, passRate: 0 })),
      ])
      const data = examRes.data
      // Map backend exercise to frontend exam format
      return {
        id: data.id,
        title: data.title || 'Đề thi',
        // Level is stored in settings.level or metadata.level
        level: data.settings?.level || data.metadata?.level || data.level || 'Khối 1',
        durationSec: data.settings?.duration_seconds || data.duration_seconds || 1800,
        passScore: data.settings?.pass_score || data.pass_score || 10,
        questionsCount: data.questions?.length || data.questions_count || 0,
        status: data.published ? 'published' : (data.settings?.scheduled_at ? 'scheduled' : 'draft'),
        updatedAt: data.updated_at || data.updatedAt || new Date().toISOString(),
        maxAttempts: data.settings?.max_attempts ?? data.max_attempts ?? 1,
        courseId: data.settings?.course_id || data.course_id || data.course?.id || data.metadata?.course_id,
        // Description is stored in settings.description
        description: data.settings?.description || data.description || '',
        scheduledAt: data.settings?.scheduled_at,
        endAt: data.settings?.end_at,
        shuffleQuestions: data.settings?.shuffle_questions ?? true,
        shuffleChoices: data.settings?.shuffle_choices ?? true,
        submissions: stats.submissions ?? 0,
        avgScore: stats.avgScore ?? 0,
        passRate: stats.passRate ?? 0,
        questions: (data.questions || []).map((q: any, idx: number) => {
          // Map backend question to frontend question format
          // Question type and score are stored in meta field
          const questionType = q.meta?.type || q.type || 'single'
          const questionScore = q.meta?.score || q.score || 1
          const base: QuestionBase = {
            id: q.id || idx,
            type: questionType,
            text: q.prompt || q.text || '',
            score: questionScore,
          }
          if (questionType === 'single' || questionType === 'multi') {
            return {
              ...base,
              type: questionType,
              choices: (q.choices || []).map((c: any, cIdx: number) => ({
                id: c.id || `c${cIdx + 1}`,
                text: c.text || '',
              })),
              answer: q.choices?.filter((c: any) => c.is_correct).map((c: any) => c.id) || [],
            }
          }
          return base as Question
        }),
      }
    } catch (e: any) {
      console.error('Load exam detail error:', e)
      throw new Error('Không thể tải chi tiết bài kiểm tra: ' + (e.response?.data?.detail || e.message))
    }
  },

  async startAttempt(examId: ID): Promise<Attempt> {
      try {
      const { data } = await api.post(`/activities/exercises/${examId}/start/`)
        // Map backend attempt to frontend attempt format
        return {
          id: data.id || data.attempt_id,
          examId: examId,
          startedAt: data.started_at || data.startedAt || new Date().toISOString(),
          deadlineAt: data.deadline_at || data.deadlineAt || new Date(Date.now() + 1800000).toISOString(),
          questions: (data.questions || []).map((q: any) => {
          // Question type and score are stored in meta field
          const questionType = q.meta?.type || q.type || 'single'
          const questionScore = q.meta?.score || q.score || 1
            const base: AttemptQuestion = {
              id: q.id,
            type: questionType,
              text: q.prompt || q.text || '',
            score: questionScore,
            }
          if (questionType === 'single' || questionType === 'multi') base.choices = (q.choices || []).map((c: any) => ({
              id: c.id,
              text: c.text || '',
            }))
          if (questionType === 'fill') base.blanks = q.blanks || 1
          if (questionType === 'match') base.pairs = q.pairs || []
            if (q.type === 'order') base.items = q.items || []
            return base
          }),
          answers: data.answers || {},
        }
      } catch (e: any) {
        // Don't log error if it's expected (already finished)
        const errorMsg = e.response?.data?.detail || e.message || ''
        if (!errorMsg.includes('đã hoàn thành') && !errorMsg.includes('chỉ được làm 1 lần')) {
          console.error('Start attempt error:', e)
        }
      throw new Error('Không thể bắt đầu làm bài: ' + errorMsg)
    }
  },

  async submit(examId: ID, attemptId: string, answers: Record<string, any>): Promise<AttemptResult> {
      try {
        // Submit all answers
        for (const [questionId, answer] of Object.entries(answers)) {
        await api.post(`/activities/attempts/${attemptId}/answers/`, {
            question_id: questionId,
            answer: answer,
          })
        }
        // Finalize attempt
      const { data } = await api.post(`/activities/attempts/${attemptId}/finalize/`)
        // Map backend result to frontend format
        return {
          attemptId: attemptId,
          examId: examId,
          totalScore: data.total_score || data.totalScore || 0,
          maxScore: data.max_score || data.maxScore || 0,
          correctCount: data.correct_count || data.correctCount || 0,
          totalCount: data.total_count || data.totalCount || 0,
          passed: data.passed || false,
          detail: (data.detail || []).map((d: any) => ({
            qid: d.question_id || d.qid,
            score: d.score || 0,
            max: d.max_score || d.max || 0,
          })),
        }
      } catch (e: any) {
        console.error('Submit exam error:', e)
      throw new Error('Không thể nộp bài: ' + (e.response?.data?.detail || e.message))
    }
  },

  async create(data: Partial<ExamDetail>): Promise<ExamDetail> {
      try {
        // Map frontend exam to backend exercise format
      // Ensure required fields are present
      const title = data.title?.trim() || ''
      if (!title) {
        throw new Error('Tên đề thi là bắt buộc')
      }
      
      const payload: any = {
        title: title,
        type: 'mcq', // Backend only accepts: 'mcq', 'short_answer', or 'matching'
          settings: {
            duration_seconds: data.durationSec || 1800,
          pass_score: data.passScore || 10,
          max_attempts: data.maxAttempts ?? 1,
            shuffle_questions: data.shuffleQuestions ?? true,
            shuffle_choices: data.shuffleChoices ?? true,
          ...(data.courseId ? { course_id: data.courseId } : {}),
          },
        questions: (data.questions || []).map((q: Question) => {
          // Ensure prompt is not empty
          if (!q.text || !q.text.trim()) {
            throw new Error('Nội dung câu hỏi không được để trống')
          }
          
          return {
            prompt: q.text.trim(),
            meta: { 
            type: q.type,
              score: q.score || 1,
              // Store additional metadata if needed
              ...(data.description ? { description: data.description } : {}),
              ...(data.level ? { level: data.level } : {}),
            },
            choices: q.type === 'single' || q.type === 'multi' 
              ? (q.choices || []).map((c, idx) => {
                  if (!c.text || !c.text.trim()) {
                    throw new Error(`Đáp án ${idx + 1} không được để trống`)
                  }
                  return {
                    text: c.text.trim(),
                  is_correct: (q.answer || []).includes(c.id),
                  position: idx,
                  }
                })
              : [],
          }
        }),
        }
      
      // Store description and level in settings if needed
      if (data.description) {
        payload.settings.description = data.description
      }
      if (data.level) {
        payload.settings.level = data.level
      }
      if (data.courseId) {
        payload.settings.course_id = data.courseId
      }
      
      // Handle scheduled publishing
      if (data.status === 'scheduled' && data.scheduledAt) {
        payload.settings.scheduled_at = data.scheduledAt
        if (data.endAt) {
          payload.settings.end_at = data.endAt
        }
        payload.published = false // Not published yet, will be published by scheduled task
      } else if (data.status === 'published') {
        payload.published = true
      } else {
        payload.published = false
      }
      
      // Ensure all required fields are present before sending
      if (!payload.title || !payload.title.trim()) {
        throw new Error('Tên đề thi không được để trống')
      }
      if (!payload.type) {
        throw new Error('Loại bài kiểm tra không hợp lệ')
      }
      
      // Debug: log payload to see what's being sent
      console.log('Creating exercise with payload:', JSON.stringify(payload, null, 2))
      console.log('Title:', payload.title, 'Type:', payload.type, 'Questions count:', payload.questions?.length)
      
      const { data: response } = await api.post('/activities/exercises/', payload)
        // Map response back to ExamDetail
        return {
          id: response.id,
          title: response.title,
        level: data.level || response.settings?.level || response.metadata?.level || 'Khối 1',
          durationSec: response.settings?.duration_seconds || 1800,
        passScore: response.settings?.pass_score || 10,
          questionsCount: response.questions?.length || 0,
          status: response.published ? 'published' : (response.settings?.scheduled_at ? 'scheduled' : 'draft'),
          updatedAt: response.updated_at || new Date().toISOString(),
        description: response.settings?.description || data.description || '',
          shuffleQuestions: response.settings?.shuffle_questions ?? true,
          shuffleChoices: response.settings?.shuffle_choices ?? true,
          questions: data.questions || [],
          scheduledAt: response.settings?.scheduled_at,
        courseId: response.settings?.course_id || response.metadata?.course_id || data.courseId,
        }
      } catch (e: any) {
        console.error('Create exam error:', e)
      throw new Error('Không thể tạo bài kiểm tra: ' + (e.response?.data?.detail || e.message))
    }
  },

  async update(id: ID, data: Partial<ExamDetail>): Promise<ExamDetail> {
      try {
        // Map frontend exam to backend exercise format
      const payload: any = {
          type: 'mcq', // Backend requires type field, always 'mcq' for exams
        }
      if (data.title) payload.title = data.title.trim()
      
      // Initialize settings object
          payload.settings = {}
      if (data.durationSec !== undefined) payload.settings.duration_seconds = data.durationSec
      if (data.passScore !== undefined) payload.settings.pass_score = data.passScore
          if (data.shuffleQuestions !== undefined) payload.settings.shuffle_questions = data.shuffleQuestions
          if (data.shuffleChoices !== undefined) payload.settings.shuffle_choices = data.shuffleChoices
      if (data.maxAttempts !== undefined) payload.settings.max_attempts = data.maxAttempts
      
      // Store description and level in settings (consistent with create method)
      if (data.description !== undefined) {
        payload.settings.description = data.description
      }
      if (data.level) {
        payload.settings.level = data.level
      }
      if (data.courseId) {
        payload.settings.course_id = data.courseId
      }
      
      // Handle scheduled publishing
      if (data.status === 'scheduled' && data.scheduledAt) {
        payload.settings.scheduled_at = data.scheduledAt
        if (data.endAt) {
          payload.settings.end_at = data.endAt
        }
        payload.published = false // Not published yet, will be published by scheduled task
      } else if (data.status === 'published') {
        payload.published = true
      } else if (data.status === 'draft') {
        payload.published = false
        // Clear scheduled_at and end_at if changing from scheduled to draft
        payload.settings.scheduled_at = null
        payload.settings.end_at = null
      }
      
        if (data.questions) {
        payload.questions = data.questions.map((q: Question) => {
          // Ensure prompt is not empty
          if (!q.text || !q.text.trim()) {
            throw new Error('Nội dung câu hỏi không được để trống')
          }
          
          return {
            prompt: q.text.trim(),
            meta: { type: q.type, score: q.score || 1 }, // Store question type and score in meta field
            choices: q.type === 'single' || q.type === 'multi' 
              ? (q.choices || []).map((c, idx) => {
                  if (!c.text || !c.text.trim()) {
                    throw new Error(`Đáp án ${idx + 1} không được để trống`)
                  }
                  return {
                    text: c.text.trim(),
                  is_correct: (q.answer || []).includes(c.id),
                  position: idx,
                  }
                })
              : [],
          }
        })
        }
      
      const { data: response } = await api.patch(`/activities/exercises/${id}/`, payload)
        // Map response back to ExamDetail
        return {
          id: response.id,
          title: response.title || data.title,
        level: data.level || response.settings?.level || response.metadata?.level || 'Khối 1',
          durationSec: response.settings?.duration_seconds || 1800,
        passScore: response.settings?.pass_score || 10,
          questionsCount: response.questions?.length || 0,
          status: response.published ? 'published' : (response.settings?.scheduled_at ? 'scheduled' : 'draft'),
          updatedAt: response.updated_at || new Date().toISOString(),
        description: response.settings?.description || response.description || '',
          shuffleQuestions: response.settings?.shuffle_questions ?? true,
          shuffleChoices: response.settings?.shuffle_choices ?? true,
          questions: data.questions || [],
          scheduledAt: response.settings?.scheduled_at,
          endAt: response.settings?.end_at,
        courseId: response.settings?.course_id || response.metadata?.course_id || data.courseId,
        }
      } catch (e: any) {
        console.error('Update exam error:', e)
      throw new Error('Không thể cập nhật bài kiểm tra: ' + (e.response?.data?.detail || e.message))
    }
  },
  
  // Ranking (for student)
  async ranking(examId: ID): Promise<{ top: any[]; me: any }> {
      try {
      const { data } = await api.get(`/activities/exercises/${examId}/stats/`)
        // Map backend stats to frontend ranking format
        return {
          top: (data.top_students || []).map((s: any, idx: number) => ({
            id: s.student_id || idx + 1,
            name: s.student_name || s.name || 'Học viên',
            attemptId: s.attempt_id || s.attemptId || s.id,
            avatar: s.avatar || s.avatar_url || s.photo || '',
            gender: s.gender || '',
            score: Math.round(s.total_score || s.score || 0),
            correct: s.correct_count || 0,
            total: s.total_count || 0,
            time: s.time_taken || '00:00',
          })),
          me: data.my_stats ? {
            rank: data.my_stats.rank || 0,
            score: Math.round(data.my_stats.total_score || data.my_stats.score || 0),
            correct: data.my_stats.correct_count || 0,
            total: data.my_stats.total_count || 0,
            time: data.my_stats.time_taken || '00:00',
            attemptId: data.my_stats.attempt_id || data.my_stats.attemptId,
            avatar: data.my_stats.avatar || data.my_stats.avatar_url || data.my_stats.photo || '',
            gender: data.my_stats.gender || '',
          } : null,
        }
      } catch (e: any) {
        console.error('Get ranking error:', e)
      throw new Error('Không thể tải bảng xếp hạng: ' + (e.response?.data?.detail || e.message))
    }
  },
  
  // Certificates (for student)
  async certificates(): Promise<any[]> {
      try {
        // Backend might have certificates endpoint, or derive from attempts
      const { data } = await api.get('/activities/certificates/')
        return Array.isArray(data) ? data : (data.results || data.items || [])
      } catch (e: any) {
        console.error('Get certificates error:', e)
      // Return empty array if endpoint doesn't exist
      return []
      }
  },

  async delete(id: ID): Promise<void> {
    try {
      await api.delete(`/activities/exercises/${id}/`)
    } catch (e: any) {
      console.error('Delete exam error:', e)
      throw new Error('Không thể xóa bài kiểm tra: ' + (e.response?.data?.detail || e.message))
    }
  },

  // Get attempt summary with answers
  async getAttemptSummary(attemptId: string): Promise<AttemptResult & { questions: any[]; answers: Record<string, any>; class_name?: string; student_class?: string; student?: any }> {
    try {
      const { data } = await api.get(`/activities/attempts/${attemptId}/`)
      
      // Map backend attempt summary to frontend format
      const questions = (data.questions || []).map((q: any) => {
        const points = Number(q.points || 0)
        const rawScore = Number(q.answer_score ?? q.score ?? 0)
        const normalizedScore = points > 0 && rawScore > points ? points : rawScore
        return {
          id: q.question_id || q.id,
          question_id: q.question_id || q.id,
          prompt: q.prompt || q.text,
          text: q.prompt || q.text,
          points,
          score: normalizedScore, // cap at max points
          maxScore: points,
          correct: q.correct || false,
          answer: q.answer || null,
          type: q.type || 'single',
          choices: q.choices || [],
          correct_answer: q.correct_answer || null,
          answer_score: normalizedScore,
        }
      })
      
      // Build answers map
      const answers: Record<string, any> = {}
      questions.forEach((q: any) => {
        if (q.answer !== null) {
          answers[String(q.id)] = q.answer
        }
      })
      
      // Calculate totals
      const totalScore = questions.reduce((sum: number, q: any) => sum + (q.score || 0), 0)
      const maxScore = questions.reduce((sum: number, q: any) => sum + (q.points || 0), 0)
      const correctCount = questions.filter((q: any) => q.correct).length
      const totalCount = questions.length
      
      return {
        attemptId: data.attempt_id || attemptId,
        examId: data.exercise_id,
        totalScore: totalScore || data.score || 0,
        maxScore: maxScore || totalScore,
        correctCount,
        totalCount,
        passed: maxScore ? totalScore >= 0.5 * maxScore : (data.score || totalScore) >= 50,
        detail: questions.map((q: any) => ({
          qid: q.id,
          score: q.score || 0,
          max: q.points || 0,
        })),
        questions,
        answers,
        // Keep class information so grading modal can display
        class_name: data.class_name || data.student_class || data.student?.class_name || '',
        student_class: data.student_class || data.class_name || '',
        student: data.student || null,
      }
    } catch (e: any) {
      console.error('Get attempt summary error:', e)
      throw new Error('Không thể tải chi tiết bài làm: ' + (e.response?.data?.detail || e.message))
    }
  },
}
