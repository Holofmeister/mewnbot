import discord
from discord import Client
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
import math
import datetime
import random
import os
from PIL import Image, ImageDraw

class Petting(commands.Cog, name='Petting'):

    def __init__(self, bot):
        self.bot = bot
        print('Petting is loaded.')

    @commands.command(help='pet anything! send a file with the command to pet it or tag someone!')
    async def pet(self, ctx, target=None):
        pet_path = './temp/pet.png'
        hand_path = './assets/hand/'
        mask_path = './assets/hand/mask/'
        if target is None:
            avatar = True
            await ctx.author.avatar_url.save(pet_path)
        else:
            if str(target).startswith('<@!'):
                avatar = True
                user = await self.bot.fetch_user(int(target[3:-1]))
                await user.avatar_url.save(pet_path)
            elif str(target).startswith('<:'):
                avatar = False
                try:
                    emoji = self.bot.get_emoji(int(str(target).split(':')[-1][0:-1]))
                    await emoji.url.save(pet_path)
                except AttributeError:
                    await ctx.send("Sorry, I can't see that emote ; - ; ")
            else:
                avatar = False
                try:
                    await ctx.message.attachments.save(pet_path)
                except:
                    pass

        upload_ = Image.open(pet_path)
        upload_ = upload_.convert('RGBA').resize((112,112))

        # TO DO: Add circular avatars, this code gives an "Images don't match" error code
        if avatar:
            mask_avatar = Image.new('L', (112,112), 0)
            draw = ImageDraw.Draw(mask_avatar)
            draw.ellipse((0,0,112,112), fill=255)
            bg = Image.new('RGBA', (112,112), (0,0,0,0))
            bg.paste(upload_, (0,0), mask_avatar)
        
        final = []
        for i in range(5):
            
            frame = Image.open(f'{hand_path}{i}.png')
            mask = Image.open(f'{mask_path}{i}.png')
            mask = mask.convert('L')
            if i < 3:
                corner = i * 10
                bg = bg.resize((112, 112 - corner))
            else:
                corner = (-i+3)*10
                bg = bg.resize((112, 112 - corner))
            background = Image.new('RGBA', (130,130), (0,0,0,0))
            background.paste(bg, (20, corner + 20))
            background.paste(frame, (0,0), mask)
            final.append(background)

        final[0].save(
            './temp/imagedraw.gif',
            save_all=True,
            append_images=final[1:],
            optimize=False,
            duration=60,
            loop=0,
        )
        attachment = discord.File('./temp/imagedraw.gif', filename='petting.gif')
        await ctx.send(file=attachment)

def setup(bot):
    bot.add_cog(Petting(bot))