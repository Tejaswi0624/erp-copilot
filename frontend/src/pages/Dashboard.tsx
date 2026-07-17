import { useQuery } from '@tanstack/react-query'
import {
  AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Legend
} from 'recharts'
import { AlertCircle } from 'lucide-react'
import { PageHeader } from '@/components/ui/PageHeader'
import { StatCard } from '@/components/ui/StatCard'
import type { DashboardSummary } from '@/types'
import api from '@/lib/api'
import { formatCurrency, formatDate, getStatusColor, capitalize } from '@/lib/utils'

function useDashboard() {
  return useQuery<DashboardSummary>({
    queryKey: ['dashboard'],
    queryFn: () => api.get('/dashboard/').then((r) => r.data),
    refetchInterval: 60_000,
  })
}

export function Dashboard() {
  const { data, isLoading } = useDashboard()

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center space-y-3">
          <div className="w-10 h-10 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-gray-500 text-sm">Loading dashboard…</p>
        </div>
      </div>
    )
  }

  if (!data) return null

  // Merge revenue + expense chart data
  const chartData = data.revenue_chart.map((point, i) => ({
    label: point.label,
    Revenue: point.value,
    Expenses: data.expense_chart[i]?.value ?? 0,
  }))

  return (
    <div className="space-y-6">
      <PageHeader title="Dashboard" subtitle="Welcome back — here's what's happening today." />

      {/* Alerts */}
      {data.alerts.length > 0 && (
        <div className="space-y-2">
          {data.alerts.map((alert, i) => (
            <div key={i} className="flex items-center gap-3 px-4 py-3 bg-amber-50 border border-amber-200 rounded-lg text-sm text-amber-800">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              {alert}
            </div>
          ))}
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard kpi={data.revenue} colorClass="text-green-600 bg-green-50" />
        <StatCard kpi={data.expenses} colorClass="text-red-500 bg-red-50" />
        <StatCard kpi={data.employees} colorClass="text-indigo-600 bg-indigo-50" />
        <StatCard kpi={data.open_orders} colorClass="text-orange-500 bg-orange-50" />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="card p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Revenue vs Expenses (6 months)</h3>
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="colorRev" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.15} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="colorExp" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.15} />
                  <stop offset="95%" stopColor="#f43f5e" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="label" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
              <Tooltip formatter={(v) => formatCurrency(Number(v ?? 0))} />
              <Legend />
              <Area type="monotone" dataKey="Revenue" stroke="#6366f1" strokeWidth={2} fill="url(#colorRev)" />
              <Area type="monotone" dataKey="Expenses" stroke="#f43f5e" strokeWidth={2} fill="url(#colorExp)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="card p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Monthly Comparison</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="label" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`} />
              <Tooltip formatter={(v) => formatCurrency(Number(v ?? 0))} />
              <Legend />
              <Bar dataKey="Revenue" fill="#6366f1" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Expenses" fill="#f43f5e" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent activity tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="card p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Recent Invoices</h3>
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left py-2 px-1 text-xs font-medium text-gray-500">Invoice</th>
                <th className="text-left py-2 px-1 text-xs font-medium text-gray-500">Customer</th>
                <th className="text-left py-2 px-1 text-xs font-medium text-gray-500">Amount</th>
                <th className="text-left py-2 px-1 text-xs font-medium text-gray-500">Status</th>
              </tr>
            </thead>
            <tbody>
              {data.recent_invoices.map((inv: Record<string, unknown>) => (
                <tr key={inv.id as number} className="border-b border-gray-50 hover:bg-gray-50">
                  <td className="py-2.5 px-1 font-mono text-xs text-indigo-600">{inv.invoice_number as string}</td>
                  <td className="py-2.5 px-1 text-gray-700">{inv.customer_name as string}</td>
                  <td className="py-2.5 px-1 text-gray-700">{formatCurrency(inv.total as number)}</td>
                  <td className="py-2.5 px-1">
                    <span className={getStatusColor(inv.status as string)}>{capitalize(inv.status as string)}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="card p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Recent Orders</h3>
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-gray-100">
                <th className="text-left py-2 px-1 text-xs font-medium text-gray-500">Order</th>
                <th className="text-left py-2 px-1 text-xs font-medium text-gray-500">Date</th>
                <th className="text-left py-2 px-1 text-xs font-medium text-gray-500">Total</th>
                <th className="text-left py-2 px-1 text-xs font-medium text-gray-500">Status</th>
              </tr>
            </thead>
            <tbody>
              {data.recent_orders.map((order: Record<string, unknown>) => (
                <tr key={order.id as number} className="border-b border-gray-50 hover:bg-gray-50">
                  <td className="py-2.5 px-1 font-mono text-xs text-indigo-600">{order.order_number as string}</td>
                  <td className="py-2.5 px-1 text-gray-500 text-xs">{formatDate(order.order_date as string)}</td>
                  <td className="py-2.5 px-1 text-gray-700">{formatCurrency(order.total as number)}</td>
                  <td className="py-2.5 px-1">
                    <span className={getStatusColor(order.status as string)}>{capitalize(order.status as string)}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
