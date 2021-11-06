from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from common.expectations import Expectations
from common.googleMaps import getGoogleMapsLink
from common.models.dataObject import DataObject
from common.nearestObject import getNearestObject
from common.stgallenApi import getKantonAPIRecords
    
def chargingStationDefault(update: Update, context: CallbackContext):
    update.message.reply_text("Bitte sende mir deinen Standort")
    return Expectations.Location

def chargingStationLocation(update: Update, context: CallbackContext):
    location = update.message.location
    lat = location["latitude"]
    long = location["longitude"]
    records = getKantonAPIRecords("ladestationen-fur-elektroautos-im-kanton-stgallen")
    chargingStations = getChargingStations(records)
    nearestChargingStation = getNearestObject(long, lat, chargingStations)
    update.message.reply_text("Die nächste Ladestation ist an der " + nearestChargingStation.name + " und " + str(nearestChargingStation.distanceInKm) + " Kilometer entfernt.")
    googleMapsLink = getGoogleMapsLink(nearestChargingStation.lat, nearestChargingStation.long)
    update.message.reply_text(googleMapsLink)
    return ConversationHandler.END

def getChargingStations(records):
    chargingStations = []
    for record in records:
        long = record["geometry"]["coordinates"][0]
        lat = record["geometry"]["coordinates"][1]
        name = record["fields"]["address_street"]
        chargingStation = DataObject(long, lat, name, 0)
        chargingStations.append(chargingStation)
    return chargingStations

    