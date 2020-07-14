import discord
from discord.ext import commands
from discord.ext.commands import bot
import asyncio
import math
import datetime
import random
import os

with open('secret.json', 'r', encoding='utf8') as s:
    secret = json.load(s)
    MOD_ID = int(secret['MOD_ID'])
    ADMIN_ID = int(secret['ADMIN'])

class Quotes(commands.Cog, name='quotes'):

    def __init__(self, bot):
        self.bot = bot
        print('Quotes is loaded.')
    
    async def is_mod(ctx):
            if MOD_ID in [role.id for role in ctx.author.roles] or ctx.author.id == ADMIN_ID:
                print('Access granted')
                return True
            else:
                await ctx.send("You don't have permission to use this command.")
                print('Access Denied')
                return False    
    
    @commands.command(help='Gems from our community, with all the needed context.')
    async def quote(self, ctx, *rqst : str):
        with open("assets/quotes.txt", encoding="utf8") as f:
            quotes = f.read().splitlines()
            if not rqst:
                for x in range(10):
                    rnd_quote = random.choice(quotes)
                    if rnd_quote != '':
                        break
                    else:
                        continue
                await ctx.send(rnd_quote)
            else:
                request = int(rqst[0]) - 1
                rqst_quote = quotes[request]
                if  rqst_quote != '':
                    await ctx.send(rqst_quote)
                else:
                    await ctx.send('Sorry, that quote is not available.')
        
    @commands.command(hidden=True)
    @commands.check(is_mod)
    async def addquote(self, ctx, user, *, quote : str):
        print(ctx.author.id)
        quotes = open("assets/quotes.txt", encoding="utf8").read().splitlines()
        quotes_a = open("assets/quotes.txt", "a" ,encoding="utf8,")
        number = len(quotes) + 1
        date = datetime.date.today()
        quotes_a.write(f'\n#{number}: "{quote}" -{user} ({date})')
        await ctx.send(f'Successfully added as quote {number}')


    @commands.command(hidden=True)
    @commands.check(is_mod)
    async def sortquotes(self, ctx):
        with open("assets/quotes.txt", mode='r', encoding="utf8") as f:
            quotes = f.read().splitlines()
            index = range(1, len(quotes))
            quotes_tuple = list(zip(index, quotes))
            rearranged = []
            for i in quotes_tuple:
                if i[1] == '':
                    continue
                else:
                    digits = len(str(i[0])) + 3
                    quote = i[1][digits : :]
                    rearranged.append(quote)
                    continue
            r_index = range(1, len(rearranged))
            rearranged_tuple = list(zip(r_index, rearranged))
            final = ''
            for x in rearranged_tuple:
                final += f'#{x[0]}: {x[1]}\n'
            print(final)
            f.close()

        with open("assets/quotes.txt", mode='w', encoding="utf8") as f:
            f.write(final)
            f.close()
        
        await ctx.send("Quotes have been sorted")
        
        

    @commands.command(hidden=True)
    @commands.check(is_mod)
    async def delquote(self, ctx, quote : int):
        file = open("assets/quotes.txt", encoding="utf8")
        quotes = file.read().splitlines()
        quotes[quote -1] = ''
        final = ''
        for i in quotes:
            final += f'{i}\n'

        file.write(final)

        await ctx.send(f'Successfully deleted quote {quote}')

    
    @commands.command(hidden=True)
    @commands.check(is_mod)
    async def changequotes(self, ctx, confirmation=None):
        if confirmation is None:
            await ctx.send('This command replaces the whole quotes list with the .txt you send, please make sure the file you are uploading is correct and use the command "!changequotes submit" to change it.\n Send the file along with the command\n "!changequotes current" sends the current version of the quotes')
        elif confirmation == 'submit':
            os.rename('./assets/quotes.txt', f'./assets/quotes_backup.txt')
            for attachment in ctx.message.attachments:
                await attachment.save('./assets/quotes.txt')
        elif confirmation == 'current':
            await ctx.send(file=discord.File('./assets/quotes.txt'))
    
    @commands.command(help="Useful for when you wanna embarrass your friends, but don't remember the quote number")
    async def findquote(self, ctx, *, search : str):
        try:
            quotes = open("assets/quotes.txt", encoding="utf8").read().splitlines()
            quotes_lower = [item.lower() for item in quotes]
            search_lower = search.lower()
            matches = []
            matches = [rst for rst in quotes_lower if search_lower in rst]
            matches_index = []
            for match in matches:
                matches_index.append(quotes_lower.index(match))
            message = ''
            for match_index in matches_index:
                message += f'{quotes[match_index]}\n'
            await ctx.send(message)
        except:
            await ctx.send("Anyway, how's your sex life?")

def setup(bot):
    bot.add_cog(Quotes(bot))