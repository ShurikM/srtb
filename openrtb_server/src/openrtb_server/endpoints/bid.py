from fastapi import APIRouter, Request
from shared.schemas import CampaignRuntime
from openrtb_server.utils.campaign_loader import fetch_active_campaigns
from uuid import uuid4
from datetime import datetime, timedelta
from shared.mytime import utc_now

import logging
import json
import os
from shared.config import RTB_HOST


router = APIRouter()

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

BID_LOG_PATH = os.path.join(LOG_DIR, "bids.log")

def log_event(file_path: str, event_type: str, campaign_id: int, extra: dict):
    now = utc_now().isoformat()
    log_line = f"{now} | {event_type} | campaign_id={campaign_id} | {json.dumps(extra)}"
    with open(file_path, "a") as f:
        f.write(log_line + "\n")

def match_campaign(campaign: CampaignRuntime, bid_request: dict) -> bool:
    rules = campaign.targeting_rules or {}

    # Match geo
    if "geo" in rules:
        geo = bid_request.get("user", {}).get("geo", {}).get("country")
        if geo != rules["geo"]:
            return False

    # Match domain
    if "domain" in rules:
        domain = bid_request.get("site", {}).get("domain") or bid_request.get("app", {}).get("bundle")
        if domain != rules["domain"]:
            return False

    # Match bid floor
    if "bid_floor" in rules:
        bidfloor = bid_request["imp"][0].get("bidfloor", 0)
        if campaign.price < bidfloor:
            return False

    return True

CAMPAIGN_COOLDOWN_SECONDS = 5
def has_exceeded_caps(campaign: CampaignRuntime) -> bool:
    if not campaign.last_impression_at:
        return False

    now = utc_now()
    next_allowed = campaign.last_impression_at + timedelta(seconds=CAMPAIGN_COOLDOWN_SECONDS)
    return now < next_allowed

# def has_exceeded_caps(campaign: CampaignRuntime) -> bool:
#     now = datetime.utcnow()
#
#     # Keep only recent timestamps
#     campaign.impression_timestamps = [
#         ts for ts in campaign.impression_timestamps
#         if ts > now - timedelta(days=1)
#     ]
#
#     # Hourly cap
#     hourly_count = sum(1 for ts in campaign.impression_timestamps if ts > now - timedelta(hours=1))
#     if campaign.hourly_cap and hourly_count >= campaign.hourly_cap:
#         return True
#
#     # Daily cap
#     if campaign.daily_cap and len(campaign.impression_timestamps) >= campaign.daily_cap:
#         return True
#
#     return False

def generate_tracking_pixel(campaign_id: int) -> str:
    return f'<img src="{RTB_HOST}/track/impression/{campaign_id}" style="display:none;" />'

@router.post("/bid")
async def handle_bid(request: Request):
    bid_request = await request.json()
    request_id = bid_request.get("id")
    imp = bid_request.get("imp", [{}])[0]
    imp_id = imp.get("id", "1")

    campaigns = fetch_active_campaigns()  # now a dict
    for campaign in campaigns.values():
        if not campaign.is_active or has_exceeded_caps(campaign):
            continue
        if match_campaign(campaign, bid_request):
            bid_id = str(uuid4())

            tracking_adm = campaign.adm + generate_tracking_pixel(campaign.id)

            bid = {
                "id": bid_id,
                "impid": imp_id,
                "price": campaign.price,
                "adm": tracking_adm,
                "crid": campaign.crid
            }

            response = {
                "id": request_id,
                "seatbid": [{"bid": [bid]}],
                "bidid": str(uuid4())
            }

            log_event(BID_LOG_PATH, "bid", campaign.id, {
                "req_id": request_id,
                "bid_id": bid_id,
                "price": campaign.price
            })

            return response

    return {"id": request_id, "seatbid": []}  # no bid

@router.post("/openrtb3/bid")
async def handle_bid_openrtb3(request: Request):
    payload = await request.json()
    openrtb = payload.get("openrtb", {})
    context = openrtb.get("context", {})
    request_obj = openrtb.get("request", {})

    request_id = payload.get("id")
    imp = request_obj.get("imp", [{}])[0]
    imp_id = imp.get("id", "1")

    simplified_request = {
        "id": request_id,
        "imp": request_obj.get("imp", []),
        "user": context.get("user", {}),
        "site": context.get("site", {}),
        "app": context.get("app", {}),
        "device": context.get("device", {}),
    }

    campaigns = fetch_active_campaigns()  # dict
    for campaign in campaigns.values():
        if not campaign.is_active or has_exceeded_caps(campaign):
            continue
        if match_campaign(campaign, simplified_request):
            bid_id = str(uuid4())

            tracking_adm = campaign.adm + generate_tracking_pixel(campaign.id)

            bid = {
                "id": bid_id,
                "impid": imp_id,
                "price": campaign.price,
                "adm": tracking_adm,
                "crid": campaign.crid
            }

            response = {
                "id": request_id,
                "seatbid": [{"bid": [bid]}],
                "bidid": str(uuid4())
            }

            log_event(BID_LOG_PATH, "bid", campaign.id, {
                "req_id": request_id,
                "bid_id": bid_id,
                "price": campaign.price,
                "openrtb_version": "3.0"
            })

            return response

    return {"id": request_id, "seatbid": []}
