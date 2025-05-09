from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7765246155:AAFn1u9gPIIrLvmt1ItVrFMS0EmwdjRlve4"
ADMIN_ID = 1148324126  # Замените на свой Telegram ID

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    form_text = (
        "👋 Привет! Чтобы отправить новость для канала 'Мичуринск Сейчас', пожалуйста, заполните форму:\n\n"
        "📌 **Тема:** (например, происшествие, событие, объявление)\n"
        "✏ **Описание:** (напишите подробности)\n"
        "📷 **Фото или видео (по желанию):** прикрепите файл\n\n"
        "После отправки мы проверим ваше сообщение!"
    )

    await update.message.reply_text(form_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message
    forward_text = f"📩 Новое предложение от @{user.username or 'без username'} (ID: {user.id}):"

    if message.text:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"{forward_text}\n\n{message.text}")
    elif message.photo:
        photo = message.photo[-1]
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo.file_id, caption=forward_text)
    elif message.video:
        await context.bot.send_video(chat_id=ADMIN_ID, video=message.video.file_id, caption=forward_text)
    else:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"{forward_text}\n\n(неизвестный тип сообщения)")

    await message.reply_text("✅ Спасибо! Ваше сообщение отправлено редакции.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
