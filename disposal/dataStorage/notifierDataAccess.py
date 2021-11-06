import mysql.connector
import json
from dataStorage.userData import UserData

class dataAccess:
    def __init__(self):
        with open('config.json') as data_file:    
            data = json.load(data_file)
            host = data["host"]
            databaseName = data["databaseName"]
            databaseUser = data["databaseUser"] 
            databasePassword = data["databasePassword"]   

        self.mydb = mysql.connector.connect(
            host=host,
            user=databaseUser,
            passwd=databasePassword,
            database=databaseName)
        
        self.mycursor = self.mydb.cursor()
        
    def getUserdata(self):   
        sql = "SELECT * FROM disposalNotificationRegistration WHERE AreaCode IS NOT NULL"
        self.mycursor.execute(sql)   
        rows = self.mycursor.fetchall()

        userDataSets = []

        for row in rows:
            userDataSets.append(UserData(row[0],row[1]))

        self.mycursor.close()
        return userDataSets


        
