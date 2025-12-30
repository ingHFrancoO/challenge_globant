import pandas as pd

def load_dataframe_to_postgres(
    df: pd.DataFrame,
    table_name: str,
    engine,
    if_exists: str = "append"
):
    """
    Load a pandas DataFrame into PostgreSQL.
    """
    df.to_sql(
        table_name,
        engine,
        if_exists=if_exists,
        index=False,
        method="multi",
        chunksize=1000
    )