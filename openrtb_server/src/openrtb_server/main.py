# openrtb_server/main.py
from fastapi import FastAPI
from openrtb_server.endpoints import bid, system
import logging
from openrtb_server.utils.campaign_loader import fetch_active_campaigns
from openrtb_server.utils.log_rotation import rotate_logs
from contextlib import asynccontextmanager
import threading
import time

active_campaigns = {}

logging.basicConfig(
    filename="bid_requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def campaign_refresh_loop():
    global active_campaigns
    while True:
        active_campaigns = fetch_active_campaigns()
        time.sleep(60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    thread = threading.Thread(target=campaign_refresh_loop, daemon=True)
    thread.start()

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
