from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from common.expectations import Expectations
    
def carparkDefault(update: Update, context: CallbackContext):
    update.message.reply_text("Bitte sende mir dein Standort")
    return Expectations.Location

def carparkLocation(update: Update, context: CallbackContext):
    location = update.message.location
    latitude = location["latitude"]
    longitude = location["longitude"]
    update.message.reply_text(latitude)
    update.message.reply_text(longitude)
    return ConversationHandler.END
