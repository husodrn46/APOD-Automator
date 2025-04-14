import os
from dotenv import load_dotenv
from pathlib import Path

current_dir = Path(__file__).parent
env_path = current_dir / '.env'
load_dotenv(dotenv_path=env_path)

# NASA API
API_KEY = os.environ.get("NASA_API_KEY")

# Pushover Ayarları
PUSHOVER_USER_KEY = os.environ.get("PUSHOVER_USER_KEY")
PUSHOVER_APP_TOKEN = os.environ.get("PUSHOVER_APP_TOKEN")

# Görsel Kaydetme
_save_dir_str = os.environ.get("SAVE_DIR", "./saved_images")
SAVE_DIR = str(Path(_save_dir_str).resolve())

# SMB/Windows Ayarları
SMB_USER = os.environ.get("SMB_USER")
SMB_PASSWORD = os.environ.get("SMB_PASSWORD")
SMB_PATH = os.environ.get("SMB_PATH")
SMB_MOUNT_POINT = os.environ.get("SMB_MOUNT_POINT", "/mnt/windows_share")

# E-posta Ayarları
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
try:
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
except ValueError:
    SMTP_PORT = 587
EMAIL_FROM = os.environ.get("EMAIL_FROM")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_TO = os.environ.get("EMAIL_TO")

# Flask Ayarları
FLASK_HOST = os.environ.get("FLASK_HOST", "127.0.0.1")
try:
    FLASK_PORT = int(os.environ.get("FLASK_PORT", "9999"))
except ValueError:
    FLASK_PORT = 9999
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() == 'true'

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
DELETE_ORIGINAL_AFTER_PROCESSING = os.environ.get("DELETE_ORIGINAL_AFTER_PROCESSING", "False").lower() == 'true'

# Kritik değişkenlerin kontrolü (opsiyonel)
REQUIRED_VARS = [
    "NASA_API_KEY", "PUSHOVER_USER_KEY", "PUSHOVER_APP_TOKEN",
    "EMAIL_FROM", "EMAIL_PASSWORD", "EMAIL_TO"
]
missing_vars = [var for var in REQUIRED_VARS if not globals().get(var)]
if missing_vars:
    print(f"UYARI: Aşağıdaki ortam değişkenleri eksik: {', '.join(missing_vars)}")
