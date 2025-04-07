import json
import requests
import time

# إعدادات البوت
BOT_TOKEN = "توكن البوت هنا"
CHAT_ID = "آي دي القروب أو القناة"
DATA_URL = "https://raw.githubusercontent.com/Ahmedaldar303/herozero-signals/main/herozero.json"

# دالة تحميل ملف التوصيات
def load_recommendations():
    response = requests.get(DATA_URL)
    return response.json()

# تنسيق رسالة التوصية
def format_recommendation(index, item):
    emoji = "🟢" if item['type'].lower() == "call" else "🔴"
    return f"""📢 التوصية {index + 1} – {item['symbol']} – {emoji} **{item['type']}**
- العقد: {item['contract']}
- شرط الدخول: {item.get('entry_condition', '—')}
- الدخول: {item['entry']}
- الهدف: {item['targets'][0]} ثم {item['targets'][1]}
- وقف الخسارة: {item['stop_loss']}
- السبب: {item['reason']}"""

# تنسيق رسالة عالية الجودة
def format_high_priority(item):
    emoji = "🟢" if item['type'].lower() == "call" else "🔴"
    return f"""🔥 **صفقة عالية الجودة – {item['symbol']}** 🔥
{emoji} **{item['type']}**
📆 العقد: {item['contract']}
📈 الدخول: {item['entry']} | 🎯 الأهداف: {item['targets'][0]} → {item['targets'][1]}
🛑 وقف الخسارة: {item['stop_loss']}
⚡️ السبب: {item['reason']}"""

# إرسال الرسالة لتلقرام
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

# التشغيل
def main():
    data = load_recommendations()

    # توصيات عادية
    for idx, rec in enumerate(data.get("recommendations", [])):
        msg = format_recommendation(idx, rec)
        send_message(msg)
        time.sleep(1)  # عشان ما تتكرر بسرعة

    # توصيات عالية الجودة
    for rec in data.get("high_priority", []):
        msg = format_high_priority(rec)
        send_message(msg)
        time.sleep(1)

if __name__ == "__main__":
    main()
