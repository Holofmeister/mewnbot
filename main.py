import discord
from discord.ext import commands
from discord.ext.commands   import bot
import asyncio
import datetime
import traceback
import random
import os
from decouple import config

TOKEN = config('TOKEN')

bot = commands.Bot(command_prefix='!', case_insensitive=True)
bot.remove_command('help')

#this is a check

@bot.event
async def on_ready():
    print('I am online!')
#    return await bot.change_presence(activity=discord.Activity(type=1, name='',))

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