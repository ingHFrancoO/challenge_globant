
from sqlalchemy.orm import Session
from collections import defaultdict

from app.repository.metrics_repo import fetch_hired_employees_by_quarter, fetch_departments_above_mean_hiring
from app.models.schemas.metrics import HiredEmployeesQuarterlyOut, QuarterlyHiring


def hired_employees_by_quarter(db: Session, year: int): 
    if year < 1900:
        raise ValueError("Invalid year")

    rows = fetch_hired_employees_by_quarter(db, year)

    grouped = defaultdict(dict)

    for r in rows:
        key = (r.department, r.job)
        grouped[key][int(r.quarter)] = r.hired_employees

    result = []

    for (department, job), quarters_data in grouped.items():
        quarters = [
            QuarterlyHiring(
                quarter=q,
                hired=quarters_data.get(q, 0)
            )
            for q in range(1, 5)
        ]

        result.append(
            HiredEmployeesQuarterlyOut(
                department=department,
                job=job,
                hired_employees=quarters,
            )
        )

    return result

def departments_above_mean_hiring(db: Session, year: int):
    if year < 1900:
        raise ValueError("Invalid year")

    rows = fetch_departments_above_mean_hiring(db, year)

    return [
        {
            "id": r.department_id,
            "name": r.department_name,
            "hired_employees": r.hired_employees,
        }
        for r in rows
    ]