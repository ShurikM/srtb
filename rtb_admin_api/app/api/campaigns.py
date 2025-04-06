from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from shared import models, schemas
from shared.db.session import get_db

router = APIRouter()

@router.post("/", response_model=schemas.CampaignRead)
def create_campaign(campaign: schemas.CampaignCreate, db: Session = Depends(get_db)):
    db_campaign = models.Campaign(**campaign.dict())
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign

@router.get("/{campaign_id}", response_model=schemas.CampaignRead)
def read_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(models.Campaign).filter(models.Campaign.id == campaign_id).first()
    if campaign is None:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.get("/", response_model=list[schemas.CampaignRead])
def read_campaigns(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Campaign).offset(skip).limit(limit).all()

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