from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from common.models.dataObject import DataObject
from common.expectations import Expectations
from common.googleMaps import getGoogleMapsLink
from common.stgallenApi import getAPIRecords
from common.nearestObject import getNearestObject
    
def carparkDefault(update: Update, context: CallbackContext):
    update.message.reply_text("Bitte sende mir deinen Standort")
    return Expectations.Location

def carparkLocation(update: Update, context: CallbackContext):
    location = update.message.location
    lat = location["latitude"]
    long = location["longitude"]
    records = getAPIRecords("freie-parkplatze-in-der-stadt-stgallen-pls")
    carparks = getFreeCarParks(records)
    nearestCarPark = getNearestObject(long, lat, carparks)
    update.message.reply_text("Das nächste Parkhaus ist " + nearestCarPark.name + ", ist " + str(nearestCarPark.distanceInKm) + " Kilometer entfernt und verfügt über " + str(nearestCarPark.freeSpace) + " freie Plätze!")
    googleMapsLink = getGoogleMapsLink(nearestCarPark.lat, nearestCarPark.long)
    update.message.reply_text(googleMapsLink)
    return ConversationHandler.END

def getFreeCarParks(records):
    carParks = []
    for record in records:
        long = record["geometry"]["coordinates"][0]
        lat = record["geometry"]["coordinates"][1]
        name = record["fields"]["phname"]
        freeSpace = record["fields"]["shortfree"]
        carPark = DataObject(long, lat, name, freeSpace)
        if(carPark.freeSpace > 0):
            carParks.append(carPark)
    return carParks

    