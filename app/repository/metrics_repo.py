from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, extract

from app.models.db.oltp import HiredEmployee, Department, Job


def fetch_hired_employees_by_quarter(db: Session, year):

    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)

    quarter_expr = extract("quarter", HiredEmployee.hired_at)

    rows = (
        db.query(
            Department.name.label("department"),
            Job.name.label("job"),
            quarter_expr.label("quarter"),
            func.count(HiredEmployee.id).label("hired_employees"),
        )
        .join(Department, HiredEmployee.department_id == Department.id)
        .join(Job, HiredEmployee.job_id == Job.id)
        .filter(
            HiredEmployee.hired_at >= start_date,
            HiredEmployee.hired_at < end_date,
        )
        .group_by(
            Department.name,
            Job.name,
            quarter_expr,
        )
        .order_by(
            Department.name.asc(),
            Job.name.asc(),
            quarter_expr.asc(),
        )
        .all()
    )

    return rows

def fetch_departments_above_mean_hiring(db: Session, year: int):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year+1, 1, 1)

    # Subquery: hires por departamento en 2021
    dept_hires_subq = (
        db.query(
            Department.id.label("department_id"),
            Department.name.label("department_name"),
            func.count(HiredEmployee.id).label("hired_employees"),
        )
        .join(HiredEmployee, HiredEmployee.department_id == Department.id)
        .filter(
            HiredEmployee.hired_at >= start_date,
            HiredEmployee.hired_at < end_date,
        )
        .group_by(Department.id, Department.name)
        .subquery()
    )

    # Subquery: promedio de contrataciones
    avg_hires_subq = (
        db.query(func.avg(dept_hires_subq.c.hired_employees))
        .scalar_subquery()
    )

    # Query final
    rows = (
        db.query(
            dept_hires_subq.c.department_id,
            dept_hires_subq.c.department_name,
            dept_hires_subq.c.hired_employees,
        )
        .filter(dept_hires_subq.c.hired_employees > avg_hires_subq)
        .order_by(dept_hires_subq.c.hired_employees.desc())
        .all()
    )

    return rows