// src/services/exam.service.ts
import api from '@/config/axios'

export type ID = string | number
export type Level = 'Khối 1–2' | 'Khối 3–5'
export type ExamStatus = 'draft' | 'published' | 'archived'

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
}

export interface ExamDetail extends ExamSummary {
  description?: string
  shuffleQuestions?: boolean
  shuffleChoices?: boolean
  questions: Question[]
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
  const durationSec = level === 'Khối 1–2' ? 20 * 60 : 30 * 60

  return {
    id,
    title: `Đề luyện tập #${id} – ${level}`,
    level,
    durationSec,
    passScore: 12, // ví dụ
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
  buildMockExam(101, 'Khối 1–2'),
  buildMockExam(102, 'Khối 1–2'),
  buildMockExam(201, 'Khối 3–5'),
  buildMockExam(202, 'Khối 3–5'),
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
  async list(params?: { level?: Level; q?: string }): Promise<ExamSummary[]> {
    if (!USE_MOCK) {
      try {
        const { data } = await api.get('/api/activities/exercises/', { params })
        // Map backend exercise to frontend exam format
        const exercises = Array.isArray(data) ? data : (data.results || data.items || [])
        return exercises.map((ex: any) => ({
          id: ex.id,
          title: ex.title || 'Đề thi',
          level: ex.level || 'Khối 1–2',
          durationSec: ex.settings?.duration_seconds || 1800,
          passScore: ex.settings?.pass_score || 12,
          questionsCount: ex.questions?.length || 0,
          status: ex.published ? 'published' : 'draft',
          updatedAt: ex.updated_at || ex.updatedAt || new Date().toISOString(),
        }))
      } catch (e: any) {
        console.error('Load exams error:', e)
        // Fallback to mock on error
      }
    }
    let list = MOCK_EXAMS.slice()
    if (params?.level) list = list.filter(e => e.level === params.level)
    if (params?.q) {
      const key = params.q.toLowerCase()
      list = list.filter(e => e.title.toLowerCase().includes(key))
    }
    return list.map(toSummary)
  },

  async detail(id: ID): Promise<ExamDetail> {
    if (!USE_MOCK) {
      try {
        const { data } = await api.get(`/api/activities/exercises/${id}/`)
        // Map backend exercise to frontend exam format
        return {
          id: data.id,
          title: data.title || 'Đề thi',
          level: data.level || 'Khối 1–2',
          durationSec: data.settings?.duration_seconds || 1800,
          passScore: data.settings?.pass_score || 12,
          questionsCount: data.questions?.length || 0,
          status: data.published ? 'published' : 'draft',
          updatedAt: data.updated_at || data.updatedAt || new Date().toISOString(),
          description: data.description,
          shuffleQuestions: data.settings?.shuffle_questions ?? true,
          shuffleChoices: data.settings?.shuffle_choices ?? true,
          questions: (data.questions || []).map((q: any) => {
            // Map backend question to frontend question format
            const base: QuestionBase = {
              id: q.id,
              type: q.type || 'single',
              text: q.prompt || q.text || '',
              score: q.score || 1,
            }
            if (q.type === 'single' || q.type === 'multi') {
              return {
                ...base,
                type: q.type,
                choices: (q.choices || []).map((c: any, idx: number) => ({
                  id: c.id || `c${idx + 1}`,
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
        // Fallback to mock on error
      }
    }
    const found = MOCK_EXAMS.find(e => String(e.id) === String(id))
    if (!found) throw new Error('Không tìm thấy đề thi')
    // deep-clone để tránh mutate bank
    return JSON.parse(JSON.stringify(found))
  },

  async startAttempt(examId: ID): Promise<Attempt> {
    if (!USE_MOCK) {
      try {
        const { data } = await api.post(`/api/activities/exercises/${examId}/start/`)
        // Map backend attempt to frontend attempt format
        return {
          id: data.id || data.attempt_id,
          examId: examId,
          startedAt: data.started_at || data.startedAt || new Date().toISOString(),
          deadlineAt: data.deadline_at || data.deadlineAt || new Date(Date.now() + 1800000).toISOString(),
          questions: (data.questions || []).map((q: any) => {
            const base: AttemptQuestion = {
              id: q.id,
              type: q.type || 'single',
              text: q.prompt || q.text || '',
              score: q.score || 1,
            }
            if (q.type === 'single' || q.type === 'multi') base.choices = (q.choices || []).map((c: any) => ({
              id: c.id,
              text: c.text || '',
            }))
            if (q.type === 'fill') base.blanks = q.blanks || 1
            if (q.type === 'match') base.pairs = q.pairs || []
            if (q.type === 'order') base.items = q.items || []
            return base
          }),
          answers: data.answers || {},
        }
      } catch (e: any) {
        console.error('Start attempt error:', e)
        throw e
      }
    }
    const d = await this.detail(examId)
    // shuffle questions/choices nếu bật
    let qs = d.questions.slice()
    if (d.shuffleQuestions) qs = randPick(qs, qs.length)
    if (d.shuffleChoices) {
      qs = qs.map(q =>
        q.type === 'single' || q.type === 'multi'
          ? { ...q, choices: randPick(q.choices, q.choices.length) }
          : q,
      )
    }
    const att: Attempt = {
      id: 'att_' + Math.random().toString(36).slice(2, 9),
      examId,
      startedAt: new Date().toISOString(),
      deadlineAt: new Date(Date.now() + d.durationSec * 1000).toISOString(),
      questions: qs.map(q => {
        const base: AttemptQuestion = {
          id: q.id, type: q.type, text: q.text, score: q.score,
        }
        if (q.type === 'single' || q.type === 'multi') base.choices = q.choices
        if (q.type === 'fill') base.blanks = q.blanks
        if (q.type === 'match') base.pairs = q.pairs
        if (q.type === 'order') base.items = q.answer // hiển thị items để kéo-thả
        return base
      }),
      answers: {},
    }
    // lưu localStorage mock
    localStorage.setItem(`attempt:${att.id}`, JSON.stringify(att))
    return att
  },

  async submit(examId: ID, attemptId: string, answers: Record<string, any>): Promise<AttemptResult> {
    if (!USE_MOCK) {
      try {
        // Submit all answers
        for (const [questionId, answer] of Object.entries(answers)) {
          await api.post(`/api/activities/attempts/${attemptId}/answers/`, {
            question_id: questionId,
            answer: answer,
          })
        }
        // Finalize attempt
        const { data } = await api.post(`/api/activities/attempts/${attemptId}/finalize/`)
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
        throw e
      }
    }
    const d = await this.detail(examId)
    let totalScore = 0
    let maxScore = 0
    let correctCount = 0
    const detail: AttemptResult['detail'] = []

    for (const q of d.questions) {
      const ans = answers[String(q.id)]
      const got = scoreQuestion(q, ans)
      totalScore += got
      maxScore += q.score
      if (Math.abs(got - q.score) < 1e-6) correctCount++
      detail.push({ qid: q.id, score: Number(got.toFixed(2)), max: q.score })
    }

    const passed = totalScore >= d.passScore
    const res: AttemptResult = {
      attemptId: attemptId,
      examId,
      totalScore: Number(totalScore.toFixed(2)),
      maxScore,
      correctCount,
      totalCount: d.questions.length,
      passed,
      detail,
    }
    // lưu result
    localStorage.setItem(`attempt:${attemptId}:result`, JSON.stringify(res))
    return res
  },

  async create(data: Partial<ExamDetail>): Promise<ExamDetail> {
    if (!USE_MOCK) {
      try {
        // Map frontend exam to backend exercise format
        const payload = {
          title: data.title,
          type: 'exam',
          settings: {
            duration_seconds: data.durationSec || 1800,
            pass_score: data.passScore || 12,
            shuffle_questions: data.shuffleQuestions ?? true,
            shuffle_choices: data.shuffleChoices ?? true,
          },
          questions: (data.questions || []).map((q: Question) => ({
            prompt: q.text,
            type: q.type,
            score: q.score,
            choices: q.type === 'single' || q.type === 'multi' 
              ? (q.choices || []).map((c, idx) => ({
                  text: c.text,
                  is_correct: (q.answer || []).includes(c.id),
                  position: idx,
                }))
              : [],
          })),
        }
        const { data: response } = await api.post('/api/activities/exercises/', payload)
        // Map response back to ExamDetail
        return {
          id: response.id,
          title: response.title,
          level: data.level || 'Khối 1–2',
          durationSec: response.settings?.duration_seconds || 1800,
          passScore: response.settings?.pass_score || 12,
          questionsCount: response.questions?.length || 0,
          status: response.published ? 'published' : 'draft',
          updatedAt: response.updated_at || new Date().toISOString(),
          description: data.description,
          shuffleQuestions: response.settings?.shuffle_questions ?? true,
          shuffleChoices: response.settings?.shuffle_choices ?? true,
          questions: data.questions || [],
        }
      } catch (e: any) {
        console.error('Create exam error:', e)
        throw e
      }
    }
    // Mock: tạo ID mới
    const newId = Math.max(...MOCK_EXAMS.map(e => Number(e.id))) + 1
    const exam: ExamDetail = {
      id: newId,
      title: data.title || `Đề mới #${newId}`,
      level: data.level || 'Khối 1–2',
      durationSec: data.durationSec || 1800,
      passScore: data.passScore || 12,
      questionsCount: data.questions?.length || 0,
      status: data.status || 'draft',
      updatedAt: new Date().toISOString(),
      description: data.description,
      shuffleQuestions: data.shuffleQuestions ?? true,
      shuffleChoices: data.shuffleChoices ?? true,
      questions: data.questions || [],
    }
    MOCK_EXAMS.push(exam)
    return JSON.parse(JSON.stringify(exam))
  },

  async update(id: ID, data: Partial<ExamDetail>): Promise<ExamDetail> {
    if (!USE_MOCK) {
      try {
        // Map frontend exam to backend exercise format
        const payload: any = {}
        if (data.title) payload.title = data.title
        if (data.description !== undefined) payload.description = data.description
        if (data.durationSec || data.passScore || data.shuffleQuestions !== undefined || data.shuffleChoices !== undefined) {
          payload.settings = {}
          if (data.durationSec) payload.settings.duration_seconds = data.durationSec
          if (data.passScore) payload.settings.pass_score = data.passScore
          if (data.shuffleQuestions !== undefined) payload.settings.shuffle_questions = data.shuffleQuestions
          if (data.shuffleChoices !== undefined) payload.settings.shuffle_choices = data.shuffleChoices
        }
        if (data.questions) {
          payload.questions = data.questions.map((q: Question) => ({
            prompt: q.text,
            type: q.type,
            score: q.score,
            choices: q.type === 'single' || q.type === 'multi' 
              ? (q.choices || []).map((c, idx) => ({
                  text: c.text,
                  is_correct: (q.answer || []).includes(c.id),
                  position: idx,
                }))
              : [],
          }))
        }
        const { data: response } = await api.patch(`/api/activities/exercises/${id}/`, payload)
        // Map response back to ExamDetail
        return {
          id: response.id,
          title: response.title,
          level: data.level || 'Khối 1–2',
          durationSec: response.settings?.duration_seconds || 1800,
          passScore: response.settings?.pass_score || 12,
          questionsCount: response.questions?.length || 0,
          status: response.published ? 'published' : 'draft',
          updatedAt: response.updated_at || new Date().toISOString(),
          description: response.description,
          shuffleQuestions: response.settings?.shuffle_questions ?? true,
          shuffleChoices: response.settings?.shuffle_choices ?? true,
          questions: data.questions || [],
        }
      } catch (e: any) {
        console.error('Update exam error:', e)
        throw e
      }
    }
    const index = MOCK_EXAMS.findIndex(e => String(e.id) === String(id))
    if (index === -1) throw new Error('Không tìm thấy đề thi')
    
    const existing = MOCK_EXAMS[index]
    const updated: ExamDetail = {
      ...existing,
      ...data,
      id: existing.id, // giữ nguyên ID
      questionsCount: data.questions?.length ?? existing.questionsCount,
      updatedAt: new Date().toISOString(),
    }
    MOCK_EXAMS[index] = updated
    return JSON.parse(JSON.stringify(updated))
  },
  
  // Ranking (for student)
  async ranking(examId: ID): Promise<{ top: any[]; me: any }> {
    if (!USE_MOCK) {
      try {
        const { data } = await api.get(`/api/activities/exercises/${examId}/stats/`)
        // Map backend stats to frontend ranking format
        return {
          top: (data.top_students || []).map((s: any, idx: number) => ({
            id: idx + 1,
            name: s.student_name || s.name || 'Học viên',
            score: s.total_score || s.score || 0,
            correct: s.correct_count || 0,
            total: s.total_count || 0,
            time: s.time_taken || '00:00',
          })),
          me: data.my_stats ? {
            rank: data.my_stats.rank || 0,
            score: data.my_stats.total_score || 0,
            correct: data.my_stats.correct_count || 0,
            total: data.my_stats.total_count || 0,
            time: data.my_stats.time_taken || '00:00',
          } : null,
        }
      } catch (e: any) {
        console.error('Get ranking error:', e)
        // Fallback to mock
      }
    }
    // Mock ranking
    const N = 73
    const top: any[] = Array.from({ length: N }).map((_, i) => {
      const correct = 50 - Math.floor(i / 2)
      const score = Math.max(0, correct * 20)
      const mm = (15 + (i % 20)).toString().padStart(2, '0')
      const ss = ((i * 7) % 60).toString().padStart(2, '0')
      return { id: i + 1, name: `Học viên ${String.fromCharCode(65 + i)}`, score, correct, total: 50, time: `${mm}:${ss}` }
    })
    return { top, me: { rank: 88, score: 720, correct: 36, total: 50, time: '22:31' } }
  },
  
  // Certificates (for student)
  async certificates(): Promise<any[]> {
    if (!USE_MOCK) {
      try {
        // Backend might have certificates endpoint, or derive from attempts
        const { data } = await api.get('/api/activities/certificates/')
        return Array.isArray(data) ? data : (data.results || data.items || [])
      } catch (e: any) {
        console.error('Get certificates error:', e)
        // Fallback to mock
      }
    }
    // Mock certificates
    const result = []
    for (let i = 0; i < 4; i++) {
      result.push({
        id: i+1,
        title: `Chứng chỉ Đề #${i+1}`,
        score: 90 - i*5,
        total: 100,
        issuedAt: '2025-03-1' + i,
        thumbnail: `https://picsum.photos/seed/cert-${i}/640/360`,
        image: `https://picsum.photos/seed/cert-${i}/960/540`,
        pdf: ''
      })
    }
    return result
  },
}
