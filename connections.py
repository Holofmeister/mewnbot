import discord
import asyncio

class Link():

    def __init__(self, table, *values):

        self.values = values
        self.table = table

        try:
            db = mysql.connector.MySQLConnection(**credentials)
            print('Database connected')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
    
    async def write(self, table, *values):

        for value in values:
            