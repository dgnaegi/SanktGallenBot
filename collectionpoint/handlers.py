from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from common.expectations import Expectations
from common.googleMaps import getGoogleMapsLink
from common.models.dataObject import DataObject
from common.stgallenApi import getAPIRecords
from common.nearestObject import getNearestObject
    
def collectionPointDefault(update: Update, context: CallbackContext):
    update.message.reply_text("Bitte sende mir deinen Standort")
    return Expectations.Location

def collectionPointLocation(update: Update, context: CallbackContext):
    location = update.message.location
    lat = location["latitude"]
    long = location["longitude"]
    records = getAPIRecords("sammelstellen")
    collectionPoints = getCollectionPoints(records)
    nearestCollectionPoint = getNearestObject(long, lat, collectionPoints)
    update.message.reply_text("Die nächste Sammelstelle ist " + nearestCollectionPoint.name + " und " + str(nearestCollectionPoint.distanceInKm) + " Kilometer entfernt.")
    googleMapsLink = getGoogleMapsLink(nearestCollectionPoint.lat, nearestCollectionPoint.long)
    update.message.reply_text(googleMapsLink)
    return ConversationHandler.END

def getCollectionPoints(records):
    collectionPoints = []
    for record in records:
        long = record["geometry"]["coordinates"][0]
        lat = record["geometry"]["coordinates"][1]
        name = record["fields"]["standort"]
        collectionPoint = DataObject(long, lat, name, 0)
        collectionPoints.append(collectionPoint)
    return collectionPoints

    