// ── Auth ──────────────────────────────────────────────────────────────────────
export interface User {
  id: number
  username: string
  email: string
  full_name: string
  role: string
  is_active: boolean
  avatar?: string
  created_at: string
}

export interface Token {
  access_token: string
  token_type: string
  user: User
}

// ── Finance ───────────────────────────────────────────────────────────────────
export interface Account {
  id: number
  code: string
  name: string
  account_type: string
  balance: number
  currency: string
  description?: string
  is_active: boolean
  created_at: string
}

export interface Transaction {
  id: number
  account_id: number
  transaction_type: string
  amount: number
  description?: string
  reference?: string
  category?: string
  date: string
  created_at: string
}

export interface Invoice {
  id: number
  invoice_number: string
  customer_name: string
  customer_email?: string
  amount: number
  tax: number
  total: number
  status: string
  due_date?: string
  paid_at?: string
  notes?: string
  created_at: string
  updated_at?: string
}

export interface Budget {
  id: number
  name: string
  department?: string
  category: string
  allocated: number
  spent: number
  period: string
  year: number
  created_at: string
}

export interface FinanceSummary {
  total_revenue: number
  total_expenses: number
  net_profit: number
  pending_invoices: number
  overdue_invoices: number
  cash_balance: number
}

// ── HR ────────────────────────────────────────────────────────────────────────
export interface Department {
  id: number
  name: string
  code: string
  manager_id?: number
  budget: number
  headcount: number
  created_at: string
}

export interface Employee {
  id: number
  employee_id: string
  first_name: string
  last_name: string
  email: string
  phone?: string
  position: string
  department_id?: number
  manager_id?: number
  salary: number
  hire_date?: string
  status: string
  avatar?: string
  created_at: string
  updated_at?: string
}

export interface Payroll {
  id: number
  employee_id: number
  period: string
  gross_salary: number
  deductions: number
  net_salary: number
  bonus: number
  paid_at?: string
  status: string
  created_at: string
}

export interface LeaveRequest {
  id: number
  employee_id: number
  leave_type: string
  start_date: string
  end_date: string
  days: number
  reason?: string
  status: string
  approved_by?: number
  created_at: string
}

export interface HRSummary {
  total_employees: number
  active_employees: number
  on_leave: number
  departments: number
  pending_leaves: number
  monthly_payroll: number
}

// ── Inventory ─────────────────────────────────────────────────────────────────
export interface Product {
  id: number
  sku: string
  name: string
  description?: string
  category?: string
  unit_price: number
  cost_price: number
  quantity_on_hand: number
  reorder_level: number
  reorder_quantity: number
  warehouse_id?: number
  is_active: boolean
  image_url?: string
  created_at: string
  updated_at?: string
}

export interface Warehouse {
  id: number
  name: string
  code: string
  location?: string
  capacity: number
  is_active: boolean
  created_at: string
}

export interface StockMovement {
  id: number
  product_id: number
  movement_type: string
  quantity: number
  reference?: string
  notes?: string
  created_at: string
}

export interface PurchaseOrder {
  id: number
  po_number: string
  supplier_name: string
  supplier_email?: string
  total_amount: number
  status: string
  order_date: string
  expected_date?: string
  received_date?: string
  notes?: string
  created_at: string
}

export interface InventorySummary {
  total_products: number
  low_stock_items: number
  out_of_stock: number
  total_value: number
  pending_orders: number
  warehouses: number
}

// ── Sales ─────────────────────────────────────────────────────────────────────
export interface Customer {
  id: number
  name: string
  email: string
  phone?: string
  company?: string
  address?: string
  city?: string
  country?: string
  credit_limit: number
  total_orders: number
  total_revenue: number
  is_active: boolean
  created_at: string
}

export interface SalesOrderItem {
  id: number
  order_id: number
  product_name: string
  sku?: string
  quantity: number
  unit_price: number
  total: number
}

export interface SalesOrder {
  id: number
  order_number: string
  customer_id: number
  status: string
  subtotal: number
  discount: number
  tax: number
  total: number
  notes?: string
  order_date: string
  shipped_date?: string
  created_at: string
  items: SalesOrderItem[]
}

export interface Opportunity {
  id: number
  title: string
  customer_id?: number
  stage: string
  value: number
  probability: number
  expected_close?: string
  owner?: string
  notes?: string
  created_at: string
}

export interface SalesSummary {
  total_customers: number
  total_orders: number
  total_revenue: number
  pending_orders: number
  pipeline_value: number
  open_opportunities: number
}

// ── CRM ───────────────────────────────────────────────────────────────────────
export interface Contact {
  id: number
  first_name: string
  last_name: string
  email?: string
  phone?: string
  company?: string
  position?: string
  source?: string
  tags?: string
  notes?: string
  is_active: boolean
  created_at: string
}

export interface Lead {
  id: number
  first_name: string
  last_name: string
  email?: string
  phone?: string
  company?: string
  source?: string
  status: string
  estimated_value: number
  assigned_to?: string
  notes?: string
  created_at: string
}

export interface Activity {
  id: number
  contact_id?: number
  activity_type: string
  subject: string
  description?: string
  due_date?: string
  completed: boolean
  completed_at?: string
  created_at: string
}

// ── Manufacturing ─────────────────────────────────────────────────────────────
export interface WorkOrder {
  id: number
  wo_number: string
  product_name: string
  quantity: number
  status: string
  priority: string
  start_date?: string
  end_date?: string
  completed_at?: string
  notes?: string
  created_at: string
}

export interface ManufacturingSummary {
  total_work_orders: number
  in_progress: number
  completed_this_month: number
  planned: number
  total_units_produced: number
  rejection_rate: number
}

// ── Dashboard ─────────────────────────────────────────────────────────────────
export interface KPICard {
  title: string
  value: string
  change: number
  trend: 'up' | 'down' | 'neutral'
  icon: string
}

export interface ChartDataPoint {
  label: string
  value: number
}

export interface DashboardSummary {
  revenue: KPICard
  expenses: KPICard
  employees: KPICard
  open_orders: KPICard
  revenue_chart: ChartDataPoint[]
  expense_chart: ChartDataPoint[]
  recent_invoices: Record<string, unknown>[]
  recent_orders: Record<string, unknown>[]
  alerts: string[]
}

// ── Chat ──────────────────────────────────────────────────────────────────────
export interface Message {
  id: number
  conversation_id: number
  role: string
  content: string
  tokens_used?: number
  created_at: string
}

export interface ConversationSummary {
  id: number
  title?: string
  module_context?: string
  created_at: string
  message_count: number
}

export interface Conversation {
  id: number
  user_id: number
  title?: string
  module_context?: string
  is_active: boolean
  created_at: string
  updated_at?: string
  messages: Message[]
}

export interface ChatResponse {
  conversation_id: number
  message: Message
  reply: Message
}
