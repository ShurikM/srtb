
import os
from dotenv import load_dotenv

load_dotenv()

RTB_HOST = os.getenv("RTB_HOST", "http://localhost:8000")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")
IS_FAKE_DB = bool(os.getenv("IS_FAKE_DB"))