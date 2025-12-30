import os
from dotenv import load_dotenv

load_dotenv()

BACKUP_PREFIX = os.getenv("BACKUP_PREFIX")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
INCOMING_PREFIX = os.getenv("INCOMING_PREFIX")
PROCESSED_PREFIX = os.getenv("PROCESSED_PREFIX")
OLAP_PREFIX = os.getenv("OLAP_PREFIX")

if not GCS_BUCKET_NAME:
    raise RuntimeError("GCS_BUCKET_NAME not defined")
