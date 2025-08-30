import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# تسجيل الأخطاء
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# تحميل الروابط من JSON
with open("links.json", "r", encoding="utf-8") as f:
    LINKS = json.load(f)

TOKEN = "8359968226:AAE2eNEr-tCip4GCJXk9E2W7neViOXDP1VY"

# قائمة المواد
SUBJECTS = list(LINKS.keys())

# ⬇️ أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(subj, callback_data=f"subject|{subj}")]
                for subj in SUBJECTS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("اختر المادة:", reply_markup=reply_markup)

# ⬇️ التعامل مع الضغط على الأزرار
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data.split("|")
    action = data[0]

    # عرض فروع المادة
    if action == "subject":
        subject = data[1]
        keyboard = [[InlineKeyboardButton(branch, callback_data=f"branch|{subject}|{branch}")]
                    for branch in LINKS[subject].keys()]
        keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data="back_to_subjects")])
        await query.edit_message_text(
            text=f"📘 اختر الفرع في مادة {subject}:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # عرض روابط الفرع
    elif action == "branch":
        subject, branch = data[1], data[2]
        links = LINKS[subject][branch]
        keyboard = [[InlineKeyboardButton(f"رابط {i+1}", url=link)] for i, link in enumerate(links)]
        keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data=f"subject|{subject}")])
        await query.edit_message_text(
            text=f"🔗 روابط {branch} ({subject}):",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # رجوع للمواد
    elif action == "back_to_subjects":
        keyboard = [[InlineKeyboardButton(subj, callback_data=f"subject|{subj}")]
                    for subj in SUBJECTS]
        await query.edit_message_text("اختر المادة:", reply_markup=InlineKeyboardMarkup(keyboard))

# ⬇️ تشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("✅ البوت شغال...")
    app.run_polling()

if __name__ == "__main__":
    main()
