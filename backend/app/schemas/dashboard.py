from pydantic import BaseModel
from typing import List, Dict, Any


class KPICard(BaseModel):
    title: str
    value: str
    change: float  # percent change vs last period
    trend: str  # "up" | "down" | "neutral"
    icon: str


class ChartDataPoint(BaseModel):
    label: str
    value: float


class DashboardSummary(BaseModel):
    revenue: KPICard
    expenses: KPICard
    employees: KPICard
    open_orders: KPICard
    revenue_chart: List[ChartDataPoint]
    expense_chart: List[ChartDataPoint]
    recent_invoices: List[Dict[str, Any]]
    recent_orders: List[Dict[str, Any]]
    alerts: List[str]
