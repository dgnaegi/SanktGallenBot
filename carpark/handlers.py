from telegram.ext import CallbackContext
from telegram import Update

def carpark(update: Update, context: CallbackContext):
    update.message.reply_text("Hallo carpark!")