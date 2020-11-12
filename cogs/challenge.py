import discord
from discord.ext import commands
import asyncio
import datetime
import random
import sys
from PIL import Image, ImageDraw, ImageFont
import mysql.connector
from mysql.connector import errorcode
import mysql
import json

with open('server.json', 'r', encoding='utf8') as s:
    credentials = json.load(s)

def json_generator():
    directory = './assets/challenge/'
    filenames = ['species',#choices[0]
        'mooncat_type',#choices[1]
        'item',#choices[2]
        'personality',#choices[3]
        'hair',#choices[4]
        'skin',#choices[5]
        'jobs_1',#choices[6]
        'jobs_2',#choices[7]
        'jobs_3',#choices[8]
        'jobs_4']#choices[9]
    files = {}
    for filename in filenames:
        with open(f'{directory}{filename}.txt', "r") as file:
            files[filename] = file.read().splitlines()
    with open('./temp/characters.json', 'w', encoding='utf8') as f:
        json.dump(files, f,  ensure_ascii=False, indent=4)

class Challenge(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, json_generator)
        
    async def character_generator(self):
        
        with open('./temp/characters.json', 'r',encoding='utf8') as f:
            files = json.loads(f.read())

        # Takes a seed and gives out a choice list with an item from each category.
        choices = []
        for category in files:
            choices.append(random.choice(files[category]))

        # Filters out category and retrieves a different job choice if the character is a mooncat.
        job = 'invalid value'
        sp = choices[0]
        if sp.startswith('Mooncat'):
            if sp.endswith('Warrior'):
                job = choices[7]
                pass
            elif sp.endswith('Mystic'):
                job = choices[6]
                pass
            elif sp.endswith('Pacifist'):
                job = choices[8]
                pass
            mooncat_type = f'\nType: {choices[1]}'
            pass
        else:
            job = choices[9]
            mooncat_type = ''
            pass
        
        choices_str = ''
        for choice in choices[0 : 6]:
            choices_str += f'{choice}$'

        choices_str += f'{mooncat_type}$'
        choices_str += f'{job}$'
        
        return choices_str
    
    async def list_converter(self, string : str):
        lst = list(string.split("$"))
        return lst
       
    @commands.command()
    async def challenge(self,ctx,*arg):
        db = mysql.connector.MySQLConnection(**credentials)
        cursor = db.cursor()
        if not arg:
            cursor.execute(f'SELECT NAME, ID, CHARA FROM CHARACTERS WHERE ID = {ctx.author.id}')
            result = cursor.fetchone()
            if result is None:
                chara = await self.character_generator()
                sql = (f'INSERT INTO CHARACTERS(NAME, ID, CHARA) VALUES(%s, %s, %s)')
                val = (str(ctx.author.name), str(ctx.author.id), chara)
                cursor.execute(sql, val)
                db.commit()
            else:
                chara = result[2]

        elif arg[0] == 'reroll':
            cursor.execute(f'SELECT NAME, ID, CHARA FROM CHARACTERS WHERE ID = {ctx.author.id}')
            result = cursor.fetchone()
            if result is None:
                chara = await self.character_generator()
                sql = (f'INSERT INTO CHARACTERS(NAME, ID, CHARA) VALUES(%s, %s, %s)')
                val = (str(ctx.author.name), str(ctx.author.id), chara)
                cursor.execute(sql, val)
                db.commit()
            else:
                chara = await self.character_generator()
                sql = ('UPDATE CHARACTERS SET CHARA = %s WHERE ID = %s')
                val = (chara, str(ctx.author.id))
                cursor.execute(sql, val)
                db.commit()
                
        db.close()
        ch = await self.list_converter(chara)

        # Generates an image of size (150, 150) 
        thumbnail = Image.new('RGBA', (150, 150), ch[5])
        draw = ImageDraw.Draw(thumbnail)
        draw.polygon([(0,0), (0, 75), (150, 75), (150, 0)], fill=(ch[4]))
        font = ImageFont.truetype('./assets/tnr.ttf', 40)
        draw.text((35, 10), text='Hair', alignment='Center', font=font, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
        draw.text((35, 85), text='Skin', alignment='Center', font=font, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
        thumbnail.save('./temp/thumbnail.png')

        # Makes sure that the if the users name ends with "s" and if it does it just adds a " ' "
        if ctx.author.name.endswith('s'):
            ap = "'"
        else:
            ap = "'s"

        # Create embed
        file = discord.File("./temp/thumbnail.png", filename="thumbnail.png")
        embed=discord.Embed(title=f'Species: {ch[0]}{ch[6]}', color=0xff00ff)
        embed.set_author(name=f'{ctx.author.name}{ap} character')
        embed.set_thumbnail(url="attachment://thumbnail.png")
        embed.add_field(name='Job:', value=f'{ch[7]}', inline=True)
        embed.add_field(name='Personality:', value=f'{ch[3]}', inline=True)
        embed.add_field(name='Item:', value=f'{ch[2]}', inline=False)
        embed.add_field(name='Colors:', value=f'Hair color: {ch[4]}\nSkin color: {ch[5]}', inline=False)
        embed.set_footer(text=f'Use !challenge reroll to change your character')
        await ctx.send(file=file, embed=embed)

def setup(bot):
    bot.add_cog(Challenge(bot))
    print('Challenge is loaded.')