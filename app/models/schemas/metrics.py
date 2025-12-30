from pydantic import BaseModel
from typing import List


class QuarterlyHiring(BaseModel):
    quarter: int
    hired: int

class HiredEmployeesQuarterlyOut(BaseModel):
    department: str
    job: str
    hired_employees: List[QuarterlyHiring]

class DepartmentHiringOut(BaseModel):
    id: int
    name: str
    hired_employees: int