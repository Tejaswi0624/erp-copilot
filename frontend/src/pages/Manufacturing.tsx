import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { PageHeader } from '@/components/ui/PageHeader'
import { DataTable } from '@/components/ui/DataTable'
import type { WorkOrder, ManufacturingSummary } from '@/types'
import api from '@/lib/api'
import { formatDate, getStatusColor, capitalize } from '@/lib/utils'

type Tab = 'overview' | 'work-orders' | 'bom'

interface BOMItem {
  id: number
  product_name: string
  version: string
  component_name: string
  component_sku?: string
  quantity: number
  unit: string
}

export function Manufacturing() {
  const [tab, setTab] = useState<Tab>('overview')

  const { data: summary } = useQuery<ManufacturingSummary>({
    queryKey: ['manufacturing-summary'],
    queryFn: () => api.get('/manufacturing/summary').then(r => r.data),
  })
  const { data: workOrders, isLoading: loadingWO } = useQuery<WorkOrder[]>({
    queryKey: ['work-orders'],
    queryFn: () => api.get('/manufacturing/work-orders').then(r => r.data),
    enabled: tab === 'work-orders' || tab === 'overview',
  })
  const { data: bom, isLoading: loadingBOM } = useQuery<BOMItem[]>({
    queryKey: ['bom'],
    queryFn: () => api.get('/manufacturing/bom').then(r => r.data),
    enabled: tab === 'bom',
  })

  const tabs: { id: Tab; label: string }[] = [
    { id: 'overview', label: 'Overview' },
    { id: 'work-orders', label: 'Work Orders' },
    { id: 'bom', label: 'Bill of Materials' },
  ]

  const priorityColor: Record<string, string> = {
    low: 'badge-gray',
    normal: 'badge-blue',
    high: 'badge-yellow',
    urgent: 'badge-red',
  }

  return (
    <div className="space-y-6">
      <PageHeader title="Manufacturing" subtitle="Track work orders, production runs, and BOMs" />

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
              { label: 'Total Work Orders', value: summary.total_work_orders },
              { label: 'In Progress', value: summary.in_progress },
              { label: 'Planned', value: summary.planned },
              { label: 'Completed This Month', value: summary.completed_this_month },
              { label: 'Total Units Produced', value: summary.total_units_produced.toLocaleString() },
              { label: 'Rejection Rate', value: `${summary.rejection_rate.toFixed(1)}%` },
            ].map(item => (
              <div key={item.label} className="card p-5">
                <p className="text-sm text-gray-500">{item.label}</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{item.value}</p>
              </div>
            ))}
          </div>

          {workOrders && (
            <div className="card p-5">
              <h3 className="font-semibold text-gray-900 mb-4">Active Work Orders</h3>
              <DataTable<WorkOrder>
                data={workOrders.filter(w => ['planned', 'in_progress'].includes(w.status))}
                columns={[
                  { key: 'wo_number', header: 'WO #', render: r => <span className="font-mono text-xs text-indigo-600">{r.wo_number}</span> },
                  { key: 'product_name', header: 'Product', render: r => <span className="font-medium">{r.product_name}</span> },
                  { key: 'quantity', header: 'Qty' },
                  { key: 'priority', header: 'Priority', render: r => <span className={priorityColor[r.priority] ?? 'badge-gray'}>{capitalize(r.priority)}</span> },
                  { key: 'status', header: 'Status', render: r => <span className={getStatusColor(r.status)}>{capitalize(r.status)}</span> },
                  { key: 'start_date', header: 'Start', render: r => formatDate(r.start_date) },
                  { key: 'end_date', header: 'Due', render: r => formatDate(r.end_date) },
                ]}
              />
            </div>
          )}
        </div>
      )}

      {tab === 'work-orders' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">All Work Orders</h3></div>
          <DataTable<WorkOrder>
            loading={loadingWO}
            data={workOrders ?? []}
            columns={[
              { key: 'wo_number', header: 'WO #', render: r => <span className="font-mono text-xs text-indigo-600">{r.wo_number}</span> },
              { key: 'product_name', header: 'Product', render: r => <span className="font-medium">{r.product_name}</span> },
              { key: 'quantity', header: 'Qty' },
              { key: 'priority', header: 'Priority', render: r => <span className={priorityColor[r.priority] ?? 'badge-gray'}>{capitalize(r.priority)}</span> },
              { key: 'status', header: 'Status', render: r => <span className={getStatusColor(r.status)}>{capitalize(r.status)}</span> },
              { key: 'start_date', header: 'Start', render: r => formatDate(r.start_date) },
              { key: 'end_date', header: 'Due', render: r => formatDate(r.end_date) },
              { key: 'completed_at', header: 'Completed', render: r => formatDate(r.completed_at) },
            ]}
          />
        </div>
      )}

      {tab === 'bom' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">Bill of Materials</h3></div>
          <DataTable<BOMItem>
            loading={loadingBOM}
            data={bom ?? []}
            columns={[
              { key: 'product_name', header: 'Product', render: r => <span className="font-medium">{r.product_name}</span> },
              { key: 'version', header: 'Version', render: r => <span className="font-mono text-xs">{r.version}</span> },
              { key: 'component_name', header: 'Component' },
              { key: 'component_sku', header: 'SKU', render: r => r.component_sku ? <span className="font-mono text-xs">{r.component_sku}</span> : '—' },
              { key: 'quantity', header: 'Qty' },
              { key: 'unit', header: 'Unit' },
            ]}
          />
        </div>
      )}
    </div>
  )
}
