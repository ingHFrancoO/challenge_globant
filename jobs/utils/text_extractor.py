from pathlib import Path

def table_name_from_blob(blob_name: str) -> str:
    """
    Extract table name from GCS blob name.
    Example: incoming/departments.csv -> departments
    """
    return Path(blob_name).stem