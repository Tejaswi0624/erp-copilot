from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.crm import (
    ContactCreate, ContactUpdate, ContactOut,
    LeadCreate, LeadUpdate, LeadOut,
    ActivityCreate, ActivityUpdate, ActivityOut,
)
from app.services import crm as svc

router = APIRouter(prefix="/crm", tags=["crm"])


# ── Contacts ──────────────────────────────────────────────────────────────────
@router.get("/contacts", response_model=List[ContactOut])
def list_contacts(skip: int = 0, limit: int = 100,
                  db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_contacts(db, skip, limit)


@router.post("/contacts", response_model=ContactOut, status_code=201)
def create_contact(data: ContactCreate, db: Session = Depends(get_db),
                   _: User = Depends(get_current_user)):
    return svc.create_contact(db, data)


@router.get("/contacts/{contact_id}", response_model=ContactOut)
def get_contact(contact_id: int, db: Session = Depends(get_db),
                _: User = Depends(get_current_user)):
    c = svc.get_contact(db, contact_id)
    if not c:
        raise HTTPException(status_code=404, detail="Contact not found")
    return c


@router.put("/contacts/{contact_id}", response_model=ContactOut)
def update_contact(contact_id: int, data: ContactUpdate, db: Session = Depends(get_db),
                   _: User = Depends(get_current_user)):
    c = svc.update_contact(db, contact_id, data)
    if not c:
        raise HTTPException(status_code=404, detail="Contact not found")
    return c


# ── Leads ─────────────────────────────────────────────────────────────────────
@router.get("/leads", response_model=List[LeadOut])
def list_leads(status: Optional[str] = None, skip: int = 0, limit: int = 100,
               db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_leads(db, status, skip, limit)


@router.post("/leads", response_model=LeadOut, status_code=201)
def create_lead(data: LeadCreate, db: Session = Depends(get_db),
                _: User = Depends(get_current_user)):
    return svc.create_lead(db, data)


@router.get("/leads/{lead_id}", response_model=LeadOut)
def get_lead(lead_id: int, db: Session = Depends(get_db),
             _: User = Depends(get_current_user)):
    lead = svc.get_lead(db, lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.put("/leads/{lead_id}", response_model=LeadOut)
def update_lead(lead_id: int, data: LeadUpdate, db: Session = Depends(get_db),
                _: User = Depends(get_current_user)):
    lead = svc.update_lead(db, lead_id, data)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


# ── Activities ────────────────────────────────────────────────────────────────
@router.get("/activities", response_model=List[ActivityOut])
def list_activities(contact_id: Optional[int] = None, skip: int = 0, limit: int = 100,
                    db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_activities(db, contact_id, skip, limit)


@router.post("/activities", response_model=ActivityOut, status_code=201)
def create_activity(data: ActivityCreate, db: Session = Depends(get_db),
                    _: User = Depends(get_current_user)):
    return svc.create_activity(db, data)


@router.put("/activities/{activity_id}", response_model=ActivityOut)
def update_activity(activity_id: int, data: ActivityUpdate, db: Session = Depends(get_db),
                    _: User = Depends(get_current_user)):
    a = svc.update_activity(db, activity_id, data)
    if not a:
        raise HTTPException(status_code=404, detail="Activity not found")
    return a
