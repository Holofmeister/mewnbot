import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
import datetime
import random

class Raffle(commands.Cog, name='mods', command_attrs=dict(hidden=True)):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(help='Starts a raffle that ends after a certain amount of minutes.')
    async def raffle(self, ctx, *, time):
        custom_emoji = self.bot.get_emoji(705858599423049800)
        embed=discord.Embed(
            title="    - - - - - -  ☾ 𝚁𝙰𝙵𝙵𝙻𝙴 𝚂𝚃𝙰𝚁𝚃𝙸𝙽𝙶 ☽  - - - - - -", 
            description=f"Starts now! React to this with {custom_emoji} to participate, ends in {time} minutes.", 
            color=0xff9cbb
        )
        rfl_message = await ctx.send(embed=embed) 
        await rfl_message.add_reaction(emoji=f"{custom_emoji}")
        final_time = int(time) * int(60)
        await asyncio.sleep(final_time)
        customemoji = self.bot.get_emoji(705858599423049800)
        reactions = [f'{customemoji}']
        cached_msg = await ctx.fetch_message(rfl_message.id)
        reactlist = cached_msg.reactions
        bot.userlist = []

        for reactions in reactlist:
            async for users in reactions.users():
                bot.userlist.append(users)

        winner = random.choice(bot.userlist)

        await ctx.send(f'{winner.mention} won the raffle!')

def setup(bot):
    bot.add_cog(Raffle(bot))
    print('Raffle is loaded.')