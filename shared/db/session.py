from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator, List
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from shared.schemas import CampaignRead
from shared.config import DATABASE_URL


# Load variables from .env.dev file
load_dotenv()
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env.dev file.")


def get_db() -> Generator[Session, None, None]:
    """
    Yields a database session. If IS_FAKE_DB is enabled, returns fake campaign data.
    """
    IS_FAKE_DB = os.getenv("IS_FAKE_DB", "").lower() in ("1", "true", "yes")
    if IS_FAKE_DB:
        # create dummy campaign data according to the CampaignRead schema
        now = datetime.utcnow()
        dummy_data: List[CampaignRead] = [
            CampaignRead(
                id="demo1",
                name="Demo Campaign",
                domain="demo.com",
                price=1.50,
                crid="demo-crid-001",
                adm="<ad-markup>",
                click_url="https://demo.com/click",
                budget=10000,
                bid_floor=0.5,
                impression_limit=100000,
                targeting_rules={"geo": "US", "device": "mobile"},
                daily_cap=10000,
                hourly_cap=1000,
                start_time=now - timedelta(days=2),
                end_time=now + timedelta(days=5),
                is_active=True
            ),
            CampaignRead(
                id="demo2",
                name="Testing Campaign",
                domain="test.com",
                price=2.25,
                crid="test-crid-002",
                adm="<ad-markup-test>",
                click_url="https://test.com/click",
                budget=5000,
                bid_floor=1.0,
                impression_limit=50000,
                targeting_rules={"geo": "EU", "device": "desktop"},
                daily_cap=5000,
                hourly_cap=500,
                start_time=now - timedelta(days=10),
                end_time=now - timedelta(days=1),
                is_active=False
            )
        ]

        class FakeQuery:
            def __init__(self, data: List[CampaignRead]):
                self._data = data
                self._offset = 0
                self._limit = len(data)

            def offset(self, skip: int):
                self._offset = skip
                return self

            def limit(self, limit: int):
                self._limit = limit
                return self

            def all(self) -> List[CampaignRead]:
                return self._data[self._offset : self._offset + self._limit]

        class FakeSession:
            def query(self, model):  # pylint: disable=unused-argument
                return FakeQuery(dummy_data)
            def add(self, obj): pass
            def commit(self): pass
            def refresh(self, obj): return obj
            def delete(self, obj): pass

        yield FakeSession()
        return

    # Only create engine and session when using the real database
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
