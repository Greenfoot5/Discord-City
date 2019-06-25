import sys
import traceback

import discord
from discord.ext import commands


class ErrorHandling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.CommandInvokeError)

        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(error)

        elif isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            seconds = round(seconds, 2)
            return await ctx.send(f"You'll be able to use this command again in **{seconds}** seconds.")

        elif isinstance(error, commands.NotOwner):
            return await ctx.send(error)

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'**{ctx.command}** cannot be used in DMs.')
            except discord.Forbidden:
                return

        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"**{error.param}** is a required argument.")

        elif isinstance(error, discord.Forbidden):
            return await ctx.send("Permition error.")

        elif isinstance(error, commands.BadArgument):
            return await ctx.send(f"Bad argument provided: {error}")

        # Unhandled errors
        print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
        tb = traceback.format_exception(
            type(error), error, error.__traceback__)
        tb = "".join(tb)

        print(tb, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandling(bot))
