import os
import re
import requests
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import mimetypes

try:
    import config as settings
except ImportError:
    logging.error("config.py bulunamadı. Varsayılan ayarlar kullanılıyor.")
    settings = type('obj', (object,), {'API_KEY': 'DEMO_KEY', 'SAVE_DIR': 'images'})()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def sanitize_filename(filename: str) -> str:
    """
    Dosya isminden geçersiz karakterleri çıkarır.
    """
    sanitized = re.sub(r'[\\/*?:"<>|]', "_", filename)
    reserved_names = {"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", 
                      "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", 
                      "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"}
    if Path(sanitized).stem.upper() in reserved_names:
        sanitized = "_" + sanitized
    if len(sanitized) > 200:
        name, ext = os.path.splitext(sanitized)
        sanitized = name[:200 - len(ext)] + ext
    return sanitized


def get_image_extension(url: str, response_headers: Dict[str, str]) -> str:
    """
    URL veya Content-Type'dan uygun dosya uzantısını belirler.
    """
    content_type = response_headers.get('Content-Type')
    if content_type:
        ext = mimetypes.guess_extension(content_type)
        if ext:
            return ".jpeg" if ext == ".jpe" else ext

    try:
        ext = Path(url).suffix.lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            return ext
    except Exception:
        pass

    logging.warning(f"Dosya uzantısı belirlenemedi, varsayılan '.jpg' kullanılıyor. URL: {url}")
    return ".jpg"


def fetch_apod() -> Optional[Dict[str, Any]]:
    """
    NASA APOD API'sinden günlük veriyi döner.
    """
    if not settings.API_KEY or settings.API_KEY == 'DEMO_KEY':
        logging.warning("NASA API_KEY ayarlanmadı veya DEMO_KEY kullanılıyor.")

    url = f"https://api.nasa.gov/planetary/apod?api_key={settings.API_KEY}"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        logging.info("APOD verisi alındı.")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"APOD API hatası: {e}")
        return None
    except Exception as e:
        logging.error(f"Beklenmedik hata: {e}")
        return None


def save_image(data: Dict[str, Any]) -> Optional[str]:
    """
    APOD verisinden görseli indirip kaydeder.
    """
    if not data:
        logging.error("APOD verisi boş.")
        return None

    image_url = data.get("hdurl") or data.get("url")
    if not image_url:
        logging.error("Geçerli görsel URL'si bulunamadı.")
        return None

    title = data.get("title", "apod_image")
    try:
        logging.info(f"Görsel indiriliyor: {image_url}")
        image_response = requests.get(image_url, timeout=60)
        image_response.raise_for_status()
        date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
        base_filename = f"{date_str}_{title}"
        sanitized_base = sanitize_filename(base_filename)
        extension = get_image_extension(image_url, image_response.headers)
        file_name = f"{sanitized_base}{extension}"
        save_dir = Path(settings.SAVE_DIR)
        save_dir.mkdir(parents=True, exist_ok=True)
        file_path = save_dir / file_name
        logging.info(f"Görsel kaydediliyor: {file_path}")
        with open(file_path, "wb") as file:
            file.write(image_response.content)
        logging.info("Görsel başarılı kaydedildi.")
        return str(file_path)
    except requests.RequestException as e:
        logging.error(f"Görsel indirirken hata: {e}")
        return None
    except IOError as e:
        logging.error(f"Dosya yazma hatası ({file_path}): {e}")
        return None
    except Exception as e:
        logging.error(f"Beklenmedik hata: {e}")
        return None


if __name__ == "__main__":
    logging.info("NASA APOD İndirici Başlatıldı...")
    apod_data = fetch_apod()
    if apod_data:
        logging.info(f"Başlık: {apod_data.get('title', 'N/A')}")
        if apod_data.get("media_type") == "image":
            saved_path = save_image(apod_data)
            if saved_path:
                print(f"Görsel kaydedildi: {saved_path}")
            else:
                print("Görsel kaydedilemedi.")
        else:
            print(f"Medya türü 'image' değil. Video: {apod_data.get('url')}")
    else:
        print("APOD verisi alınamadı.")
