import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Configuración básica de logs
import logging
logger = logging.getLogger(__name__)

def load_dataframe_to_postgres(
    db: Session,
    df: pd.DataFrame,
    table_name: str,
    if_exists: str = "append"
):
    """
    Load a pandas DataFrame into PostgreSQL.
    """
    try:
        conn = db.get_bind()
        
        df.to_sql(
            table_name,
            con=conn,
            if_exists=if_exists,
            index=False,
            method="multi",
            chunksize=1000
        )

        logger.info(f"Success: {len(df)} rows loaded into table ‘{table_name}’.")

    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity Error (Duplicates or FK): {e.orig}")
        raise ValueError(f"Data error: You probably violated a unique key constraint. {e.orig}")

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"SQLAlchemy error: {str(e)}")
        raise e

    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error: {str(e)}")
        raise e