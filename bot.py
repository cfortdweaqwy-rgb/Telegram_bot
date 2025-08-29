import telebot
import json
import os

# ضع التوكن الخاص بالبوت هنا
TOKEN = "ضع_التوكن_حقك_هنا"
bot = telebot.TeleBot(TOKEN)

# تحميل ملف links.json من نفس مجلد البوت
LINKS_FILE = os.path.join(os.path.dirname(__file__), "links.json")

with open(LINKS_FILE, "r", encoding="utf-8") as f:
    links = json.load(f)

# رسالة الترحيب عند بدء البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 أهلاً بك في البوت! استخدم الأوامر أو اكتب اسم المادة للحصول على الملفات.")

# إرسال الروابط عند كتابة اسم المادة
@bot.message_handler(func=lambda message: True)
def send_links(message):
    subject = message.text.strip()
    if subject in links:
        response = f"📚 الروابط الخاصة بمادة: {subject}\n\n"
        for category, urls in links[subject].items():
            if urls:
                response += f"🔹 {category}:\n" + "\n".join(urls) + "\n\n"
        bot.reply_to(message, response if response else "❌ لا توجد روابط حالياً لهذه المادة.")
    else:
        bot.reply_to(message, "❌ المادة غير موجودة في القائمة.")

# تشغيل البوت
print("🤖 البوت يعمل الآن...")
bot.infinity_polling()
