from datetime import datetime
from helper.stgallenApi import stgallenApi
from dataStorage.dataAccess import dataAccess
from helper.bot import bot
import json

with open('../config.json') as data_file:    
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
      messageBot.SendMessage(userDataSet.chatId, "Paper disposal will be tomorrow!")
      sentMessageStGallen = sentMessageStGallen + 1
    if userDataSet.areaCode in todaySGPaperDisposalAreaCodes and datetime.now().hour < 12:
      messageBot.SendMessage(userDataSet.chatId, "Paper disposal is today!") 
      sentMessageStGallen = sentMessageStGallen + 1
    if userDataSet.areaCode in tomorrowSGCardboardDisposalAreaCodes and datetime.now().hour > 12:
      messageBot.SendMessage(userDataSet.chatId, "Cardboard disposal will be tomorrow!")
      sentMessageStGallen = sentMessageStGallen + 1
    if userDataSet.areaCode in todaySGCardboardDisposalAreaCodes and datetime.now().hour < 12:
      messageBot.SendMessage(userDataSet.chatId, "Cardboard disposal is today!") 
      sentMessageStGallen = sentMessageStGallen + 1
  except:
    logf.write("An exception occurred for Area: " + str(userDataSet.areaCode) + "\r\n")

sendLog = open("send.log", "w")
sendLog.write("Sent messages Zurich: " + str(sentMessageZurich) + "\r\n")
sendLog.write("Sent messages St.Gallen: " + str(sentMessageStGallen) + "\r\n")
