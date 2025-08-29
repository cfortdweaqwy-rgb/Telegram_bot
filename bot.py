import telebot
import json
from telebot import types

# ضع التوكن الخاص بك
TOKEN = "8359968226:AAE2eNEr-tCip4GCJXk9E2W7neViOXDP1VY"
bot = telebot.TeleBot(TOKEN)

# تحميل البيانات من links.json
with open("links.json", "r", encoding="utf-8") as f:
    links = json.load(f)

# رسالة الترحيب
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for subject in links.keys():
        markup.add(subject)
    bot.send_message(
        message.chat.id,
        "👋 أهلاً بك!\nاختر المادة 📚:",
        reply_markup=markup
    )

# عند اختيار مادة
@bot.message_handler(func=lambda msg: msg.text in links.keys())
def subject_menu(message):
    subject = message.text
    markup = types.InlineKeyboardMarkup()
    for branch, url in links[subject].items():
        markup.add(types.InlineKeyboardButton(branch, url=url))
    bot.send_message(
        message.chat.id,
        f"📖 اختر الفرع الخاص بـ {subject}:",
        reply_markup=markup
    )

print("✅ Bot is running...")
bot.polling(none_stop=True)
