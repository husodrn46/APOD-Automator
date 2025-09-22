import os
import logging
from pathlib import Path
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

try:
    from PIL import Image, UnidentifiedImageError
except ImportError as e:
    logger.error(
        f"Pillow kütüphanesi yüklenemedi ({e}). Lütfen 'pip install Pillow' komutunu çalıştırın."
    )
    Image = None
    UnidentifiedImageError = None

DEFAULT_MAX_SIZE = (1920, 1080)
DEFAULT_QUALITY = 85

def optimize_image(
    image_path: str,
    output_dir: Optional[str] = None,
    max_size: Tuple[int, int] = DEFAULT_MAX_SIZE,
    quality: int = DEFAULT_QUALITY,
    suffix: str = "_optimized",
    output_format: str = "JPEG"
) -> Optional[str]:
    """
    Verilen görseli yeniden boyutlandırır ve optimize edilmiş halini kaydeder.
    """
    if Image is None:
        logger.error("Pillow yüklü değil.")
        return None

    input_path = Path(image_path)
    if not input_path.is_file():
        logger.error(f"Dosya bulunamadı: {image_path}")
        return None

    output_path_dir = Path(output_dir) if output_dir else input_path.parent
    try:
        output_path_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logger.error(f"Çıktı dizini oluşturulamadı: {e}")
        return None

    output_filename_base = f"{input_path.stem}{suffix}"
    output_extension = ".jpg" if output_format.upper() == "JPEG" else f".{output_format.lower()}"
    output_path = output_path_dir / f"{output_filename_base}{output_extension}"

    try:
        logger.info(f"Optimizasyon: {input_path.name} -> {output_path.name}")
        with Image.open(input_path) as img:
            original_size = img.size
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            logger.info(f"Boyut {original_size} -> {img.size}")
            save_options = {"optimize": True}
            save_format = output_format.upper()

            if save_format == 'JPEG':
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img_to_save = background
                else:
                    img_to_save = img
                save_options.update({"quality": quality, "progressive": True, "subsampling": 0})
            elif save_format == 'PNG':
                save_options["compress_level"] = 6
                img_to_save = img
            else:
                img_to_save = img

            img_to_save.save(output_path, format=save_format, **save_options)
            logger.info(f"Optimizasyon tamam: {output_path}")
            return str(output_path)
    except (FileNotFoundError, UnidentifiedImageError) as e:
        logger.error(f"Optimizasyon hatası: {e}")
        return None
    except Exception as e:
        logger.error(f"Beklenmedik hata: {e}", exc_info=True)
        return None

if __name__ == "__main__":
    print("Görsel Optimizasyon Testi Başlatıldı...")
    if Image is None:
        print("Pillow yüklü değil.")
    else:
        test_dir = Path("test_optimizer_images")
        test_dir.mkdir(exist_ok=True)
        test_image_path = test_dir / "test_image_large.jpg"
        optimized_dir = test_dir / "optimized"
        # Basit bir test görseli oluşturma (örneğin 2500x1500)
        img = Image.new('RGB', (2500, 1500), color=(100, 150, 200))
        img.save(test_image_path)
        optimized_path = optimize_image(str(test_image_path), output_dir=str(optimized_dir))
        if optimized_path:
            print(f"Optimize edilmiş dosya: {optimized_path}")
