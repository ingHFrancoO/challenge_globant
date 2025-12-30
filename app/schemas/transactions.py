from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any

class TableBatch(BaseModel):
    # We avoid empty table names and limit length
    table_name: str = Field(
        ..., 
        min_length=1, 
        max_length=63, 
        pattern="^[a-zA-Z0-9_]+$",
        description="Name of the table in the database"
    )
    
    # We optimize list validation
    rows: List[Dict[str, Any]] = Field(
        ..., 
        min_length=1,
        max_items=1000,
        description="List of records to insert. Maximum 1,000 per batch."
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "table_name": "jobs",
                "rows": [
                    {"id": 1, "name": "Alice"},
                    {"id": 2, "name": "Bob"}
                ]
            }
        }
    )