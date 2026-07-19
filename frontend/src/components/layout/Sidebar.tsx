import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard, DollarSign, Users, Package, ShoppingCart,
  Factory, Target, Bot
} from 'lucide-react'
import { useAuth } from '@/hooks/useAuth'
import { cn } from '@/lib/utils'

const nav = [
  { label: 'Dashboard', icon: LayoutDashboard, to: '/' },
  { label: 'Finance', icon: DollarSign, to: '/finance' },
  { label: 'Human Resources', icon: Users, to: '/hr' },
  { label: 'Inventory', icon: Package, to: '/inventory' },
  { label: 'Sales', icon: ShoppingCart, to: '/sales' },
  { label: 'CRM', icon: Target, to: '/crm' },
  { label: 'Manufacturing', icon: Factory, to: '/manufacturing' },
  { label: 'Chatbot', icon: Bot, to: '/copilot' },
]

export function Sidebar() {
  const { user, logout } = useAuth()

  return (
    <aside className="fixed inset-y-0 left-0 z-40 w-[var(--sidebar-width)] bg-slate-950 border-r border-slate-800/80">
      <div className="flex h-full flex-col">
        <div className="flex-1 overflow-y-auto">
          <div className="flex items-center gap-3 px-6 py-6 border-b border-slate-800/70">
            <div className="w-11 h-11 rounded-3xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-white font-semibold text-sm leading-tight">ERP Copilot</p>
              <p className="text-slate-400 text-xs mt-1">AI workspace for operations</p>
            </div>
          </div>

          <div className="px-6 py-4">
            <p className="text-xs uppercase tracking-[0.3em] text-slate-500 font-semibold mb-3">Navigation</p>
            <nav className="space-y-2">
              {nav.map(({ label, icon: Icon, to }) => (
                <NavLink
                  key={to}
                  to={to}
                  end={to === '/'}
                  className={({ isActive }) =>
                    cn(
                      'group flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-medium transition',
                      isActive
                        ? 'bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-lg shadow-indigo-500/20'
                        : 'text-slate-400 hover:text-white hover:bg-slate-800/80'
                    )
                  }
                >
                  <Icon className="w-4 h-4 flex-shrink-0" />
                  <span className="flex-1">{label}</span>
                </NavLink>
              ))}
            </nav>
          </div>
        </div>

        <div className="flex-shrink-0 border-t border-slate-800/70 bg-slate-950/95 px-6 py-5 backdrop-blur-lg">
          <div className="rounded-3xl bg-slate-900/95 border border-slate-800/80 p-4 shadow-xl shadow-slate-950/20">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-indigo-500 flex items-center justify-center text-white font-semibold">
                {user?.full_name?.slice(0, 2).toUpperCase() || user?.username?.slice(0, 2).toUpperCase() || 'ER'}
              </div>
              <div className="min-w-0">
                <p className="text-sm font-semibold text-white truncate">{user?.full_name || user?.username || 'Guest user'}</p>
                <p className="text-xs text-slate-500 truncate">{user?.role || 'Member'}</p>
              </div>
            </div>
            <p className="mt-3 text-xs leading-5 text-slate-500">Fast access to every module with an intelligent sidebar.</p>
            <button
              onClick={logout}
              className="mt-4 w-full rounded-2xl bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500 transition"
            >
              Log out
            </button>
          </div>
        </div>
      </div>
    </aside>
  )
}
