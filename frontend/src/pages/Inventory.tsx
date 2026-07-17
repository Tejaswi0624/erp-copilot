import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { AlertTriangle } from 'lucide-react'
import { PageHeader } from '@/components/ui/PageHeader'
import { DataTable } from '@/components/ui/DataTable'
import type { Product, Warehouse, PurchaseOrder, InventorySummary } from '@/types'
import api from '@/lib/api'
import { formatCurrency, formatDate, getStatusColor, capitalize } from '@/lib/utils'

type Tab = 'overview' | 'products' | 'warehouses' | 'purchase-orders'

export function Inventory() {
  const [tab, setTab] = useState<Tab>('overview')

  const { data: summary } = useQuery<InventorySummary>({
    queryKey: ['inventory-summary'],
    queryFn: () => api.get('/inventory/summary').then(r => r.data),
  })
  const { data: products, isLoading: loadingProducts } = useQuery<Product[]>({
    queryKey: ['products'],
    queryFn: () => api.get('/inventory/products').then(r => r.data),
    enabled: tab === 'products' || tab === 'overview',
  })
  const { data: warehouses, isLoading: loadingWH } = useQuery<Warehouse[]>({
    queryKey: ['warehouses'],
    queryFn: () => api.get('/inventory/warehouses').then(r => r.data),
    enabled: tab === 'warehouses' || tab === 'overview',
  })
  const { data: orders, isLoading: loadingPO } = useQuery<PurchaseOrder[]>({
    queryKey: ['purchase-orders'],
    queryFn: () => api.get('/inventory/purchase-orders').then(r => r.data),
    enabled: tab === 'purchase-orders',
  })

  const tabs: { id: Tab; label: string }[] = [
    { id: 'overview', label: 'Overview' },
    { id: 'products', label: 'Products' },
    { id: 'warehouses', label: 'Warehouses' },
    { id: 'purchase-orders', label: 'Purchase Orders' },
  ]

  const lowStockProducts = products?.filter(p => p.quantity_on_hand <= p.reorder_level) ?? []

  return (
    <div className="space-y-6">
      <PageHeader title="Inventory" subtitle="Track products, stock levels, and purchase orders" />

      <div className="flex gap-1 p-1 bg-gray-100 rounded-xl w-fit flex-wrap">
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
              { label: 'Total Products', value: summary.total_products },
              { label: 'Low Stock Items', value: summary.low_stock_items },
              { label: 'Out of Stock', value: summary.out_of_stock },
              { label: 'Inventory Value', value: formatCurrency(summary.total_value) },
              { label: 'Pending POs', value: summary.pending_orders },
              { label: 'Warehouses', value: summary.warehouses },
            ].map(item => (
              <div key={item.label} className="card p-5">
                <p className="text-sm text-gray-500">{item.label}</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{item.value}</p>
              </div>
            ))}
          </div>

          {lowStockProducts.length > 0 && (
            <div className="card p-5">
              <div className="flex items-center gap-2 mb-4">
                <AlertTriangle className="w-4 h-4 text-amber-500" />
                <h3 className="font-semibold text-gray-900">Low Stock Alerts</h3>
              </div>
              <DataTable<Product>
                data={lowStockProducts}
                columns={[
                  { key: 'sku', header: 'SKU', render: r => <span className="font-mono text-xs">{r.sku}</span> },
                  { key: 'name', header: 'Product', render: r => <span className="font-medium">{r.name}</span> },
                  { key: 'category', header: 'Category', render: r => r.category ?? '—' },
                  { key: 'quantity_on_hand', header: 'In Stock', render: r => (
                    <span className={r.quantity_on_hand === 0 ? 'text-red-600 font-semibold' : 'text-amber-600 font-semibold'}>
                      {r.quantity_on_hand}
                    </span>
                  )},
                  { key: 'reorder_level', header: 'Reorder At' },
                  { key: 'unit_price', header: 'Unit Price', render: r => formatCurrency(r.unit_price) },
                ]}
              />
            </div>
          )}

          {warehouses && (
            <div className="card p-5">
              <h3 className="font-semibold text-gray-900 mb-4">Warehouses</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {warehouses.map(w => (
                  <div key={w.id} className="p-4 rounded-lg bg-blue-50 border border-blue-100">
                    <p className="font-semibold text-blue-900">{w.name}</p>
                    <p className="text-xs text-blue-600 mt-0.5">{w.code}</p>
                    <p className="text-sm text-gray-600 mt-2">{w.location}</p>
                    <p className="text-sm text-gray-600">Capacity: {w.capacity.toLocaleString()} units</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {tab === 'products' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">All Products</h3></div>
          <DataTable<Product>
            loading={loadingProducts}
            data={products ?? []}
            columns={[
              { key: 'sku', header: 'SKU', render: r => <span className="font-mono text-xs">{r.sku}</span> },
              { key: 'name', header: 'Product', render: r => <span className="font-medium">{r.name}</span> },
              { key: 'category', header: 'Category', render: r => r.category ?? '—' },
              { key: 'quantity_on_hand', header: 'In Stock', render: r => (
                <span className={r.quantity_on_hand === 0 ? 'text-red-600 font-semibold' : r.quantity_on_hand <= r.reorder_level ? 'text-amber-600 font-semibold' : 'text-green-700 font-semibold'}>
                  {r.quantity_on_hand}
                </span>
              )},
              { key: 'reorder_level', header: 'Reorder At' },
              { key: 'cost_price', header: 'Cost', render: r => formatCurrency(r.cost_price) },
              { key: 'unit_price', header: 'Sell Price', render: r => formatCurrency(r.unit_price) },
              { key: 'is_active', header: 'Status', render: r => <span className={r.is_active ? 'badge-green' : 'badge-gray'}>{r.is_active ? 'Active' : 'Inactive'}</span> },
            ]}
          />
        </div>
      )}

      {tab === 'warehouses' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">Warehouses</h3></div>
          <DataTable<Warehouse>
            loading={loadingWH}
            data={warehouses ?? []}
            columns={[
              { key: 'code', header: 'Code', render: r => <span className="font-mono text-xs">{r.code}</span> },
              { key: 'name', header: 'Name', render: r => <span className="font-medium">{r.name}</span> },
              { key: 'location', header: 'Location', render: r => r.location ?? '—' },
              { key: 'capacity', header: 'Capacity', render: r => r.capacity.toLocaleString() },
              { key: 'is_active', header: 'Status', render: r => <span className={r.is_active ? 'badge-green' : 'badge-gray'}>{r.is_active ? 'Active' : 'Inactive'}</span> },
            ]}
          />
        </div>
      )}

      {tab === 'purchase-orders' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">Purchase Orders</h3></div>
          <DataTable<PurchaseOrder>
            loading={loadingPO}
            data={orders ?? []}
            columns={[
              { key: 'po_number', header: 'PO #', render: r => <span className="font-mono text-xs text-indigo-600">{r.po_number}</span> },
              { key: 'supplier_name', header: 'Supplier', render: r => <span className="font-medium">{r.supplier_name}</span> },
              { key: 'total_amount', header: 'Amount', render: r => formatCurrency(r.total_amount) },
              { key: 'status', header: 'Status', render: r => <span className={getStatusColor(r.status)}>{capitalize(r.status)}</span> },
              { key: 'order_date', header: 'Ordered', render: r => formatDate(r.order_date) },
              { key: 'expected_date', header: 'Expected', render: r => formatDate(r.expected_date) },
              { key: 'received_date', header: 'Received', render: r => formatDate(r.received_date) },
            ]}
          />
        </div>
      )}
    </div>
  )
}
