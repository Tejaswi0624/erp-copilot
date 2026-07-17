from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ── Account ──────────────────────────────────────────────────────────────────

class AccountBase(BaseModel):
    code: str
    name: str
    account_type: str
    balance: float = 0.0
    currency: str = "USD"
    description: Optional[str] = None
    is_active: bool = True


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    account_type: Optional[str] = None
    balance: Optional[float] = None
    currency: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class AccountOut(AccountBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Transaction ───────────────────────────────────────────────────────────────

class TransactionBase(BaseModel):
    account_id: int
    transaction_type: str
    amount: float
    description: Optional[str] = None
    reference: Optional[str] = None
    category: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionOut(TransactionBase):
    id: int
    date: datetime
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Invoice ───────────────────────────────────────────────────────────────────

class InvoiceBase(BaseModel):
    invoice_number: str
    customer_name: str
    customer_email: Optional[str] = None
    amount: float
    tax: float = 0.0
    total: float
    status: str = "draft"
    due_date: Optional[datetime] = None
    notes: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(BaseModel):
    status: Optional[str] = None
    paid_at: Optional[datetime] = None
    notes: Optional[str] = None
    due_date: Optional[datetime] = None


class InvoiceOut(InvoiceBase):
    id: int
    paid_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Budget ────────────────────────────────────────────────────────────────────

class BudgetBase(BaseModel):
    name: str
    department: Optional[str] = None
    category: str
    allocated: float
    spent: float = 0.0
    period: str
    year: int


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    spent: Optional[float] = None
    allocated: Optional[float] = None


class BudgetOut(BudgetBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Dashboard summary ─────────────────────────────────────────────────────────

class FinanceSummary(BaseModel):
    total_revenue: float
    total_expenses: float
    net_profit: float
    pending_invoices: int
    overdue_invoices: int
    cash_balance: float
