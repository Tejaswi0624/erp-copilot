"""
Builds a rich context snapshot from the DB to inject into the AI system prompt.
This lets the copilot answer questions like "how many employees do we have?"
without needing to call separate tool APIs.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from app.models.finance import Invoice, Account, Transaction
from app.models.hr import Employee, Department
from app.models.inventory import Product
from app.models.sales import SalesOrder, Customer, Opportunity
from app.models.crm import Lead
from app.models.manufacturing import WorkOrder


def build_erp_context(db: Session, module: Optional[str] = None) -> str:
    """Return a concise ERP state snapshot as plain text for the LLM system prompt."""
    lines = ["=== ERP SYSTEM CONTEXT SNAPSHOT ===\n"]

    if module in (None, "finance"):
        revenue = db.query(func.coalesce(func.sum(SalesOrder.total), 0)).filter(
            SalesOrder.status.in_(["delivered", "shipped", "confirmed"])
        ).scalar() or 0
        pending_inv = db.query(func.count(Invoice.id)).filter(
            Invoice.status.in_(["draft", "sent"])
        ).scalar() or 0
        overdue_inv = db.query(func.count(Invoice.id)).filter(Invoice.status == "overdue").scalar() or 0
        cash = db.query(func.coalesce(func.sum(Account.balance), 0)).filter(
            Account.account_type == "asset"
        ).scalar() or 0
        lines.append(f"FINANCE: Total Revenue=${revenue:,.2f}, Cash/Assets=${cash:,.2f}, "
                     f"Pending Invoices={pending_inv}, Overdue Invoices={overdue_inv}")

    if module in (None, "hr"):
        total_emp = db.query(func.count(Employee.id)).filter(Employee.status == "active").scalar() or 0
        depts = db.query(func.count(Department.id)).scalar() or 0
        payroll = db.query(func.coalesce(func.sum(Employee.salary), 0)).filter(
            Employee.status == "active"
        ).scalar() or 0
        lines.append(f"HR: Active Employees={total_emp}, Departments={depts}, "
                     f"Monthly Payroll=${payroll:,.2f}")

    if module in (None, "inventory"):
        total_prod = db.query(func.count(Product.id)).filter(Product.is_active == True).scalar() or 0
        low_stock = db.query(func.count(Product.id)).filter(
            Product.is_active == True,
            Product.quantity_on_hand <= Product.reorder_level,
        ).scalar() or 0
        inv_value = db.query(
            func.coalesce(func.sum(Product.quantity_on_hand * Product.cost_price), 0)
        ).filter(Product.is_active == True).scalar() or 0
        lines.append(f"INVENTORY: Products={total_prod}, Low Stock={low_stock}, "
                     f"Inventory Value=${inv_value:,.2f}")

    if module in (None, "sales"):
        customers = db.query(func.count(Customer.id)).filter(Customer.is_active == True).scalar() or 0
        open_orders = db.query(func.count(SalesOrder.id)).filter(
            SalesOrder.status.in_(["draft", "confirmed", "processing"])
        ).scalar() or 0
        pipeline = db.query(func.coalesce(func.sum(Opportunity.value), 0)).filter(
            Opportunity.stage.notin_(["closed_won", "closed_lost"])
        ).scalar() or 0
        lines.append(f"SALES: Customers={customers}, Open Orders={open_orders}, "
                     f"Pipeline Value=${pipeline:,.2f}")

    if module in (None, "crm"):
        leads = db.query(func.count(Lead.id)).filter(Lead.status.in_(["new", "contacted"])).scalar() or 0
        lines.append(f"CRM: Active Leads={leads}")

    if module in (None, "manufacturing"):
        wos_active = db.query(func.count(WorkOrder.id)).filter(
            WorkOrder.status.in_(["planned", "in_progress"])
        ).scalar() or 0
        lines.append(f"MANUFACTURING: Active Work Orders={wos_active}")

    lines.append("\n=== END OF CONTEXT ===")
    return "\n".join(lines)


SYSTEM_PROMPT_BASE = """You are an intelligent ERP AI Copilot assistant. You help users understand and 
manage their business operations across Finance, HR, Inventory, Sales, CRM, and Manufacturing modules.

You can:
- Answer questions about current business data using the context provided
- Provide analysis, trends, and actionable recommendations
- Explain ERP concepts and best practices
- Help draft reports, summaries, and business insights
- Guide users through workflows in the ERP system

Always be concise, professional, and data-driven. When referencing numbers, use the context snapshot 
provided. If you don't have specific data, say so clearly and suggest where to find it.

{context}
"""
