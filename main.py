import discord,asyncio,json,os
from discord.ext import commands, tasks
from DiscordUtils import Music
from discord_components import *

bot = commands.Bot(command_prefix="?")
music = Music()
DiscordComponents(bot)

for i in os.listdir("./cogs/"):
    
    if i[-3:] == ".py":
        
        bot.load_extension(f"cogs.{i[:-3]}")
        
@bot.event
async def on_ready():
    print("The LEGEND has AWOKEN!!")
    
    for i in bot.voice_clients:
        try:
            await i.disconnect()
        except:
            pass
        
bot.run(os.environ.get("Token"))