import discord
from discord.ext import commands
import asyncio
import datetime
import random

class Help(commands.Cog, name='help'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='u ok?')
    async def help(self, ctx, *cog):
        if not cog:
            embed = discord.Embed(description='Use !help (category) to list commands', color=0xff9cbb)
            cog_desc = ''
            for x in self.bot.cogs:
#                cog_desc += f'{x} - {self.bot.cogs[x].__doc__}\n'
                cog_desc += f'{x}\n'
            embed.add_field(name='Command categories:', value=cog_desc)
            await ctx.send(embed=embed)
        else:
            if len(cog) > 1:
                embed = discord.Embed(Title='Error', description='Too many cogs!')
                await ctx.send(embed=embed)
            else:
                found = False
                for x in self.bot.cogs:
                    for y in cog:
                        if x == y:
                            embed = discord.Embed(color=0xff9cbb)
                            scog_info = ''
                            for c in self.bot.get_cog(y).get_commands():
                                if not c.hidden:
                                    scog_info += f'!{c.name} - {c.help}\n'
                            embed.add_field(name=f'{cog[0]} category', value=scog_info)
#                            embed.add_field(name=f'{cog[0]} category - {self.bot.cogs[cog[0]].__doc__}', value=scog_info)
                            found = True
                if not found:
                    for x in self.bot.cogs:
                        for c in self.bot.get_cog(x).get_commands():

                            if c.name == cog[0]:
                                embed = discord.Embed(color=0xff9cbb)
                                embed.add_field(name=f'!{c.name} - {c.help}', value=f'Proper Syntax:\n{c.qualified_name} {c.signature}')
                        found = True
                    if not found:
                        embed = discord.Embed(title='Error!', description='we couldn\'t find that command')
                
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
    print('Help is loaded.')