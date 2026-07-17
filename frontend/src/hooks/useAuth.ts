import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User } from '@/types'
import api from '@/lib/api'

interface AuthState {
  user: User | null
  token: string | null
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: () => boolean
}

export const useAuth = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      login: async (username, password) => {
        const res = await api.post('/auth/login', { username, password })
        const { access_token, user } = res.data
        localStorage.setItem('token', access_token)
        set({ token: access_token, user })
      },
      logout: () => {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        set({ token: null, user: null })
        window.location.href = '/login'
      },
      isAuthenticated: () => !!get().token && !!get().user,
    }),
    {
      name: 'erp-auth',
      partialize: (state) => ({ user: state.user, token: state.token }),
    }
  )
)
