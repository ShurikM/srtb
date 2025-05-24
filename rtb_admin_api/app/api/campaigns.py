# rtb_admin_api/app/api/campaigns.py
from datetime import datetime
from shared.schemas import CampaignRuntime
from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from shared import models, schemas
from shared.db.session import get_db
from shared.config import IS_FAKE_DB
from rtb_admin_api.app.fake_store import campaign_store, init_fake_campaigns
from typing import List
from rtb_admin_api.app.api.auth import get_logged_user

router = APIRouter()

if IS_FAKE_DB:
    init_fake_campaigns()

@router.get("/secure", response_model=List[CampaignRuntime])
# === FAKE DB ACCESS (NO DB NEEDED) ===
def secure_list_campaigns(session: str = Cookie(None)):
    # Special test cookie that never expires
    if session == "devtest-session":
        return list(campaign_store.values())
    user = get_logged_user(session)
    return list(campaign_store.values())

@router.get("/", response_model=List[CampaignRuntime])
def list_campaigns():
    return list(campaign_store.values())

# === REAL DB ACCESS ===
@router.get("/active", response_model=list[CampaignRuntime])
def get_active_campaigns(db: Session = Depends(get_db)):
    now = datetime.utcnow()
    campaigns = db.query(models.Campaign).filter(
        models.Campaign.is_active == True,
        models.Campaign.start_time <= now,
        models.Campaign.end_time >= now,
    ).all()
    return campaigns

@router.get("/db", response_model=list[schemas.CampaignRead])
def read_campaigns(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Campaign).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.CampaignRead)
def create_campaign(campaign: schemas.CampaignCreate, db: Session = Depends(get_db)):
    db_campaign = models.Campaign(**campaign.dict())
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

@router.put("/{campaign_id}", response_model=schemas.CampaignRead)
def update_campaign(campaign_id: int, campaign_data: schemas.CampaignCreate, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    for key, value in campaign_data.dict().items():
        setattr(campaign, key, value)
    db.commit()
    db.refresh(campaign)
    return campaign

@router.delete("/{campaign_id}")
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    db.delete(campaign)
    db.commit()
    return {"detail": "Campaign deleted successfully"}

@router.get("/{campaign_id}", response_model=schemas.CampaignRead)
def read_campaign(campaign_id: str, db: Session = Depends(get_db)):
    print(f"🔍 Incoming GET /campaigns/{campaign_id}")
    if IS_FAKE_DB:
        print("📦 FAKE DB mode is ON")
        if campaign_id not in campaign_store:
            print(f"❌ Campaign {campaign_id} not found in fake store")
            raise HTTPException(status_code=404, detail="Campaign not found")
        campaign = campaign_store[campaign_id]
        print("✅ Campaign found:", campaign)
        return campaign
    else:
        print("🛢️ REAL DB mode")
        campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
        if campaign is None:
            print(f"❌ Campaign {campaign_id} not found in DB")
            raise HTTPException(status_code=404, detail="Campaign not found")
        print("✅ Campaign from DB:", campaign)
        return campaign