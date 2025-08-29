import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تحميل ملف المواد والروابط
with open("links.json", "r", encoding="utf-8") as f:
    data = json.load(f)


# ========== دوال ==========
# عرض المواد
async def show_subjects(update_or_query, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(subj, callback_data=f"subject|{subj}")] for subj in data.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = "👋 أهلاً بك في بوت المواد.\n\n📚 اختر مادة من القائمة:"

    if hasattr(update_or_query, "message"):  # من /start
        await update_or_query.message.reply_text(text, reply_markup=reply_markup)
    else:  # من زر "رجوع"
        await update_or_query.edit_message_text(text, reply_markup=reply_markup)


# بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await show_subjects(update, context)


# التعامل مع الأزرار
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selection = query.data

    # اختيار مادة
    if selection.startswith("subject|"):
        subject = selection.split("|", 1)[1]
        branches = data[subject]

        keyboard = [
            [InlineKeyboardButton(branch, callback_data=f"branch|{subject}|{branch}")]
            for branch in branches.keys()
        ]
        keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data="back_subjects")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=f"📖 اختر فرع من *{subject}*: ",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    # اختيار فرع
    elif selection.startswith("branch|"):
        _, subject, branch = selection.split("|", 2)
        links = data[subject][branch]

        if links:
            message = f"🔗 روابط *{branch}* لمادة *{subject}*:\n\n"
            for i, link in enumerate(links, start=1):
                message += f"{i}. {link}\n"
        else:
            message = f"🚫 لا توجد روابط حالياً لفرع *{branch}* في مادة *{subject}*."

        keyboard = [[InlineKeyboardButton("⬅️ رجوع", callback_data=f"subject|{subject}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(message, parse_mode="Markdown", reply_markup=reply_markup)

    # زر الرجوع للمواد
    elif selection == "back_subjects":
        await show_subjects(query, context)


# ========== تشغيل البوت ==========
def main():
    application = Application.builder().token("8359968226:AAE2eNEr-tCip4GCJXk9E2W7neViOXDP1VY").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()


if __name__ == "__main__":
    main()
