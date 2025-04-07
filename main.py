import json
import requests
import time
import os

# إعدادات التليجرام
BOT_TOKEN = "توكن البوت"
CHAT_ID = "معرف القروب أو القناة"
JSON_URL = "https://raw.githubusercontent.com/herozero-ai/daily-signals/main/herozero.json"

# تحميل التوصيات من GitHub
def load_recommendations():
    response = requests.get(JSON_URL)
    return response.json()

# تنسيق الصفقة بلون مناسب
def format_recommendation(index, item):
    emoji = "🟢" if item["type"].lower() == "call" else "🔴"
    header = f"🔥 صفقة عالية الجودة – {item['symbol']} 🔥" if item.get("vip") else f"📢 التوصية {index+1}"
    return f"""{header} – {item['symbol']} – {emoji} {item['type']}
- العقد: {item['contract']}
- شرط الدخول: {item['entry_condition']}
- الدخول: {item['entry']}
- الهدف: {item['target1']} ثم {item['target2']}
- وقف الخسارة: {item['stop']}
- السبب: {item['reason']}"""

# إرسال رسالة إلى تليجرام
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=data)

# الفلترة والإرسال
def process_recommendations():
    data = load_recommendations()
    for i, rec in enumerate(data):
        try:
            entry_price = float(rec["entry"])
            if entry_price > 2.5:
                continue  # تجاهل العقود الغالية
            message = format_recommendation(i, rec)
            send_message(message)
            time.sleep(2)
        except Exception as e:
            print(f"خطأ في التوصية {i}: {e}")

# بدء التنفيذ
if __name__ == "__main__":
    process_recommendations()
