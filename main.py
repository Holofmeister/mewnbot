import discord
from discord.ext import commands
from discord.ext.commands   import bot
import asyncio
import datetime
import traceback
import random
import os
import json

with open('secret.json', 'r', encoding='utf8') as s:
    secret = json.load(s)
    TOKEN = secret['TOKEN']

with open('server.json', 'r', encoding='utf8') as s:
    credentials = json.load(s)

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

bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('I am online!')

initial_extensions = ['cogs.jokes',
                    'cogs.leveling',
                    'cogs.raffle',
                    'cogs.quotes',
                    'cogs.help',
                    'cogs.challenge'
                    ]

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f'Failed to load extension {extension}')
            traceback.print_exc()

bot.run(TOKEN)