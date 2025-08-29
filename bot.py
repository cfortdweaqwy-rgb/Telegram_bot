import os
import json
import telebot

# ضع هنا التوكن الخاص بالبوت
TOKEN = "8359968226:AAE2eNEr-tCip4GCJXk9E2W7neViOXDP1VY"

bot = telebot.TeleBot(TOKEN)

# تحديد المسار الصحيح للملف links.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LINKS_FILE = os.path.join(BASE_DIR, "links.json")

# قراءة ملف links.json
with open(LINKS_FILE, "r", encoding="utf-8") as f:
    links = json.load(f)


# مثال: أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! 🌹\nهذا بوت التجربة يعمل الآن.")


# مثال: إرسال الروابط من ملف links.json
@bot.message_handler(commands=['get'])
def send_links(message):
    text = "📂 الروابط المتوفرة:\n\n"
    for subject, data in links.items():
        text += f"📌 {subject}\n"
        for section, urls in data.items():
            if urls:
                text += f"   🔗 {section}: {', '.join(urls)}\n"
    bot.send_message(message.chat.id, text)


# تشغيل البوت
bot.polling()
