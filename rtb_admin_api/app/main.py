# rtb_admin_api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shared.config import IS_FAKE_DB  # ensures config is loaded at startup
from rtb_admin_api.app.api.campaigns import router as campaigns_router
from rtb_admin_api.app.api.auth import router as auth_router

app = FastAPI()

# CORS setup for local UI development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # adjust if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(campaigns_router, prefix="/api/campaigns", tags=["campaigns"])
