import json
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# تفعيل اللوقات عشان نشوف الأخطاء
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# تحميل البيانات من links.json
with open("links.json", "r", encoding="utf-8") as f:
    subjects = json.load(f)

TOKEN = "8359968226:AAE2eNEr-tCip4GCJXk9E2W7neViOXDP1VY"


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(sub, callback_data=f"subject:{sub}")]
        for sub in subjects.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 اختر المادة:", reply_markup=reply_markup)


# التعامل مع الأزرار
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # لو اختار مادة
    if data.startswith("subject:"):
        sub = data.split(":")[1]
        keyboard = [
            [InlineKeyboardButton(branch, callback_data=f"branch:{sub}:{branch}")]
            for branch in subjects[sub].keys()
        ]
        keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(f"📖 اختر فرع من مادة {sub}:", reply_markup=reply_markup)

    # لو اختار فرع
    elif data.startswith("branch:"):
        sub = data.split(":")[1]
        branch = data.split(":")[2]
        links = subjects[sub][branch]

        text = f"✅ اخترت: {branch}\n\n🔗 الروابط:\n"
        text += "\n".join([f"{i+1}. {link}" for i, link in enumerate(links)])

        keyboard = [[InlineKeyboardButton("⬅️ رجوع", callback_data=f"subject:{sub}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup)

    # رجوع للقائمة الرئيسية
    elif data == "back_main":
        keyboard = [
            [InlineKeyboardButton(sub, callback_data=f"subject:{sub}")]
            for sub in subjects.keys()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 اختر المادة:", reply_markup=reply_markup)


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("✅ البوت شغال ...")
    app.run_polling()


if __name__ == "__main__":
    main()
