# bot.py
import os
import discord
from discord.flags import Intents
import music
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix="$", Intents=discord.Intents.all())

cogs = [music]

for i in range(len(cogs)):
    cogs[i].setup(bot)


@bot.event
async def on_ready():
    print("Bot Started!")
    print("Logged in as: {0.user}".format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='$play | Bukan Ayame asli'))

# @bot.event
# async def on_message(ctx):
#     # channel = bot.get_channel(msg_dump_channel)
#     if ctx.author == bot.user:
#         return
#     server = ctx.guild.name
#     user = ctx.author
#     message = ctx.content
#     print(f"{user}: {message}")
#     await bot.process_commands(ctx)

@bot.command(name='ping')
async def pingpong(ctx):
    await ctx.send(f'Pong!!')

bot.run(TOKEN)
