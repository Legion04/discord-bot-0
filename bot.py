import discord,json,asyncio,os
from discord.ext import tasks,commands
from discord_components import DiscordComponents , Button

with open(r'data.json') as f:
    envs = json.load(f)

bot = commands.Bot(command_prefix=['0'],intents=discord.Intents().all())

bot.cp = 0
bot.sp = 0
bot.disabled = 1
bot.userone = envs["User"]
bot.usertwo = envs["User2"]
bot.chone = envs["Ch"]
bot.chtwo = envs["Ch2"]
bot.chevents = envs["Events"]

async def chsend(msg):
    ch = bot.get_channel(bot.chone)
    await ch.send(msg)
    
async def ch2send(msg):
    ch = bot.get_channel(bot.chtwo)
    await ch.send(msg)
    
async def disabled(msg=None):
    if msg == None:
        if bot.disabled == 0:
            return
    if bot.disabled == 0:
        await ch2send(msg)
        return

async def cp():
    if bot.cp == 1:
        bot.sp = 1
        return

async def chchange():
    alpha = envs["alpha"]
    num = envs["num"] + 1
    envs["num"] = num
    with open("data.json","w") as f:
        json.dump(envs,f,indent=4)
    await chsend(f"!setchannel 1 {alpha+str(num)}")

async def breakraider(msg,num = 0):
    
    try:
        a = msg.content
    except:
        a = msg.message.content
        
    if "BREAK" in a:
        
        cat = discord.utils.get(msg.guild.categories,name="Raids")
        n = len(cat.channels) + 1
        await msg.channel.edit(name=f"break-raider-{n}")
        await msg.channel.move(category=cat,end=True)

    elif num == 1:
        
        cat = discord.utils.get(msg.guild.categories,name="Raids")
        n = len(cat.channels) + 1
        await msg.channel.edit(name=f"break-raider-{n}")
        await msg.channel.move(category=cat,end=True)
        return
    
    else:
        
        await rareraider(msg,num)
    
async def rareraider(msg,num = 0):
    
    try:
        a = msg.content
    except:
        a = msg.message.content
        
    if "rare" in a:
        
        cat = discord.utils.get(msg.guild.categories,name="Rraids")
        n = len(cat.channels) + 1
        await msg.channel.edit(name=f"rare-raider-{n}")
        await msg.channel.move(category=cat,end=True)
        
    elif num == 2:
        
        cat = discord.utils.get(msg.guild.categories,name="Rraids")
        n = len(cat.channels) + 1
        await msg.channel.edit(name=f"rare-raider-{n}")
        await msg.channel.move(category=cat,end=True)
        return
        
async def multi(embed,msg,num=0):
    
    if num == 0:
        a = embed["fields"][0]["name"]
        b = a.split("-")
        c = str(b[0])
        d = c.strip()
        e = {"Pinchers Admin Red Eyes":"RedEyes","Arley The Destroyer":"Arley","Societea Member Hocus":"Hocus","Sky Fortress":"Sky","Pinchers Head Admin Purple Eyes":"PurpleEyes","Pinchers Admin Blue Eyes":"BlueEyes","Societea Leader Edward":"Edward","Societea Member Kasa":"Kasa"}
        try:
            f = e[d]
        except:
            f = ""
            
    else:
        
        if num == 1:
            f = "RedEyes"
        elif num==2:
            f = "BlueEyes"
        elif num==3:
            f = "PurpleEyes"
        elif num==4:
            f = "Hocus"
        elif num==5:
            f = "Kasa"
        elif num==6:
            f = "Arley"
        elif num==7:
            f ="Edward"
        elif num==8:
            f = "Sky"
            
    cat = discord.utils.get(msg.guild.categories,name="Multis")
    n = len(cat.channels) + 1
    await msg.channel.edit(name=f"multi-{f}-{n}")
    await msg.channel.move(category=cat,end=True)
        
@bot.event
async def on_ready():

    DiscordComponents(bot)
    print(f"{bot.user.name} has Awoken!")

@bot.event
async def on_message(message):

    await bot.process_commands(message)
    
    if message.author != bot.user and message.guild.id == envs["Guild"]:
        
        if "Get a different captcha by typing any command." in message.content:
                
            grind.cancel()
            await ch2send(f"! | <@!{envs['User']}> | Captcha in {message.channel.mention}")
            bot.cp = 1
                
        elif "Raider Pokémon has arrived! Who will be brave enough to take on the challenge?" in message.content:
                
            grind.cancel()
            await disabled(f"! | <@!{envs['User']}> | Raider spawned in {message.channel.mention}")
            await cp()
            await breakraider(message)
            await chchange()
            grind.start()
                
        embeds = message.embeds
        
        if len(embeds) == 0:
            return
        a = embeds[0].to_dict()
        
        if message.channel.id == bot.chevents:
            return
        try:
            z = a["title"]
            zz = a["fields"][1]["value"]
            pass
        except:
            return

        if a["title"] == "Dynamax Raid Alert" and a["fields"][1]["value"] == "5 minutes left":
                    
            grind.cancel()
            try:
                b = "<@!" + str(bot.usertwo) +">"
            except KeyError:
                b = " "
            await ch2send(f"! | <@!{envs['User']}> | {b} | Raid in {message.channel.mention}")
            await disabled()
            await cp()
            await chchange()
            grind.start()
            
        elif a["title"] == "Multibattle Challenge Alert" and a["fields"][1]["value"] == "15 minutes left.":
                    
            grind.cancel()
            await disabled(f"! | <@!{envs['User']}> | Multi in {message.channel.mention}")
            await cp()
            await multi(a,message)
            await chchange()
            grind.start()

def guildcheck():
    
    def predicate(ctx):
        
        gid = envs["Guild"]
        return ctx.guild.id == gid

    return commands.check(predicate)

@bot.command(aliases=["b",])
@guildcheck()
async def start(ctx):
    grind.start()
    await ctx.message.delete()

@bot.command(aliases=["s",])
@guildcheck()
async def stop(ctx):
    grind.stop()
    await ctx.message.delete()
    
@bot.command(aliases=["cp",])
@guildcheck()
async def captcha(ctx,cp):
    await chsend(f"!cp {cp}")
    await ctx.message.delete()
    await asyncio.sleep(2)
    
    if bot.sp == 1:
        await chchange()
    bot.cp = 0
    bot.sp = 0
    await asyncio.sleep(3)
    grind.start()
    
@bot.command(aliases=["d",])
@guildcheck()
async def do(ctx,*comds):
    cmd = " ".join(comds)
    await ctx.message.delete()
    await chsend(f"!{cmd}")
    
@bot.command(aliases=["st",])
@guildcheck()
async def setchannel(ctx,alpha : str,num :int):
    
    envs["alpha"] = alpha
    envs["num"] = num
    with open('data.json',"w") as f:
        json.dump(envs,f)
    await ctx.message.delete()
    ch = bot.get_channel(bot.chone)
    msg = await ch.send(f"!setchannel 1 {alpha+str(num)}")
    
@bot.command(aliases=["spd",])
@guildcheck()
async def speed(ctx,count:float):
    
    grind.change_interval(seconds=count)
    await asyncio.sleep(1)
    await ctx.message.delete()
    
@bot.command()
async def stc(ctx,num:int):
    
    bot.disabled = num
    await asyncio.sleep(2)
    await ctx.message.delete()
    
@bot.command(aliases=["msr",])
async def moveandsetraiders(ctx,num:int):
    
    await breakraider(ctx,num)
    await ctx.message.delete()
    
@bot.command(aliases=["msm",])
async def moveandsetmultis(ctx,num:int):
    
    await multi(bot,ctx,num)
    await ctx.message.delete()
    
@tasks.loop(seconds=2.75)
async def grind():
    ch = bot.get_channel(bot.chone)
    await ch.send("!s")
    await asyncio.sleep(1)
    await ch.send("!f 2")

bot.run(envs["Token"])