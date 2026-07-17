from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.hr import (
    DepartmentCreate, DepartmentUpdate, DepartmentOut,
    EmployeeCreate, EmployeeUpdate, EmployeeOut,
    PayrollCreate, PayrollUpdate, PayrollOut,
    LeaveRequestCreate, LeaveRequestUpdate, LeaveRequestOut,
    HRSummary,
)
from app.services import hr as svc

router = APIRouter(prefix="/hr", tags=["hr"])


@router.get("/summary", response_model=HRSummary)
def summary(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_hr_summary(db)


# ── Departments ───────────────────────────────────────────────────────────────
@router.get("/departments", response_model=List[DepartmentOut])
def list_departments(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_departments(db)


@router.post("/departments", response_model=DepartmentOut, status_code=201)
def create_department(data: DepartmentCreate, db: Session = Depends(get_db),
                      _: User = Depends(get_current_user)):
    return svc.create_department(db, data)


@router.put("/departments/{dept_id}", response_model=DepartmentOut)
def update_department(dept_id: int, data: DepartmentUpdate, db: Session = Depends(get_db),
                      _: User = Depends(get_current_user)):
    dept = svc.update_department(db, dept_id, data)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept


# ── Employees ─────────────────────────────────────────────────────────────────
@router.get("/employees", response_model=List[EmployeeOut])
def list_employees(dept_id: Optional[int] = None, status: Optional[str] = None,
                   skip: int = 0, limit: int = 100,
                   db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_employees(db, dept_id, status, skip, limit)


@router.post("/employees", response_model=EmployeeOut, status_code=201)
def create_employee(data: EmployeeCreate, db: Session = Depends(get_db),
                    _: User = Depends(get_current_user)):
    return svc.create_employee(db, data)


@router.get("/employees/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int, db: Session = Depends(get_db),
                 _: User = Depends(get_current_user)):
    emp = svc.get_employee(db, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.put("/employees/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, data: EmployeeUpdate, db: Session = Depends(get_db),
                    _: User = Depends(get_current_user)):
    emp = svc.update_employee(db, employee_id, data)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db),
                    _: User = Depends(get_current_user)):
    if not svc.delete_employee(db, employee_id):
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee terminated"}


# ── Payroll ───────────────────────────────────────────────────────────────────
@router.get("/payroll", response_model=List[PayrollOut])
def list_payrolls(employee_id: Optional[int] = None, period: Optional[str] = None,
                  skip: int = 0, limit: int = 100,
                  db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_payrolls(db, employee_id, period, skip, limit)


@router.post("/payroll", response_model=PayrollOut, status_code=201)
def create_payroll(data: PayrollCreate, db: Session = Depends(get_db),
                   _: User = Depends(get_current_user)):
    return svc.create_payroll(db, data)


@router.put("/payroll/{payroll_id}", response_model=PayrollOut)
def update_payroll(payroll_id: int, data: PayrollUpdate, db: Session = Depends(get_db),
                   _: User = Depends(get_current_user)):
    p = svc.update_payroll(db, payroll_id, data)
    if not p:
        raise HTTPException(status_code=404, detail="Payroll record not found")
    return p


# ── Leave Requests ────────────────────────────────────────────────────────────
@router.get("/leaves", response_model=List[LeaveRequestOut])
def list_leaves(employee_id: Optional[int] = None, status: Optional[str] = None,
                skip: int = 0, limit: int = 100,
                db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return svc.get_leave_requests(db, employee_id, status, skip, limit)


@router.post("/leaves", response_model=LeaveRequestOut, status_code=201)
def create_leave(data: LeaveRequestCreate, db: Session = Depends(get_db),
                 _: User = Depends(get_current_user)):
    return svc.create_leave_request(db, data)


@router.put("/leaves/{leave_id}", response_model=LeaveRequestOut)
def update_leave(leave_id: int, data: LeaveRequestUpdate, db: Session = Depends(get_db),
                 _: User = Depends(get_current_user)):
    leave = svc.update_leave_request(db, leave_id, data)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave request not found")
    return leave
