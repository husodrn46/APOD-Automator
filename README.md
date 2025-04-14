# APOD Automator

APOD Automator, NASA'nın *Astronomy Picture of the Day* (APOD) API'sini kullanarak günlük görseli indirir, optimize eder ve çeşitli bildirim mekanizmaları (e‑posta, Pushover, SMB) aracılığıyla paylaşır.

## Özellikler
- APOD verisinin otomatik çekilmesi
- Görselin indirilip kaydedilmesi
- Görsel optimizasyonu (yeniden boyutlandırma & sıkıştırma)
- Flask tabanlı basit web arayüzü
- E‑posta ve Pushover bildirimleri
- SMB paylaşımına otomatik kopyalama

## Kurulum
```bash
pip install -r requirements.txt
cp .env.example .env   # Ortam değişkenlerini doldur
python src/main.py
```

## Katkı
Katkıda bulunmak isterseniz lütfen [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını inceleyin.

## Lisans
MIT — detaylar için [LICENSE](LICENSE) dosyasına bakın.
