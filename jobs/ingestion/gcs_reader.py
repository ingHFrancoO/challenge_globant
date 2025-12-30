from google.cloud import storage
import pandas as pd
import io

def read_gcs_file(bucket_name: str, blob_name: str) -> pd.DataFrame:
    """
    Reads a CSV file stored in Google Cloud Storage (GCS) and loads it into a pandas DataFrame.

    This function connects to GCS using the default service account credentials
    configured in the environment, downloads the specified object as bytes,
    and parses it as a CSV file.

    Args:
        bucket_name (str): Name of the GCS bucket where the file is stored.
        blob_name (str): Path (object name) of the file inside the bucket.

    Returns:
        pd.DataFrame: DataFrame containing the contents of the CSV file.

    Raises:
        google.cloud.exceptions.NotFound: If the bucket or blob does not exist.
        pandas.errors.ParserError: If the file content cannot be parsed as CSV.
    """
    # Initialize GCS client using default credentials
    client = storage.Client()
    # Get bucket and blob references
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    # Download file content as bytes
    content = blob.download_as_bytes()
    # Load CSV content into a DataFrame
    return pd.read_csv(io.BytesIO(content))