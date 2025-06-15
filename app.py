import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📽️ Send a video file (not a link or GIF), and I’ll give you a VLC streamable link.")

# Video/file handler
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    file = message.video or (
        message.document if message.document and message.document.mime_type.startswith("video/") else None
    )

    if not file:
        await message.reply_text("❌ Unsupported file. Please send a proper video file.")
        return

    try:
        tg_file = await context.bot.get_file(file.file_id)

        if not tg_file.file_path:
            await message.reply_text("❌ Couldn’t retrieve stream link. Telegram didn't return a file path.")
            return

        final_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{tg_file.file_path}"

        await message.reply_text(
            f"✅ VLC Stream Link:\n`{final_url}`\n\n🎬 Open VLC → Media → Open Network Stream",
            parse_mode='Markdown'
        )

    except Exception as e:
        await message.reply_text(f"⚠️ Internal error: `{e}`", parse_mode="Markdown")


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, handle_video))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
