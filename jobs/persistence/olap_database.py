from datetime import datetime
from fastavro import writer, parse_schema
from pathlib import Path
from typing import Dict, Any

import os
import pandas as pd

def _infer_avro_schema(
    df: pd.DataFrame,
    name: str,
) -> Dict[str, Any]:
    type_mapping = {
        "int64": "long",
        "float64": "double",
        "object": "string",
        "bool": "boolean",
    }

    fields = []
    for col, dtype in df.dtypes.items():
        avro_type = type_mapping.get(str(dtype), "string")
        fields.append({
            "name": col,
            "type": ["null", avro_type],
            "default": None,
        })

    return {
        "type": "record",
        "name": name,
        "fields": fields,
    }

def _normalize_df_for_avro(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts non-AVRO-native pandas types into AVRO-compatible ones.
    """

    df = df.copy()

    for col in df.columns:
        # datetime / timestamp → ISO string
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime("%Y-%m-%dT%H:%M:%S%z")

    return df


def _save_df_to_avro(df: pd.DataFrame, file_name: str) -> Path:
    """Helper to save any DataFrame to Avro."""
    base_path = Path(os.getenv("AVRO_BASE_PATH"))
    base_path.mkdir(parents=True, exist_ok=True)
    file_path = base_path / f"{file_name}.avro"
    schema = _infer_avro_schema(df, file_name)
    parsed_schema = parse_schema(schema)
    with open(file_path, "wb") as f:
        writer(f, parsed_schema, df.to_dict(orient="records"))
    return file_path

def olap_table_to_avro(
    df: pd.DataFrame,
    table_name: str,
) -> None:
    """
    Saves a DataFrame as an AVRO OLAP file.

    Args:
        df: DataFrame to backup
        table_name: logical table name
        base_path: root backup directory
    """
    df = _normalize_df_for_avro(df)

    if table_name == "hired_employees":
        # --- DATE DIMMENSION ---
        # Convertir hired_at a datetime primero
        df["hired_at"] = pd.to_datetime(df["hired_at"], errors="coerce")
        df_time = (
            df[["hired_at"]]
            .dropna()
            .drop_duplicates()
            .assign(
                date=lambda x: pd.to_datetime(x["hired_at"]).dt.strftime("%Y-%m-%d"),
                date_id=lambda x: pd.to_datetime(x["hired_at"]).dt.strftime("%Y%m%d"),
                year=lambda x: pd.to_datetime(x["hired_at"]).dt.year.astype(str),
                quarter=lambda x: pd.to_datetime(x["hired_at"]).dt.quarter.astype(str),
                month=lambda x: pd.to_datetime(x["hired_at"]).dt.month.astype(str),
            )
        )[["date_id", "date", "year", "quarter", "month"]]

        # --- FACT TABLE ---
        df_fact = (
            df.assign(hired_at_id=pd.to_datetime(df["hired_at"]).dt.strftime("%Y%m%d").astype(int))
            .groupby(["hired_at_id", "department_id", "job_id"], as_index=False)
            .agg(total_hires=("id", "count"))
        )

        # save Avro
        path_time = _save_df_to_avro(df_time, "dim_date")
        path_fact = _save_df_to_avro(df_fact, "fact_hires")
        return path_time, path_fact

    return _save_df_to_avro(df, "dim_" + table_name)