from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.models.inventory import Product, Warehouse, StockMovement, PurchaseOrder
from app.schemas.inventory import (
    ProductCreate, ProductUpdate,
    WarehouseCreate,
    StockMovementCreate,
    PurchaseOrderCreate, PurchaseOrderUpdate,
    InventorySummary,
)


# ── Warehouse ─────────────────────────────────────────────────────────────────

def get_warehouses(db: Session) -> List[Warehouse]:
    return db.query(Warehouse).filter(Warehouse.is_active == True).all()


def create_warehouse(db: Session, data: WarehouseCreate) -> Warehouse:
    wh = Warehouse(**data.model_dump())
    db.add(wh)
    db.commit()
    db.refresh(wh)
    return wh


# ── Product ───────────────────────────────────────────────────────────────────

def get_products(db: Session, category: Optional[str] = None, low_stock: bool = False,
                 skip: int = 0, limit: int = 100) -> List[Product]:
    q = db.query(Product).filter(Product.is_active == True)
    if category:
        q = q.filter(Product.category == category)
    if low_stock:
        q = q.filter(Product.quantity_on_hand <= Product.reorder_level)
    return q.offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, data: ProductCreate) -> Product:
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product_id: int, data: ProductUpdate) -> Optional[Product]:
    product = get_product(db, product_id)
    if not product:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> bool:
    product = get_product(db, product_id)
    if not product:
        return False
    product.is_active = False
    db.commit()
    return True


# ── Stock Movement ────────────────────────────────────────────────────────────

def get_stock_movements(db: Session, product_id: Optional[int] = None,
                        skip: int = 0, limit: int = 100) -> List[StockMovement]:
    q = db.query(StockMovement)
    if product_id:
        q = q.filter(StockMovement.product_id == product_id)
    return q.order_by(StockMovement.created_at.desc()).offset(skip).limit(limit).all()


def create_stock_movement(db: Session, data: StockMovementCreate) -> StockMovement:
    movement = StockMovement(**data.model_dump())
    db.add(movement)
    # Update product quantity
    product = get_product(db, data.product_id)
    if product:
        if data.movement_type == "in":
            product.quantity_on_hand += data.quantity
        elif data.movement_type == "out":
            product.quantity_on_hand = max(0, product.quantity_on_hand - data.quantity)
        elif data.movement_type == "adjustment":
            product.quantity_on_hand = data.quantity
    db.commit()
    db.refresh(movement)
    return movement


# ── Purchase Order ────────────────────────────────────────────────────────────

def get_purchase_orders(db: Session, status: Optional[str] = None,
                        skip: int = 0, limit: int = 100) -> List[PurchaseOrder]:
    q = db.query(PurchaseOrder)
    if status:
        q = q.filter(PurchaseOrder.status == status)
    return q.order_by(PurchaseOrder.created_at.desc()).offset(skip).limit(limit).all()


def get_purchase_order(db: Session, po_id: int) -> Optional[PurchaseOrder]:
    return db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()


def create_purchase_order(db: Session, data: PurchaseOrderCreate) -> PurchaseOrder:
    po = PurchaseOrder(**data.model_dump())
    db.add(po)
    db.commit()
    db.refresh(po)
    return po


def update_purchase_order(db: Session, po_id: int, data: PurchaseOrderUpdate) -> Optional[PurchaseOrder]:
    po = get_purchase_order(db, po_id)
    if not po:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(po, field, value)
    db.commit()
    db.refresh(po)
    return po


# ── Summary ───────────────────────────────────────────────────────────────────

def get_inventory_summary(db: Session) -> InventorySummary:
    total_products = db.query(func.count(Product.id)).filter(Product.is_active == True).scalar() or 0
    low_stock = db.query(func.count(Product.id)).filter(
        Product.is_active == True,
        Product.quantity_on_hand <= Product.reorder_level,
        Product.quantity_on_hand > 0,
    ).scalar() or 0
    out_of_stock = db.query(func.count(Product.id)).filter(
        Product.is_active == True,
        Product.quantity_on_hand == 0,
    ).scalar() or 0
    total_value = db.query(
        func.coalesce(func.sum(Product.quantity_on_hand * Product.cost_price), 0)
    ).filter(Product.is_active == True).scalar() or 0.0
    pending_orders = db.query(func.count(PurchaseOrder.id)).filter(
        PurchaseOrder.status.in_(["draft", "sent", "partial"])
    ).scalar() or 0
    warehouses = db.query(func.count(Warehouse.id)).filter(Warehouse.is_active == True).scalar() or 0

    return InventorySummary(
        total_products=int(total_products),
        low_stock_items=int(low_stock),
        out_of_stock=int(out_of_stock),
        total_value=float(total_value),
        pending_orders=int(pending_orders),
        warehouses=int(warehouses),
    )
