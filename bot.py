import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# تحميل المواد والفروع من ملف JSON
with open("links.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# رسالة الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بك!\nاستخدم الأمر /menu لاختيار المادة."
    )

# عرض المواد
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(subj, callback_data=subj)] for subj in data.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 اختر المادة:", reply_markup=reply_markup)

# عند اختيار مادة → عرض الفروع
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subject = query.data
    branches = data.get(subject, {})

    if branches:
        keyboard = [
            [InlineKeyboardButton(branch, url=link)]
            for branch, link in branches.items()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"📖 اختر الفرع الخاص بـ *{subject}*:",
            reply_markup=reply_markup,
            parse_mode="Markdown",
        )
    else:
        await query.edit_message_text(f"❌ لا توجد فروع للمادة {subject}")

def main():
    # ضع التوكن تبعك هنا
    TOKEN = "8359968226:AAE2eNEr-tCip4GCJXk9E2W7neViOXDP1VY"

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
