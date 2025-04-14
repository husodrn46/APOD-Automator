import requests
import logging
import mimetypes
from pathlib import Path
from typing import Optional

try:
    import config as settings
    if not hasattr(settings, 'PUSHOVER_APP_TOKEN') or not hasattr(settings, 'PUSHOVER_USER_KEY'):
        raise ImportError("Pushover ayarları eksik.")
except ImportError as e:
    logging.basicConfig(level=logging.ERROR)
    logging.error(f"Pushover ayarları yüklenemedi: {e}")
    settings = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"

def send_pushover_notification(
    title: str,
    message: str,
    attachment_path: Optional[str] = None
) -> bool:
    """
    Pushover API'si ile bildirim gönderir. İsteğe bağlı ek dosya gönderilebilir.
    """
    if settings is None:
        logging.error("Pushover ayarları eksik; bildirim gönderilemiyor.")
        return False

    payload = {
        "token": settings.PUSHOVER_APP_TOKEN,
        "user": settings.PUSHOVER_USER_KEY,
        "title": title,
        "message": message
    }

    files_to_send = None
    file_handle = None

    try:
        if attachment_path:
            attachment_file = Path(attachment_path)
            if not attachment_file.is_file():
                logging.error(f"Pushover eki bulunamadı: {attachment_path}")
                return False

            file_size = attachment_file.stat().st_size
            if file_size > 2.6 * 1024 * 1024:
                logging.warning(f"Eki dosya boyutu limiti aşıyor: {attachment_path}")

            content_type, _ = mimetypes.guess_type(attachment_file.name)
            if not content_type:
                content_type = 'application/octet-stream'
                logging.warning(f"İçerik türü tahmin edilemedi; varsayılan '{content_type}' kullanılıyor.")

            file_handle = open(attachment_file, "rb")
            files_to_send = {"attachment": (attachment_file.name, file_handle, content_type)}

        response = requests.post(PUSHOVER_API_URL, data=payload, files=files_to_send, timeout=30)
        if response.status_code == 200 and response.json().get("status") == 1:
            logging.info("Pushover bildirimi gönderildi.")
            return True
        else:
            logging.error(f"Pushover API hatası: {response.text}")
            return False
    except Exception as e:
        logging.error(f"Pushover bildirimi hatası: {e}", exc_info=True)
        return False
    finally:
        if file_handle:
            file_handle.close()
            logging.debug("Ek dosyası kapatıldı.")

if __name__ == "__main__":
    print("Pushover Bildirim Testi Başlatıldı...")
    if settings is None:
        print("Pushover ayarları eksik; test atlanıyor.")
    else:
        success_text = send_pushover_notification(
            "Test Bildirimi (Python)",
            "Bu sadece metin içeren test mesajıdır."
        )
        print("Test bildirimi gönderildi." if success_text else "Test bildirimi başarısız.")
