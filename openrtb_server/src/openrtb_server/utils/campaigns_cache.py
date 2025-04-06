from shared.models import Campaign
from shared.db.session import get_db xc
from sqlalchemy.orm import Session

campaigns_by_id: dict[int, Campaign] = {}

def load_active_campaigns():
    global campaigns_by_id
    db: Session = get_db_session()
    campaigns = db.query(Campaign).filter(Campaign.is_active == True).all()
    campaigns_by_id = {c.id: c for c in campaigns}
    db.close()

def get_campaign(campaign_id: int) -> Campaign | None:
    return campaigns_by_id.get(campaign_id)

def get_all_campaigns() -> list[Campaign]:
    return list(campaigns_by_id.values())
