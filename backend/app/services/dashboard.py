from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
from typing import List

from app.models.finance import Invoice, Transaction, Account
from app.models.hr import Employee
from app.models.sales import SalesOrder, Customer
from app.models.inventory import Product
from app.schemas.dashboard import DashboardSummary, KPICard, ChartDataPoint

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def get_dashboard_summary(db: Session) -> DashboardSummary:
    now = datetime.utcnow()
    year = now.year
    month = now.month

    # ── KPI: Revenue ──────────────────────────────────────────────────────────
    rev_this = db.query(func.coalesce(func.sum(SalesOrder.total), 0)).filter(
        SalesOrder.status.in_(["delivered", "shipped", "confirmed"]),
        extract("year", SalesOrder.order_date) == year,
        extract("month", SalesOrder.order_date) == month,
    ).scalar() or 0.0

    rev_last = db.query(func.coalesce(func.sum(SalesOrder.total), 0)).filter(
        SalesOrder.status.in_(["delivered", "shipped", "confirmed"]),
        extract("year", SalesOrder.order_date) == (year if month > 1 else year - 1),
        extract("month", SalesOrder.order_date) == (month - 1 if month > 1 else 12),
    ).scalar() or 0.0

    rev_change = ((rev_this - rev_last) / rev_last * 100) if rev_last else 0.0

    # ── KPI: Expenses ─────────────────────────────────────────────────────────
    exp_this = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.transaction_type == "debit",
        extract("year", Transaction.date) == year,
        extract("month", Transaction.date) == month,
    ).scalar() or 0.0

    exp_last = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.transaction_type == "debit",
        extract("year", Transaction.date) == (year if month > 1 else year - 1),
        extract("month", Transaction.date) == (month - 1 if month > 1 else 12),
    ).scalar() or 0.0

    exp_change = ((exp_this - exp_last) / exp_last * 100) if exp_last else 0.0

    # ── KPI: Employees ────────────────────────────────────────────────────────
    total_emp = db.query(func.count(Employee.id)).filter(Employee.status == "active").scalar() or 0

    # ── KPI: Open Orders ─────────────────────────────────────────────────────
    open_orders = db.query(func.count(SalesOrder.id)).filter(
        SalesOrder.status.in_(["draft", "confirmed", "processing"])
    ).scalar() or 0

    # ── Revenue chart (last 6 months) ─────────────────────────────────────────
    revenue_chart: List[ChartDataPoint] = []
    for i in range(5, -1, -1):
        m = month - i
        y = year
        if m <= 0:
            m += 12
            y -= 1
        val = db.query(func.coalesce(func.sum(SalesOrder.total), 0)).filter(
            SalesOrder.status.in_(["delivered", "shipped", "confirmed"]),
            extract("year", SalesOrder.order_date) == y,
            extract("month", SalesOrder.order_date) == m,
        ).scalar() or 0.0
        revenue_chart.append(ChartDataPoint(label=MONTHS[m - 1], value=float(val)))

    # ── Expense chart (last 6 months) ─────────────────────────────────────────
    expense_chart: List[ChartDataPoint] = []
    for i in range(5, -1, -1):
        m = month - i
        y = year
        if m <= 0:
            m += 12
            y -= 1
        val = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
            Transaction.transaction_type == "debit",
            extract("year", Transaction.date) == y,
            extract("month", Transaction.date) == m,
        ).scalar() or 0.0
        expense_chart.append(ChartDataPoint(label=MONTHS[m - 1], value=float(val)))

    # ── Recent invoices ────────────────────────────────────────────────────────
    recent_invoices = db.query(Invoice).order_by(Invoice.created_at.desc()).limit(5).all()
    invoices_data = [
        {
            "id": inv.id,
            "invoice_number": inv.invoice_number,
            "customer_name": inv.customer_name,
            "total": inv.total,
            "status": inv.status,
            "due_date": inv.due_date.isoformat() if inv.due_date else None,
        }
        for inv in recent_invoices
    ]

    # ── Recent orders ──────────────────────────────────────────────────────────
    recent_orders = db.query(SalesOrder).order_by(SalesOrder.created_at.desc()).limit(5).all()
    orders_data = [
        {
            "id": o.id,
            "order_number": o.order_number,
            "customer_id": o.customer_id,
            "total": o.total,
            "status": o.status,
            "order_date": o.order_date.isoformat() if o.order_date else None,
        }
        for o in recent_orders
    ]

    # ── Alerts ────────────────────────────────────────────────────────────────
    alerts = []
    low_stock = db.query(func.count(Product.id)).filter(
        Product.is_active == True,
        Product.quantity_on_hand <= Product.reorder_level,
    ).scalar() or 0
    if low_stock > 0:
        alerts.append(f"{low_stock} product(s) are at or below reorder level")

    overdue = db.query(func.count(Invoice.id)).filter(Invoice.status == "overdue").scalar() or 0
    if overdue > 0:
        alerts.append(f"{overdue} invoice(s) are overdue")

    return DashboardSummary(
        revenue=KPICard(
            title="Revenue (This Month)",
            value=f"${rev_this:,.2f}",
            change=round(rev_change, 1),
            trend="up" if rev_change >= 0 else "down",
            icon="trending-up",
        ),
        expenses=KPICard(
            title="Expenses (This Month)",
            value=f"${exp_this:,.2f}",
            change=round(exp_change, 1),
            trend="up" if exp_change >= 0 else "down",
            icon="trending-down",
        ),
        employees=KPICard(
            title="Active Employees",
            value=str(total_emp),
            change=0.0,
            trend="neutral",
            icon="users",
        ),
        open_orders=KPICard(
            title="Open Orders",
            value=str(open_orders),
            change=0.0,
            trend="neutral",
            icon="shopping-cart",
        ),
        revenue_chart=revenue_chart,
        expense_chart=expense_chart,
        recent_invoices=invoices_data,
        recent_orders=orders_data,
        alerts=alerts,
    )
