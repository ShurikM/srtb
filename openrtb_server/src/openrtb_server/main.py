# openrtb_server/main.py
from fastapi import FastAPI
from openrtb_server.endpoints import system, bid, track
import logging
from openrtb_server.utils.campaigns_cache import load_active_campaigns
from openrtb_server.utils.log_rotation import rotate_logs
from contextlib import asynccontextmanager
import time

from shared.config import IS_FAKE_DB



import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "rtb_tracking.log")),
        logging.StreamHandler()  # to see logs in terminal
    ]
)

def campaign_refresh_loop():
    global active_campaigns
    while True:
        active_campaigns = load_active_campaigns(is_fake=IS_FAKE_DB)
        time.sleep(60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    # thread = threading.Thread(target=campaign_refresh_loop, daemon=True)
    # thread.start()
    app.state.active_campaigns = load_active_campaigns(is_fake=True)

    yield  # App runs here

    # Shutdown logic
    rotate_logs()

app = FastAPI(
    title="OpenRTB Server",
    version="0.1.0",
    description="Supports OpenRTB 2.x and 3.0 request formats.",
    lifespan=lifespan
)

app.include_router(bid.router)
app.include_router(system.router)

app.include_router(track.router)

