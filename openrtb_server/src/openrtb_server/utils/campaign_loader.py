import requests
from shared.schemas import CampaignRuntime

ACTIVE_CAMPAIGNS_URL = "http://rtb-admin-api:8000/campaigns/active"  # adjust as needed

def fetch_active_campaigns() -> dict[int, CampaignRuntime]:
    try:
        response = requests.get(ACTIVE_CAMPAIGNS_URL, timeout=5)
        response.raise_for_status()
        campaigns = [CampaignRuntime(**item) for item in response.json()]
        return {campaign.id: campaign for campaign in campaigns}
    except Exception as e:
        print(f"[WARN] Failed to fetch campaigns: {e}")
        return {}
