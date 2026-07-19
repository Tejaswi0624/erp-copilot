import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { PageHeader } from '@/components/ui/PageHeader'
import { DataTable } from '@/components/ui/DataTable'
import type { Contact, Lead, Activity } from '@/types'
import api from '@/lib/api'
import { formatCurrency, formatDate, getStatusColor, capitalize } from '@/lib/utils'

type Tab = 'contacts' | 'leads' | 'activities'

export function CRM() {
  const [tab, setTab] = useState<Tab>('contacts')

  const { data: contacts, isLoading: loadingContacts } = useQuery<Contact[]>({
    queryKey: ['contacts'],
    queryFn: () => api.get('/crm/contacts').then(r => r.data),
    enabled: tab === 'contacts',
  })
  const { data: leads, isLoading: loadingLeads } = useQuery<Lead[]>({
    queryKey: ['leads'],
    queryFn: () => api.get('/crm/leads').then(r => r.data),
    enabled: tab === 'leads',
  })
  const { data: activities, isLoading: loadingActivities } = useQuery<Activity[]>({
    queryKey: ['activities'],
    queryFn: () => api.get('/crm/activities').then(r => r.data),
    enabled: tab === 'activities',
  })

  const tabs: { id: Tab; label: string }[] = [
    { id: 'contacts', label: 'Contacts' },
    { id: 'leads', label: 'Leads' },
    { id: 'activities', label: 'Activities' },
  ]

  return (
    <div className="space-y-6">
      <PageHeader title="CRM" subtitle="Manage contacts, leads, and customer activities" />

      <div className="tab-group">
        {tabs.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)}
            className={`tab-btn ${tab === t.id ? 'tab-btn-active' : 'tab-btn-inactive'}`}>
            {t.label}
          </button>
        ))}
      </div>

      {tab === 'contacts' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">Contacts</h3></div>
          <DataTable<Contact>
            loading={loadingContacts}
            data={contacts ?? []}
            columns={[
              { key: 'name', header: 'Name', render: r => <span className="font-medium">{r.first_name} {r.last_name}</span> },
              { key: 'company', header: 'Company', render: r => r.company ?? '—' },
              { key: 'position', header: 'Position', render: r => r.position ?? '—' },
              { key: 'email', header: 'Email', render: r => r.email ?? '—' },
              { key: 'phone', header: 'Phone', render: r => r.phone ?? '—' },
              { key: 'source', header: 'Source', render: r => r.source ? capitalize(r.source) : '—' },
              { key: 'is_active', header: 'Status', render: r => <span className={r.is_active ? 'badge-green' : 'badge-gray'}>{r.is_active ? 'Active' : 'Inactive'}</span> },
            ]}
          />
        </div>
      )}

      {tab === 'leads' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">Leads</h3></div>
          <DataTable<Lead>
            loading={loadingLeads}
            data={leads ?? []}
            columns={[
              { key: 'name', header: 'Name', render: r => <span className="font-medium">{r.first_name} {r.last_name}</span> },
              { key: 'company', header: 'Company', render: r => r.company ?? '—' },
              { key: 'email', header: 'Email', render: r => r.email ?? '—' },
              { key: 'source', header: 'Source', render: r => r.source ? capitalize(r.source) : '—' },
              { key: 'status', header: 'Status', render: r => <span className={getStatusColor(r.status)}>{capitalize(r.status)}</span> },
              { key: 'estimated_value', header: 'Est. Value', render: r => formatCurrency(r.estimated_value) },
              { key: 'assigned_to', header: 'Assigned To', render: r => r.assigned_to ?? '—' },
              { key: 'created_at', header: 'Created', render: r => formatDate(r.created_at) },
            ]}
          />
        </div>
      )}

      {tab === 'activities' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">Activities</h3></div>
          <DataTable<Activity>
            loading={loadingActivities}
            data={activities ?? []}
            columns={[
              { key: 'activity_type', header: 'Type', render: r => (
                <span className={
                  r.activity_type === 'call' ? 'badge-blue' :
                  r.activity_type === 'meeting' ? 'badge-purple' :
                  r.activity_type === 'email' ? 'badge-green' : 'badge-gray'
                }>{capitalize(r.activity_type)}</span>
              )},
              { key: 'subject', header: 'Subject', render: r => <span className="font-medium">{r.subject}</span> },
              { key: 'description', header: 'Description', render: r => r.description ?? '—' },
              { key: 'due_date', header: 'Due Date', render: r => formatDate(r.due_date) },
              { key: 'completed', header: 'Status', render: r => (
                <span className={r.completed ? 'badge-green' : 'badge-yellow'}>
                  {r.completed ? 'Completed' : 'Pending'}
                </span>
              )},
              { key: 'created_at', header: 'Created', render: r => formatDate(r.created_at) },
            ]}
          />
        </div>
      )}
    </div>
  )
}
