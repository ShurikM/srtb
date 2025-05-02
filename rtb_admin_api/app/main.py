# rtb_admin_api/app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import campaigns
import os
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "rtb_admin.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Set up rotating file handler
rotating_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,  # 5 MB per file
    backupCount=5              # Keep last 5 log files
)
rotating_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[rotating_handler, console_handler]
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_UI_BUILD_DIR = BASE_DIR.parent / "web_ui" / "build"

logger.info(f"WEB_UI_BUILD_DIR = {WEB_UI_BUILD_DIR}")

app = FastAPI(
    title="RTB Admin API",
    version="0.1.0",
    description="Manage RTB campaigns via CRUD endpoints."
)

app.include_router(campaigns.router)

# Serve the React build
app.mount("/", StaticFiles(directory=WEB_UI_BUILD_DIR, html=True), name="static")
