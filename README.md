# 🚀 APOD Automator

_For an English version, see [README_EN.md](README_EN.md)._

**APOD Automator**, NASA'nın _Astronomy Picture of the Day_ (APOD) API'sini kullanarak günlük görseli indirir, optimize eder ve çeşitli yöntemlerle paylaşır:

- 💌 E‑posta
- 📱 Pushover bildirimi
- 📁 SMB paylaşımlı klasör
- 🌐 Flask ile web üzerinden yayın

---

## ✨ Özellikler

- ✅ NASA APOD verisinin günlük olarak çekilmesi  
- ✅ Görsellerin yerel dosya sistemine kaydedilmesi  
- ✅ Yeniden boyutlandırma ve sıkıştırma ile optimizasyon  
- ✅ SMB paylaşımına otomatik kopyalama  
- ✅ Flask web arayüzü ile görsellerin tarayıcıda görüntülenmesi  
- ✅ E‑posta ve Pushover ile bildirim gönderimi

---

## ⚙️ Kurulum

1. Repository'yi klonla:
   ```bash
   git clone git@github.com:husodrn46/APOD-Automator.git
   cd APOD-Automator
   ```

2. Ortam değişkenleri için `.env` dosyası oluştur:
   ```bash
   cp .env.example .env
   ```
   Ardından `.env` dosyasını kendi bilgilerinle doldur.

3. Gerekli bağımlılıkları yükle:
   ```bash
   pip install -r requirements.txt
   ```

4. Uygulamayı başlat:
   ```bash
   python main.py
   ```

---

## 🧪 Kullanım

- `main.py`: Ana iş akışını başlatır (veri al, görsel indir, optimize et, paylaş).
- `flask_server.py`: Flask sunucusunu başlatır.
   ```bash
   python flask_server.py
   ```
   Ardından tarayıcında `http://localhost:9999` adresine gidebilirsin.

---

## 🛠 Ortam Değişkenleri (.env)

Projeyi çalıştırmak için aşağıdaki ortam değişkenlerini `.env` dosyasında tanımlamalısın.  
Örnek dosya için bkz: `.env.example`

| Değişken | Açıklama |
|----------|----------|
| `NASA_API_KEY` | NASA Developer API anahtarın |
| `EMAIL_FROM`, `EMAIL_TO` | E‑posta gönderici ve alıcı adresleri |
| `EMAIL_PASSWORD` | Gönderici e‑posta şifresi |
| `SMTP_SERVER`, `SMTP_PORT` | SMTP sunucu ayarları |
| `PUSHOVER_USER_KEY`, `PUSHOVER_APP_TOKEN` | Pushover API bilgileri |
| `SMB_PATH`, `SMB_USER`, `SMB_PASSWORD` | SMB paylaşımı için bilgiler |
| `SMB_MOUNT_POINT` | Raspberry Pi'de mount edilen yol |
| `SAVE_DIR` | Görsellerin kaydedileceği klasör |
| `LOG_LEVEL` | Uygulama log seviyesi (örn: INFO) |
| `DELETE_ORIGINAL_AFTER_PROCESSING` | Orijinal dosya silinsin mi? (True/False)

---

## 🧾 Lisans

MIT Lisansı — detaylar için [LICENSE](LICENSE) dosyasına göz atabilirsin.

---

## 🤖 Not

Bu proje, [ChatGPT](https://openai.com/chatgpt) yardımıyla planlandı ve geliştirildi.  
Fikir, yazım, yapılandırma ve dökümantasyon aşamalarında destek alınmıştır.

