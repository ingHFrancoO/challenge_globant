from pathlib import Path
from fastavro import reader
import pandas as pd
import os

from persistence.oltp_database import load_dataframe_to_postgres
from config.config import GCS_BUCKET_NAME, BACKUP_PREFIX
from config.db_config import get_postgres_engine
from ingestion.gcs_client import download_file_from_gcs


def read_avro_to_df(avro_path: Path) -> pd.DataFrame:
    """
    Reads an AVRO file and returns a pandas DataFrame.
    """
    records = []
    with open(avro_path, "rb") as f:
        avro_reader = reader(f)
        for record in avro_reader:
            records.append(record)

    df = pd.DataFrame(records)
    return df

def restore_table_from_gcs_backup(table_name: str, backup_date: str) -> None:
    """
    Restores a table from its AVRO backup stored in GCS.

    Args:
        table_name: Logical table name
        backup_date: Folder name / date of backup, e.g., "2025-12-30"
    """
    # if table_name not in TABLE_LOADERS:
    #     raise ValueError(f"Unknown table: {table_name}")

    gcs_path = f"{BACKUP_PREFIX}/{backup_date}_{table_name}.avro"
    local_tmp_path = Path("/tmp") / f"{table_name}.avro"

    # Descargar AVRO desde GCS
    dowloaded = download_file_from_gcs(GCS_BUCKET_NAME, gcs_path, local_tmp_path)

    if not dowloaded: 
        return 

    # Leer AVRO y convertir a DataFrame
    df = read_avro_to_df(local_tmp_path)
    os.remove(local_tmp_path)
    # Persistir en la DB
    engine = get_postgres_engine()
    load_dataframe_to_postgres(df, table_name, engine)
