import discord
from discord.ext import commands
import asyncio
import datetime
import sqlite3
import math
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import mysql.connector
from mysql.connector import errorcode
import mysql
import json

with open('secret.json', 'r', encoding='utf8') as s:
    secret = json.load(s)
    BOT_ID = secret['BOT_ID']

with open('server.json', 'r', encoding='utf8') as s:
    credentials = json.load(s)

class Leveling(commands.Cog, name='leveling'):

    def __init__(self, bot):
        self.bot = bot
        print('Leveling is loaded.')

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author.id == BOT_ID:
                return
            else:
                db = mysql.connector.MySQLConnection(**credentials)
                cursor = db.cursor()
                cursor.execute(f"SELECT user_id FROM levels WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
                result = cursor.fetchone()
                if result is None:
                    sql = ("INSERT INTO levels(guild_id, user_id, exp, lvl, public) VALUES(%s,%s,%s,%s,%s)")
                    val = (message.author.guild.id, message.author.id, 2, 1, 1)
                    cursor.execute(sql, val)
                    db.commit()
                else:
                    cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
                    result1 = cursor.fetchone()
                    exp = int(result1[1])
                    sql = ("UPDATE levels SET exp = %s WHERE guild_id = %s and user_id = %s")
                    val = (exp + 2, str(message.guild.id), str(message.author.id))
                    cursor.execute(sql, val)
                    db.commit()
                    
                    cursor.execute(f"SELECT user_id, exp, lvl, public FROM levels WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
                    result2 = cursor.fetchone()

                    xp_start = int(result2[1])
                    lvl_start = int(result2[2])
                    public_u = int(result2[3])
                    xp_end = math.floor(5 * (lvl_start ^ 3) + 50 * lvl_start + 100 )
                    if xp_end < xp_start:
                        if public_u == 1:
                            await message.channel.send(f'{message.author.mention} has leveled up to level {lvl_start + 1}.')
                            sql = ("UPDATE levels SET lvl = %s WHERE guild_id = %s and user_id = %s")
                            val = (int(lvl_start + 1), str(message.guild.id), str(message.author.id))
                            cursor.execute(sql, val)
                            db.commit()
                            sql = ("UPDATE levels SET exp = %s WHERE guild_id = %s and user_id = %s")
                            val = (int(0), str(message.guild.id), str(message.author.id))
                            cursor.execute(sql, val)
                            db.commit()
                            cursor.close()
                            db.close
                        else:
                            sql = ("UPDATE levels SET lvl = %s WHERE guild_id = %s and user_id = %s")
                            val = (int(lvl_start + 1), str(message.guild.id), str(message.author.id))
                            cursor.execute(sql, val)
                            db.commit()
                            sql = ("UPDATE levels SET exp = %s WHERE guild_id = %s and user_id = %s")
                            val = (int(0), str(message.guild.id), str(message.author.id))
                            cursor.execute(sql, val)
                            db.commit()
                            cursor.close()
                            db.close
        except AttributeError:
            print('DM')
    @commands.command(help='Gives lvl and xp of an mentioned user, or the author of the message.')
    async def rank(self, ctx, user:discord.User=None):
        if user is not None:
            db = mysql.connector.MySQLConnection(**credentials)
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.message.author.guild.id}' and user_id = '{user.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send("That user is not yet ranked.")
            else:
                nivel = int(result[2])
                
                nxtlvl1 = math.floor(5 * ( nivel ^ 3) + 50 * nivel + 100 )
                tolvl1 = math.floor(nxtlvl1 - int(result[1]))
                
                avatar_url = user.avatar_url
                await avatar_url.save('./temp/avatar.png')

                avatar = Image.open('./temp/avatar.png').resize((270, 270))

                template = Image.open('./assets/template.png')
                template_copy = template.copy()

                mask_img = Image.open('./assets/mask.png').resize(avatar.size).convert('L')

                template_copy.paste(avatar, (39,36), mask_img)
                
                exp = int(result[1])
                ammount = exp / (5 * ( nivel ^ 3) + 50 * nivel + 100)
                final_ammount = 50 + ammount * 1400
                draw = ImageDraw.Draw(template_copy)
                draw.line((50, 440, final_ammount, 440), fill=(71, 143, 252), width=60)

                font = ImageFont.truetype(r'./assets/tnr.ttf', 90)
                font_2 = ImageFont.truetype(r'./assets/tnr.ttf', 110)
                fill = (0, 0, 0)
                align = "center"

                # name
                draw.text((350,50), user.name, fill= fill, font = font_2, align = align)
                # exp
                draw.text((1175,168), str(result[1]), fill= fill, font = font, align = align)
                # nxt_lvl
                draw.text((1175,283), str(tolvl1), fill= fill, font = font, align = align)
                # Level
                draw.text((555,283), str(result[2]), fill= fill, font = font, align = align)

                template_copy.save('./temp/final.png')
                await ctx.send(file=discord.File('./temp/final.png'))

            cursor.close()
            db.close()
        else:
            db = mysql.connector.MySQLConnection(**credentials)
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.message.author.guild.id}' and user_id = '{ctx.message.author.id}'")
            result = cursor.fetchone()
            if result is None:
                await ctx.send("That user is not yet ranked.")
            else:
                nivel = int(result[2])
                nxtlvl2 = math.floor(5 * ( nivel ^ 3) + 50 * nivel + 100 )
                tolvl2 = math.floor(nxtlvl2 - int(result[1]))

                avatar_url = ctx.message.author.avatar_url
                await avatar_url.save('./temp/avatar.png')

                avatar = Image.open('./temp/avatar.png').resize((270, 270))

                template = Image.open('./assets/template.png')
                template_copy = template.copy()

                mask_img = Image.open('./assets/mask.png').resize(avatar.size).convert('L')

                template_copy.paste(avatar, (39,36), mask_img)
                
                exp = int(result[1])
                ammount = exp / (5 * ( nivel ^ 3) + 50 * nivel + 100)
                final_ammount = 50 + ammount * 1400
                draw = ImageDraw.Draw(template_copy)
                draw.line((50, 440, final_ammount, 440), fill=(71, 143, 252), width=60)

                font = ImageFont.truetype(r'./assets/tnr.ttf', 90)
                font_2 = ImageFont.truetype(r'./assets/tnr.ttf', 110)
                fill = (0, 0, 0)
                align = "center"

                # name
                draw.text((350,50), ctx.author.name, fill= fill, font = font_2, align = align)
                # exp
                draw.text((1175,168), str(result[1]), fill= fill, font = font, align = align)
                # nxt_lvl
                draw.text((1175,283), str(tolvl2), fill= fill, font = font, align = align)
                # Level
                draw.text((555,283), str(result[2]), fill= fill, font = font, align = align)

                template_copy.save('./temp/final.png')
                await ctx.send(file=discord.File('./temp/final.png'))
            cursor.close()
            db.close()

    @commands.command(help='If true, makes the author private')
    async def private(self, ctx, status : str = 'on'):
        if ctx.guild_id is None:
            guild = str(215011552141639681)
        else:
            guild = ctx.guild_id
        if status in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
            db = mysql.connector.MySQLConnection(**credentials)
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id FROM levels WHERE guild_id = '{ctx.author.guild.id}' and user_id = '{ctx.author.id}'")
            sql = ("UPDATE levels SET public = %s WHERE guild_id = %s and user_id is %s")
            val = (int(0), guild, str(ctx.author.id))
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close
            await ctx.send(f"{ctx.author.name} is now private.")
        else:
            db = mysql.connector.MySQLConnection(**credentials)
            cursor = db.cursor()
            cursor.execute(f"SELECT user_id FROM levels WHERE guild_id = '{ctx.author.guild.id}' and user_id = '{ctx.author.id}'")
            sql = ("UPDATE levels SET public = %s WHERE guild_id = %s and user_id is %s")
            val = (int(1), guild, str(ctx.author.id))
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close
            await ctx.send(f"{ctx.author.name} is now public.")

def setup(bot):
    bot.add_cog(Leveling(bot))