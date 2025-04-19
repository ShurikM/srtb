# shared/utils/campaigns_cache.py or wherever appropriate

from shared.schemas.campaign import CampaignRuntime
from shared.models import Campaign
from shared.db.session import get_db
from sqlalchemy.orm import Session

def load_active_campaigns(is_fake: bool = False) -> dict[int, CampaignRuntime]:
    if is_fake:
        fake_campaign = CampaignRuntime(
            id=1,
            crid="creative-001",
            adm="<img src='http://example.com/ad.png'/>",
            price=1.5,
            click_url="http://example.com/click",
            targeting_rules={"countries": ["US"], "device_types": ["mobile"]},
            budget=10.0,
            is_active=True
        )
        return {fake_campaign.id: fake_campaign}

    # Real DB-backed loading
    db: Session = get_db()
    try:
        db_campaigns = db.query(Campaign).filter(Campaign.is_active == True).all()

        runtime_campaigns: dict[int, CampaignRuntime] = {}
        for campaign in db_campaigns:
            runtime_campaigns[campaign.id] = CampaignRuntime(
                id=campaign.id,
                crid=campaign.crid,
                adm=campaign.adm,
                price=campaign.price,
                click_url=campaign.click_url,
                targeting_rules=campaign.targeting_rules,
                budget=campaign.budget,
                is_active=campaign.is_active
            )

        return runtime_campaigns

    finally:
        db.close()
