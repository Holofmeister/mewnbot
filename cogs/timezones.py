import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
from decouple import config
import json
from pytz import timezone
import pytz
from datetime import datetime, timedelta

MOD_ID = int(config('MOD_ID'))
ADMIN_ID = int(config('ADMIN'))

class Timezone(commands.Cog, command_attrs=dict(hidden=True)):

    def __init__(self, bot):
        self.bot = bot

    async def flag_to_tz(self, emoji):
        with open("countries.json", "r", encoding='utf8') as json_file:
            data = json.loads(json_file.read())
            for i in data:
                if i == str(emoji):
                    return data[i]['abbreviation']

    async def flag_to_name(self, emoji):
        with open("countries.json", "r", encoding='utf8') as json_file:
            data = json.loads(json_file.read())
            for i in data:
                if i == str(emoji):
                    return data[i]['name']
                else:
                    continue

    async def tz_conv(self, tz_in, tz_out, dt):
        time_in = datetime.strptime(dt, '%d/%m/%Y %H:%M')
        return pytz.timezone(tz_in).localize(time_in).astimezone(timezone(tz_out))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        with open('events.json', 'r', encoding='utf8') as j:
            events = json.loads(j.read())

        for i in events:
            print(i)
            print(reaction.message.id)
            if str(i) == reaction.message.id:
                print('true')
                event_time = events[i]['time']
                print(event_time)
            #     break
            # else:
            #     continue
            # with open('countries.json', 'r', encoding='utf8') as j:s



    @commands.command(help='Starts a raffle that ends after a certain amount of minutes.')
    async def timezone(self, ctx, date, time, tz='America/Los_Angeles'):
        time_str = f'{date} {time}'
        time_in = datetime.strptime(time_str, '%d/%m/%Y %H:%M')
        embed=discord.Embed(
            title=f"Time on {tz}:", 
            description= time_str, 
            color=0xff9cbb
        )
        common_tzs = ["America/Los_Angeles", "America/Phoenix", "America/Denver", "America/Chicago"]
        for tz_ in common_tzs:
            embed.add_field(name=tz_, value=pytz.timezone(tz).localize(time_in).astimezone(timezone(tz_)), inline=False)
        event_message = await ctx.send(embed=embed)

        w_json = {}
        w_json[event_message.id] = {'time' : time_str}
        with open('events.json','w', encoding='utf8') as j:
            json.dump(w_json, j, indent=4, ensure_ascii=False)

def setup(bot):
    bot.add_cog(Timezone(bot))
    print('Timezone is loaded.')