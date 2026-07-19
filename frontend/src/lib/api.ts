import axios from 'axios'

// Demo mode detection: force with VITE_FORCE_DEMO, or enable automatically on Vercel domain
const FORCE_DEMO = import.meta.env.VITE_FORCE_DEMO === 'true'
const IS_VERCEL = typeof window !== 'undefined' && window.location.hostname.endsWith('vercel.app')
const DEMO_MODE = FORCE_DEMO || IS_VERCEL

// Simple demo users (matches backend seed)
const DEMO_USERS = {
  admin: { username: 'admin', password: 'admin123', role: 'admin', full_name: 'Admin User', email: 'admin@erp.com', id: 1 },
  finance: { username: 'finance', password: 'finance123', role: 'finance', full_name: 'Finance Manager', email: 'finance@erp.com', id: 2 },
  hr: { username: 'hr', password: 'hr123', role: 'hr', full_name: 'HR Manager', email: 'hr@erp.com', id: 3 },
  sales: { username: 'sales', password: 'sales123', role: 'sales', full_name: 'Sales Manager', email: 'sales@erp.com', id: 4 },
}

function makeDemoResponse(data: any) {
  return Promise.resolve({ data })
}

function demoHandler(method: string, url: string, payload?: any) {
  // Normalize URL
  const path = url.replace(/^\/|\/?$/g, '')

  // Auth
  if (method === 'post' && path === 'auth/login') {
    const { username, password } = payload || {}
    const user = Object.values(DEMO_USERS).find((u: any) => u.username === username && u.password === password)
    if (!user) return Promise.reject({ response: { status: 401, data: { detail: 'Invalid credentials' } } })
    const access_token = `demo-token-${user.username}`
    const tokenResponse = { access_token, user }
    return makeDemoResponse(tokenResponse)
  }

  if (method === 'get' && path === 'auth/me') {
    // return stored demo user if token present
    const token = localStorage.getItem('token')
    if (!token) return Promise.reject({ response: { status: 401 } })
    const username = token.replace('demo-token-', '')
    const user = Object.values(DEMO_USERS).find((u: any) => u.username === username)
    return makeDemoResponse(user)
  }

  // Dashboard summary (minimal mock)
  if (method === 'get' && path === 'dashboard/') {
    const summary = {
      revenue: { title: 'Revenue (This Month)', value: '$85,400.00', change: 4.2, trend: 'up', icon: 'trending-up' },
      expenses: { title: 'Expenses (This Month)', value: '$42,300.00', change: -1.1, trend: 'down', icon: 'trending-down' },
      employees: { title: 'Active Employees', value: '128', change: 0.0, trend: 'neutral', icon: 'users' },
      open_orders: { title: 'Open Orders', value: '12', change: 0.0, trend: 'neutral', icon: 'shopping-cart' },
      revenue_chart: [{ label: 'Feb', value: 50000 }, { label: 'Mar', value: 60000 }],
      expense_chart: [{ label: 'Feb', value: 30000 }, { label: 'Mar', value: 35000 }],
      recent_invoices: [],
      recent_orders: [],
      alerts: [],
    }
    return makeDemoResponse(summary)
  }

  // Copilot chat mock
  if (method === 'post' && path === 'copilot/chat') {
    const message = payload?.message || ''
    const reply = `Demo assistant: I received your message "${message}". This is a demo response.`
    return makeDemoResponse({ reply: { content: reply } })
  }

  // Default: empty successful response
  return makeDemoResponse({})
}

let api: any

if (DEMO_MODE) {
  // mock API that resembles axios instance methods
  api = {
    get: (url: string, _config?: any) => demoHandler('get', url.replace(/^\//, ''), undefined),
    post: (url: string, payload?: any) => demoHandler('post', url.replace(/^\//, ''), payload),
    put: (url: string, payload?: any) => demoHandler('put', url.replace(/^\//, ''), payload),
    delete: (url: string) => demoHandler('delete', url.replace(/^\//, ''), undefined),
  }
} else {
  api = axios.create({
    baseURL: '/api',
    headers: { 'Content-Type': 'application/json' },
  })

  // Attach token from localStorage on every request
  api.interceptors.request.use((config: any) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })

  // On 401, clear token and redirect to login
  api.interceptors.response.use(
    (response: any) => response,
    (error: any) => {
      if (error.response?.status === 401) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        window.location.href = '/login'
      }
      return Promise.reject(error)
    }
  )
}

export default api
