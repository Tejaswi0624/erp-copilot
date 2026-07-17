from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ── Customer ──────────────────────────────────────────────────────────────────

class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    credit_limit: float = 0.0
    is_active: bool = True


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    credit_limit: Optional[float] = None
    is_active: Optional[bool] = None


class CustomerOut(CustomerBase):
    id: int
    total_orders: int
    total_revenue: float
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Sales Order Item ──────────────────────────────────────────────────────────

class SalesOrderItemBase(BaseModel):
    product_name: str
    sku: Optional[str] = None
    quantity: int = 1
    unit_price: float
    total: float


class SalesOrderItemCreate(SalesOrderItemBase):
    pass


class SalesOrderItemOut(SalesOrderItemBase):
    id: int
    order_id: int

    model_config = {"from_attributes": True}


# ── Sales Order ───────────────────────────────────────────────────────────────

class SalesOrderBase(BaseModel):
    order_number: str
    customer_id: int
    status: str = "draft"
    subtotal: float = 0.0
    discount: float = 0.0
    tax: float = 0.0
    total: float = 0.0
    notes: Optional[str] = None


class SalesOrderCreate(SalesOrderBase):
    items: Optional[List[SalesOrderItemCreate]] = []


class SalesOrderUpdate(BaseModel):
    status: Optional[str] = None
    shipped_date: Optional[datetime] = None
    notes: Optional[str] = None
    discount: Optional[float] = None
    tax: Optional[float] = None


class SalesOrderOut(SalesOrderBase):
    id: int
    order_date: datetime
    shipped_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    items: List[SalesOrderItemOut] = []

    model_config = {"from_attributes": True}


# ── Opportunity ───────────────────────────────────────────────────────────────

class OpportunityBase(BaseModel):
    title: str
    customer_id: Optional[int] = None
    stage: str = "prospecting"
    value: float = 0.0
    probability: int = 0
    expected_close: Optional[datetime] = None
    owner: Optional[str] = None
    notes: Optional[str] = None


class OpportunityCreate(OpportunityBase):
    pass


class OpportunityUpdate(BaseModel):
    stage: Optional[str] = None
    value: Optional[float] = None
    probability: Optional[int] = None
    expected_close: Optional[datetime] = None
    owner: Optional[str] = None
    notes: Optional[str] = None


class OpportunityOut(OpportunityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Sales Summary ─────────────────────────────────────────────────────────────

class SalesSummary(BaseModel):
    total_customers: int
    total_orders: int
    total_revenue: float
    pending_orders: int
    pipeline_value: float
    open_opportunities: int
