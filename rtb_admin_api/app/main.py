# rtb_admin_api/app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

# Setup logging directory and file
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "rtb_admin.log")

# Configure rotating file handler
rotating_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,  # 5 MB per file
    backupCount=5
)
rotating_handler.setFormatter(
    logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
)

# Configure console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
)

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[rotating_handler, console_handler]
)
logger = logging.getLogger(__name__)

# Determine base and UI build directories
BASE_DIR = Path(__file__).resolve().parent.parent
WEB_UI_BUILD_DIR = BASE_DIR.parent / "web_ui" / "dist"
logger.info(f"Serving React UI from: {WEB_UI_BUILD_DIR}")

# Initialize FastAPI
app = FastAPI(
    title="RTB Admin API",
    version="0.1.0",
    description="Manage RTB campaigns via CRUD endpoints."
)

# Include API routers
from app.api import campaigns
app.include_router(campaigns.router)

# Mount the static files (React build)
if WEB_UI_BUILD_DIR.exists():
    app.mount(
        "/",
        StaticFiles(directory=str(WEB_UI_BUILD_DIR), html=True),
        name="static"
    )
else:
    logger.error(f"React build directory not found: {WEB_UI_BUILD_DIR}")
