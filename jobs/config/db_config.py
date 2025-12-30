from sqlalchemy import create_engine
import os


def get_postgres_engine():
    """
    Create PostgreSQL SQLAlchemy engine using environment variables.
    """
    user = os.getenv("PG_USER")
    password = os.getenv("PG_PASSWORD")
    host = os.getenv("PG_HOST")
    port = os.getenv("PG_PORT", "5432")
    db = os.getenv("PG_DB")

    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)
