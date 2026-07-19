import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { DollarSign, FileText, TrendingUp, AlertCircle } from 'lucide-react'
import { PageHeader } from '@/components/ui/PageHeader'
import { DataTable } from '@/components/ui/DataTable'
import type { Invoice, Transaction, FinanceSummary, Account } from '@/types'
import api from '@/lib/api'
import { formatCurrency, formatDate, getStatusColor, capitalize } from '@/lib/utils'

type Tab = 'overview' | 'invoices' | 'transactions' | 'accounts'

export function Finance() {
  const [tab, setTab] = useState<Tab>('overview')

  const { data: summary } = useQuery<FinanceSummary>({
    queryKey: ['finance-summary'],
    queryFn: () => api.get('/finance/summary').then((r) => r.data),
  })
  const { data: invoices, isLoading: loadingInvoices } = useQuery<Invoice[]>({
    queryKey: ['invoices'],
    queryFn: () => api.get('/finance/invoices').then((r) => r.data),
    enabled: tab === 'invoices' || tab === 'overview',
  })
  const { data: transactions, isLoading: loadingTx } = useQuery<Transaction[]>({
    queryKey: ['transactions'],
    queryFn: () => api.get('/finance/transactions').then((r) => r.data),
    enabled: tab === 'transactions',
  })
  const { data: accounts, isLoading: loadingAccounts } = useQuery<Account[]>({
    queryKey: ['accounts'],
    queryFn: () => api.get('/finance/accounts').then((r) => r.data),
    enabled: tab === 'accounts',
  })

  const tabs: { id: Tab; label: string }[] = [
    { id: 'overview', label: 'Overview' },
    { id: 'invoices', label: 'Invoices' },
    { id: 'transactions', label: 'Transactions' },
    { id: 'accounts', label: 'Accounts' },
  ]

  return (
    <div className="space-y-6">
      <PageHeader title="Finance" subtitle="Manage accounts, invoices, and transactions" />

      {/* Tabs */}
      <div className="tab-group">
        {tabs.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`tab-btn ${tab === t.id ? 'tab-btn-active' : 'tab-btn-inactive'}`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {tab === 'overview' && summary && (
        <div className="space-y-6">
          <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { label: 'Total Revenue', value: formatCurrency(summary.total_revenue), icon: TrendingUp, color: 'text-green-600 bg-green-50' },
              { label: 'Total Expenses', value: formatCurrency(summary.total_expenses), icon: DollarSign, color: 'text-red-500 bg-red-50' },
              { label: 'Net Profit', value: formatCurrency(summary.net_profit), icon: TrendingUp, color: summary.net_profit >= 0 ? 'text-green-600 bg-green-50' : 'text-red-500 bg-red-50' },
              { label: 'Cash & Assets', value: formatCurrency(summary.cash_balance), icon: DollarSign, color: 'text-indigo-600 bg-indigo-50' },
              { label: 'Pending Invoices', value: summary.pending_invoices.toString(), icon: FileText, color: 'text-yellow-600 bg-yellow-50' },
              { label: 'Overdue Invoices', value: summary.overdue_invoices.toString(), icon: AlertCircle, color: 'text-red-600 bg-red-50' },
            ].map((item) => (
              <div key={item.label} className="card p-5">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500">{item.label}</p>
                    <p className="text-xl font-bold text-gray-900 mt-1">{item.value}</p>
                  </div>
                  <span className={`w-10 h-10 rounded-xl flex items-center justify-center ${item.color}`}>
                    <item.icon className="w-5 h-5" />
                  </span>
                </div>
              </div>
            ))}
          </div>

          {invoices && (
            <div className="card p-5">
              <h3 className="font-semibold text-gray-900 mb-4">Recent Invoices</h3>
              <DataTable
                data={invoices.slice(0, 10)}
                columns={[
                  { key: 'invoice_number', header: 'Invoice #', render: (r) => <span className="font-mono text-xs text-indigo-600">{r.invoice_number}</span> },
                  { key: 'customer_name', header: 'Customer' },
                  { key: 'total', header: 'Total', render: (r) => formatCurrency(r.total) },
                  { key: 'status', header: 'Status', render: (r) => <span className={getStatusColor(r.status)}>{capitalize(r.status)}</span> },
                  { key: 'due_date', header: 'Due Date', render: (r) => formatDate(r.due_date) },
                ]}
              />
            </div>
          )}
        </div>
      )}

      {tab === 'invoices' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100">
            <h3 className="font-semibold text-gray-900">All Invoices</h3>
          </div>
          <DataTable<Invoice>
            loading={loadingInvoices}
            data={invoices ?? []}
            columns={[
              { key: 'invoice_number', header: 'Invoice #', render: (r) => <span className="font-mono text-xs text-indigo-600">{r.invoice_number}</span> },
              { key: 'customer_name', header: 'Customer' },
              { key: 'amount', header: 'Amount', render: (r) => formatCurrency(r.amount) },
              { key: 'tax', header: 'Tax', render: (r) => formatCurrency(r.tax) },
              { key: 'total', header: 'Total', render: (r) => <span className="font-semibold">{formatCurrency(r.total)}</span> },
              { key: 'status', header: 'Status', render: (r) => <span className={getStatusColor(r.status)}>{capitalize(r.status)}</span> },
              { key: 'due_date', header: 'Due Date', render: (r) => formatDate(r.due_date) },
              { key: 'paid_at', header: 'Paid', render: (r) => formatDate(r.paid_at) },
            ]}
          />
        </div>
      )}

      {tab === 'transactions' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100">
            <h3 className="font-semibold text-gray-900">Transactions</h3>
          </div>
          <DataTable<Transaction>
            loading={loadingTx}
            data={transactions ?? []}
            columns={[
              { key: 'date', header: 'Date', render: (r) => formatDate(r.date) },
              { key: 'description', header: 'Description', render: (r) => r.description || '—' },
              { key: 'category', header: 'Category', render: (r) => r.category || '—' },
              { key: 'transaction_type', header: 'Type', render: (r) => (
                <span className={r.transaction_type === 'credit' ? 'badge-green' : 'badge-red'}>
                  {capitalize(r.transaction_type)}
                </span>
              ) },
              { key: 'amount', header: 'Amount', render: (r) => (
                <span className={r.transaction_type === 'credit' ? 'text-green-600 font-semibold' : 'text-red-600 font-semibold'}>
                  {r.transaction_type === 'credit' ? '+' : '-'}{formatCurrency(r.amount)}
                </span>
              ) },
              { key: 'reference', header: 'Reference', render: (r) => r.reference || '—' },
            ]}
          />
        </div>
      )}

      {tab === 'accounts' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100">
            <h3 className="font-semibold text-gray-900">Chart of Accounts</h3>
          </div>
          <DataTable<Account>
            loading={loadingAccounts}
            data={accounts ?? []}
            columns={[
              { key: 'code', header: 'Code', render: (r) => <span className="font-mono text-xs">{r.code}</span> },
              { key: 'name', header: 'Name', render: (r) => <span className="font-medium">{r.name}</span> },
              { key: 'account_type', header: 'Type', render: (r) => <span className="badge-blue">{capitalize(r.account_type)}</span> },
              { key: 'balance', header: 'Balance', render: (r) => <span className="font-semibold">{formatCurrency(r.balance)}</span> },
              { key: 'currency', header: 'Currency' },
            ]}
          />
        </div>
      )}
    </div>
  )
}
