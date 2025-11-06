import os
from telegram.ext import Updater, CommandHandler

TOKEN = os.getenv("BOT_TOKEN")

def start(update, context):
    update.message.reply_text("🚀 أهلاً بيك في Abo Joe Space Bot 😎🛸")

updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(CommandHandler("start", start))

updater.start_polling()
updater.idle()
