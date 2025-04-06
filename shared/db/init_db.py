from db.session import engine
from db.base import Base

Base.metadata.create_all(bind=engine)
