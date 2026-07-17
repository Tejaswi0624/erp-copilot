from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.finance import (
    AccountCreate, AccountUpdate, AccountOut,
    TransactionCreate, TransactionOut,
    InvoiceCreate, InvoiceUpdate, InvoiceOut,
    BudgetCreate, BudgetUpdate, BudgetOut,
    FinanceSummary,
)
from app.services import finance as svc

router = APIRouter(prefix="/finance", tags=["finance"])


# ── Summary ───────────────────────────────────────────────────────────────────
@router.get("/summary", response_model=FinanceSummary)
def summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_finance_summary(db)


# ── Accounts ──────────────────────────────────────────────────────────────────
@router.get("/accounts", response_model=List[AccountOut])
def list_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                  _: User = Depends(get_current_user)):
    return svc.get_accounts(db, skip, limit)


@router.post("/accounts", response_model=AccountOut, status_code=201)
def create_account(data: AccountCreate, db: Session = Depends(get_db),
                   _: User = Depends(get_current_user)):
    return svc.create_account(db, data)


@router.get("/accounts/{account_id}", response_model=AccountOut)
def get_account(account_id: int, db: Session = Depends(get_db),
                _: User = Depends(get_current_user)):
    account = svc.get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


@router.put("/accounts/{account_id}", response_model=AccountOut)
def update_account(account_id: int, data: AccountUpdate, db: Session = Depends(get_db),
                   _: User = Depends(get_current_user)):
    account = svc.update_account(db, account_id, data)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


# ── Transactions ──────────────────────────────────────────────────────────────
@router.get("/transactions", response_model=List[TransactionOut])
def list_transactions(account_id: Optional[int] = None, skip: int = 0, limit: int = 100,
                      db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_transactions(db, account_id, skip, limit)


@router.post("/transactions", response_model=TransactionOut, status_code=201)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db),
                       _: User = Depends(get_current_user)):
    return svc.create_transaction(db, data)


# ── Invoices ──────────────────────────────────────────────────────────────────
@router.get("/invoices", response_model=List[InvoiceOut])
def list_invoices(status: Optional[str] = None, skip: int = 0, limit: int = 100,
                  db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_invoices(db, status, skip, limit)


@router.post("/invoices", response_model=InvoiceOut, status_code=201)
def create_invoice(data: InvoiceCreate, db: Session = Depends(get_db),
                   _: User = Depends(get_current_user)):
    return svc.create_invoice(db, data)


@router.get("/invoices/{invoice_id}", response_model=InvoiceOut)
def get_invoice(invoice_id: int, db: Session = Depends(get_db),
                _: User = Depends(get_current_user)):
    inv = svc.get_invoice(db, invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv


@router.put("/invoices/{invoice_id}", response_model=InvoiceOut)
def update_invoice(invoice_id: int, data: InvoiceUpdate, db: Session = Depends(get_db),
                   _: User = Depends(get_current_user)):
    inv = svc.update_invoice(db, invoice_id, data)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return inv


# ── Budgets ───────────────────────────────────────────────────────────────────
@router.get("/budgets", response_model=List[BudgetOut])
def list_budgets(year: Optional[int] = None, db: Session = Depends(get_db),
                 _: User = Depends(get_current_user)):
    return svc.get_budgets(db, year)


@router.post("/budgets", response_model=BudgetOut, status_code=201)
def create_budget(data: BudgetCreate, db: Session = Depends(get_db),
                  _: User = Depends(get_current_user)):
    return svc.create_budget(db, data)


@router.put("/budgets/{budget_id}", response_model=BudgetOut)
def update_budget(budget_id: int, data: BudgetUpdate, db: Session = Depends(get_db),
                  _: User = Depends(get_current_user)):
    b = svc.update_budget(db, budget_id, data)
    if not b:
        raise HTTPException(status_code=404, detail="Budget not found")
    return b
