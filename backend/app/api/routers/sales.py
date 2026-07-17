from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.sales import (
    CustomerCreate, CustomerUpdate, CustomerOut,
    SalesOrderCreate, SalesOrderUpdate, SalesOrderOut,
    OpportunityCreate, OpportunityUpdate, OpportunityOut,
    SalesSummary,
)
from app.services import sales as svc

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("/summary", response_model=SalesSummary)
def summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_sales_summary(db)


# ── Customers ─────────────────────────────────────────────────────────────────
@router.get("/customers", response_model=List[CustomerOut])
def list_customers(skip: int = 0, limit: int = 100,
                   db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_customers(db, skip, limit)


@router.post("/customers", response_model=CustomerOut, status_code=201)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db),
                    _: User = Depends(get_current_user)):
    return svc.create_customer(db, data)


@router.get("/customers/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db),
                 _: User = Depends(get_current_user)):
    c = svc.get_customer(db, customer_id)
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    return c


@router.put("/customers/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, data: CustomerUpdate, db: Session = Depends(get_db),
                    _: User = Depends(get_current_user)):
    c = svc.update_customer(db, customer_id, data)
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    return c


# ── Sales Orders ──────────────────────────────────────────────────────────────
@router.get("/orders", response_model=List[SalesOrderOut])
def list_orders(customer_id: Optional[int] = None, status: Optional[str] = None,
                skip: int = 0, limit: int = 100,
                db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_orders(db, customer_id, status, skip, limit)


@router.post("/orders", response_model=SalesOrderOut, status_code=201)
def create_order(data: SalesOrderCreate, db: Session = Depends(get_db),
                 _: User = Depends(get_current_user)):
    return svc.create_order(db, data)


@router.get("/orders/{order_id}", response_model=SalesOrderOut)
def get_order(order_id: int, db: Session = Depends(get_db),
              _: User = Depends(get_current_user)):
    o = svc.get_order(db, order_id)
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    return o


@router.put("/orders/{order_id}", response_model=SalesOrderOut)
def update_order(order_id: int, data: SalesOrderUpdate, db: Session = Depends(get_db),
                 _: User = Depends(get_current_user)):
    o = svc.update_order(db, order_id, data)
    if not o:
        raise HTTPException(status_code=404, detail="Order not found")
    return o


# ── Opportunities ─────────────────────────────────────────────────────────────
@router.get("/opportunities", response_model=List[OpportunityOut])
def list_opportunities(stage: Optional[str] = None, skip: int = 0, limit: int = 100,
                       db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_opportunities(db, stage, skip, limit)


@router.post("/opportunities", response_model=OpportunityOut, status_code=201)
def create_opportunity(data: OpportunityCreate, db: Session = Depends(get_db),
                       _: User = Depends(get_current_user)):
    return svc.create_opportunity(db, data)


@router.get("/opportunities/{opp_id}", response_model=OpportunityOut)
def get_opportunity(opp_id: int, db: Session = Depends(get_db),
                    _: User = Depends(get_current_user)):
    o = svc.get_opportunity(db, opp_id)
    if not o:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return o


@router.put("/opportunities/{opp_id}", response_model=OpportunityOut)
def update_opportunity(opp_id: int, data: OpportunityUpdate, db: Session = Depends(get_db),
                       _: User = Depends(get_current_user)):
    o = svc.update_opportunity(db, opp_id, data)
    if not o:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return o
