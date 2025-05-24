from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class CampaignBase(BaseModel):
    id: str
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
    pass

class CampaignRuntime(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    crid: str
    adm: str
    price: float
    click_url: Optional[str] = None
    targeting_rules: Optional[Dict[str, Any]] = None
    budget: Optional[float] = None
    is_active: bool = True
    daily_cap: Optional[int] = None
    hourly_cap: Optional[int] = None
    impression_timestamps: List[datetime] = Field(default_factory=list)
    last_impression_at: Optional[datetime] = None