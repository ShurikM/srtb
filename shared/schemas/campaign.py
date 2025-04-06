from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class CampaignBase(BaseModel):
    name: str
    domain: str
    price: float
    crid: str
    adm: str
    click_url: Optional[str] = None

    budget: Optional[float] = None
    bid_floor: Optional[float] = None
    impression_limit: Optional[int] = None
    targeting_rules: Optional[Dict[str, Any]] = None  # Flexible targeting logic

    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    is_active: bool = True

class CampaignCreate(CampaignBase):
    pass

class CampaignRead(CampaignBase):
    id: int

    class Config:
        orm_mode = True
