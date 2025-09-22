# 🚀 APOD Automator

**APOD Automator** downloads the daily image from NASA's _Astronomy Picture of the Day_ (APOD) API, optimizes it, and shares it in multiple ways:

- 📱 Pushover notification
- 📁 SMB shared folder
- 🌐 Serve via Flask web interface

---

## ✨ Features

- ✅ Fetches NASA APOD data on a daily basis
- ✅ Saves images to the local file system
- ✅ Optimizes them by resizing and compressing
- ✅ Automatically copies to an SMB share
- ✅ Offers a Flask web interface to view images in the browser
- ✅ Sends notifications via Pushover

---

## ⚙️ Setup

1. Clone the repository:
   ```bash
   git clone git@github.com:husodrn46/APOD-Automator.git
   cd APOD-Automator
   ```

2. Create an `.env` file for environment variables:
   ```bash
   cp .env.example .env
   ```
   Then fill in your own values in `.env`.

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the application:
   ```bash
   python main.py
   ```

---

## 🧪 Usage

- `main.py`: Starts the main workflow (fetch data, download, optimize and share).
- `flask_server.py`: Launches the Flask server.
   ```bash
   python flask_server.py
   ```
   Then navigate to `http://localhost:9999` in your browser.

---

## 🛠 Environment Variables (.env)

You need to set the following variables in your `.env` file.
See `.env.example` for a template.

| Variable | Description |
|----------|-------------|
| `NASA_API_KEY` | Your NASA Developer API key |
| `PUSHOVER_USER_KEY`, `PUSHOVER_APP_TOKEN` | Pushover API details |
| `SMB_PATH`, `SMB_USER`, `SMB_PASSWORD` | Credentials for the SMB share |
| `SMB_MOUNT_POINT` | Mount point on a Raspberry Pi |
| `SAVE_DIR` | Directory to save images |
| `LOG_LEVEL` | Application log level (e.g. INFO) |
| `DELETE_ORIGINAL_AFTER_PROCESSING` | Delete the original file after processing? (True/False)

> ℹ️ The email delivery feature has been removed; the application no longer opens SMTP connections.

---

## 🧾 License

This project is licensed under the MIT License—see [LICENSE](LICENSE) for details.

---

## 🤖 Note

This project was planned and developed with assistance from [ChatGPT](https://openai.com/chatgpt).
Support was received during the planning, writing, configuration, and documentation phases.
