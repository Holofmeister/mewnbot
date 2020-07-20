import discord
import os
import json
from datetime import datetime, timedelta
import pytz
from pytz import timezone
from discord.ext import commands

class Events(commands.Cog, name='Event planner'):

    def __init__(self, bot):
        self.bot = bot
        print('Events is loaded.')
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        with open('events.json', 'r', encoding='utf8') as j_read:
            events = json.loads(j_read.read())
        with open('./assets/countries.json', 'r', encoding='utf8') as j_flags:
            flags = json.loads(j_flags.read())
        if str(reaction.message.id) in events:
            if str(reaction.emoji) in flags:
                local_timezones = flags[reaction.emoji]['timezones']
                date = events[str(reaction.message.id)][0]
                time = events[str(reaction.message.id)][1]
                time_str = f'{date} {time}'
                embed=discord.Embed(title=f'Event time: {date} {time}', color=0xff00ff)
                time_in = datetime.strptime(time_str, '%d/%m/%Y %H:%M')
                for local_timezone in local_timezones:
                    embed.add_field(name=local_timezone, value=pytz.timezone('America/Los_Angeles').localize(time_in).astimezone(timezone(local_timezone)))
                await user.send(embed=embed)

    @commands.command()
    async def event(self, ctx, date, time):
        with open('events.json', 'r', encoding='utf8') as j_read:
            events = json.loads(j_read.read())
        await ctx.send('this is an event message')
        embed=discord.Embed(title=f'Event time: {date} {time}', color=0xff00ff)
        embed.set_author(name=f'')
        time_str = f'{date} {time}'
        default_tzs = [
            "America/Los_Angeles",
            "America/Phoenix",
            "America/Denver",
            "America/Chicago",
            "Europe/London",
            "Asia/Tokyo"
        ]
        time_in = datetime.strptime(time_str, '%d/%m/%Y %H:%M')
        for default_tz in default_tzs:
            embed.add_field(name=default_tz, value=pytz.timezone('America/Los_Angeles').localize(time_in).astimezone(timezone(default_tz)))
        embed.set_footer(text=f'React with a flag emote to recieve a DM with your country\'s timezones')
        event_msg = await ctx.send(embed=embed)

        events[event_msg.id] = (date, time)

        with open('events.json', 'w', encoding='utf8') as j_write:
            json.dump(events, j_write, ensure_ascii=False, indent=4)

    @commands.command()
    async def purgeevents(self, ctx):
        purged = {}
        with open('events.json', 'w', encoding='utf8') as j:
            json.dump(purged, j, ensure_ascii=False, indent=4)

def setup(bot):
    bot.add_cog(Events(bot))

