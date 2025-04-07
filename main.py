"import json import requests import time import os import re

BOT_TOKEN = "7734197510:AAHHHUCO2g0YLfQfoCxNWEJgcUk1nZasC_M" CHANNEL_ID = "@anythingtestus" SENT_FILE = "sent.json" API_KEY = "cvp3ju1r01qihjtrv64gcvp3ju1r01qihjtrv650"

جلب السعر الحالي

def get_price(symbol): try: url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}" response = requests.get(url) data = response.json() return data.get("c", None) except: return None

استخراج Strike من اسم العقد

def extract_strike_price(contract): match = re.search(r'(\d+)([CP])$', contract) return float(match.group(1)) if match else None

إرسال تيليجرام

def send_to_telegram(text): url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage" data = { "chat_id": CHANNEL_ID, "text": text, "parse_mode": "Markdown" } requests.post(url, data=data)

تحميل التوصيات

def load_recommendations(): with open("herozero.json", "r", encoding="utf-8") as f: data = json.load(f) return data.get("recommendations", []), data.get("high_priority", [])

فلترة التوصيات بناءً على شرط الدخول وسعر العقد

def filter_recommendations(recommendations): filtered = [] for item in recommendations: current_price = get_price(item["symbol"]) item["current_price"] = current_price

# فلتر السعر: تجاهل إذا كان السعر أقل من 2.5
    if item.get("entry", 0) < 2.5:
        continue

    condition = item["entry_condition"]

    if "كسر دعم" in condition:
        try:
            level = float(condition.replace("كسر دعم", "").strip())
            if current_price and current_price < level:
                filtered.append(item)
        except:
            pass
    elif "كسر مقاومة" in condition:
        try:
            level = float(condition.replace("كسر مقاومة", "").strip())
            if current_price and current_price > level:
                filtered.append(item)
        except:
            pass
    elif "VWAP" in condition:
        filtered.append(item)
    else:
        filtered.append(item)
return filtered

توليد معرف فريد للتوصية

def get_unique_id(item): return f"{item['symbol']}_{item['contract']}"

إرسال التوصيات

def format_recommendation(i, rec): type_icon = "🟢 Call" if rec["type"].lower() == "call" else "🔴 Put" current_price = rec.get("current_price") strike_price = extract_strike_price(rec["contract"])

price_line = f"\n💵 السعر الحالي: {current_price}" if current_price else ""
warning = ""
if current_price and strike_price:
    distance = abs(strike_price - current_price)
    if distance / current_price > 1:
        warning = "\n⚠️ *تحذير: العقد بعيد جدًا عن السعر الحالي، تأكد من صحة البيانات.*"

return f"""📢 *التوصية {i+1}* – {rec['symbol']} – {type_icon}

العقد: {rec['contract']}

شرط الدخول: {rec['entry_condition']}

الدخول: {rec['entry']}

الهدف: {rec['targets'][0]} ثم {rec['targets'][1]}

وقف الخسارة: {rec['stop_loss']}

السبب: {rec['reason']}{price_line}{warning} """


صفقة عالية الجودة

def format_high_priority(rec): type_icon = "🟢 Call" if rec["type"].lower() == "call" else "🔴 Put" current_price = rec.get("current_price") strike_price = extract_strike_price(rec["contract"])

price_line = f"\n💵 السعر الحالي: {current_price}" if current_price else ""
warning = ""
if current_price and strike_price:
    distance = abs(strike_price - current_price)
    if distance / current_price > 1:
        warning = "\n⚠️ *تحذير: العقد بعيد جدًا عن السعر الحالي، تأكد من صحة البيانات.*"

return f"""🔥 *صفقة عالية الجودة – {rec['symbol']}* 🔥

{type_icon} 📆 العقد: {rec['contract']} 📈 الدخول: {rec['entry']} | 🎯 الأهداف: {rec['targets'][0]} → {rec['targets'][1]} 🛑 وقف الخسارة: {rec['stop_loss']} ⚡️ السبب: {rec['reason']}{price_line}{warning} """

تحميل المُرسلة

def load_sent(): if not os.path.exists(SENT_FILE): return set() with open(SENT_FILE, "r", encoding="utf-8") as f: return set(json.load(f))

حفظ المُرسلة

def save_sent(sent_ids): with open(SENT_FILE, "w", encoding="utf-8") as f: json.dump(list(sent_ids), f, ensure_ascii=False, indent=2)

إرسال التوصيات الجديدة فقط

def send_recommendations(): recommendations, high_priority = load_recommendations() sent_ids = load_sent()

filtered = filter_recommendations(recommendations)
for i, rec in enumerate(filtered):
    rec_id = get_unique_id(rec)
    if rec_id not in sent_ids:
        msg = format_recommendation(i, rec)
        send_to_telegram(msg)
        sent_ids.add(rec_id)
        time.sleep(2)

filtered_hp = filter_recommendations(high_priority)
for rec in filtered_hp:
    rec_id = get_unique_id(rec)
    if rec_id not in sent_ids:
        msg = format_high_priority(rec)
        send_to_telegram(msg)
        sent_ids.add(rec_id)
        time.sleep(2)

save_sent(sent_ids)

تكرار الإرسال كل دقيقة

while True: send_recommendations() time.sleep(60)

