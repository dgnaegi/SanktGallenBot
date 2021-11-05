import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from carpark.handlers import carpark

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Willkommen beim SanktGallenBot! Für xy mach abc")

def main() -> None:
    with open('config.json') as data_file:
            data = json.load(data_file)
            token = data["token"]
    
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("parkhaus", carpark))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()