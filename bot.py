import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تحميل الروابط من الملف
with open("links.json", "r", encoding="utf-8") as f:
    data = json.load(f)

TOKEN = os.getenv("BOT_TOKEN")  # لازم تضيف BOT_TOKEN في إعدادات Render
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # رابط البوت على Render

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(subj, callback_data=subj)] for subj in data.keys()]
    await update.message.reply_text("اختر المادة:", reply_markup=InlineKeyboardMarkup(keyboard))

# عرض الفروع
async def show_branches(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    subject = query.data

    if subject in data:
        keyboard = [[InlineKeyboardButton(branch, callback_data=f"{subject}|{branch}")]
                    for branch in data[subject].keys()]
        keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data="back_main")])
        await query.edit_message_text(f"اختر الفرع من {subject}:",
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    elif "|" in subject:
        subject_name, branch = subject.split("|")
        links = data[subject_name][branch]

        keyboard = [[InlineKeyboardButton(f"رابط {i+1}", url=link)]
                    for i, link in enumerate(links)]
        keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data=subject_name)])
        await query.edit_message_text(f"روابط {branch} ({subject_name}):",
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    elif subject == "back_main":
        keyboard = [[InlineKeyboardButton(subj, callback_data=subj)] for subj in data.keys()]
        await query.edit_message_text("اختر المادة:", reply_markup=InlineKeyboardMarkup(keyboard))


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(show_branches))

    # إعداد الـ Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 10000)),
        url_path=TOKEN,
        webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
    )

if __name__ == "__main__":
    main()
