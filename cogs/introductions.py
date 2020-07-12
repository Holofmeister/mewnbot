import discord
from discord.ext import commands
import asyncio
import datetime
import random

class Intros(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        intro_channel = 704403344730357863
        if ctx.channel.id == intro_channel:
            if "https://www.twitch.tv/" or "https://twitch.tv/" in ctx.content:
                return
            
            else:
                await ctx.author.send('hai')
        else:
            return

def setup(bot):
    bot.add_cog(Intros(bot))
    print('Introductions is loaded.')