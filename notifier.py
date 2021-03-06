from datetime import datetime
from disposal.dataStorage.dataAccess import dataAccess
from disposal.helper.stgallenApi import stgallenApi
from disposal.helper.bot import bot
import json

with open('config.json') as data_file:    
    data = json.load(data_file)
    token = data["token"]

messageBot = bot(token)
logf = open("error.log", "w")

sentMessageZurich = 0

dataAccessObject = dataAccess()
sgUserDataSets = dataAccess.getUserdata(dataAccessObject)

tomorrowSGPaperDisposalAreaCodes = stgallenApi.GetTomorrowPaperDisposalAreaCodes()
todaySGPaperDisposalAreaCodes = stgallenApi.GetTodayPaperDisposalAreaCodes()

tomorrowSGCardboardDisposalAreaCodes = stgallenApi.GetTomorrowCardboardDisposalAreaCodes()
todaySGCardboardDisposalAreaCodes = stgallenApi.GetTodayCardboardDisposalAreaCodes()

sentMessageStGallen = 0

for userDataSet in sgUserDataSets:
  try:
    if userDataSet.areaCode in tomorrowSGPaperDisposalAreaCodes and datetime.now().hour > 12:
      messageBot.SendMessage(userDataSet.chatId, "Morgen ist Papierabfuhr!")
      sentMessageStGallen = sentMessageStGallen + 1
    if userDataSet.areaCode in todaySGPaperDisposalAreaCodes and datetime.now().hour < 12:
      messageBot.SendMessage(userDataSet.chatId, "Heute ist Papierabfuhr!") 
      sentMessageStGallen = sentMessageStGallen + 1
    if userDataSet.areaCode in tomorrowSGCardboardDisposalAreaCodes and datetime.now().hour > 12:
      messageBot.SendMessage(userDataSet.chatId, "Morgen ist Kartonabfuhr!")
      sentMessageStGallen = sentMessageStGallen + 1
    if userDataSet.areaCode in todaySGCardboardDisposalAreaCodes and datetime.now().hour < 12:
      messageBot.SendMessage(userDataSet.chatId, "Heute ist Kartonabfuhr!") 
      sentMessageStGallen = sentMessageStGallen + 1
  except:
    logf.write("An exception occurred for Area: " + str(userDataSet.areaCode) + "\r\n")

sendLog = open("send.log", "w")
sendLog.write("Sent messages Zurich: " + str(sentMessageZurich) + "\r\n")
sendLog.write("Sent messages St.Gallen: " + str(sentMessageStGallen) + "\r\n")
