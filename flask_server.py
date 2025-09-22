import os
import logging
from flask import Flask, send_from_directory, render_template_string, abort, url_for, request
from pathlib import Path
from werkzeug.exceptions import NotFound

logger = logging.getLogger(__name__)

try:
    import config as settings
except ImportError:
    logger.error("config.py bulunamadı. Varsayılan ayarlar kullanılıyor.")
    settings = type('obj', (object,), {
        'SAVE_DIR': 'saved_images',
        'FLASK_HOST': '0.0.0.0',
        'FLASK_PORT': 9999,
        'FLASK_DEBUG': True
    })()

app = Flask(__name__)
IMAGE_DIR = Path(settings.SAVE_DIR).resolve()
if not IMAGE_DIR.is_dir():
    logger.warning(f"Görsel dizini bulunamadı: {IMAGE_DIR}")

INDEX_HTML = """
<!doctype html>
<html>
<head>
    <title>Kaydedilmiş NASA Görselleri</title>
    <style>
        body { font-family: sans-serif; margin: 2em; }
        ul { list-style: none; padding: 0; }
        li { margin-bottom: 1em; border-bottom: 1px solid #eee; padding-bottom: 1em; }
        a { text-decoration: none; color: #007bff; }
        a:hover { text-decoration: underline; }
        img { max-width: 150px; max-height: 100px; vertical-align: middle; margin-right: 1em; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>Kaydedilmiş NASA Görselleri</h1>
    {% if images %}
        <p>{{ images|length }} adet görsel bulundu:</p>
        <ul>
            {% for image in images %}
            <li>
                <a href="{{ url_for('serve_image', filename=image) }}" target="_blank">
                    <img src="{{ url_for('serve_image', filename=image) }}" alt="{{ image }}" loading="lazy">
                    {{ image }}
                </a>
            </li>
            {% endfor %}
        </ul>
    {% else %}
        <p>Dizin içinde görsel bulunamadı.</p>
    {% endif %}
    <p><small>Flask sunucusu çalışıyor.</small></p>
</body>
</html>
"""

@app.route('/images/<path:filename>')
def serve_image(filename: str):
    try:
        return send_from_directory(IMAGE_DIR, filename)
    except NotFound:
        logger.warning(f"Dosya bulunamadı: {filename}")
        abort(404, description="Kaynak bulunamadı.")

@app.route('/')
def index():
    image_files = []
    if IMAGE_DIR.is_dir():
        allowed = {".jpg", ".jpeg", ".png", ".gif"}
        image_files = sorted([f.name for f in IMAGE_DIR.iterdir() if f.is_file() and f.suffix.lower() in allowed])
        logger.info(f"{len(image_files)} görsel bulundu.")
    return render_template_string(INDEX_HTML, images=image_files)

@app.errorhandler(404)
def page_not_found(e):
    return render_template_string("""
        <!doctype html>
        <html>
        <head><title>404 Bulunamadı</title></head>
        <body><h1>404 - Sayfa Bulunamadı</h1>
        <p>Aradığınız kaynak bulunamadı.</p>
        <p><a href="{{ url_for('index') }}">Ana Sayfa</a></p>
        </body></html>
    """), 404

if __name__ == "__main__":
    host = settings.FLASK_HOST
    port = settings.FLASK_PORT
    debug_mode = settings.FLASK_DEBUG
    logger.info(f"Flask sunucusu başlatılıyor: http://{host}:{port}")
    app.run(host=host, port=port, debug=debug_mode)
