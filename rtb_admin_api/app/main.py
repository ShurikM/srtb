# rtb_admin_api/app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import campaigns
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Prepare log directory and rotating handler
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
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

# Compute path to React build directory (build)
WEB_UI_BUILD_DIR = BASE_DIR.parent / "web_ui" / "build"
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
