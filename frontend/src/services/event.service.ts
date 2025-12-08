import api from '@/config/axios'

export interface EventItem {
  id: string
  name: string
  description?: string
  start_date: string
  end_date?: string
  type: string
  status: string
  course_id?: string
  course_title?: string
  notify_students?: boolean
  time?: string
  created_at?: string
}

export interface CreateEventPayload {
  name: string
  description?: string
  start_date: string
  end_date?: string
  type?: string
  course_id?: string
  notify_students?: boolean
}

export const eventService = {
  // Get upcoming events for dashboard
  async getUpcoming(): Promise<EventItem[]> {
    const { data } = await api.get('/events/upcoming/')
    return data.items || []
  },

  // Get all events for teacher
  async getTeacherEvents(): Promise<EventItem[]> {
    const { data } = await api.get('/events/teacher/')
    return data.items || []
  },

  // Create new event
  async create(payload: CreateEventPayload): Promise<{ id: string; message: string }> {
    const { data } = await api.post('/events/teacher/', payload)
    return data
  },

  // Update event
  async update(eventId: string, payload: Partial<CreateEventPayload>): Promise<{ id: string; message: string }> {
    const { data } = await api.patch(`/events/teacher/${eventId}/`, payload)
    return data
  },

  // Delete event
  async delete(eventId: string): Promise<void> {
    await api.delete(`/events/teacher/${eventId}/`)
  },

  // Get event detail
  async getDetail(eventId: string): Promise<EventItem> {
    const { data } = await api.get(`/events/teacher/${eventId}/`)
    return data
  },
}
