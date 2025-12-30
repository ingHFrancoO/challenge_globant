import pandas as pd
import os
from typing import Literal

_TABLE_SCHEMAS: dict[str, list[str]] = {
    "departments": ["id", "name"],
    "jobs": ["id", "name"],
    "hired_employees": [
        "id",
        "full_name",
        "hired_at",
        "department_id",
        "job_id",
    ],
}


def apply_schema(
    df: pd.DataFrame,
    schema: Literal["departments", "jobs", "hired_employees"],
) -> pd.DataFrame:
    """
    Rename columns according to schema mapping.
    """
    df = df.copy()
    df.columns = _TABLE_SCHEMAS[schema]
    return df

def normalize_df(df: pd.DataFrame, schema:str) -> pd.DataFrame:
    undentified_value = int(os.getenv("UNDENTIFIED_CELL_VALUE"))
    df = df.copy()
    if schema == 'hired_employees':
        df = df.dropna(subset=["full_name"])    # Delete records without employee names
        df["job_id"] = df["job_id"].fillna(undentified_value).astype(int) # If job is null, it is assigned id 9999 (unidentified).
        df["department_id"] = df["department_id"].fillna(undentified_value).astype(int) # If department is null, it is assigned id 9999 (unidentified).
        df["hired_at"] = df["hired_at"].fillna(pd.Timestamp.utcnow())
        df["hired_at"] = pd.to_datetime(
            df["hired_at"],
            utc=True,
            errors="coerce"
        )
    else:
        df.loc[len(df)] = [undentified_value, "unidentified"]

    df = df.apply(lambda c: c.str.lower() if c.dtype == "object" else c)

    return df