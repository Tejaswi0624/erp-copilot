import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { PageHeader } from '@/components/ui/PageHeader'
import { DataTable } from '@/components/ui/DataTable'
import type { Customer, SalesOrder, Opportunity, SalesSummary } from '@/types'
import api from '@/lib/api'
import { formatCurrency, formatDate, getStatusColor, capitalize } from '@/lib/utils'

type Tab = 'overview' | 'customers' | 'orders' | 'pipeline'

export function Sales() {
  const [tab, setTab] = useState<Tab>('overview')

  const { data: summary } = useQuery<SalesSummary>({
    queryKey: ['sales-summary'],
    queryFn: () => api.get('/sales/summary').then(r => r.data),
  })
  const { data: customers, isLoading: loadingCust } = useQuery<Customer[]>({
    queryKey: ['customers'],
    queryFn: () => api.get('/sales/customers').then(r => r.data),
    enabled: tab === 'customers' || tab === 'overview',
  })
  const { data: orders, isLoading: loadingOrders } = useQuery<SalesOrder[]>({
    queryKey: ['sales-orders'],
    queryFn: () => api.get('/sales/orders').then(r => r.data),
    enabled: tab === 'orders' || tab === 'overview',
  })
  const { data: opportunities, isLoading: loadingOpps } = useQuery<Opportunity[]>({
    queryKey: ['opportunities'],
    queryFn: () => api.get('/sales/opportunities').then(r => r.data),
    enabled: tab === 'pipeline' || tab === 'overview',
  })

  const tabs: { id: Tab; label: string }[] = [
    { id: 'overview', label: 'Overview' },
    { id: 'customers', label: 'Customers' },
    { id: 'orders', label: 'Orders' },
    { id: 'pipeline', label: 'Pipeline' },
  ]

  const STAGE_ORDER = ['prospecting', 'qualification', 'proposal', 'negotiation', 'closed_won', 'closed_lost']

  return (
    <div className="space-y-6">
      <PageHeader title="Sales" subtitle="Manage customers, orders, and your sales pipeline" />

      <div className="flex gap-1 p-1 bg-gray-100 rounded-xl w-fit">
        {tabs.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${tab === t.id ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'}`}>
            {t.label}
          </button>
        ))}
      </div>

      {tab === 'overview' && summary && (
        <div className="space-y-6">
          <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { label: 'Total Customers', value: summary.total_customers },
              { label: 'Total Orders', value: summary.total_orders },
              { label: 'Total Revenue', value: formatCurrency(summary.total_revenue) },
              { label: 'Pending Orders', value: summary.pending_orders },
              { label: 'Pipeline Value', value: formatCurrency(summary.pipeline_value) },
              { label: 'Open Opportunities', value: summary.open_opportunities },
            ].map(item => (
              <div key={item.label} className="card p-5">
                <p className="text-sm text-gray-500">{item.label}</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{item.value}</p>
              </div>
            ))}
          </div>

          {/* Pipeline kanban summary */}
          {opportunities && (
            <div className="card p-5">
              <h3 className="font-semibold text-gray-900 mb-4">Pipeline Overview</h3>
              <div className="grid grid-cols-3 lg:grid-cols-6 gap-2">
                {STAGE_ORDER.map(stage => {
                  const opps = opportunities.filter(o => o.stage === stage)
                  const value = opps.reduce((sum, o) => sum + o.value, 0)
                  return (
                    <div key={stage} className="text-center p-3 rounded-lg bg-gray-50 border border-gray-100">
                      <p className="text-xs font-medium text-gray-500 mb-1">{capitalize(stage)}</p>
                      <p className="text-lg font-bold text-gray-900">{opps.length}</p>
                      <p className="text-xs text-indigo-600 font-medium">{formatCurrency(value)}</p>
                    </div>
                  )
                })}
              </div>
            </div>
          )}

          {orders && (
            <div className="card p-5">
              <h3 className="font-semibold text-gray-900 mb-4">Recent Orders</h3>
              <DataTable<SalesOrder>
                data={orders.slice(0, 8)}
                columns={[
                  { key: 'order_number', header: 'Order #', render: r => <span className="font-mono text-xs text-indigo-600">{r.order_number}</span> },
                  { key: 'customer_id', header: 'Customer ID' },
                  { key: 'total', header: 'Total', render: r => <span className="font-semibold">{formatCurrency(r.total)}</span> },
                  { key: 'status', header: 'Status', render: r => <span className={getStatusColor(r.status)}>{capitalize(r.status)}</span> },
                  { key: 'order_date', header: 'Date', render: r => formatDate(r.order_date) },
                ]}
              />
            </div>
          )}
        </div>
      )}

      {tab === 'customers' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">All Customers</h3></div>
          <DataTable<Customer>
            loading={loadingCust}
            data={customers ?? []}
            columns={[
              { key: 'name', header: 'Name', render: r => <span className="font-medium">{r.name}</span> },
              { key: 'company', header: 'Company', render: r => r.company ?? '—' },
              { key: 'email', header: 'Email' },
              { key: 'city', header: 'City', render: r => `${r.city ?? '—'}${r.country ? ', ' + r.country : ''}` },
              { key: 'total_orders', header: 'Orders' },
              { key: 'total_revenue', header: 'Revenue', render: r => formatCurrency(r.total_revenue) },
              { key: 'credit_limit', header: 'Credit Limit', render: r => formatCurrency(r.credit_limit) },
              { key: 'is_active', header: 'Status', render: r => <span className={r.is_active ? 'badge-green' : 'badge-gray'}>{r.is_active ? 'Active' : 'Inactive'}</span> },
            ]}
          />
        </div>
      )}

      {tab === 'orders' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">All Orders</h3></div>
          <DataTable<SalesOrder>
            loading={loadingOrders}
            data={orders ?? []}
            columns={[
              { key: 'order_number', header: 'Order #', render: r => <span className="font-mono text-xs text-indigo-600">{r.order_number}</span> },
              { key: 'customer_id', header: 'Customer ID' },
              { key: 'subtotal', header: 'Subtotal', render: r => formatCurrency(r.subtotal) },
              { key: 'discount', header: 'Discount', render: r => formatCurrency(r.discount) },
              { key: 'tax', header: 'Tax', render: r => formatCurrency(r.tax) },
              { key: 'total', header: 'Total', render: r => <span className="font-semibold">{formatCurrency(r.total)}</span> },
              { key: 'status', header: 'Status', render: r => <span className={getStatusColor(r.status)}>{capitalize(r.status)}</span> },
              { key: 'order_date', header: 'Date', render: r => formatDate(r.order_date) },
            ]}
          />
        </div>
      )}

      {tab === 'pipeline' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">Sales Pipeline</h3></div>
          <DataTable<Opportunity>
            loading={loadingOpps}
            data={opportunities ?? []}
            columns={[
              { key: 'title', header: 'Opportunity', render: r => <span className="font-medium">{r.title}</span> },
              { key: 'stage', header: 'Stage', render: r => <span className={getStatusColor(r.stage)}>{capitalize(r.stage)}</span> },
              { key: 'value', header: 'Value', render: r => <span className="font-semibold text-indigo-700">{formatCurrency(r.value)}</span> },
              { key: 'probability', header: 'Probability', render: r => (
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-1.5 rounded-full bg-gray-100 w-16">
                    <div className="h-1.5 rounded-full bg-indigo-500" style={{ width: `${r.probability}%` }} />
                  </div>
                  <span className="text-xs text-gray-600">{r.probability}%</span>
                </div>
              )},
              { key: 'owner', header: 'Owner', render: r => r.owner ?? '—' },
              { key: 'expected_close', header: 'Close Date', render: r => formatDate(r.expected_close) },
            ]}
          />
        </div>
      )}
    </div>
  )
}
