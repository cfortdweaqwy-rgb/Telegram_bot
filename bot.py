import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ضع التوكن الخاص بك هنا
TOKEN = "8359968226:AAE2eNEr-tCip4GCJXk9E2W7neViOXDP1VY"

# تفعيل اللوج للمتابعة
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# المواد
subjects = {
    "1": "📘 مادة الاحتمالات",
    "2": "📘 مادة التجريبية",
    "3": "📘 مادة صناعية 2",
    "4": "📘 مادة تخطيط الانتاج",
    "5": "📘 مادة بحوث عمليات 2",
    "6": "📘 مادة التسويق والمبيعات"
}

# الفروع
branches = {
    "محاضرات": "📚 روابط المحاضرات",
    "ملخصات": "📄 روابط الملخصات",
    "مراجع": "📘 روابط المراجع",
    "نماذج اختبارات": "📝 روابط النماذج"
}


# رسالة البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"subject_{id}")]
        for id, name in subjects.items()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 أهلاً بك!\n\nاختر المادة من القائمة:", reply_markup=reply_markup
    )


# عند اختيار مادة
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("subject_"):
        # استخراج رقم المادة
        subject_id = query.data.split("_")[1]
        subject_name = subjects[subject_id]

        # أزرار الفروع
        keyboard = [
            [InlineKeyboardButton(branch, callback_data=f"branch_{branch}")]
            for branch in branches.keys()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=f"📚 لقد اخترت: {subject_name}\n\nاختر الفرع:",
            reply_markup=reply_markup,
        )

    elif query.data.startswith("branch_"):
        branch_name = query.data.split("_")[1]
        await query.edit_message_text(
            text=f"✅ تم اختيار الفرع: {branch_name}\n{branches[branch_name]}"
        )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 البوت شغال...")
    app.run_polling()


if __name__ == "__main__":
    main()
