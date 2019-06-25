import discord
from discord.ext import commands


class HelpCommand(commands.MinimalHelpCommand):
    def get_opening_note(self):
        command_name = self.invoked_with
        return "Use `{0}{1} [command]` for more info on a command.\n" \
               "You can also use `{0}{1} [Category]` for more info on a category.".format(self.clean_prefix, command_name)

    def get_command_signature(self, command):
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            aliases = '|'.join(command.aliases)
            fmt = f'[{command.name}|{aliases}]'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{alias} {command.signature}'

    def add_command_formatting(self, command):
        if command.description:
            self.paginator.add_line(command.description, empty=True)

        signature = self.get_command_signature(command)
        self.paginator.add_line(signature, empty=True)

        if command.help:
            try:
                self.paginator.add_line(command.help, empty=True)
            except RuntimeError:
                for line in command.help.splitlines():
                    self.paginator.add_line(line)
                self.paginator.add_line()

    def add_bot_commands_formatting(self, commands, heading):
        if commands:
            # U+2022 Bullet
            joined = ' \U00002022 '.join(c.name for c in commands)
            self.paginator.add_line(f'__**{heading}**__')
            self.paginator.add_line(joined)


class Info(commands.Cog):
    # TODO: cog help string
    """
    """

    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = HelpCommand()
        bot.help_command.cog = self

    @commands.command(aliases=["info"])
    async def about(self, ctx):
        """
        Tells you information about the bot itself.
        """
        # basic info for now
        await ctx.send(self.bot.description)

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


def setup(bot):
    bot.add_cog(Info(bot))
