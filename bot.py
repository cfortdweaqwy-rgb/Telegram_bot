import os
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# تحميل المواد والفروع من ملف links.json
with open("links.json", "r", encoding="utf-8") as f:
    LINKS = json.load(f)

# إظهار قائمة المواد
async def show_subjects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[subj] for subj in LINKS.keys()]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("📚 اختر المادة:", reply_markup=reply_markup)

# أمر البداية /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك في البوت!\n")
    await show_subjects(update, context)

# عند اختيار مادة
async def subject_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in LINKS:
        branches = LINKS[text].keys()
        keyboard = [[b] for b in branches] + [["⬅️ رجوع"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(f"📖 اختر الفرع من {text}:", reply_markup=reply_markup)

# عند اختيار فرع أو رجوع
async def branch_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "⬅️ رجوع":
        await show_subjects(update, context)
        return
    
    if text == "⬅️ رجوع للقائمة الرئيسية":
        await show_subjects(update, context)
        return

    for subj, branches in LINKS.items():
        if text in branches:
            links = "\n".join(branches[text])
            keyboard = [["⬅️ رجوع للقائمة الرئيسية"]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(f"🔗 روابط {text}:\n{links}", reply_markup=reply_markup)
            return

# تشغيل البوت
def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("❌ BOT_TOKEN غير موجود في Environment Variables")
        return

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, subject_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, branch_handler))

    print("✅ البوت شغال ...")
    app.run_polling()

if __name__ == "__main__":
    main()
