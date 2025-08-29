import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تحميل البيانات من links.json
with open("links.json", "r", encoding="utf-8") as f:
    data = json.load(f)

TOKEN = "8359968226:AAE2eNEr-tCip4GCJXk9E2W7neViOXDP1VY"

# رسالة الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(subject, callback_data=subject)]
        for subject in data.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 أهلاً بك!\n\n📚 اختر المادة:", reply_markup=reply_markup)

# التعامل مع اختيار المادة
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subject = query.data
    branches = data[subject]

    keyboard = [
        [InlineKeyboardButton(branch, url=branches[branch])]
        for branch in branches
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"📖 اختر فرع من {subject}:", reply_markup=reply_markup)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
