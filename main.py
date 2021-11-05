import json
from logging import error
from telegram import Update
from telegram.ext import Filters, MessageHandler, Updater, CommandHandler, CallbackContext
from telegram.ext import (Updater,
                          PicklePersistence,
                          CommandHandler,
                          CallbackQueryHandler,
                          CallbackContext,
                          ConversationHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from common.expectations import Expectations


from carpark.handlers import carparkDefault, carparkLocation

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Willkommen beim SanktGallenBot! Für xy mach abc")
    
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Error!")

def main() -> None:
    handlers = {}
    handlers['start_handler'] = CommandHandler('start', start)
    
    with open('config.json') as data_file:
            data = json.load(data_file)
            token = data["token"]
    
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
        
    _handlers = {}
    _handlers['start_handler'] = CommandHandler('start', start)
    _handlers['carpark_conversation_handler'] = ConversationHandler(
        entry_points=[CommandHandler('parkhaus', carparkDefault)],
        states={
            Expectations.Location: [MessageHandler(Filters.location, carparkLocation)],
        },
        fallbacks=[CommandHandler('error', error)]
    )
    
    for name, _handler in _handlers.items():
        print(f'Adding handler {name}')
        dispatcher.add_handler(_handler)
    
    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()