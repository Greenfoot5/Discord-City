import discord
from discord.ext import commands
import pickle
import sys, traceback

def get_prefix(bot, message):

    if not message.guild:
        return ['asfajaskdaj']

    else:
        prefix = ['.']

    return commands.when_mentioned_or(*prefix)(bot, message)

initial_extensions = []

bot = commands.Bot(command_prefix=get_prefix, decription="A bot for Discord Hack Week.", self_bot=False)

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print(f"Successfully loaded extension - {extension}")
        except Exception as e:
            print(f"Failed to load extension - {extension}", file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():

    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id)\nVersion: {discord.__version__}\n')

    await bot.change_presence(activity=discord.Activity(name="Building Cities...",type=0))

    print("Logged in and booted!")

print("Connecting to discordapp")

tooken = pickle.load(open('tooken.data','rb'))
bot.run(tooken, bot=True, reconnect=True)
