from fastapi import APIRouter, Request, HTTPException
from pydantic import ValidationError
from openrtb_server.models.openrtb2 import OpenRTB2Request
from openrtb_server.models.openrtb3 import OpenRTB3Request
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/bid")
async def handle_bid(request: Request):
    body = await request.json()

    try:
        if "openrtb" in body:
            data = OpenRTB3Request(**body["openrtb"])
            version = "3.0"
        else:
            data = OpenRTB2Request(**body)
            version = "2.x"
    except ValidationError as e:
        logger.warning(f"Invalid OpenRTB {version} request: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid OpenRTB {version} request: {e}")

    logger.info(f"Received valid OpenRTB {version} request: {body}")

    # Hardcoded response
    return {
        "id": body.get("id", "test123"),
        "seatbid": [
            {
                "bid": [
                    {
                        "id": "1",
                        "impid": "imp1",
                        "price": 0.5,
                        "adm": "<!-- Sample Creative -->",
                        "crid": "creative-123"
                    }
                ]
            }
        ],
        "bidid": "bid-123"
    }
