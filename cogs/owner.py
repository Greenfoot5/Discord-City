import discord
from discord.ext import commands
import asyncio
from asyncio.subprocess import PIPE, STDOUT


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

    @commands.command()
    @commands.is_owner()
    async def shutdown(self,ctx):
        #give shutdown command via cmd
        #temp via file
        open("shutdown", "a").close()
        await self.bot.close()

    @commands.command()
    @commands.is_owner()
    async def update(self, ctx):
        """
        Pulls files from github.
        """
        async with ctx.typing():
            p = await asyncio.create_subprocess_shell(
                "git pull",
                stdin=PIPE,
                stdout=PIPE,
                stderr=STDOUT
            )
            stdout, stderr = await p.communicate()
            code = p.returncode

            if stdout:
                stdout = stdout.decode("utf-8")
            if stderr:
                stderr = stderr.decode("utf-8")

            if stderr:
                out = f"stdout:\n{stdout}\nstderr:\n{stderr}\n\nReturn code: {code}"
            else:
                out = stdout
                if not code:
                    out = f"stdout:\n{stdout}\nstderr:\n{stderr}\n\nReturn code: {code}"

            await ctx.send(out)


    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        """
        Restarts the bot and pulls from github
        """
        await self.bot.close()


def setup(bot):
    bot.add_cog(Owner(bot))
