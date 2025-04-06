import json
import requests
import time
import os

# إعدادات البوت
BOT_TOKEN = "7734197510:AAHHHUCO2g0YLfQfoCxNWEJgcUk1nZasC_M"
CHANNEL_ID = "@anythingtestus"
SENT_FILE = "sent.json"

# إرسال رسالة إلى تيليجرام
def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=data)

# تحميل التوصيات من herozero.json
def load_recommendations():
    with open("herozero.json", "r", encoding="utf-8") as f:
        return json.load(f).get("recommendations", [])

# توليد معرف فريد للتوصية (السهم + العقد)
def get_unique_id(item):
    return f"{item['symbol']}_{item['contract']}"

# تحميل التوصيات المُرسلة سابقًا
def load_sent():
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))

# حفظ التوصيات المُرسلة
def save_sent(sent_ids):
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        json.dump(list(sent_ids), f, ensure_ascii=False, indent=2)

# إرسال التوصيات الجديدة فقط
def send_recommendations():
    recommendations = load_recommendations()
    sent_ids = load_sent()

    for i, rec in enumerate(recommendations):
        rec_id = get_unique_id(rec)
        if rec_id not in sent_ids:
            msg = f"""التوصية {i+1}: {rec['symbol']} – صفقة {rec['type']}
- العقد: {rec['contract']}
- شرط الدخول: {rec['entry_condition']}
- الدخول: {rec['entry']}
- الهدف: {rec['targets'][0]} ثم {rec['targets'][1]}
- وقف الخسارة: {rec['stop_loss']}
- السبب: {rec['reason']}
"""
            send_to_telegram(msg)
            sent_ids.add(rec_id)
            time.sleep(2)

    save_sent(sent_ids)

# تكرار الإرسال كل دقيقة
while True:
    send_recommendations()
    time.sleep(60)
