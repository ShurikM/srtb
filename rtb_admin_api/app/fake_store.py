from shared.schemas import CampaignRuntime
from datetime import datetime, timedelta
from typing import Dict

campaign_store: Dict[str, CampaignRuntime] = {}

def init_fake_campaigns():
     campaign_store["demo1"] = CampaignRuntime(
        id="demo1",
        name="Demo Campaign 1",
        domain="demo.com",
        price=1.5,
        crid="demo-crid-001",
        adm="<ad-markup>",
        click_url="https://demo.com/click",
        budget=10000.0,
        bid_floor=0.5,
        impression_limit=100000,
        targeting_rules={"geo": "US", "device": "mobile"},
        daily_cap=10000,
        hourly_cap=1000,
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(days=7),
    )

     campaign_store["demo2"] = CampaignRuntime(
        id="demo2",
        name="Demo Campaign 2",
        domain="demo.com",
        price=1.5,
        crid="demo-crid-002",
        adm="<ad-markup>",
        click_url="https://demo.com/click",
        budget=10000.0,
        bid_floor=0.5,
        impression_limit=100000,
        targeting_rules={"geo": "US", "device": "mobile"},
        daily_cap=1000,
        hourly_cap=100,
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow() + timedelta(days=7),
     )
