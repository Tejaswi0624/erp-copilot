from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.finance import Account, Transaction, Invoice, Budget
from app.schemas.finance import (
    AccountCreate, AccountUpdate,
    TransactionCreate,
    InvoiceCreate, InvoiceUpdate,
    BudgetCreate, BudgetUpdate,
    FinanceSummary,
)


# ── Account ───────────────────────────────────────────────────────────────────

def get_accounts(db: Session, skip: int = 0, limit: int = 100) -> List[Account]:
    return db.query(Account).filter(Account.is_active == True).offset(skip).limit(limit).all()


def get_account(db: Session, account_id: int) -> Optional[Account]:
    return db.query(Account).filter(Account.id == account_id).first()


def create_account(db: Session, data: AccountCreate) -> Account:
    account = Account(**data.model_dump())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def update_account(db: Session, account_id: int, data: AccountUpdate) -> Optional[Account]:
    account = get_account(db, account_id)
    if not account:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(account, field, value)
    db.commit()
    db.refresh(account)
    return account


def delete_account(db: Session, account_id: int) -> bool:
    account = get_account(db, account_id)
    if not account:
        return False
    account.is_active = False
    db.commit()
    return True


# ── Transaction ───────────────────────────────────────────────────────────────

def get_transactions(db: Session, account_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Transaction]:
    q = db.query(Transaction)
    if account_id:
        q = q.filter(Transaction.account_id == account_id)
    return q.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()


def create_transaction(db: Session, data: TransactionCreate) -> Transaction:
    tx = Transaction(**data.model_dump())
    db.add(tx)
    # Update account balance
    account = get_account(db, data.account_id)
    if account:
        if data.transaction_type == "credit":
            account.balance += data.amount
        else:
            account.balance -= data.amount
    db.commit()
    db.refresh(tx)
    return tx


# ── Invoice ───────────────────────────────────────────────────────────────────

def get_invoices(db: Session, status: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Invoice]:
    q = db.query(Invoice)
    if status:
        q = q.filter(Invoice.status == status)
    return q.order_by(Invoice.created_at.desc()).offset(skip).limit(limit).all()


def get_invoice(db: Session, invoice_id: int) -> Optional[Invoice]:
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()


def create_invoice(db: Session, data: InvoiceCreate) -> Invoice:
    invoice = Invoice(**data.model_dump())
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice


def update_invoice(db: Session, invoice_id: int, data: InvoiceUpdate) -> Optional[Invoice]:
    invoice = get_invoice(db, invoice_id)
    if not invoice:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(invoice, field, value)
    if data.status == "paid" and not invoice.paid_at:
        invoice.paid_at = datetime.utcnow()
    db.commit()
    db.refresh(invoice)
    return invoice


# ── Budget ────────────────────────────────────────────────────────────────────

def get_budgets(db: Session, year: Optional[int] = None) -> List[Budget]:
    q = db.query(Budget)
    if year:
        q = q.filter(Budget.year == year)
    return q.all()


def create_budget(db: Session, data: BudgetCreate) -> Budget:
    budget = Budget(**data.model_dump())
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


def update_budget(db: Session, budget_id: int, data: BudgetUpdate) -> Optional[Budget]:
    budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not budget:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(budget, field, value)
    db.commit()
    db.refresh(budget)
    return budget


# ── Summary ───────────────────────────────────────────────────────────────────

def get_finance_summary(db: Session) -> FinanceSummary:
    # Revenue = sum of credit transactions this year
    current_year = datetime.utcnow().year
    revenue = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.transaction_type == "credit",
        extract("year", Transaction.date) == current_year,
    ).scalar() or 0.0

    expenses = db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.transaction_type == "debit",
        extract("year", Transaction.date) == current_year,
    ).scalar() or 0.0

    pending = db.query(func.count(Invoice.id)).filter(Invoice.status.in_(["draft", "sent"])).scalar() or 0
    overdue = db.query(func.count(Invoice.id)).filter(Invoice.status == "overdue").scalar() or 0

    cash_account = db.query(Account).filter(Account.account_type == "asset").first()
    cash_balance = db.query(func.coalesce(func.sum(Account.balance), 0)).filter(
        Account.account_type == "asset"
    ).scalar() or 0.0

    return FinanceSummary(
        total_revenue=float(revenue),
        total_expenses=float(expenses),
        net_profit=float(revenue) - float(expenses),
        pending_invoices=int(pending),
        overdue_invoices=int(overdue),
        cash_balance=float(cash_balance),
    )
