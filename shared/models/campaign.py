from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON
from shared.db.base import Base
import datetime

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    domain = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    crid = Column(String, nullable=False)
    adm = Column(String, nullable=False)
    click_url = Column(String, nullable=True)

    budget = Column(Float, nullable=True)
    bid_floor = Column(Float, nullable=True)
    impression_limit = Column(Integer, nullable=True)
    targeting_rules = Column(JSON, nullable=True)  # Flexible: geo, device, time, etc.

    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

    is_active = Column(Boolean, default=True)
