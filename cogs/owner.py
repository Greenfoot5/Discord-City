import discord
from discord.ext import commands


class Owner(commands.Cog):
    """
    Owner only commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, ext):
        """
        Loads an extention.
        """
        try:
            self.bot.load_extension(ext)
        except Exception as e:
            await ctx.send(f"Error:\n```fix\n{type(e).__name__}: {e}\n```")
        else:
            await ctx.send("\N{WHITE HEAVY CHECK MARK}")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, ext):
        """
        Unloads an extention.
        """
        try:
            self.bot.unload_extension(ext)
        except Exception as e:
            await ctx.send(f"Error:\n```fix\n{type(e).__name__}: {e}\n```")
        else:
            await ctx.send("\N{WHITE HEAVY CHECK MARK}")

    @commands.command(aliases=["rl"])
    @commands.is_owner()
    async def reload(self, ctx, ext):
        """
        Reloads an extention.
        """
        try:
            self.bot.reload_extension(ext)
        except Exception as e:
            await ctx.send(f"Error:\n```fix\n{type(e).__name__}: {e}\n```")
        else:
            await ctx.send("\N{WHITE HEAVY CHECK MARK}")


def setup(bot):
    bot.add_cog(Owner(bot))
