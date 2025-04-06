# openrtb_server/main.py.py
from fastapi import FastAPI
from openrtb_server.endpoints import bid, system
import logging
from shared.db.session import SessionLocal
from shared.models import Campaign


logging.basicConfig(
    filename="bid_requests.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
app = FastAPI(
    title="OpenRTB Server",
    version="0.1.0",
    description="Supports OpenRTB 2.x and 3.0 request formats."
)

app.include_router(bid.router)
app.include_router(system.router)
