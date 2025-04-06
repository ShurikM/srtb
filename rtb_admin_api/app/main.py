# rtb_admin_api/app/main.py
from fastapi import FastAPI
from app.api import campaigns

app = FastAPI(
    title="RTB Admin API",
    version="0.1.0",
    description="Manage RTB campaigns via CRUD endpoints."
)

app.include_router(campaigns.router)
