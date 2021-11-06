import json
from logging import error
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, Filters, MessageHandler, Updater, CommandHandler, CallbackContext
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from chargingstation.handlers import chargingStationDefault, chargingStationLocation
from collectionpoint.handlers import collectionPointDefault, collectionPointLocation

from carpark.handlers import carparkDefault, carparkLocation
from common.expectations import Expectations
from disposal.handlers import disposalArea, disposalDefault, disposalStop

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Willkommen, ich bin der SanktGallenBot und helfe dir gerne weiter 😘")
    update.message.reply_text("Unten links im Menü findest du meine Befehle")
    update.message.reply_text("Für weitere Infos klicke hier: /help")

def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Dieser Bot wurde inital im Rahmen des Open Data Hack St.Gallen 2021 erstellt. Er hilft dir öffentliche Daten zu beziehen.")
    update.message.reply_text("Die möglichen Befehle siehst du im Menu unten links.")
    update.message.reply_text("Weitere Informationen findest du auf der Projekthomepage https://sanktgallenbot.ch oder kontaktiere @ignobled")

def unexcpected(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Das war unerwartet 😲")
    update.message.reply_text("Bitte sende mir nochmals einen Befehl")
    return ConversationHandler.END

def main() -> None:
    with open('config.json') as data_file:
            data = json.load(data_file)
            token = data["token"]

    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))

    _handlers = {}
    _handlers['start_handler'] = CommandHandler('start', start)
    _handlers['help_handler'] = CommandHandler('help', help)
    _handlers['disposal_stop'] = CommandHandler('stop', disposalStop)
    _handlers['carpark_conversation_handler'] = ConversationHandler(
        entry_points=[CommandHandler('parkhaus', carparkDefault)],
        states={
            Expectations.Location: [MessageHandler(Filters.location, carparkLocation)],
        },
        fallbacks=[MessageHandler(Filters.command, unexcpected)]
    )
    _handlers['collectionpoint_conversation_handler'] = ConversationHandler(
        entry_points=[CommandHandler('sammelstelle', collectionPointDefault)],
        states={
            Expectations.Location: [MessageHandler(Filters.location, collectionPointLocation)],
        },
        fallbacks=[MessageHandler(Filters.command, unexcpected)]
    )
    _handlers['chargingstation_conversation_handler'] = ConversationHandler(
        entry_points=[CommandHandler('ladestation', chargingStationDefault)],
        states={
            Expectations.Location: [MessageHandler(Filters.location, chargingStationLocation)],
        },
        fallbacks=[MessageHandler(Filters.command, unexcpected)]
    )
    _handlers['disposal_conversation_handler'] = ConversationHandler(
        entry_points=[CommandHandler('abfuhr', disposalDefault)],
        states={
            Expectations.Text: [CallbackQueryHandler(disposalArea)],
        },
        fallbacks=[MessageHandler(Filters.command, unexcpected)]
    )

    for name, _handler in _handlers.items():
        print(f'Adding handler {name}')
        dispatcher.add_handler(_handler)


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()