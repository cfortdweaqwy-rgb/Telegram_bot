import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تحميل بيانات المواد من الملف
with open("links.json", "r", encoding="utf-8") as f:
    subjects = json.load(f)

# بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(sub, callback_data=sub)] for sub in subjects.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📚 اختر المادة:", reply_markup=reply_markup)

# التعامل مع اختيار المادة
async def subject_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subject = query.data

    keyboard = [
        [InlineKeyboardButton(item, callback_data=f"{subject}|{item}")]
        for item in subjects[subject].keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"📖 اختر نوع الملفات لمادة *{subject}*:", reply_markup=reply_markup, parse_mode="Markdown")

# التعامل مع اختيار النوع (صور محاضرات، ملخصات، ...)
async def links_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subject, category = query.data.split("|")

    links = subjects[subject][category]

    if not links:
        await query.edit_message_text(f"⚠️ لا توجد روابط حالياً لـ *{category}* في مادة *{subject}*.", parse_mode="Markdown")
    else:
        text = f"🔗 روابط *{category}* لمادة *{subject}*:\n\n"
        for i, link in enumerate(links, start=1):
            text += f"{i}. {link}\n"
        await query.edit_message_text(text, parse_mode="Markdown")

# تشغيل البوت
def main():
    BOT_TOKEN = "8359968226:AAE2eNEr-tCip4GCJXk9E2W7neViOXDP1VY"
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(subject_handler, pattern="^[^|]+$"))
    app.add_handler(CallbackQueryHandler(links_handler, pattern=".+\\|.+"))

    print("✅ البوت شغال...")
    app.run_polling()

if __name__ == "__main__":
    main()
