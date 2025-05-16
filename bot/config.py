import os
from dotenv import load_dotenv
from pathlib import Path

# Путь к корню проекта (на уровень выше папки bot)
BASE_DIR = Path(__file__).parent.parent

# Явно загружаем .env из корня проекта
load_dotenv(dotenv_path=BASE_DIR / ".env")

BOT_TOKEN = "7575046919:AAE8eD-KhEMfgBrkhFV_VTVhfxSkokb5_5A"
BASE_CHAT_URL = "https://lv4mmdhp-8000.uks1.devtunnels.ms/"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")