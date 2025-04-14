import shutil
import os
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

try:
    import config as settings
except ImportError:
    logging.error("config.py bulunamadı. Varsayılan ayarlar kullanılıyor.")
    settings = type('obj', (object,), {'SMB_MOUNT_POINT': '/mnt/windows_share'})()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_to_smb(image_path: str) -> Optional[str]:
    """
    Görseli önceden mount edilmiş SMB paylaşımına kopyalar.
    """
    source_path = Path(image_path)
    mount_point = Path(settings.SMB_MOUNT_POINT)

    if not source_path.is_file():
        logging.error(f"Kaynak dosya bulunamadı: {source_path}")
        return None

    if not mount_point.exists() or not mount_point.is_dir():
        logging.error(f"SMB mount noktası hatalı: {mount_point}")
        return None

    if os.name == 'posix' and not os.path.ismount(str(mount_point)):
        logging.error(f"SMB paylaşımı mount edilmemiş: {mount_point}")
        return None
    if not os.access(str(mount_point), os.W_OK):
        logging.error(f"Yazma izni yok: {mount_point}")
        return None

    destination_path = mount_point / source_path.name
    try:
        logging.info(f"Kopyalama: {source_path.name} -> {destination_path}")
        shutil.copy(source_path, destination_path)
        logging.info(f"Kopyalama başarılı: {destination_path}")
        return str(destination_path)
    except Exception as e:
        logging.error(f"Kopyalama hatası: {e}", exc_info=True)
        return None

if __name__ == "__main__":
    print("SMB Kaydedici Testi Başlatıldı...")
    logging.info(f"SMB mount noktası: {settings.SMB_MOUNT_POINT}")
    test_dir = Path("test_smb_source")
    test_dir.mkdir(exist_ok=True)
    test_file = test_dir / "test_smb_image.txt"
    with open(test_file, "w") as f:
        f.write(f"Test dosyası. Timestamp: {datetime.now()}")
    if not Path(settings.SMB_MOUNT_POINT).exists():
        print(f"UYARI: SMB mount noktası bulunamadı: {settings.SMB_MOUNT_POINT}")
    else:
        copied = save_to_smb(str(test_file))
        if copied:
            print(f"Dosya kopyalandı: {copied}")
        else:
            print("Dosya kopyalanamadı.")
