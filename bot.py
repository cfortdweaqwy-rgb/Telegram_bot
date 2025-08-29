import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تحميل ملف المواد والروابط
with open("links.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# رسالة الترحيب + عرض المواد
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(subj, callback_data=subj)] for subj in data.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 أهلاً بك في بوت المواد.\n\n📚 اختر مادة من القائمة:",
        reply_markup=reply_markup
    )

# التعامل مع الأزرار
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subject = query.data

    # زر الرجوع للقائمة الرئيسية
    if subject == "رجوع":
        keyboard = [[InlineKeyboardButton(subj, callback_data=subj)] for subj in data.keys()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 اختر مادة من القائمة:", reply_markup=reply_markup)
        return

    # لو المادة موجودة في JSON
    if subject in data:
        branches = data[subject]
        keyboard = []
        for branch, links in branches.items():
            if isinstance(links, list) and len(links) > 0:
                for i, link in enumerate(links, start=1):
                    keyboard.append([InlineKeyboardButton(f"{branch} {i}", url=link)])
            else:
                keyboard.append([InlineKeyboardButton(f"{branch} (🚫 لا يوجد)", callback_data="no_link")])

        # زر الرجوع
        keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data="رجوع")])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=f"📖 اختر فرع من *{subject}*: ",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await query.edit_message_text("🚫 هذا الخيار غير موجود.")

# تشغيل البوت
def main():
    application = Application.builder().token("8359968226:AAE2eNEr-tCip4GCJXk9E2W7neViOXDP1VY").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()

if __name__ == "__main__":
    main()
