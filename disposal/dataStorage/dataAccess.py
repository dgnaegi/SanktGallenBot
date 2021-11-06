import mysql.connector
import json


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
               
    def saveUserData(self, UserData):
        query = "SELECT * FROM disposalNotificationRegistration WHERE ChatId = %s"    
        data = (UserData.chatId,)       
        self.mycursor.execute(query, data) 
        rows = self.mycursor.fetchall()

        if len(rows) > 0:
            return False

        sql = "INSERT INTO disposalNotificationRegistration (ChatId, AreaCode) VALUES (%s, %s)"
        val = (UserData.chatId, UserData.areaCode)
        self.mycursor.execute(sql, val)    
        self.mydb.commit()

        if self.mycursor.rowcount > 0:
            self.mycursor.close()
            return True
        else:
            self.mycursor.close()
            return False

    def getUserdata(self):  
        sql = "SELECT * FROM disposalNotificationRegistration WHERE AreaCode IS NOT NULL"
        self.mycursor.execute(sql)   
        rows = self.mycursor.fetchall()

        userDataSets = []

        for row in rows:
            userDataSets.append(UserData(row[0],row[1]))

        self.mycursor.close()
        return userDataSets

    def deleteUserData(self,chatId):          
        query = "DELETE FROM disposalNotificationRegistration WHERE ChatId = %s"    
        data = (chatId,)        
        self.mycursor.execute(query, data)      
        self.mydb.commit()        
        self.mycursor.close()


        
