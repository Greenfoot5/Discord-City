import discord
from discord.ext import commands


class Info(commands.Cog):
    # TODO: cog help string
    """
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["info"])
    async def about(self, ctx):
        """
        Tells you information about the bot itself.
        """
        # basic info for now
        await ctx.send(self.bot.description)


def setup(bot):
    bot.add_cog(Info(bot))
