import os
import logging
import sys


def _parse_log_level(level_value):
    """Convert different LOG_LEVEL representations into logging levels."""
    if isinstance(level_value, int):
        return level_value

    if isinstance(level_value, str):
        candidate = level_value.strip()
        if candidate.isdigit():
            return int(candidate)

        resolved = logging.getLevelName(candidate.upper())
        if isinstance(resolved, int):
            return resolved

    return None


_raw_log_level = os.environ.get("LOG_LEVEL", "INFO")
_log_format = '%(asctime)s - %(levelname)s - [%(module)s.%(funcName)s] - %(message)s'
_parsed_level = _parse_log_level(_raw_log_level)
_invalid_env_level = _parsed_level is None

if _invalid_env_level:
    _parsed_level = logging.INFO

if not logging.getLogger().handlers:
    logging.basicConfig(level=_parsed_level, format=_log_format)

logger = logging.getLogger(__name__)

if _invalid_env_level:
    logger.warning(
        f"Geçersiz LOG_LEVEL değeri '{_raw_log_level}'. Varsayılan INFO seviyesi kullanılacak."
    )

try:
    import config as settings
except ImportError as e:
    logger.error(f"config.py yüklenemedi: {e}. Bağımlılıkları kontrol edin.")
    sys.exit(1)

_settings_log_level = getattr(settings, "LOG_LEVEL", "INFO")
_settings_level = _parse_log_level(_settings_log_level)
if _settings_level is None:
    logger.warning(
        f"config.LOG_LEVEL değeri '{_settings_log_level}' geçersiz. INFO kullanılacak."
    )
    _settings_level = logging.INFO

logging.getLogger().setLevel(_settings_level)

try:
    import apod
    from image_optimizer import optimize_image
    from image_saver import save_to_smb
    from email_sender import send_email_with_image
    import pushover
except ImportError as e:
    logger.error(f"Gerekli modül bulunamadı: {e}. Bağımlılıkları kontrol edin.")
    sys.exit(1)

logger.info("="*20 + " İşlem Başlatıldı " + "="*20)


def main():
    logger.info("1. NASA APOD verisi çekiliyor...")
    apod_data = apod.fetch_apod()
    if not apod_data:
        logger.error("APOD verisi alınamadı.")
        sys.exit(1)

    media_type = apod_data.get("media_type")
    apod_title = apod_data.get("title", "Başlıksız APOD")
    logger.info(f"APOD: '{apod_title}' - Tür: {media_type}")

    if media_type != "image":
        logger.info("APOD görsel değil. İşlem sonlandırılıyor.")
        sys.exit(0)

    logger.info("2. Görsel indiriliyor...")
    original_image_path = apod.save_image(apod_data)
    if not original_image_path:
        logger.error("Görsel indirilemedi.")
        sys.exit(1)
    logger.info(f"Orijinal görsel: {original_image_path}")

    logger.info("3. Görsel optimize ediliyor...")
    optimized_output_dir = os.path.join(settings.SAVE_DIR, "optimized")
    optimized_image_path = optimize_image(original_image_path, output_dir=optimized_output_dir)
    if not optimized_image_path:
        logger.error("Görsel optimizasyonu başarısız.")
        sys.exit(1)
    logger.info(f"Optimizasyon tamam: {optimized_image_path}")

    logger.info("4. SMB paylaşımına kaydediliyor...")
    smb_image_path = save_to_smb(optimized_image_path)
    if not smb_image_path:
        logger.error("SMB kaydı başarısız.")
        sys.exit(1)
    logger.info(f"SMB kaydı tamam: {smb_image_path}")

    logger.info("5. Pushover bildirimi gönderiliyor...")
    try:
        pushover_success = pushover.send_pushover_notification(
            title=f"Yeni APOD: {apod_title}",
            message=apod_data.get('explanation', '')[:150] + "...",
            attachment_path=optimized_image_path
        )
        if pushover_success:
            logger.info("Pushover bildirimi gönderildi.")
        else:
            logger.warning("Pushover bildirimi başarısız.")
    except Exception as e:
        logger.error(f"Pushover bildirimi hatası: {e}", exc_info=True)

    logger.info("6. E-posta gönderiliyor...")
    email_success = send_email_with_image(
        image_path=optimized_image_path,
        subject=f"Günün NASA Fotoğrafı: {apod_title}",
        body=apod_data.get('explanation', 'Açıklama mevcut değil.')
    )
    if email_success:
        logger.info("E-posta gönderildi.")
    else:
        logger.warning("E-posta gönderimi başarısız.")

    if settings.DELETE_ORIGINAL_AFTER_PROCESSING and os.path.exists(original_image_path):
        try:
            logger.info(f"Orijinal görsel siliniyor: {original_image_path}")
            os.remove(original_image_path)
            logger.info("Orijinal görsel silindi.")
        except OSError as e:
            logger.error(f"Görsel silme hatası: {e}")

    logger.info("="*20 + " İşlem Tamamlandı " + "="*20)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Kritik hata: {e}", exc_info=True)
        sys.exit(1)
