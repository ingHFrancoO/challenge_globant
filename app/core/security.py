import os
from fastapi import Header, HTTPException, status

def verify_token(x_token: str = Header(...)):
    expected_token = os.getenv("API_TOKEN")
    print(expected_token)
    print(x_token)
    if not expected_token or x_token != expected_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API token",
        )