from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


# ── Department ────────────────────────────────────────────────────────────────

class DepartmentBase(BaseModel):
    name: str
    code: str
    manager_id: Optional[int] = None
    budget: float = 0.0


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    manager_id: Optional[int] = None
    budget: Optional[float] = None


class DepartmentOut(DepartmentBase):
    id: int
    headcount: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Employee ──────────────────────────────────────────────────────────────────

class EmployeeBase(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    position: str
    department_id: Optional[int] = None
    manager_id: Optional[int] = None
    salary: float = 0.0
    hire_date: Optional[date] = None
    status: str = "active"
    avatar: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None
    department_id: Optional[int] = None
    manager_id: Optional[int] = None
    salary: Optional[float] = None
    status: Optional[str] = None
    avatar: Optional[str] = None


class EmployeeOut(EmployeeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Payroll ───────────────────────────────────────────────────────────────────

class PayrollBase(BaseModel):
    employee_id: int
    period: str
    gross_salary: float
    deductions: float = 0.0
    net_salary: float
    bonus: float = 0.0
    status: str = "pending"


class PayrollCreate(PayrollBase):
    pass


class PayrollUpdate(BaseModel):
    status: Optional[str] = None
    paid_at: Optional[datetime] = None
    bonus: Optional[float] = None
    deductions: Optional[float] = None


class PayrollOut(PayrollBase):
    id: int
    paid_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Leave Request ─────────────────────────────────────────────────────────────

class LeaveRequestBase(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    days: int = 1
    reason: Optional[str] = None


class LeaveRequestCreate(LeaveRequestBase):
    pass


class LeaveRequestUpdate(BaseModel):
    status: Optional[str] = None
    approved_by: Optional[int] = None


class LeaveRequestOut(LeaveRequestBase):
    id: int
    status: str
    approved_by: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── HR Summary ────────────────────────────────────────────────────────────────

class HRSummary(BaseModel):
    total_employees: int
    active_employees: int
    on_leave: int
    departments: int
    pending_leaves: int
    monthly_payroll: float
