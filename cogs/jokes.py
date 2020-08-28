import discord
from discord.ext import commands
import asyncio
import datetime
import random

class Jokes(commands.Cog, name='Jokes'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def channel_id(self, ctx):
        print(ctx.channel.id)

    @commands.command(help='AAAAAAAA')
    async def screech(self, ctx):
        await ctx.send(file=discord.File('assets/screech.png'))

    @commands.command(help=':racehorse:')
    async def horse(self, ctx):
        await ctx.send(':racehorse:')
    
    @commands.command(help='Custom manual for Keep Talking and nobody explodes')
    async def bomb(self, ctx):
        await ctx.send('Original manual: https://bombmanual.com/print/KeepTalkingAndNobodyExplodes-BombDefusalManual-v1.pdf \nCustom manual by Chromerian:', file=discord.File('assets/Mooncat_Bomb_Manual_v1.3.pdf'))

    @commands.command(hidden=True)
    async def gosuckit(self, ctx):
        await ctx.send('no u')

    # @commands.command()
    # async def send_message(self,ctx, id, *, content)

    @commands.command(help='butts, what did you expected')
    async def butts(self, ctx):
        await ctx.send('╭━☾ ∙∙∙━━━━━━━∙∙∙☽━╮\n ---- | ) ) b u t t s r n i c e ( ( | ----\n╰━☾∙∙∙━━━✦━━━∙∙∙☽━╯')

    @commands.command(help='thatcommandforthatguy')
    async def thatguyname(self, ctx):
        await ctx.send('Akihiko Yoshida')

    @commands.command(hidden=True)
    async def ignoreme(self, ctx):
        if ctx.author.id == int(253331667731611651):
            await ctx.send('Holof is probably editing the bot and sucking at it, please ignore him.')
        else:
            await ctx.send('You are doing great and deserve recognition, no ignoring for you.')

def setup(bot):
    bot.add_cog(Jokes(bot))
    print('Jokes is loaded.')