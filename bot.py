import json
import os
import requests
import datetime

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
DATA_FILE = "herozero.json"
LOG_FILE = "last_sent.log"

def load_last_sent():
    if not os.path.exists(LOG_FILE):
        return None
    with open(LOG_FILE, "r") as file:
        return file.read().strip()

def save_last_sent(id_str):
    with open(LOG_FILE, "w") as file:
        file.write(id_str)

def format_message(t):
    return f"""🔻 التوصية 1: {t['ticker']} – صفقة {t['type']}
📅 العقد: *{t['contract']}*
📉 شرط الدخول: `{t['entry_condition']}`
🎯 الدخول: *{t['entry_price']}*
🎯 الهدف: *{t['target1']}* ثم *{t['target2']}*
⛔ وقف الخسارة: *{t['stop_loss']}*
🧠 السبب: `{t['reason']}`"""

def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def check_and_send():
    now = datetime.datetime.now()
    if now.hour == 15 and now.minute == 30:  # الساعة 3:30 مساءً بتوقيت السعودية
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                if data:
                    trade = data[0]
                    unique_id = f"{trade['ticker']}_{trade['contract']}"
                    last_sent = load_last_sent()
                    if unique_id != last_sent:
                        msg = format_message(trade)
                        send_telegram_message(msg)
                        save_last_sent(unique_id)

if __name__ == "__main__":
    while True:
        check_and_send()
        import time
        time.sleep(60)
