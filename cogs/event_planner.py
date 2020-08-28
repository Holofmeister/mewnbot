import discord
import os
import json
from datetime import datetime, timedelta
import pytz
from pytz import timezone
from discord.ext import commands

with open('secret.json', 'r', encoding='utf8') as s:
    secret = json.load(s)
    MOD_ID = int(secret['MOD_ID'])
    ADMIN_ID = int(secret['ADMIN'])

class Events(commands.Cog, name='Event'):

    def __init__(self, bot):
        self.bot = bot
        print('Events is loaded.')
    
    async def is_mod(ctx):
        if not ctx.guild:
            if ctx.author.id == ADMIN_ID:
                return True
            else:
                await ctx.send("You don't have permission to use this command.")
                return False
        else:
            if MOD_ID in [role.id for role in ctx.author.roles] or ctx.author.id == ADMIN_ID:
                return True
            else:
                await ctx.send("You don't have permission to use this command.")
                return False
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        print(payload)
        reaction = payload.emoji.name #emoji
        user = await self.bot.fetch_user(payload.user_id)
        with open('events.json', 'r', encoding='utf8') as j_read:
            events = json.loads(j_read.read())
        with open('./assets/countries.json', 'r', encoding='utf8') as j_flags:
            flags = json.loads(j_flags.read())
        if str(payload.message_id) in events:
            if str(payload.emoji.name) in flags:
                local_timezones = flags[payload.emoji.name]['timezones']
                date = events[str(payload.message_id)]['date']
                time = events[str(payload.message_id)]['time']
                timezone_object = pytz.timezone(events[str(payload.message_id)]['timezone'])
                time_str = f'{date} {time}'
                embed=discord.Embed(title=f'Event time: {date} {time}', color=0xff00ff)
                time_in = datetime.strptime(time_str, '%d/%m/%Y %H:%M')
                for local_timezone in local_timezones:
                    embed.add_field(name=local_timezone, value=str(timezone_object.localize(time_in).astimezone(timezone(local_timezone)))[0:19])
                await user.send(embed=embed)

    @commands.command()
    async def event(self, ctx, date, time, *, timezone_input = 'America/Los_Angeles'):
        try:
            with open('events.json', 'r', encoding='utf8') as j_read:
                events = json.loads(j_read.read())
        except FileNotFoundError:
            with open('events.json', 'w', encoding='utf8') as j_write:
                json.dump({}, j_write, ensure_ascii=False, indent=4)
            with open('events.json', 'r', encoding='utf8') as j_read:
                events = json.loads(j_read.read())

        common_tz = {
                    'PDT' :"America/Los_Angeles",
                    'MDT' :"America/Denver",
                    'CDT' :"America/Chicago",
                    'EDT' :"America/New_York",
                    'MST' :"America/Phoenix",
                    'CEST':"Europe/Madrid",
                    'BST' :"Europe/London",
                    'JST' :"Asia/Tokyo"
                    }

        timezone_input = timezone_input.replace(' ', '_')

        if timezone_input in common_tz:
            timezone_input = common_tz[timezone_input]
        
        if timezone_input in pytz.all_timezones:
            timezone_object = pytz.timezone(timezone_input)
            embed=discord.Embed(title=f'Event time: {date} {time}', color=0xff00ff)

            time_str = f'{date} {time}'
            
            default_tzs = [
                "America/Los_Angeles",
                "America/Phoenix",
                "America/Denver",
                "America/Chicago",
                "America/New_York",
                "Europe/London",
                "Asia/Tokyo"
            ]

            time_in = datetime.strptime(time_str, '%d/%m/%Y %H:%M')
            for default_tz in default_tzs:
                embed.add_field(name=default_tz.replace('_', ' '), value=str(timezone_object.localize(time_in).astimezone(timezone(default_tz))).replace('-', '/')[0:16])
            embed.set_footer(text=f'React with a flag emote to recieve a DM with your country\'s timezones')
            event_msg = await ctx.send(embed=embed)

            events[event_msg.id] = {'date': date, 'time': time, 'timezone': timezone_input}

            with open('events.json', 'w', encoding='utf8') as j_write:
                json.dump(events, j_write, ensure_ascii=False, indent=4)
        else:
            await ctx.send('Please use a timezone in the format of \"America/Los Angeles\"')

    @commands.command()
    @commands.check(is_mod)
    async def purgeevents(self, ctx):
        with open('events.json', 'w', encoding='utf8') as j:
            json.dump({}, j, ensure_ascii=False, indent=4)

def setup(bot):
    bot.add_cog(Events(bot))