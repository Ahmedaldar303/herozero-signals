import json
import requests
import time
import os

# إعدادات البوت
BOT_TOKEN = "7734197510:AAHHHUCO2g0YLfQfoCxNWEJgcUk1nZasC_M"
CHANNEL_ID = "@anythingtestus"
SENT_FILE = "sent.json"

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

def load_recommendations():
    with open("herozero.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("recommendations", []), data.get("high_priority", [])

def get_unique_id(item):
    return f"{item['symbol']}_{item['contract']}"

def load_sent():
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))

def save_sent(sent_ids):
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        json.dump(list(sent_ids), f, ensure_ascii=False, indent=2)

def format_recommendation(i, rec):
    type_icon = "🟢 *Call*" if rec["type"].lower() == "call" else "🔴 *Put*"
    return f"""📢 *التوصية {i+1}* – {rec['symbol']} – {type_icon}
- العقد: {rec['contract']}
- شرط الدخول: {rec['entry_condition']}
- الدخول: {rec['entry']}
- الهدف: {rec['targets'][0]} ثم {rec['targets'][1]}
- وقف الخسارة: {rec['stop_loss']}
- السبب: {rec['reason']}"""

def format_high_priority(rec):
    type_icon = "🟢 *Call*" if rec["type"].lower() == "call" else "🔴 *Put*"
    return f"""🔥 *صفقة عالية الجودة – {rec['symbol']}* 🔥
{type_icon}
📆 العقد: {rec['contract']}
📈 الدخول: {rec['entry']} | 🎯 الأهداف: {rec['targets'][0]} → {rec['targets'][1]}
🛑 وقف الخسارة: {rec['stop_loss']}
⚡️ السبب: {rec['reason']}"""

def send_recommendations():
    recommendations, high_priority = load_recommendations()
    sent_ids = load_sent()

    for i, rec in enumerate(recommendations):
        rec_id = get_unique_id(rec)
        if rec_id not in sent_ids:
            msg = format_recommendation(i, rec)
            send_to_telegram(msg)
            sent_ids.add(rec_id)
            time.sleep(2)

    for rec in high_priority:
        rec_id = get_unique_id(rec)
        if rec_id not in sent_ids:
            msg = format_high_priority(rec)
            send_to_telegram(msg)
            sent_ids.add(rec_id)
            time.sleep(2)

    save_sent(sent_ids)

while True:
    send_recommendations()
    time.sleep(60)
