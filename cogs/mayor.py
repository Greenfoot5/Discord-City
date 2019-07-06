import discord
from discord.ext import commands
import random
import math

class Mayor(commands.Cog):

    def __init__(self,bot):
    self.bot = bot

    @commands.command(name='create')
    @commands.is_owner()
    async def register(self,ctx):
        print("User registering")

def setup(bot):
    bot.add_cog(Mayor(bot))
