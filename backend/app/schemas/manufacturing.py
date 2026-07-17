from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ── Work Order ────────────────────────────────────────────────────────────────

class WorkOrderBase(BaseModel):
    wo_number: str
    product_name: str
    quantity: int = 1
    status: str = "draft"
    priority: str = "normal"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    notes: Optional[str] = None


class WorkOrderCreate(WorkOrderBase):
    pass


class WorkOrderUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None


class WorkOrderOut(WorkOrderBase):
    id: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Bill of Materials ─────────────────────────────────────────────────────────

class BOMBase(BaseModel):
    product_name: str
    version: str = "1.0"
    component_name: str
    component_sku: Optional[str] = None
    quantity: float = 1.0
    unit: str = "pcs"
    notes: Optional[str] = None
    is_active: bool = True


class BOMCreate(BOMBase):
    pass


class BOMOut(BOMBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Production Run ────────────────────────────────────────────────────────────

class ProductionRunBase(BaseModel):
    work_order_id: int
    quantity_planned: int
    quantity_produced: int = 0
    quantity_rejected: int = 0
    operator: Optional[str] = None
    machine: Optional[str] = None
    notes: Optional[str] = None


class ProductionRunCreate(ProductionRunBase):
    pass


class ProductionRunUpdate(BaseModel):
    quantity_produced: Optional[int] = None
    quantity_rejected: Optional[int] = None
    operator: Optional[str] = None
    machine: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None


class ProductionRunOut(ProductionRunBase):
    id: int
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Manufacturing Summary ─────────────────────────────────────────────────────

class ManufacturingSummary(BaseModel):
    total_work_orders: int
    in_progress: int
    completed_this_month: int
    planned: int
    total_units_produced: int
    rejection_rate: float
