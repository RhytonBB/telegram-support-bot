import os
from dotenv import load_dotenv
from pathlib import Path

# Загрузить переменные из .env
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback_secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///executors.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
