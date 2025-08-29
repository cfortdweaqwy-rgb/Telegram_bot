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
    selection = query.data

    # زر الرجوع للقائمة الرئيسية
    if selection == "رجوع":
        keyboard = [[InlineKeyboardButton(subj, callback_data=subj)] for subj in data.keys()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("📚 اختر مادة من القائمة:", reply_markup=reply_markup)
        return

    # لو المستخدم اختار مادة
    if selection in data:
        subject = selection
        branches = data[subject]

        keyboard = [[InlineKeyboardButton(branch, callback_data=f"{subject}|{branch}")]
                    for branch in branches.keys()]

        # زر الرجوع
        keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data="رجوع")])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=f"📖 اختر فرع من *{subject}*: ",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return

    # لو المستخدم اختار فرع من مادة
    if "|" in selection:
        subject, branch = selection.split("|", 1)
        links = data[subject][branch]

        if links:
            message = f"🔗 روابط *{branch}* لمادة *{subject}*:\n\n"
            for i, link in enumerate(links, start=1):
                message += f"{i}. {link}\n"
        else:
            message = f"🚫 لا توجد روابط حالياً لفرع *{branch}* في مادة *{subject}*."

        await query.edit_message_text(message, parse_mode="Markdown")

# تشغيل البوت
def main():
    application = Application.builder().token("8359968226:AAE2eNEr-tCip4GCJXk9E2W7neViOXDP1VY").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()

if __name__ == "__main__":
    main()
