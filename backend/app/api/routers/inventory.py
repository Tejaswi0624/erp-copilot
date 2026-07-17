from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.inventory import (
    WarehouseCreate, WarehouseOut,
    ProductCreate, ProductUpdate, ProductOut,
    StockMovementCreate, StockMovementOut,
    PurchaseOrderCreate, PurchaseOrderUpdate, PurchaseOrderOut,
    InventorySummary,
)
from app.services import inventory as svc

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/summary", response_model=InventorySummary)
def summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_inventory_summary(db)


# ── Warehouses ────────────────────────────────────────────────────────────────
@router.get("/warehouses", response_model=List[WarehouseOut])
def list_warehouses(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_warehouses(db)


@router.post("/warehouses", response_model=WarehouseOut, status_code=201)
def create_warehouse(data: WarehouseCreate, db: Session = Depends(get_db),
                     _: User = Depends(get_current_user)):
    return svc.create_warehouse(db, data)


# ── Products ──────────────────────────────────────────────────────────────────
@router.get("/products", response_model=List[ProductOut])
def list_products(category: Optional[str] = None, low_stock: bool = False,
                  skip: int = 0, limit: int = 100,
                  db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_products(db, category, low_stock, skip, limit)


@router.post("/products", response_model=ProductOut, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db),
                   _: User = Depends(get_current_user)):
    return svc.create_product(db, data)


@router.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db),
                _: User = Depends(get_current_user)):
    p = svc.get_product(db, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p


@router.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, data: ProductUpdate, db: Session = Depends(get_db),
                   _: User = Depends(get_current_user)):
    p = svc.update_product(db, product_id, data)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db),
                   _: User = Depends(get_current_user)):
    if not svc.delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deactivated"}


# ── Stock Movements ───────────────────────────────────────────────────────────
@router.get("/movements", response_model=List[StockMovementOut])
def list_movements(product_id: Optional[int] = None, skip: int = 0, limit: int = 100,
                   db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_stock_movements(db, product_id, skip, limit)


@router.post("/movements", response_model=StockMovementOut, status_code=201)
def create_movement(data: StockMovementCreate, db: Session = Depends(get_db),
                    _: User = Depends(get_current_user)):
    return svc.create_stock_movement(db, data)


# ── Purchase Orders ───────────────────────────────────────────────────────────
@router.get("/purchase-orders", response_model=List[PurchaseOrderOut])
def list_purchase_orders(status: Optional[str] = None, skip: int = 0, limit: int = 100,
                         db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_purchase_orders(db, status, skip, limit)


@router.post("/purchase-orders", response_model=PurchaseOrderOut, status_code=201)
def create_purchase_order(data: PurchaseOrderCreate, db: Session = Depends(get_db),
                          _: User = Depends(get_current_user)):
    return svc.create_purchase_order(db, data)


@router.get("/purchase-orders/{po_id}", response_model=PurchaseOrderOut)
def get_purchase_order(po_id: int, db: Session = Depends(get_db),
                       _: User = Depends(get_current_user)):
    po = svc.get_purchase_order(db, po_id)
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return po


@router.put("/purchase-orders/{po_id}", response_model=PurchaseOrderOut)
def update_purchase_order(po_id: int, data: PurchaseOrderUpdate, db: Session = Depends(get_db),
                          _: User = Depends(get_current_user)):
    po = svc.update_purchase_order(db, po_id, data)
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return po
