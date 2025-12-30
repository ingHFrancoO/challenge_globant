from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from app.api.v1.endpoints import users, auth, colors
from app.api.v1.endpoints import transactions
from app.db.init_db import init_db

origins = ["*"]

app = FastAPI(
    title="Globant Challenge API",
    version="1.0.0",
    description="API for CSV ingestion, backup and restore"
)

@app.on_event("startup")
def startup_event():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["All DB"])
