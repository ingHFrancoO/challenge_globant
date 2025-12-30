from fastapi import APIRouter, Depends, HTTPException, Path

from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.schemas.transactions import TableBatch
from app.services.metrics_service import hired_employees_by_quarter, departments_above_mean_hiring
from app.models.schemas.metrics import HiredEmployeesQuarterlyOut, DepartmentHiringOut
import pandas as pd 

router = APIRouter()

@router.get(
        "/hired-employees/quarterly/{year}", 
        response_model=List[HiredEmployeesQuarterlyOut],
        summary="Employees hired per quarter",
        )
def get_hired_employees_by_quarter(
    year: int = Path(..., ge=1900, le=2100),
    db: Session = Depends(get_db),
):
    """
    Number of employees hired for each job and department in YEAR divided by quarter. The 
    data must be ordered alphabetically by department and job
    """
    try:
        report = hired_employees_by_quarter(db, year)
        return report
    except Exception:
        raise HTTPException(
                status_code=500,
                detail="Internal server error"
        )

@router.get(
    "/departments/hired-above-mean/{year}",
    response_model=List[DepartmentHiringOut],
    summary="Departments that hired more than the mean in 2021",
)
def get_departments_above_mean_hiring_2021(
    year: int = Path(..., ge=1900, le=2100),
    db: Session = Depends(get_db),
):
    """
    Returns a list of departments (id, name, hired_employees) that hired
    more employees than the average number of hires across all departments
    in 2021. Results are ordered by hired_employees (descending).
    """
    try:
        return departments_above_mean_hiring(db, year)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )