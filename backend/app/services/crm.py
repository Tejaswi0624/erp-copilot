from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from app.models.crm import Contact, Lead, Activity
from app.schemas.crm import (
    ContactCreate, ContactUpdate,
    LeadCreate, LeadUpdate,
    ActivityCreate, ActivityUpdate,
)


# ── Contact ───────────────────────────────────────────────────────────────────

def get_contacts(db: Session, skip: int = 0, limit: int = 100) -> List[Contact]:
    return db.query(Contact).filter(Contact.is_active == True).offset(skip).limit(limit).all()


def get_contact(db: Session, contact_id: int) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.id == contact_id).first()


def create_contact(db: Session, data: ContactCreate) -> Contact:
    contact = Contact(**data.model_dump())
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def update_contact(db: Session, contact_id: int, data: ContactUpdate) -> Optional[Contact]:
    contact = get_contact(db, contact_id)
    if not contact:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact


# ── Lead ──────────────────────────────────────────────────────────────────────

def get_leads(db: Session, status: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Lead]:
    q = db.query(Lead)
    if status:
        q = q.filter(Lead.status == status)
    return q.order_by(Lead.created_at.desc()).offset(skip).limit(limit).all()


def get_lead(db: Session, lead_id: int) -> Optional[Lead]:
    return db.query(Lead).filter(Lead.id == lead_id).first()


def create_lead(db: Session, data: LeadCreate) -> Lead:
    lead = Lead(**data.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


def update_lead(db: Session, lead_id: int, data: LeadUpdate) -> Optional[Lead]:
    lead = get_lead(db, lead_id)
    if not lead:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(lead, field, value)
    db.commit()
    db.refresh(lead)
    return lead


# ── Activity ──────────────────────────────────────────────────────────────────

def get_activities(db: Session, contact_id: Optional[int] = None,
                   skip: int = 0, limit: int = 100) -> List[Activity]:
    q = db.query(Activity)
    if contact_id:
        q = q.filter(Activity.contact_id == contact_id)
    return q.order_by(Activity.created_at.desc()).offset(skip).limit(limit).all()


def create_activity(db: Session, data: ActivityCreate) -> Activity:
    activity = Activity(**data.model_dump())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def update_activity(db: Session, activity_id: int, data: ActivityUpdate) -> Optional[Activity]:
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(activity, field, value)
    if data.completed and not activity.completed_at:
        activity.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(activity)
    return activity
