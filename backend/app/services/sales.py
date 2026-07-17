from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.models.sales import Customer, SalesOrder, SalesOrderItem, Opportunity
from app.schemas.sales import (
    CustomerCreate, CustomerUpdate,
    SalesOrderCreate, SalesOrderUpdate,
    OpportunityCreate, OpportunityUpdate,
    SalesSummary,
)


# ── Customer ──────────────────────────────────────────────────────────────────

def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[Customer]:
    return db.query(Customer).filter(Customer.is_active == True).offset(skip).limit(limit).all()


def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
    return db.query(Customer).filter(Customer.id == customer_id).first()


def create_customer(db: Session, data: CustomerCreate) -> Customer:
    customer = Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def update_customer(db: Session, customer_id: int, data: CustomerUpdate) -> Optional[Customer]:
    customer = get_customer(db, customer_id)
    if not customer:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(customer, field, value)
    db.commit()
    db.refresh(customer)
    return customer


# ── Sales Order ───────────────────────────────────────────────────────────────

def get_orders(db: Session, customer_id: Optional[int] = None, status: Optional[str] = None,
               skip: int = 0, limit: int = 100) -> List[SalesOrder]:
    q = db.query(SalesOrder)
    if customer_id:
        q = q.filter(SalesOrder.customer_id == customer_id)
    if status:
        q = q.filter(SalesOrder.status == status)
    return q.order_by(SalesOrder.created_at.desc()).offset(skip).limit(limit).all()


def get_order(db: Session, order_id: int) -> Optional[SalesOrder]:
    return db.query(SalesOrder).filter(SalesOrder.id == order_id).first()


def create_order(db: Session, data: SalesOrderCreate) -> SalesOrder:
    items_data = data.items or []
    order_dict = data.model_dump(exclude={"items"})
    order = SalesOrder(**order_dict)
    db.add(order)
    db.flush()  # get order.id

    for item_data in items_data:
        item = SalesOrderItem(order_id=order.id, **item_data.model_dump())
        db.add(item)

    # Update customer stats
    customer = get_customer(db, data.customer_id)
    if customer:
        customer.total_orders += 1
        customer.total_revenue += data.total

    db.commit()
    db.refresh(order)
    return order


def update_order(db: Session, order_id: int, data: SalesOrderUpdate) -> Optional[SalesOrder]:
    order = get_order(db, order_id)
    if not order:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(order, field, value)
    db.commit()
    db.refresh(order)
    return order


# ── Opportunity ───────────────────────────────────────────────────────────────

def get_opportunities(db: Session, stage: Optional[str] = None,
                      skip: int = 0, limit: int = 100) -> List[Opportunity]:
    q = db.query(Opportunity)
    if stage:
        q = q.filter(Opportunity.stage == stage)
    return q.order_by(Opportunity.created_at.desc()).offset(skip).limit(limit).all()


def get_opportunity(db: Session, opp_id: int) -> Optional[Opportunity]:
    return db.query(Opportunity).filter(Opportunity.id == opp_id).first()


def create_opportunity(db: Session, data: OpportunityCreate) -> Opportunity:
    opp = Opportunity(**data.model_dump())
    db.add(opp)
    db.commit()
    db.refresh(opp)
    return opp


def update_opportunity(db: Session, opp_id: int, data: OpportunityUpdate) -> Optional[Opportunity]:
    opp = get_opportunity(db, opp_id)
    if not opp:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(opp, field, value)
    db.commit()
    db.refresh(opp)
    return opp


# ── Summary ───────────────────────────────────────────────────────────────────

def get_sales_summary(db: Session) -> SalesSummary:
    total_customers = db.query(func.count(Customer.id)).filter(Customer.is_active == True).scalar() or 0
    total_orders = db.query(func.count(SalesOrder.id)).scalar() or 0
    total_revenue = db.query(func.coalesce(func.sum(SalesOrder.total), 0)).filter(
        SalesOrder.status.in_(["delivered", "shipped", "confirmed"])
    ).scalar() or 0.0
    pending_orders = db.query(func.count(SalesOrder.id)).filter(
        SalesOrder.status.in_(["draft", "confirmed", "processing"])
    ).scalar() or 0
    pipeline_value = db.query(func.coalesce(func.sum(Opportunity.value), 0)).filter(
        Opportunity.stage.notin_(["closed_won", "closed_lost"])
    ).scalar() or 0.0
    open_opps = db.query(func.count(Opportunity.id)).filter(
        Opportunity.stage.notin_(["closed_won", "closed_lost"])
    ).scalar() or 0

    return SalesSummary(
        total_customers=int(total_customers),
        total_orders=int(total_orders),
        total_revenue=float(total_revenue),
        pending_orders=int(pending_orders),
        pipeline_value=float(pipeline_value),
        open_opportunities=int(open_opps),
    )
