import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { cn } from '@/lib/utils'
import type { KPICard } from '@/types'

interface Props {
  kpi: KPICard
  colorClass?: string
}

export function StatCard({ kpi, colorClass = 'text-indigo-600 bg-indigo-50' }: Props) {
  return (
    <div className="card p-5">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-500 font-medium">{kpi.title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{kpi.value}</p>
        </div>
        <span className={cn('w-10 h-10 rounded-xl flex items-center justify-center', colorClass)}>
          {kpi.trend === 'up' ? (
            <TrendingUp className="w-5 h-5" />
          ) : kpi.trend === 'down' ? (
            <TrendingDown className="w-5 h-5" />
          ) : (
            <Minus className="w-5 h-5" />
          )}
        </span>
      </div>
      <div className="mt-3 flex items-center gap-1">
        {kpi.change !== 0 ? (
          <>
            <span className={cn('text-xs font-semibold', kpi.trend === 'up' ? 'text-green-600' : 'text-red-600')}>
              {kpi.change > 0 ? '+' : ''}{kpi.change.toFixed(1)}%
            </span>
            <span className="text-xs text-gray-500">vs last month</span>
          </>
        ) : (
          <span className="text-xs text-gray-500">No change</span>
        )}
      </div>
    </div>
  )
}
