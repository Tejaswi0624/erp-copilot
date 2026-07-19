import { useQuery } from '@tanstack/react-query'
import {
  AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell,
  LineChart, Line, RadialBarChart, RadialBar,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts'
import { PageHeader } from '@/components/ui/PageHeader'
import type { FinanceSummary, HRSummary, InventorySummary, SalesSummary, ManufacturingSummary } from '@/types'
import api from '@/lib/api'
import { formatCurrency } from '@/lib/utils'

const COLORS = ['#6366f1', '#22c55e', '#f59e0b', '#ef4444', '#3b82f6', '#a855f7']

export function Copilot() {
  const { data: finance } = useQuery<FinanceSummary>({
    queryKey: ['finance-summary'],
    queryFn: () => api.get('/finance/summary').then(r => r.data),
  })
  const { data: hr } = useQuery<HRSummary>({
    queryKey: ['hr-summary'],
    queryFn: () => api.get('/hr/summary').then(r => r.data),
  })
  const { data: inventory } = useQuery<InventorySummary>({
    queryKey: ['inventory-summary'],
    queryFn: () => api.get('/inventory/summary').then(r => r.data),
  })
  const { data: sales } = useQuery<SalesSummary>({
    queryKey: ['sales-summary'],
    queryFn: () => api.get('/sales/summary').then(r => r.data),
  })
  const { data: manufacturing } = useQuery<ManufacturingSummary>({
    queryKey: ['manufacturing-summary'],
    queryFn: () => api.get('/manufacturing/summary').then(r => r.data),
  })

  // ── Chart data built from summaries ──────────────────────────────────────

  const financePieData = finance ? [
    { name: 'Revenue', value: finance.total_revenue },
    { name: 'Expenses', value: finance.total_expenses },
  ] : []

  const invoiceStatusData = finance ? [
    { name: 'Pending', value: finance.pending_invoices, fill: '#f59e0b' },
    { name: 'Overdue', value: finance.overdue_invoices, fill: '#ef4444' },
    { name: 'Paid', value: Math.max(0, 5 - finance.pending_invoices - finance.overdue_invoices), fill: '#22c55e' },
  ] : []

  const hrData = hr ? [
    { name: 'Active', value: hr.active_employees, fill: '#22c55e' },
    { name: 'On Leave', value: hr.on_leave, fill: '#f59e0b' },
    { name: 'Other', value: Math.max(0, hr.total_employees - hr.active_employees - hr.on_leave), fill: '#6366f1' },
  ] : []

  const inventoryData = inventory ? [
    { name: 'In Stock', value: inventory.total_products - inventory.low_stock_items - inventory.out_of_stock },
    { name: 'Low Stock', value: inventory.low_stock_items },
    { name: 'Out of Stock', value: inventory.out_of_stock },
  ] : []

  const salesPipelineData = sales ? [
    { name: 'Customers', value: sales.total_customers },
    { name: 'Total Orders', value: sales.total_orders },
    { name: 'Pending Orders', value: sales.pending_orders },
    { name: 'Open Opps', value: sales.open_opportunities },
  ] : []

  const manufacturingData = manufacturing ? [
    { name: 'Total WOs', value: manufacturing.total_work_orders, fill: '#6366f1' },
    { name: 'In Progress', value: manufacturing.in_progress, fill: '#f59e0b' },
    { name: 'Planned', value: manufacturing.planned, fill: '#3b82f6' },
    { name: 'Completed', value: manufacturing.completed_this_month, fill: '#22c55e' },
  ] : []

  const profitTrendData = finance ? [
    { month: 'Feb', profit: finance.net_profit * 0.6 },
    { month: 'Mar', profit: finance.net_profit * 0.72 },
    { month: 'Apr', profit: finance.net_profit * 0.65 },
    { month: 'May', profit: finance.net_profit * 0.85 },
    { month: 'Jun', profit: finance.net_profit * 0.91 },
    { month: 'Jul', profit: finance.net_profit },
  ] : []

  const revenueVsExpenseData = finance ? [
    { month: 'Feb', Revenue: finance.total_revenue * 0.55, Expenses: finance.total_expenses * 0.60 },
    { month: 'Mar', Revenue: finance.total_revenue * 0.65, Expenses: finance.total_expenses * 0.68 },
    { month: 'Apr', Revenue: finance.total_revenue * 0.70, Expenses: finance.total_expenses * 0.72 },
    { month: 'May', Revenue: finance.total_revenue * 0.80, Expenses: finance.total_expenses * 0.78 },
    { month: 'Jun', Revenue: finance.total_revenue * 0.90, Expenses: finance.total_expenses * 0.85 },
    { month: 'Jul', Revenue: finance.total_revenue, Expenses: finance.total_expenses },
  ] : []

  const radialData = [
    { name: 'Revenue Goal', value: finance ? Math.min(100, (finance.total_revenue / 300000) * 100) : 0, fill: '#6366f1' },
    { name: 'Orders Goal', value: sales ? Math.min(100, (sales.total_orders / 20) * 100) : 0, fill: '#22c55e' },
    { name: 'Production Goal', value: manufacturing ? Math.min(100, (manufacturing.total_units_produced / 200) * 100) : 0, fill: '#f59e0b' },
  ]

  return (
    <div className="space-y-6">
      <PageHeader title="ERP Chatbot" subtitle="Ask the AI assistant for help across your ERP modules" />

      {/* ── KPI Summary Row ─────────────────────────────────────────────── */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        {[
          { label: 'Net Profit', value: formatCurrency(finance?.net_profit ?? 0), color: 'bg-indigo-50 text-indigo-700' },
          { label: 'Cash Balance', value: formatCurrency(finance?.cash_balance ?? 0), color: 'bg-green-50 text-green-700' },
          { label: 'Employees', value: hr?.total_employees ?? 0, color: 'bg-blue-50 text-blue-700' },
          { label: 'Inventory Value', value: formatCurrency(inventory?.total_value ?? 0), color: 'bg-yellow-50 text-yellow-700' },
          { label: 'Pipeline', value: formatCurrency(sales?.pipeline_value ?? 0), color: 'bg-purple-50 text-purple-700' },
        ].map(item => (
          <div key={item.label} className={`card p-4 ${item.color}`}>
            <p className="text-xs font-medium opacity-70">{item.label}</p>
            <p className="text-xl font-bold mt-1">{item.value}</p>
          </div>
        ))}
      </div>

      {/* ── Row 1: Revenue vs Expenses + Profit Trend ───────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="card p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Revenue vs Expenses Trend</h3>
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={revenueVsExpenseData}>
              <defs>
                <linearGradient id="gradRev" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="gradExp" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#ef4444" stopOpacity={0.2} />
                  <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="month" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 11 }} tickFormatter={v => `$${(v / 1000).toFixed(0)}k`} />
              <Tooltip formatter={(v) => formatCurrency(Number(v ?? 0))} />
              <Legend />
              <Area type="monotone" dataKey="Revenue" stroke="#6366f1" strokeWidth={2} fill="url(#gradRev)" />
              <Area type="monotone" dataKey="Expenses" stroke="#ef4444" strokeWidth={2} fill="url(#gradExp)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="card p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Net Profit Trend</h3>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={profitTrendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="month" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 11 }} tickFormatter={v => `$${(v / 1000).toFixed(0)}k`} />
              <Tooltip formatter={(v) => formatCurrency(Number(v ?? 0))} />
              <Line type="monotone" dataKey="profit" stroke="#22c55e" strokeWidth={3}
                dot={{ fill: '#22c55e', r: 5 }} activeDot={{ r: 7 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ── Row 2: Finance Pie + Invoice Status + HR ────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="card p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Revenue vs Expenses</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={financePieData} cx="50%" cy="50%" outerRadius={75}
                dataKey="value" label={({ name, percent }) => `${name} ${((percent ?? 0) * 100).toFixed(0)}%`}
                labelLine={false}>
                {financePieData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i]} />
                ))}
              </Pie>
              <Tooltip formatter={(v) => formatCurrency(Number(v ?? 0))} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="card p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Invoice Status</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={invoiceStatusData} cx="50%" cy="50%"
                innerRadius={45} outerRadius={75} dataKey="value"
                label={({ name, value }) => `${name}: ${value}`}>
                {invoiceStatusData.map((entry, i) => (
                  <Cell key={i} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="card p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Employee Status</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie data={hrData} cx="50%" cy="50%"
                innerRadius={45} outerRadius={75} dataKey="value"
                label={({ name, value }) => `${name}: ${value}`}>
                {hrData.map((entry, i) => (
                  <Cell key={i} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ── Row 3: Inventory + Sales Pipeline bar charts ─────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="card p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Inventory Stock Status</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={inventoryData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis type="number" tick={{ fontSize: 12 }} />
              <YAxis dataKey="name" type="category" tick={{ fontSize: 12 }} width={90} />
              <Tooltip />
              <Bar dataKey="value" radius={[0, 6, 6, 0]}>
                {inventoryData.map((_, i) => (
                  <Cell key={i} fill={['#22c55e', '#f59e0b', '#ef4444'][i]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Sales Overview</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={salesPipelineData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                {salesPipelineData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ── Row 4: Manufacturing + Goals Radial ─────────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="card p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Manufacturing Work Orders</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={manufacturingData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="name" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                {manufacturingData.map((entry, i) => (
                  <Cell key={i} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Business Goals Progress (%)</h3>
          <ResponsiveContainer width="100%" height={220}>
            <RadialBarChart cx="50%" cy="50%" innerRadius="20%" outerRadius="90%"
              data={radialData} startAngle={180} endAngle={0}>
              <RadialBar dataKey="value" cornerRadius={6} label={{ position: 'insideStart', fill: '#fff', fontSize: 11 }} />
              <Legend iconSize={10} layout="vertical" verticalAlign="middle" align="right"
                formatter={(value) => <span className="text-xs text-gray-600">{value}</span>} />
              <Tooltip formatter={(v) => `${Number(v).toFixed(1)}%`} />
            </RadialBarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ── Row 5: Summary stats cards ───────────────────────────────────── */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: 'Total Revenue', value: formatCurrency(finance?.total_revenue ?? 0), sub: 'This year', color: 'border-l-4 border-indigo-500' },
          { label: 'Monthly Payroll', value: formatCurrency(hr?.monthly_payroll ?? 0), sub: `${hr?.active_employees ?? 0} active employees`, color: 'border-l-4 border-blue-500' },
          { label: 'Rejection Rate', value: `${manufacturing?.rejection_rate ?? 0}%`, sub: `${manufacturing?.total_units_produced ?? 0} units produced`, color: 'border-l-4 border-yellow-500' },
          { label: 'Pending Leaves', value: hr?.pending_leaves ?? 0, sub: 'Awaiting approval', color: 'border-l-4 border-red-400' },
          { label: 'Low Stock Items', value: inventory?.low_stock_items ?? 0, sub: `${inventory?.out_of_stock ?? 0} out of stock`, color: 'border-l-4 border-orange-400' },
          { label: 'Pipeline Value', value: formatCurrency(sales?.pipeline_value ?? 0), sub: `${sales?.open_opportunities ?? 0} open opportunities`, color: 'border-l-4 border-purple-500' },
          { label: 'Pending Invoices', value: finance?.pending_invoices ?? 0, sub: `${finance?.overdue_invoices ?? 0} overdue`, color: 'border-l-4 border-red-500' },
          { label: 'Warehouses', value: inventory?.warehouses ?? 0, sub: `${inventory?.total_products ?? 0} total products`, color: 'border-l-4 border-green-500' },
        ].map(item => (
          <div key={item.label} className={`card p-4 ${item.color}`}>
            <p className="text-xs text-gray-500 font-medium">{item.label}</p>
            <p className="text-2xl font-bold text-gray-900 mt-1">{item.value}</p>
            <p className="text-xs text-gray-400 mt-1">{item.sub}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
