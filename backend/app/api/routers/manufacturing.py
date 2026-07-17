from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.manufacturing import (
    WorkOrderCreate, WorkOrderUpdate, WorkOrderOut,
    BOMCreate, BOMOut,
    ProductionRunCreate, ProductionRunUpdate, ProductionRunOut,
    ManufacturingSummary,
)
from app.services import manufacturing as svc

router = APIRouter(prefix="/manufacturing", tags=["manufacturing"])


@router.get("/summary", response_model=ManufacturingSummary)
def summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_manufacturing_summary(db)


# ── Work Orders ───────────────────────────────────────────────────────────────
@router.get("/work-orders", response_model=List[WorkOrderOut])
def list_work_orders(status: Optional[str] = None, skip: int = 0, limit: int = 100,
                     db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_work_orders(db, status, skip, limit)


@router.post("/work-orders", response_model=WorkOrderOut, status_code=201)
def create_work_order(data: WorkOrderCreate, db: Session = Depends(get_db),
                      _: User = Depends(get_current_user)):
    return svc.create_work_order(db, data)


@router.get("/work-orders/{wo_id}", response_model=WorkOrderOut)
def get_work_order(wo_id: int, db: Session = Depends(get_db),
                   _: User = Depends(get_current_user)):
    wo = svc.get_work_order(db, wo_id)
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    return wo


@router.put("/work-orders/{wo_id}", response_model=WorkOrderOut)
def update_work_order(wo_id: int, data: WorkOrderUpdate, db: Session = Depends(get_db),
                      _: User = Depends(get_current_user)):
    wo = svc.update_work_order(db, wo_id, data)
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    return wo


# ── Bill of Materials ─────────────────────────────────────────────────────────
@router.get("/bom", response_model=List[BOMOut])
def list_bom(product_name: Optional[str] = None,
             db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_bom(db, product_name)


@router.post("/bom", response_model=BOMOut, status_code=201)
def create_bom(data: BOMCreate, db: Session = Depends(get_db),
               _: User = Depends(get_current_user)):
    return svc.create_bom(db, data)


# ── Production Runs ───────────────────────────────────────────────────────────
@router.get("/production-runs", response_model=List[ProductionRunOut])
def list_production_runs(wo_id: Optional[int] = None,
                         db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_production_runs(db, wo_id)


@router.post("/production-runs", response_model=ProductionRunOut, status_code=201)
def create_production_run(data: ProductionRunCreate, db: Session = Depends(get_db),
                          _: User = Depends(get_current_user)):
    return svc.create_production_run(db, data)


@router.put("/production-runs/{run_id}", response_model=ProductionRunOut)
def update_production_run(run_id: int, data: ProductionRunUpdate, db: Session = Depends(get_db),
                          _: User = Depends(get_current_user)):
    run = svc.update_production_run(db, run_id, data)
    if not run:
        raise HTTPException(status_code=404, detail="Production run not found")
    return run
