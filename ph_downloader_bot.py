import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_API_TOKEN = os.getenv("7649034288:AAGVXxddJfBjkeNwVwB8mBVCHPX5TvzuP_Q")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Send me a PornHub link!")

def download_video(url: str, output_path: str = "downloads") -> str:
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'http_headers': {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0'},
        'verbose': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    if "pornhub.com" not in url:
        await update.message.reply_text("Send a PornHub link!")
        return
    await update.message.reply_text("Downloading...")
    try:
        video_path = download_video(url)
        with open(video_path, 'rb') as video_file:
            await update.message.reply_video(video=video_file)
        await update.message.reply_text("Video sent!")
    except Exception as e:
        await update.message.reply_text(f"Failed: {str(e)}")
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Error: {context.error}")
    await update.message.reply_text("Something broke!")

def run_bot():
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    run_bot()
