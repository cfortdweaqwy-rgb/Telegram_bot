import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تفعيل اللوغز
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# قراءة المواد من ملف JSON
with open("links.json", "r", encoding="utf-8") as f:
    subjects = json.load(f)

# رسالة الترحيب + عرض المواد
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(name, callback_data=name)] for name in subjects.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 أهلاً بك!\n\nاختر المادة من القائمة:", reply_markup=reply_markup)

# عند اختيار المادة → عرض الفروع
async def subject_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subject = query.data
    branches = subjects[subject]

    keyboard = [
        [InlineKeyboardButton(branch, callback_data=f"{subject}|{branch}")]
        for branch in branches.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"📘 اختر الفرع في مادة: {subject}",
        reply_markup=reply_markup,
    )

# عند اختيار الفرع → إرسال الرابط
async def branch_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subject, branch = query.data.split("|")
    link = subjects[subject][branch]

    await query.edit_message_text(
        text=f"✅ هذا رابط {branch} لمادة {subject}:\n\n{link}"
    )

def main():
    TOKEN = "YOUR_BOT_TOKEN"

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(branch_handler, pattern=".*\|.*"))
    app.add_handler(CallbackQueryHandler(subject_handler, pattern="^(?!.*\|).*"))

    app.run_polling()

if __name__ == "__main__":
    main()
