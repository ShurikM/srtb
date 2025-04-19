from pydantic import BaseModel
from typing import Optional, Dict, Any, List
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

    daily_cap: Optional[int] = None
    hourly_cap: Optional[int] = None

    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    is_active: bool = True

class CampaignCreate(CampaignBase):
    pass

class CampaignRead(CampaignBase):
    id: int

    class Config:
        orm_mode = True

class CampaignRuntime(BaseModel):
    id: int
    crid: str
    adm: str
    price: float
    click_url: Optional[str] = None
    targeting_rules: Optional[Dict[str, Any]] = None

    budget: Optional[float] = None
    is_active: bool = True
    daily_cap: Optional[int] = None
    hourly_cap: Optional[int] = None
    last_impression_at: Optional[datetime] = None

    class Config:
        orm_mode = True