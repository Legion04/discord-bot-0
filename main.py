import discord,asyncio,json,os
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix="?")

for i in os.listdir("./cogs/"):
    
    if i[-3:] == ".py":
        
        bot.load_extension(f"cogs.{i[:-3]}")
        
@bot.event
async def on_ready():
    print("The LEGEND has AWOKEN!!")
    await asyncio.sleep(15)
    for i in bot.voice_clients:
        if not i is None:
            try:
                await i.disconnect()
            except:
                pass
        
bot.run(os.environ.get("Token"))