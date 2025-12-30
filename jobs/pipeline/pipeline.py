import os
from config.config import OLAP_PREFIX
from config.db_config import get_postgres_engine
from ingestion.gcs_client import list_gcs_files, read_csv_from_gcs, move_to_processed, upload_file_to_gcs
from pipeline.validators import validate_required_files
from persistence.avro_backup import backup_table_to_avro
from persistence.oltp_database import load_dataframe_to_postgres
from persistence.olap_database import olap_table_to_avro
from processing.transformations import apply_schema, normalize_df
from utils.text_extractor import table_name_from_blob

_LOAD_ORDER = [
    "incoming/departments.csv",
    "incoming/jobs.csv",
    "incoming/hired_employees.csv",
]

def pipeline():
    files = list_gcs_files("incoming/")
     # ---- Early exit: nothing to process ----
    if not files:
        return
    # ---- Validate required files ----
    validate_required_files(files)

    engine = get_postgres_engine()

    for blob_name in _LOAD_ORDER:
        table_name = table_name_from_blob(blob_name)

        df = read_csv_from_gcs(blob_name)
        df = apply_schema(df, table_name)
        df = normalize_df(df, table_name)
        load_dataframe_to_postgres(
            df,
            table_name,
            engine
        )
        
        move_to_processed(blob_name)

        avro_file = backup_table_to_avro(df, table_name)
        upload_file_to_gcs(avro_file)
        os.remove(avro_file)

        avro_file = olap_table_to_avro(df, table_name)
        # Make sure you always have a list of paths
        paths = avro_file if isinstance(avro_file, tuple) else [avro_file]
        for path in paths:
            upload_file_to_gcs(path, OLAP_PREFIX)
            os.remove(path)
