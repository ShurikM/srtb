from pydantic import BaseModel
from typing import List, Optional

class Banner(BaseModel):
    w: int
    h: int

class Item(BaseModel):
    id: str
    banner: Optional[Banner]

class Site(BaseModel):
    id: str
    domain: str

class Context(BaseModel):
    site: Site

class Device(BaseModel):
    ua: str
    ip: str

class User(BaseModel):
    id: str

class RequestObject(BaseModel):
    id: str
    context: Context
    item: List[Item]
    device: Device
    user: User

class OpenRTB3Request(BaseModel):
    ver: str
    request: RequestObject
