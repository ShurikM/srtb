from fastapi import APIRouter
from fastapi.responses import JSONResponse
import time
import os
from shared.s3_upload import upload_file_to_s3


router = APIRouter()
start_time = int(time.time())
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

@router.post("/logs/sync")
def sync_logs_to_s3():
    uploaded = 0
    for file in os.listdir("logs"):
        if file.endswith(".zip"):
            local_path = os.path.join("logs", file)
            s3_key = f"logs/{file}"
            if upload_file_to_s3(local_path, s3_key):
                uploaded += 1
    return {"uploaded": uploaded}
