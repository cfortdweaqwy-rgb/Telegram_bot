import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, 
    CommandHandler, 
    CallbackQueryHandler, 
    CallbackContext
)

# 1. التوكن (من الـ Environment Variables في Render)
TOKEN = os.getenv("BOT_TOKEN")

# 2. روابط المواد والفروع
subjects = {
    "رياضيات": {
        "جبر": "https://example.com/jabr",
        "تفاضل": "https://example.com/tafadol"
    },
    "برمجة": {
        "بايثون": "https://example.com/python",
        "جافا": "https://example.com/java"
    },
    "شبكات": {
        "مقدمة": "https://example.com/network1",
        "أمان": "https://example.com/network2"
    }
}

# دالة /start
def start(update: Update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(subj, callback_data=subj)] for subj in subjects]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("اختر المادة:", reply_markup=reply_markup)

# التعامل مع الأزرار
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    # لو المستخدم اختار مادة
    if query.data in subjects:
        keyboard = [
            [InlineKeyboardButton(branch, url=link)] for branch, link in subjects[query.data].items()
        ]
        keyboard.append([InlineKeyboardButton("↩️ رجوع", callback_data="رجوع")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text=f"اختر فرع من {query.data}:", reply_markup=reply_markup)

    # لو المستخدم ضغط رجوع
    elif query.data == "رجوع":
        keyboard = [[InlineKeyboardButton(subj, callback_data=subj)] for subj in subjects]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="اختر المادة:", reply_markup=reply_markup)

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    # إعداد Webhook لـ Render
    PORT = int(os.environ.get("PORT", 8443))
    HEROKU_URL = os.environ.get("RENDER_EXTERNAL_URL")  # Render يعطيك هذا الرابط تلقائياً

    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{HEROKU_URL}/{TOKEN}"
    )

    updater.idle()

if __name__ == '__main__':
    main()
