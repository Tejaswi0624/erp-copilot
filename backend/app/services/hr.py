from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from app.models.hr import Employee, Department, Payroll, LeaveRequest
from app.schemas.hr import (
    EmployeeCreate, EmployeeUpdate,
    DepartmentCreate, DepartmentUpdate,
    PayrollCreate, PayrollUpdate,
    LeaveRequestCreate, LeaveRequestUpdate,
    HRSummary,
)


# ── Department ────────────────────────────────────────────────────────────────

def get_departments(db: Session) -> List[Department]:
    return db.query(Department).all()


def get_department(db: Session, dept_id: int) -> Optional[Department]:
    return db.query(Department).filter(Department.id == dept_id).first()


def create_department(db: Session, data: DepartmentCreate) -> Department:
    dept = Department(**data.model_dump())
    db.add(dept)
    db.commit()
    db.refresh(dept)
    return dept


def update_department(db: Session, dept_id: int, data: DepartmentUpdate) -> Optional[Department]:
    dept = get_department(db, dept_id)
    if not dept:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(dept, field, value)
    db.commit()
    db.refresh(dept)
    return dept


# ── Employee ──────────────────────────────────────────────────────────────────

def get_employees(db: Session, dept_id: Optional[int] = None, status: Optional[str] = None,
                  skip: int = 0, limit: int = 100) -> List[Employee]:
    q = db.query(Employee)
    if dept_id:
        q = q.filter(Employee.department_id == dept_id)
    if status:
        q = q.filter(Employee.status == status)
    return q.offset(skip).limit(limit).all()


def get_employee(db: Session, employee_id: int) -> Optional[Employee]:
    return db.query(Employee).filter(Employee.id == employee_id).first()


def create_employee(db: Session, data: EmployeeCreate) -> Employee:
    employee = Employee(**data.model_dump())
    db.add(employee)
    # Update department headcount
    if data.department_id:
        dept = get_department(db, data.department_id)
        if dept:
            dept.headcount += 1
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee_id: int, data: EmployeeUpdate) -> Optional[Employee]:
    employee = get_employee(db, employee_id)
    if not employee:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)
    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee_id: int) -> bool:
    employee = get_employee(db, employee_id)
    if not employee:
        return False
    employee.status = "terminated"
    db.commit()
    return True


# ── Payroll ───────────────────────────────────────────────────────────────────

def get_payrolls(db: Session, employee_id: Optional[int] = None, period: Optional[str] = None,
                 skip: int = 0, limit: int = 100) -> List[Payroll]:
    q = db.query(Payroll)
    if employee_id:
        q = q.filter(Payroll.employee_id == employee_id)
    if period:
        q = q.filter(Payroll.period == period)
    return q.order_by(Payroll.created_at.desc()).offset(skip).limit(limit).all()


def create_payroll(db: Session, data: PayrollCreate) -> Payroll:
    payroll = Payroll(**data.model_dump())
    db.add(payroll)
    db.commit()
    db.refresh(payroll)
    return payroll


def update_payroll(db: Session, payroll_id: int, data: PayrollUpdate) -> Optional[Payroll]:
    payroll = db.query(Payroll).filter(Payroll.id == payroll_id).first()
    if not payroll:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(payroll, field, value)
    if data.status == "paid" and not payroll.paid_at:
        payroll.paid_at = datetime.utcnow()
    db.commit()
    db.refresh(payroll)
    return payroll


# ── Leave Request ─────────────────────────────────────────────────────────────

def get_leave_requests(db: Session, employee_id: Optional[int] = None,
                       status: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[LeaveRequest]:
    q = db.query(LeaveRequest)
    if employee_id:
        q = q.filter(LeaveRequest.employee_id == employee_id)
    if status:
        q = q.filter(LeaveRequest.status == status)
    return q.order_by(LeaveRequest.created_at.desc()).offset(skip).limit(limit).all()


def create_leave_request(db: Session, data: LeaveRequestCreate) -> LeaveRequest:
    leave = LeaveRequest(**data.model_dump())
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave


def update_leave_request(db: Session, leave_id: int, data: LeaveRequestUpdate) -> Optional[LeaveRequest]:
    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()
    if not leave:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(leave, field, value)
    db.commit()
    db.refresh(leave)
    return leave


# ── Summary ───────────────────────────────────────────────────────────────────

def get_hr_summary(db: Session) -> HRSummary:
    total = db.query(func.count(Employee.id)).scalar() or 0
    active = db.query(func.count(Employee.id)).filter(Employee.status == "active").scalar() or 0
    on_leave = db.query(func.count(Employee.id)).filter(Employee.status == "on_leave").scalar() or 0
    departments = db.query(func.count(Department.id)).scalar() or 0
    pending_leaves = db.query(func.count(LeaveRequest.id)).filter(LeaveRequest.status == "pending").scalar() or 0
    monthly_payroll = db.query(func.coalesce(func.sum(Employee.salary), 0)).filter(
        Employee.status == "active"
    ).scalar() or 0.0

    return HRSummary(
        total_employees=int(total),
        active_employees=int(active),
        on_leave=int(on_leave),
        departments=int(departments),
        pending_leaves=int(pending_leaves),
        monthly_payroll=float(monthly_payroll),
    )
