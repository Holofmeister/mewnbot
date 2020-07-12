import discord
from discord.ext import commands
import asyncio
import datetime
import random
import sqlite3
import sys
from PIL import Image, ImageDraw, ImageFont

class Challenge(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def character_generator(self):
        filenames = ['./assets/challenge/species.txt', #choices[0]
                     './assets/challenge/mooncat_type.txt', #choices[1]
                     './assets/challenge/item.txt', #choices[2]
                     './assets/challenge/personality.txt', #choices[3]
                     './assets/challenge/hair.txt', #choices[4]
                     './assets/challenge/skin.txt', #choices[5]
                     './assets/challenge/jobs_1.txt', #choices[6] }JOB
                     './assets/challenge/jobs_2.txt', #choices[7] }JOB
                     './assets/challenge/jobs_3.txt', #choices[8] }JOB
                     './assets/challenge/jobs_4.txt'] #choices[9] }JOB
        files = {}
        for filename in filenames:
            with open(filename, "r") as file:
                if filename in files:
                    continue
                files[filename] = file.read().splitlines()

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
        db = sqlite3.connect('challenge.sqlite')
        cursor = db.cursor()
        if not arg:
            cursor.execute(f'SELECT NAME, ID, CHARA FROM CHARACTERS WHERE ID = {ctx.author.id}')
            result = cursor.fetchone()
            if result is None:
                chara = await self.character_generator()
                sql = (f'INSERT INTO CHARACTERS(NAME, ID, CHARA) VALUES(?, ?, ?)')
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
                sql = (f'INSERT INTO CHARACTERS(NAME, ID, CHARA) VALUES(?, ?, ?)')
                val = (str(ctx.author.name), str(ctx.author.id), chara)
                cursor.execute(sql, val)
                db.commit()
            else:
                chara = await self.character_generator()
                sql = ('UPDATE CHARACTERS SET CHARA = ? WHERE ID = ?')
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