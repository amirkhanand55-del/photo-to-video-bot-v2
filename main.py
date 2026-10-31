import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

TOKEN =9178976133:AAHfBvIJCA3IU7oT0F_6iXQFjB6cbn0jOqQ


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋 به ربات تبدیل عکس به ویدئو خوش آمدی!\n\n"
        "عکس خودت را بفرست تا دریافتش کنم."
    )


async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("عکس دریافت شد! ⏳")

    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)

    os.makedirs("photos", exist_ok=True)

    filename = f"photos/{update.effective_user.id}_{photo.file_unique_id}.jpg"
    await file.download_to_drive(filename)

    await update.message.reply_text(
        "عکس با موفقیت دریافت شد. ✅\n\n"
        "موتور هوش مصنوعی ساخت ویدئو هنوز متصل نشده است."
    )


async def main():
    if not TOKEN:
        raise RuntimeError("توکن ربات تنظیم نشده است.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, receive_photo))

    logging.info("Bot is running...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        import asyncio
        await asyncio.Event().wait()
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
