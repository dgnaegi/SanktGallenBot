import json
from logging import error
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, Filters, MessageHandler, Updater, CommandHandler, CallbackContext
from chargingstation.handlers import chargingStationDefault, chargingStationLocation
from collectionpoint.handlers import collectionPointDefault, collectionPointLocation
from common.expectations import Expectations

from carpark.handlers import carparkDefault, carparkLocation
    
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Willkommen, ich bin der SanktGallenBot und helfe dir gerne weiter 😘")
    update.message.reply_text("Unten links im Menü findest du meine Befehle")
    update.message.reply_text("Für weitere Infos klicke hier: /help")
    
def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hilfe muss noch angepasst werden")

def main() -> None:
    handlers = {}
    
    with open('config.json') as data_file:
            data = json.load(data_file)
            token = data["token"]
    
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
        
    _handlers = {}
    _handlers['start_handler'] = CommandHandler('start', start)
    _handlers['help_handler'] = CommandHandler('help', help)
    _handlers['carpark_conversation_handler'] = ConversationHandler(
        entry_points=[CommandHandler('parkhaus', carparkDefault)],
        states={
            Expectations.Location: [MessageHandler(Filters.location, carparkLocation)],
        },
        fallbacks=[CommandHandler('error', error)]
    )
    _handlers['collectionpoint_conversation_handler'] = ConversationHandler(
        entry_points=[CommandHandler('sammelstelle', collectionPointDefault)],
        states={
            Expectations.Location: [MessageHandler(Filters.location, collectionPointLocation)],
        },
        fallbacks=[CommandHandler('error', error)]
    )
    _handlers['chargingstation_conversation_handler'] = ConversationHandler(
        entry_points=[CommandHandler('ladestation', chargingStationDefault)],
        states={
            Expectations.Location: [MessageHandler(Filters.location, chargingStationLocation)],
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