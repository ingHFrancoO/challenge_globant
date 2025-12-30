from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


from app.db.session import get_db
from app.schemas.transactions import TableBatch
from app.services.transactions_service import save_rows_in_table

import pandas as pd

router = APIRouter()

@router.post(
        "/add_records/batch", 
        # response_model=list[ColorOut]
        )
def add_records(transactions: List[TableBatch],  db: Session = Depends(get_db)):
    """
    Insert batch transactions (up to 1000 rows per table)
    """
    try:
        correct_tablets = ['jobs', 'departments', 'hired_employees']
        for table_batch in transactions:
            table_name = table_batch.table_name
            rows = table_batch.rows
            if table_name not in correct_tablets:
                return {"status": "error", "message": f"Unknown table {table_name}"}

            if len(rows) > 1000:
                return {"status": "error", "message": f"Max 1000 rows per batch for {table_name}"}
            
            try:
                save_rows_in_table(table_name, rows, db)
                return {"status":  "ok", "message": "Data processed correctly"}
            except Exception as e:
                raise HTTPException(status_code=500, detail="Error processing bulk upload")
    except Exception:
        raise HTTPException(
                status_code=500,
                detail="Internal server error"
        )
