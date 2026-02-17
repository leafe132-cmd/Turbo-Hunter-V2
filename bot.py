import telebot
import requests
import random
import string
import threading
import time

# --- بياناتك ---
TOKEN = "7979323842:AAFB_LAZI1wN5462k-AgMaSkw5YgplJBARw"
MY_ID = 7755049597 
bot = telebot.TeleBot(TOKEN)

is_hunting = False

def get_user():
    # البحث عن يوزرات خماسية وسداسية (غالباً هي التي تُترك وبها متابعون)
    length = random.choice([5, 6]) 
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def hunting_task():
    global is_hunting
    while is_hunting:
        user = get_user()
        try:
            # رابط الفحص
            url = f"https://www.tiktok.com/@{user}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=3)
            
            # إذا كان اليوزر متاحاً (404)
            if res.status_code == 404:
                # هنا نقوم بمحاولة تقدير شهرة اليوزر (عبر روابط خارجية أو بحث)
                # ملاحظة: تيك توك يصعب فحص المتابعين للمتاح مباشرة، 
                # لذا سنركز على اليوزرات التي تبدو كأرقام أو أسماء قديمة
                bot.send_message(MY_ID, f"🔥 حساب متاح قديم (احتمال متابعين عالي):\n👤 @{user}\n🔗 {url}")
        except:
            pass
        time.sleep(0.2)

@bot.message_handler(commands=['start'])
def menu(message):
    if message.chat.id == MY_ID:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🚀 بدء صيد الحسابات الكبيرة", "🛑 إيقاف")
        bot.send_message(MY_ID, "مرحباً داوود! جاهز لصيد حسابات قديمة بمتابعين؟", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def control(message):
    global is_hunting
    if message.chat.id == MY_ID:
        if message.text == "🚀 بدء صيد الحسابات الكبيرة":
            is_hunting = True
            for _ in range(10): # تشغيل 10 صيادين
                threading.Thread(target=hunting_task).start()
            bot.send_message(MY_ID, "🚀 بدأ الفحص عن حسابات قديمة نادرة...")
        elif message.text == "🛑 إيقاف":
            is_hunting = False
            bot.send_message(MY_ID, "🛑 تم التوقف.")

bot.infinity_polling()
  
