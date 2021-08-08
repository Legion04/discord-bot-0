import discord,asyncio,json,os
from discord.ext import commands, tasks
from DiscordUtils import Music

bot = commands.Bot(command_prefix="?")
music = Music()

for i in os.listdir("./cogs/"):
    
    if i[-3:] == ".py":
        
        bot.load_extension(f"cogs.{i[:-3]}")
        
@bot.event
async def on_ready():
    print("The LEGEND has AWOKEN!!")
        
bot.run(os.environ.get("Token"))