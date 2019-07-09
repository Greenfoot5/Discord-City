import discord
from discord.ext import commands
import random
import math
import pickle

'''
Ideas/TODO list. Not command specific
● Increase population based off amount of houses. Random 2-4 pop with 20% chance for 2-7 people
● Have people move in over time
● Add upgrades
● Add Demands (more of this, more of that ect)
● Allow users to see city info easily
● Output the city into an image
● Add a better system for building (backend handling)
● Add custom checks like has_city()
'''

class Mayor(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.buildables = ["road","house","commerical","industrial"]

    @commands.command(name='create',hidden=True)
    async def register(self,ctx,name:str=None):
        if name is None:
            await ctx.send("You haven't chosen a city name!")
            return
        cities = pickle.load(open('data.cities.data','rb'))
        try:
            cities[str(ctx.author.id)]
            await ctx.send("You already have a city!")
            return
        except KeyError:
            cities[str(ctx.author.id)] = {'name':name,'pop':1,'cash':100}
            pickle.dump(cities,open('data.cities.data','wb'))
            await ctx.send("City created")

    @commands.command(name='build',hidden=True)
    @commands.is_owner()
    async def build(self,ctx,item:int=None,amount:int=1):
        if item is None:
            ##TODO - Display it better
            await ctx.send("__**Buildables**__\n**Road** - `0`:£10\n**Residential** - `1`:£0\n**Commercial** - `2`:£0\n**Industrial** - `3`:£0")
            return
        cities = pickle.load(open('data.cities.data','rb'))
        try:
            cities[str(ctx.author.id)]
        except KeyError:
            await ctx.send(f"You haven't got an account yet! Use `{ctx.prefix}create` to make one!")
            return
        #TODO - Build
        #TODO - Take money
        
        if self.buildables[item] == "road":
            try:
                cities[str(ctx.author.id)]['roads'] += amount
            except KeyError:
                cities[str(ctx.author.id)]['roads'] = amount
            pickle.dump(cities,open('data.cities.data','wb'))
            await ctx.send("Built a road")

    @commands.command(name='c-info',hidden=True)
    @commands.is_owner()
    async def city_info(self,ctx):
        cities = pickle.load(open('data.cities.data','rb'))
        try:
            cities[str(ctx.author.id)]
        except KeyError:
            await ctx.send(f"You haven't go a city! Use `{ctx.prefix}create` to create one!")
            return
        #TODO - Add a nice embed
        await ctx.send(f"{cities[str(ctx.author.id)]}")
            
        
    @commands.command(name='reset_cities')
    @commands.is_owner()
    async def kill_all_cities(self,ctx,hidden=True):
        cities = {'id':'Value','id2':'Value2'}
        pickle.dump(cities,open('data.cities.data','wb'))
        await ctx.send("Cities reset.")
        

def setup(bot):
    bot.add_cog(Mayor(bot))
