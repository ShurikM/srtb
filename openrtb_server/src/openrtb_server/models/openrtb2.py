from pydantic import BaseModel
from typing import List, Optional

class Banner(BaseModel):
    w: int
    h: int

class Imp(BaseModel):
    id: str
    banner: Banner

class Site(BaseModel):
    id: str
    domain: str

class Device(BaseModel):
    ua: str
    ip: str

class User(BaseModel):
    id: str

class OpenRTB2Request(BaseModel):
    id: str
    imp: List[Imp]
    site: Site
    device: Device
    user: User
