# scripts/utils.py
import requests
import json
import os

# Lokasi config.json
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "../config/config.json")

if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError("File config.json tidak ditemukan. Silakan buat dulu di folder config.")

# Baca config
with open(CONFIG_PATH) as f:
    config = json.load(f)

BOT_TOKEN = config["telegram_token"]
CHAT_ID = config["telegram_chat_id"]

def send_telegram(message: str):
    """
    Kirim pesan Telegram.
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, json=payload)

    if response.ok:
        print("✅ Pesan Telegram berhasil dikirim.")
    else:
        print("❌ Gagal kirim Telegram:", response.text)

    return response
