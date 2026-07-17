from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import datetime

from app.models.manufacturing import WorkOrder, BillOfMaterials, ProductionRun
from app.schemas.manufacturing import (
    WorkOrderCreate, WorkOrderUpdate,
    BOMCreate,
    ProductionRunCreate, ProductionRunUpdate,
    ManufacturingSummary,
)


# ── Work Order ────────────────────────────────────────────────────────────────

def get_work_orders(db: Session, status: Optional[str] = None,
                    skip: int = 0, limit: int = 100) -> List[WorkOrder]:
    q = db.query(WorkOrder)
    if status:
        q = q.filter(WorkOrder.status == status)
    return q.order_by(WorkOrder.created_at.desc()).offset(skip).limit(limit).all()


def get_work_order(db: Session, wo_id: int) -> Optional[WorkOrder]:
    return db.query(WorkOrder).filter(WorkOrder.id == wo_id).first()


def create_work_order(db: Session, data: WorkOrderCreate) -> WorkOrder:
    wo = WorkOrder(**data.model_dump())
    db.add(wo)
    db.commit()
    db.refresh(wo)
    return wo


def update_work_order(db: Session, wo_id: int, data: WorkOrderUpdate) -> Optional[WorkOrder]:
    wo = get_work_order(db, wo_id)
    if not wo:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(wo, field, value)
    if data.status == "completed" and not wo.completed_at:
        wo.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(wo)
    return wo


# ── Bill of Materials ─────────────────────────────────────────────────────────

def get_bom(db: Session, product_name: Optional[str] = None) -> List[BillOfMaterials]:
    q = db.query(BillOfMaterials).filter(BillOfMaterials.is_active == True)
    if product_name:
        q = q.filter(BillOfMaterials.product_name.ilike(f"%{product_name}%"))
    return q.all()


def create_bom(db: Session, data: BOMCreate) -> BillOfMaterials:
    bom = BillOfMaterials(**data.model_dump())
    db.add(bom)
    db.commit()
    db.refresh(bom)
    return bom


# ── Production Run ────────────────────────────────────────────────────────────

def get_production_runs(db: Session, wo_id: Optional[int] = None) -> List[ProductionRun]:
    q = db.query(ProductionRun)
    if wo_id:
        q = q.filter(ProductionRun.work_order_id == wo_id)
    return q.order_by(ProductionRun.created_at.desc()).all()


def create_production_run(db: Session, data: ProductionRunCreate) -> ProductionRun:
    run = ProductionRun(**data.model_dump())
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


def update_production_run(db: Session, run_id: int, data: ProductionRunUpdate) -> Optional[ProductionRun]:
    run = db.query(ProductionRun).filter(ProductionRun.id == run_id).first()
    if not run:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(run, field, value)
    db.commit()
    db.refresh(run)
    return run


# ── Summary ───────────────────────────────────────────────────────────────────

def get_manufacturing_summary(db: Session) -> ManufacturingSummary:
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    total_wo = db.query(func.count(WorkOrder.id)).scalar() or 0
    in_progress = db.query(func.count(WorkOrder.id)).filter(WorkOrder.status == "in_progress").scalar() or 0
    planned = db.query(func.count(WorkOrder.id)).filter(WorkOrder.status == "planned").scalar() or 0
    completed_month = db.query(func.count(WorkOrder.id)).filter(
        WorkOrder.status == "completed",
        extract("month", WorkOrder.completed_at) == current_month,
        extract("year", WorkOrder.completed_at) == current_year,
    ).scalar() or 0

    total_produced = db.query(func.coalesce(func.sum(ProductionRun.quantity_produced), 0)).scalar() or 0
    total_rejected = db.query(func.coalesce(func.sum(ProductionRun.quantity_rejected), 0)).scalar() or 0
    rejection_rate = (float(total_rejected) / float(total_produced) * 100) if total_produced > 0 else 0.0

    return ManufacturingSummary(
        total_work_orders=int(total_wo),
        in_progress=int(in_progress),
        completed_this_month=int(completed_month),
        planned=int(planned),
        total_units_produced=int(total_produced),
        rejection_rate=round(rejection_rate, 2),
    )
