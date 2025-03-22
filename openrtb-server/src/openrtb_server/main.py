from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Impression(BaseModel):
    id: str

class BidRequest(BaseModel):
    id: str
    imp: List[Impression]

@app.post("/bid")
async def bid(request: Request, bid_request: BidRequest):
    print("Received bid request:", bid_request.dict())

    response = {
        "id": bid_request.id,
        "seatbid": [
            {
                "bid": [
                    {
                        "id": "1",
                        "impid": bid_request.imp[0].id,
                        "price": 0.5,
                        "adm": "<!-- Sample Creative -->",
                        "crid": "creative-123"
                    }
                ]
            }
        ],
        "bidid": "bid-123"
    }
    return response
