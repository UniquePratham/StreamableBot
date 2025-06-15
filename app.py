import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📽️ Send a video and I’ll give you a VLC streaming link.")

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.video or update.message.document
    if not file:
        await update.message.reply_text("❌ Only video files supported.")
        return

    tg_file = await context.bot.get_file(file.file_id)
    stream_url = tg_file.file_path
    final_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{stream_url}"

    await update.message.reply_text(
        f"✅ VLC Stream Link:\n`{final_url}`\n\n🎬 Open VLC → Media → Open Network Stream",
        parse_mode='Markdown'
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
