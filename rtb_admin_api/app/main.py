from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import campaigns
import os
from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

# Prepare log directory and rotating handler
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE = LOG_DIR / "rtb_admin.log"
LOG_DIR.mkdir(parents=True, exist_ok=True)

rotating_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,  # 5 MB per file
    backupCount=5              # keep last 5 files
)
rotating_handler.setFormatter(
    logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
)

# Configure root logger
logging.basicConfig(level=logging.INFO, handlers=[rotating_handler, console_handler])
logger = logging.getLogger(__name__)

# Compute path to React output directory (dist)
BASE_DIR = Path(__file__).resolve().parent.parent
WEB_UI_BUILD_DIR = BASE_DIR.parent / "web_ui" / "dist"

logger.info(f"Serving React UI from: {WEB_UI_BUILD_DIR}")

# Create FastAPI app
app = FastAPI(
    title="RTB Admin API",
    version="0.1.0",
    description="Manage RTB campaigns via CRUD endpoints."
)

# Mount API routes
app.include_router(campaigns.router)

# Serve React build as SPA
app.mount(
    "/",
    StaticFiles(directory=str(WEB_UI_BUILD_DIR), html=True),
    name="static"
)
