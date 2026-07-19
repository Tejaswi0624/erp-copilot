import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { PageHeader } from '@/components/ui/PageHeader'
import { DataTable } from '@/components/ui/DataTable'
import type { Employee, Department, Payroll, LeaveRequest, HRSummary } from '@/types'
import api from '@/lib/api'
import { formatCurrency, formatDate, getStatusColor, capitalize } from '@/lib/utils'

type Tab = 'overview' | 'employees' | 'departments' | 'payroll' | 'leaves'

export function HR() {
  const [tab, setTab] = useState<Tab>('overview')

  const { data: summary } = useQuery<HRSummary>({
    queryKey: ['hr-summary'],
    queryFn: () => api.get('/hr/summary').then((r) => r.data),
  })
  const { data: employees, isLoading: loadingEmp } = useQuery<Employee[]>({
    queryKey: ['employees'],
    queryFn: () => api.get('/hr/employees').then((r) => r.data),
    enabled: tab === 'employees' || tab === 'overview',
  })
  const { data: departments, isLoading: loadingDepts } = useQuery<Department[]>({
    queryKey: ['departments'],
    queryFn: () => api.get('/hr/departments').then((r) => r.data),
    enabled: tab === 'departments' || tab === 'overview',
  })
  const { data: payrolls, isLoading: loadingPayroll } = useQuery<Payroll[]>({
    queryKey: ['payrolls'],
    queryFn: () => api.get('/hr/payroll').then((r) => r.data),
    enabled: tab === 'payroll',
  })
  const { data: leaves, isLoading: loadingLeaves } = useQuery<LeaveRequest[]>({
    queryKey: ['leaves'],
    queryFn: () => api.get('/hr/leaves').then((r) => r.data),
    enabled: tab === 'leaves',
  })

  const tabs: { id: Tab; label: string }[] = [
    { id: 'overview', label: 'Overview' },
    { id: 'employees', label: 'Employees' },
    { id: 'departments', label: 'Departments' },
    { id: 'payroll', label: 'Payroll' },
    { id: 'leaves', label: 'Leave Requests' },
  ]

  return (
    <div className="space-y-6">
      <PageHeader title="Human Resources" subtitle="Manage employees, departments, payroll and leave" />

      <div className="tab-group">
        {tabs.map((t) => (
          <button key={t.id} onClick={() => setTab(t.id)}
            className={`tab-btn ${tab === t.id ? 'tab-btn-active' : 'tab-btn-inactive'}`}>
            {t.label}
          </button>
        ))}
      </div>

      {tab === 'overview' && summary && (
        <div className="space-y-6">
          <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { label: 'Total Employees', value: summary.total_employees },
              { label: 'Active', value: summary.active_employees },
              { label: 'On Leave', value: summary.on_leave },
              { label: 'Departments', value: summary.departments },
              { label: 'Pending Leave Requests', value: summary.pending_leaves },
              { label: 'Monthly Payroll', value: formatCurrency(summary.monthly_payroll) },
            ].map((item) => (
              <div key={item.label} className="card p-5">
                <p className="text-sm text-gray-500">{item.label}</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{item.value}</p>
              </div>
            ))}
          </div>

          {employees && (
            <div className="card p-5">
              <h3 className="font-semibold text-gray-900 mb-4">Recent Employees</h3>
              <DataTable<Employee>
                data={employees.slice(0, 8)}
                columns={[
                  { key: 'employee_id', header: 'ID', render: (r) => <span className="font-mono text-xs">{r.employee_id}</span> },
                  { key: 'name', header: 'Name', render: (r) => <span className="font-medium">{r.first_name} {r.last_name}</span> },
                  { key: 'position', header: 'Position' },
                  { key: 'salary', header: 'Salary', render: (r) => formatCurrency(r.salary) },
                  { key: 'status', header: 'Status', render: (r) => <span className={getStatusColor(r.status)}>{capitalize(r.status)}</span> },
                ]}
              />
            </div>
          )}

          {departments && (
            <div className="card p-5">
              <h3 className="font-semibold text-gray-900 mb-4">Departments</h3>
              <div className="grid grid-cols-2 lg:grid-cols-3 gap-3">
                {departments.map((d) => (
                  <div key={d.id} className="p-4 rounded-lg bg-indigo-50 border border-indigo-100">
                    <p className="font-semibold text-indigo-900">{d.name}</p>
                    <p className="text-xs text-indigo-600 mt-0.5">{d.code}</p>
                    <p className="text-sm text-gray-600 mt-2">{d.headcount} employees</p>
                    <p className="text-sm text-gray-600">Budget: {formatCurrency(d.budget)}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {tab === 'employees' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">All Employees</h3></div>
          <DataTable<Employee>
            loading={loadingEmp}
            data={employees ?? []}
            columns={[
              { key: 'employee_id', header: 'ID', render: (r) => <span className="font-mono text-xs">{r.employee_id}</span> },
              { key: 'name', header: 'Name', render: (r) => <span className="font-medium">{r.first_name} {r.last_name}</span> },
              { key: 'email', header: 'Email' },
              { key: 'position', header: 'Position' },
              { key: 'salary', header: 'Salary', render: (r) => formatCurrency(r.salary) },
              { key: 'hire_date', header: 'Hired', render: (r) => formatDate(r.hire_date) },
              { key: 'status', header: 'Status', render: (r) => <span className={getStatusColor(r.status)}>{capitalize(r.status)}</span> },
            ]}
          />
        </div>
      )}

      {tab === 'departments' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">Departments</h3></div>
          <DataTable<Department>
            loading={loadingDepts}
            data={departments ?? []}
            columns={[
              { key: 'code', header: 'Code', render: (r) => <span className="font-mono text-xs">{r.code}</span> },
              { key: 'name', header: 'Department', render: (r) => <span className="font-medium">{r.name}</span> },
              { key: 'headcount', header: 'Headcount' },
              { key: 'budget', header: 'Budget', render: (r) => formatCurrency(r.budget) },
            ]}
          />
        </div>
      )}

      {tab === 'payroll' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">Payroll Records</h3></div>
          <DataTable<Payroll>
            loading={loadingPayroll}
            data={payrolls ?? []}
            columns={[
              { key: 'period', header: 'Period' },
              { key: 'employee_id', header: 'Employee ID' },
              { key: 'gross_salary', header: 'Gross', render: (r) => formatCurrency(r.gross_salary) },
              { key: 'deductions', header: 'Deductions', render: (r) => formatCurrency(r.deductions) },
              { key: 'bonus', header: 'Bonus', render: (r) => formatCurrency(r.bonus) },
              { key: 'net_salary', header: 'Net', render: (r) => <span className="font-semibold text-green-700">{formatCurrency(r.net_salary)}</span> },
              { key: 'status', header: 'Status', render: (r) => <span className={getStatusColor(r.status)}>{capitalize(r.status)}</span> },
            ]}
          />
        </div>
      )}

      {tab === 'leaves' && (
        <div className="card">
          <div className="p-5 border-b border-gray-100"><h3 className="font-semibold text-gray-900">Leave Requests</h3></div>
          <DataTable<LeaveRequest>
            loading={loadingLeaves}
            data={leaves ?? []}
            columns={[
              { key: 'employee_id', header: 'Employee ID' },
              { key: 'leave_type', header: 'Type', render: (r) => capitalize(r.leave_type) },
              { key: 'start_date', header: 'Start', render: (r) => formatDate(r.start_date) },
              { key: 'end_date', header: 'End', render: (r) => formatDate(r.end_date) },
              { key: 'days', header: 'Days' },
              { key: 'reason', header: 'Reason', render: (r) => r.reason || '—' },
              { key: 'status', header: 'Status', render: (r) => <span className={getStatusColor(r.status)}>{capitalize(r.status)}</span> },
            ]}
          />
        </div>
      )}
    </div>
  )
}
