from google.cloud import storage
from datetime import datetime
import io
import pandas as pd
from config.config import GCS_BUCKET_NAME
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
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(blob_name)

    content = blob.download_as_bytes()
    return pd.read_csv(io.BytesIO(content))

def move_to_processed(blob_name: str):
    bucket = client.bucket(GCS_BUCKET_NAME)

    source_blob = bucket.blob(blob_name)

    filename = blob_name.split("/")[-1]
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    destination_blob_name = f"processed/{timestamp}_{filename}"

    bucket.copy_blob(
        source_blob,
        bucket,
        destination_blob_name
    )

    source_blob.delete()