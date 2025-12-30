import pandas as pd

def process_data(df: pd.DataFrame) -> list[dict]:
    df.columns = [c.lower().strip() for c in df.columns]
    df["processed_at"] = pd.Timestamp.utcnow()
    return df.to_dict(orient="records")