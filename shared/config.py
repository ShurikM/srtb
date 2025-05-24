
import os
from pathlib import Path
from dotenv import load_dotenv

print("CONFIG DEBUG: __file__ =", __file__)
print("CONFIG DEBUG: ROOT_DIR =", Path(__file__).resolve().parents)

# Determine environment
env_name = os.getenv("ENV", "dev")

# Load .env.dev or .env.prod from project root
ROOT_DIR = Path(__file__).resolve().parents[1]  # ~/srtb
env_path = ROOT_DIR / f".env.{env_name}"
if not env_path.exists():
    raise FileNotFoundError(f"Could not find environment file: {env_path}")
load_dotenv(dotenv_path=env_path)

RTB_HOST = os.getenv("RTB_HOST", "http://localhost:8000")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")
IS_FAKE_DB = bool(os.getenv("IS_FAKE_DB"))
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")