from typing import List, Dict, Any

import pandas as pd

from app.repository.transactions_repo import load_dataframe_to_postgres

def save_rows_in_table(table_name: str, rows: List[Dict[str, Any]], db):
    #1. Convert to DataFrame efficiently
    df = pd.DataFrame(rows)

    #2. Quick cleanup: remove nulls if necessary or extra columns
    df = df.dropna(how='all') 

    #3. Call the load function
    load_dataframe_to_postgres(db, df, table_name)

