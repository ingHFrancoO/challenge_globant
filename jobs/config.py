import os
from dotenv import load_dotenv

load_dotenv()

GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

if not GCS_BUCKET_NAME:
    raise RuntimeError("GCS_BUCKET_NAME not defined")
