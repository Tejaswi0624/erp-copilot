from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ── Contact ───────────────────────────────────────────────────────────────────

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    source: Optional[str] = None
    tags: Optional[str] = None
    notes: Optional[str] = None
    is_active: bool = True


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    source: Optional[str] = None
    tags: Optional[str] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class ContactOut(ContactBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Lead ──────────────────────────────────────────────────────────────────────

class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = None
    status: str = "new"
    estimated_value: float = 0.0
    assigned_to: Optional[str] = None
    notes: Optional[str] = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    estimated_value: Optional[float] = None
    notes: Optional[str] = None


class LeadOut(LeadBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Activity ──────────────────────────────────────────────────────────────────

class ActivityBase(BaseModel):
    contact_id: Optional[int] = None
    activity_type: str
    subject: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: bool = False


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None
    completed_at: Optional[datetime] = None


class ActivityOut(ActivityBase):
    id: int
    completed_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}
