import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from typing import Optional, List, Union
import socket

logger = logging.getLogger(__name__)

try:
    import config as settings
except ImportError:
    logger.error("config.py bulunamadı. Varsayılan ayarlar kullanılıyor.")
    settings = type('obj', (object,), {
        'EMAIL_FROM': 'default@example.com',
        'EMAIL_TO': 'recipient@example.com',
        'EMAIL_PASSWORD': 'DEFAULT_PASSWORD',
        'SMTP_SERVER': 'smtp.example.com',
        'SMTP_PORT': 587
    })()


def send_email_with_image(
    image_path: str,
    subject: str,
    body: str,
    recipient: Optional[Union[str, List[str]]] = None,
    sender: Optional[str] = None
) -> bool:
    """
    Belirtilen e-posta bilgileriyle, ek olarak görsel içeren e-posta gönderir.
    """
    actual_sender = sender or settings.EMAIL_FROM
    actual_recipient = recipient or settings.EMAIL_TO
    smtp_password = settings.EMAIL_PASSWORD

    if isinstance(actual_recipient, list):
        recipient_header = ", ".join(actual_recipient)
        recipient_list = actual_recipient
    else:
        recipient_header = actual_recipient
        recipient_list = [actual_recipient]

    if not os.path.exists(image_path) or not os.path.isfile(image_path):
        logger.error(f"Görsel dosyası bulunamadı: {image_path}")
        return False

    msg = MIMEMultipart()
    msg['From'] = actual_sender
    msg['To'] = recipient_header
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with open(image_path, 'rb') as img_file:
            img = MIMEImage(img_file.read())
            img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
            msg.attach(img)
    except Exception as e:
        logger.error(f"Görsel eklenecek dosya okunamadı: {e}")
        return False

    try:
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(actual_sender, smtp_password)
            server.sendmail(actual_sender, recipient_list, msg.as_string())
            logger.info(f"E-posta gönderildi: {recipient_header}")
            return True
    except (smtplib.SMTPAuthenticationError, smtplib.SMTPConnectError,
            smtplib.SMTPSenderRefused, smtplib.SMTPRecipientsRefused,
            smtplib.SMTPDataError, socket.gaierror, TimeoutError) as e:
        logger.error(f"SMTP hatası: {e}")
        return False
    except Exception as e:
        logger.error(f"E-posta gönderiminde beklenmedik hata: {e}")
        return False


if __name__ == "__main__":
    test_image_path = "test_image.png"
    if not os.path.exists(test_image_path):
        with open(test_image_path, "w") as f:
            f.write("test")
        print(f"Geçici test dosyası oluşturuldu: {test_image_path}")

    print(f"Test e-postası {settings.EMAIL_TO} adresine gönderiliyor...")
    success = send_email_with_image(
        image_path=test_image_path,
        subject="Test E-postası (Python)",
        body="Test mesajı. Görsel ekli."
    )
    print("E-posta gönderildi." if success else "E-posta gönderilemedi.")
