from datetime import datetime
from fastavro import writer, parse_schema
from pathlib import Path
from typing import Dict, Any

import os
import pandas as pd

def infer_avro_schema(
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

def normalize_df_for_avro(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts non-AVRO-native pandas types into AVRO-compatible ones.
    """

    df = df.copy()

    for col in df.columns:
        # datetime / timestamp → ISO string
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime("%Y-%m-%dT%H:%M:%S%z")

    return df

def backup_table_to_avro(
    df: pd.DataFrame,
    table_name: str,
) -> None:
    """
    Saves a DataFrame as an AVRO backup file.

    Args:
        df: DataFrame to backup
        table_name: logical table name
        base_path: root backup directory
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    base_path = Path(os.getenv("AVRO_BASE_PATH"))  

    base_path.mkdir(parents=True, exist_ok=True)
    file_path = base_path / f"{timestamp}_{table_name}.avro"

    schema = infer_avro_schema(df, table_name)
    parsed_schema = parse_schema(schema)

    df = normalize_df_for_avro(df)
    records = df.to_dict(orient="records")
    with open(file_path, "wb") as f:
        writer(f, parsed_schema, records)

    return file_path