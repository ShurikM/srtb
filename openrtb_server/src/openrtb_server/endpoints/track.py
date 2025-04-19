from fastapi import APIRouter
from datetime import datetime
from openrtb_server.main import active_campaigns  # now a dict
from shared.db.session import get_db
from shared import models
from sqlalchemy.orm import Session
import os

router = APIRouter()
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
IMP_LOG = os.path.join(LOG_DIR, "impressions.log")

def log_impression(campaign_id: int):
    now = datetime.utcnow().isoformat()
    with open(IMP_LOG, "a") as f:
        f.write(f"{now} | impression | campaign_id={campaign_id}\n")

@router.get("/track/impression/{campaign_id}")
def track_impression(campaign_id: int):
    campaign = active_campaigns.get(campaign_id)
    if not campaign:
        return {"error": "Campaign not found"}

    campaign.impression_timestamps.append(datetime.utcnow())

    if campaign.budget is not None:
        campaign.budget -= campaign.price

        if campaign.budget <= 0:
            campaign.budget = 0
            campaign.is_active = False

            # Persist to DB only when deactivated
            db: Session = next(get_db())
            db_campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
            if db_campaign:
                db_campaign.budget = 0
                db_campaign.is_active = False
                db.commit()
            db.close()

    log_impression(campaign_id)
    return {"ok": True}

CLICK_LOG = os.path.join(LOG_DIR, "clicks.log")

def log_click(campaign_id: int):
    now = datetime.utcnow().isoformat()
    with open(CLICK_LOG, "a") as f:
        f.write(f"{now} | click | campaign_id={campaign_id}\n")

@router.get("/track/click/{campaign_id}")
def track_click(campaign_id: int):
    campaign = active_campaigns.get(campaign_id)
    if not campaign:
        return {"error": "Campaign not found"}
    log_click(campaign_id)
    return {"ok": True}

