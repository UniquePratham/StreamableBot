import os
from telegram import Update, File
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Replace with your Telegram username (without @)
CDN_USERNAME = os.environ.get("CDN_USERNAME", "yourusername")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎥 Send me a video and I'll give you a VLC streaming link.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.video and not update.message.document:
        await update.message.reply_text("❌ Only video files are supported.")
        return

    file = update.message.video or update.message.document
    file_id = file.file_id

    tg_file: File = await context.bot.get_file(file_id)
    file_path = tg_file.file_path.split('/')[-1]

    stream_link = f"https://cdn4.telegram-cdn.org/file/{file_path}"
    
    await update.message.reply_text(
        f"✅ Your streamable VLC link:\n\n🔗 `{stream_link}`\n\n"
        f"▶ Open in VLC > Stream > Network:\nPaste the link.\n\n"
        f"Works as long as Telegram caches the file.\nKeep it safe!",
        parse_mode='Markdown'
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
