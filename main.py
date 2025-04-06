import json
import requests
import time

# إعدادات البوت
BOT_TOKEN = "توكن البوت هنا"
CHANNEL_ID = "@اسم_القناة_او_القروب"

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=data)

def load_recommendations():
    with open("herozero.json", "r", encoding="utf-8") as f:
        return json.load(f).get("recommendations", [])

def send_recommendations():
    recommendations = load_recommendations()
    for i, rec in enumerate(recommendations):
        msg = f"""التوصية {i+1}: {rec['symbol']} – صفقة {rec['type']}
- العقد: {rec['contract']}
- شرط الدخول: {rec['entry_condition']}
- الدخول: {rec['entry']}
- الهدف: {rec['targets'][0]} ثم {rec['targets'][1]}
- وقف الخسارة: {rec['stop_loss']}
- السبب: {rec['reason']}
"""
        send_to_telegram(msg)
        time.sleep(2)

while True:
    send_recommendations()
    time.sleep(60)
