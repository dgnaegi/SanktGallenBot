from telegram.ext import CallbackContext
from telegram import Update
from telegram.ext import CallbackContext
from common.expectations import Expectations
    
def carparkDefault(update: Update, context: CallbackContext):
    update.message.reply_text("Bitte sende mir dein Standort")
    return Expectations.Location

def carparkLocation(update: Update, context: CallbackContext):
    update.message.reply_text("Answer")
