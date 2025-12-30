# from app.gcs_client import read_csv_from_gcs, move_to_processed
# from app.processor import process_data

# def pipeline(event: dict):
#     blob_name = event["name"]

#     # Procesar solo archivos en incoming/
#     if not blob_name.startswith("incoming/"):
#         print(f"Ignorado: {blob_name}")
#         return

#     print(f"Procesando {blob_name}")

#     df = read_csv_from_gcs(blob_name)

#     records = process_data(df)

#     # Aquí iría tu insert a DB
#     print(f"{len(records)} registros procesados")

#     move_to_processed(blob_name)

#     print("Archivo movido a processed/")
from config.db_config import get_postgres_engine
from ingestion.gcs_client import list_gcs_files, read_csv_from_gcs
from pipeline.validators import validate_required_files
from persistence.oltp_database import load_dataframe_to_postgres
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