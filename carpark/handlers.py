from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from carpark.models.carpark import CarPark
from common.expectations import Expectations
from common.stgallenApi import getAPIRecords
    
def carparkDefault(update: Update, context: CallbackContext):
    update.message.reply_text("Bitte sende mir dein Standort")
    return Expectations.Location

def carparkLocation(update: Update, context: CallbackContext):
    location = update.message.location
    latitude = location["latitude"]
    longitude = location["longitude"]
    update.message.reply_text(latitude)
    update.message.reply_text(longitude)
    records = getAPIRecords("freie-parkplatze-in-der-stadt-stgallen-pls")
    getCarparks(records)
    return ConversationHandler.END

def getCarparks(records):
    for record in records:
        long = record["geometry"]["coordinates"][0]
        lat = record["geometry"]["coordinates"][1]
        name = record["fields"]["phname"]
        freeSpace = record["fields"]["phname"]
        carpark = CarPark(long, lat, name, freeSpace)
        print(carpark.long)

    