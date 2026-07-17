import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatCurrency(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(amount)
}

export function formatDate(dateStr?: string | null): string {
  if (!dateStr) return '—'
  return new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' }).format(new Date(dateStr))
}

export function formatDateTime(dateStr?: string | null): string {
  if (!dateStr) return '—'
  return new Intl.DateTimeFormat('en-US', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(dateStr))
}

export function getStatusColor(status: string): string {
  const map: Record<string, string> = {
    active: 'badge-green',
    paid: 'badge-green',
    delivered: 'badge-green',
    completed: 'badge-green',
    received: 'badge-green',
    approved: 'badge-green',
    closed_won: 'badge-green',
    draft: 'badge-gray',
    pending: 'badge-yellow',
    sent: 'badge-blue',
    confirmed: 'badge-blue',
    processing: 'badge-blue',
    planned: 'badge-blue',
    contacted: 'badge-blue',
    qualified: 'badge-blue',
    prospecting: 'badge-blue',
    proposal: 'badge-purple',
    negotiation: 'badge-purple',
    in_progress: 'badge-purple',
    on_leave: 'badge-yellow',
    overdue: 'badge-red',
    cancelled: 'badge-red',
    terminated: 'badge-red',
    rejected: 'badge-red',
    closed_lost: 'badge-red',
    unqualified: 'badge-red',
    partial: 'badge-yellow',
    new: 'badge-blue',
    probation: 'badge-yellow',
  }
  return map[status] ?? 'badge-gray'
}

export function capitalize(str: string): string {
  return str.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}

export function initials(name: string): string {
  return name.split(' ').map((n) => n[0]).join('').toUpperCase().slice(0, 2)
}
