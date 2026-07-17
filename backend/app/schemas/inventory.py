from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ── Warehouse ─────────────────────────────────────────────────────────────────

class WarehouseBase(BaseModel):
    name: str
    code: str
    location: Optional[str] = None
    capacity: int = 0
    is_active: bool = True


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseOut(WarehouseBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Product ───────────────────────────────────────────────────────────────────

class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    unit_price: float = 0.0
    cost_price: float = 0.0
    quantity_on_hand: int = 0
    reorder_level: int = 10
    reorder_quantity: int = 50
    warehouse_id: Optional[int] = None
    is_active: bool = True
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    unit_price: Optional[float] = None
    cost_price: Optional[float] = None
    quantity_on_hand: Optional[int] = None
    reorder_level: Optional[int] = None
    reorder_quantity: Optional[int] = None
    is_active: Optional[bool] = None
    image_url: Optional[str] = None


class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Stock Movement ────────────────────────────────────────────────────────────

class StockMovementBase(BaseModel):
    product_id: int
    movement_type: str
    quantity: int
    reference: Optional[str] = None
    notes: Optional[str] = None


class StockMovementCreate(StockMovementBase):
    pass


class StockMovementOut(StockMovementBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Purchase Order ────────────────────────────────────────────────────────────

class PurchaseOrderBase(BaseModel):
    po_number: str
    supplier_name: str
    supplier_email: Optional[str] = None
    total_amount: float = 0.0
    status: str = "draft"
    expected_date: Optional[datetime] = None
    notes: Optional[str] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    pass


class PurchaseOrderUpdate(BaseModel):
    status: Optional[str] = None
    received_date: Optional[datetime] = None
    notes: Optional[str] = None
    total_amount: Optional[float] = None


class PurchaseOrderOut(PurchaseOrderBase):
    id: int
    order_date: datetime
    received_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Inventory Summary ─────────────────────────────────────────────────────────

class InventorySummary(BaseModel):
    total_products: int
    low_stock_items: int
    out_of_stock: int
    total_value: float
    pending_orders: int
    warehouses: int
