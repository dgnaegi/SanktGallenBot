from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext.conversationhandler import ConversationHandler
from common.expectations import Expectations
from disposal.dataStorage.dataAccess import dataAccess
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from disposal.dataStorage.userData import UserData
    
def disposalDefault(update: Update, context: CallbackContext):
    chatId = update.message.chat_id
    disposalAreas = {"A (Winkeln)": "A:" + str(chatId), "B (Lachen)": "B:" + str(chatId), "C (Rosenberg)": "C:" + str(chatId), "D (Rotmonten)": "D:" + str(chatId), "E (Bruggen/Riethüsli)": "E:" + str(chatId), "F (St.Georgen/Notkersegg)": "F:" + str(chatId), "G (Heiligkreuz)": "G:" + str(chatId), "H (Stephanshorn)": "H:" + str(chatId), "I (St.Fiden)": "I:" + str(chatId), "K (Neudorf)": "K:" + str(chatId), "L-OST (Innenstadt Ost)": "L OST:" + str(chatId), "L-WEST (Innenstadt West)": "L WEST:" + str(chatId)}

    keyboards = []
    for key, value in disposalAreas.items():
        keyboards.append([InlineKeyboardButton(key, callback_data=value)])
    reply_markup = InlineKeyboardMarkup(keyboards)
    update.message.reply_text('Wähle deine Entsorgungszone:', reply_markup=reply_markup)
    
    return Expectations.Text

def disposalArea(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    args = query.data.split(":")
    areaCode = args[0]
    chatId = args[1]
    
    userData = UserData(chatId, areaCode)
    dataAccessObject = dataAccess()
    success = dataAccess.saveUserData(dataAccessObject, userData)
    if success:
        query.edit_message_text("Die Erinnerungsmeldung ist erfolgreich eingerichtet. Du wirst nun für Karton- und Papierabfuhr in der Zone {} benachrichtigt. Abmelden kannst du dich jederzeit mittels /stop".format(areaCode))
    else:
        query.edit_message_text("Du hast die Erinnerungsmeldung bereits eingerichtet. Deaktiviere diese zuerst wieder mittels /stop")

    return ConversationHandler.END

def disposalStop(update: Update, context: CallbackContext):
    chatId = update.message.chat_id
    dataAccessObject = dataAccess()
    dataAccessObject.deleteUserData(chatId)
    update.message.reply_text("Du wirst nun nicht mehr bei Karton- und Papierabfuhr benachrichtigt.")
