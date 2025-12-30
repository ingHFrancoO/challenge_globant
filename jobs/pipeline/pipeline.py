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

from ingestion.gcs_client import list_gcs_files
from pipeline.validators import validate_required_files
from ingestion.gcs_client import read_csv_from_gcs

def pipeline():
    files = list_gcs_files("incoming/")
     # ---- Early exit: nothing to process ----
    if not files:
        return
    # ---- Validate required files ----
    validate_required_files(files)

    df = read_csv_from_gcs(files[0])
    print(df)
    
    print(files)