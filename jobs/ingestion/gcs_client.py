from datetime import datetime
from google.cloud import storage
from pathlib import Path
import io
import pandas as pd

from config.config import GCS_BUCKET_NAME, PROCESSED_PREFIX, BACKUP_PREFIX

client = storage.Client()

def list_gcs_files( prefix: str | None = None) -> list[str]:
    """
    List files stored in a Google Cloud Storage bucket.

    Args:
        bucket_name (str): Name of the GCS bucket.
        prefix (str, optional): Filter files by prefix (e.g. 'input/', 'processed/').

    Returns:
        List[str]: List of blob names found in the bucket.
    """
    blobs = client.list_blobs(GCS_BUCKET_NAME, prefix=prefix)

    return [
        blob.name
        for blob in blobs
        if not blob.name.endswith("/")
    ]

def read_csv_from_gcs(blob_name: str) -> pd.DataFrame:
    """
    Reed CSV from Storage.
    """
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(blob_name)

    content = blob.download_as_bytes()
    return pd.read_csv(
        io.BytesIO(content),
        header=None
        )

def move_to_processed(blob_name: str):
    """
    Move filo from inbound folter to processed folder.
    """
    bucket = client.bucket(GCS_BUCKET_NAME)

    source_blob = bucket.blob(blob_name)

    filename = blob_name.split("/")[-1]
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    destination_blob_name = f"{PROCESSED_PREFIX}/{timestamp}_{filename}"

    bucket.copy_blob(
        source_blob,
        bucket,
        destination_blob_name
    )

    source_blob.delete()

def upload_file_to_gcs(
    local_path: Path,
    remote_path_profix: str = BACKUP_PREFIX
) -> None:
    """
    Uploads a local file to Google Cloud Storage.
    """
    bucket = client.bucket(GCS_BUCKET_NAME)
    # Construimos el path en GCS: remote_path_profix + filename
    destination_path = f"{remote_path_profix}/{local_path.name}"

    blob = bucket.blob(destination_path)
    blob.upload_from_filename(local_path)

def download_file_from_gcs(bucket_name: str, gcs_path: str, local_path: Path) -> None:
    """
    Downloads a file from GCS to local filesystem.

    Args:
        bucket_name: Name of the GCS bucket
        gcs_path: Path to the file in GCS
        local_path: Path to save the file locally
    """
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    
    if not blob.exists():
        print(f"File {gcs_path} does not exist in bucket {bucket_name}")
        return False

    local_path.parent.mkdir(parents=True, exist_ok=True)
    blob.download_to_filename(local_path)
    print(f"Downloaded {gcs_path} to {local_path}")