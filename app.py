import os
from telegram import Update, File
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎥 Send me a video file and I’ll give you a VLC streaming link.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.video or update.message.document
    if not file:
        await update.message.reply_text("❌ Only video files are supported.")
        return

    tg_file: File = await context.bot.get_file(file.file_id)
    file_path = tg_file.file_path.split('/')[-1]
    stream_link = f"https://cdn4.telegram-cdn.org/file/{file_path}"

    await update.message.reply_text(
        f"✅ Your VLC stream link:\n\n🔗 `{stream_link}`\n\n"
        f"▶ Open VLC > Media > Open Network Stream\nPaste the link there.\n\n"
        f"⚠ Link stays valid as long as Telegram caches it.",
        parse_mode='Markdown'
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
