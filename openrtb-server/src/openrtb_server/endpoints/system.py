from fastapi import APIRouter
from fastapi.responses import JSONResponse
import time

router = APIRouter()

request_count = 0

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/version")
def version():
    return {"version": "0.1.0"}

@router.get("/metrics")
def metrics():
    uptime = int(time.time() - start_time)
    return {
        "requests_total": request_count,
        "uptime_seconds": uptime
    }
