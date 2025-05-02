# rtb_admin_api/app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import campaigns
import os


app = FastAPI(
    title="RTB Admin API",
    version="0.1.0",
    description="Manage RTB campaigns via CRUD endpoints."
)

app.include_router(campaigns.router)

# Serve the React build
app.mount("/", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "..", "web_ui", "build"), html=True), name="static")
