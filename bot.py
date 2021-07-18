import discord,json,asyncio,os
from discord.ext import tasks,commands
from discord_components import DiscordComponents , Button

with open(r'data.json') as f:
    envs = json.load(f)

client = commands.Bot(command_prefix=['0'],intents=discord.Intents().all())

@client.event
async def on_ready():

    DiscordComponents(client)
    print(f"{client.user.name} has Awoken!")

@client.event
async def on_message(message):

    await client.process_commands(message)
    
    if message.author != client.user:
        
        if message.guild.id == envs["Guild"]:
            
            if "Get a different captcha by typing any command." in message.content:
                
                grind.cancel()
                ch = client.get_channel(envs["Ch2"])
                msg = await ch.send(f"<@!{envs['User']}> | >.<")
                
            elif "Raider Pokémon has arrived! Who will be brave enough to take on the challenge?" in message.content:
                
                grind.cancel()
                ch = client.get_channel(envs["Ch"])
                if envs["Set"] == 0:
                    await ch.send(f"! <@!{envs['User']}>")
                    return
                alpha = envs["alpha"]
                num = envs["num"] + 1
                envs["num"] = num
                with open("data.json","w") as f:
                    json.dump(envs,f)
                msg = await ch.send(f"!setchannel 1 {alpha+str(num)}")
                grind.start()
                
            embeds = message.embeds
            
            for i in embeds:
                
                a = i.to_dict()
                #with open("log.txt","a") as f:
                    #f.write(str(a))
                if message.channel.id != envs["Events"]:
                    return
                if a["title"] == "Dynamax Raid Alert" and a["fields"][1]["value"] == "5 minutes left":
                    grind.cancel()
                    b = " "
                    if envs["User2"] is not None:
                        b = "<@!" + str(envs["User2"]) +">"
                    ch2 = client.get_channel(envs["Ch2"])
                    await ch2.send(f"! <@!{envs['User']}>  {b}")
                    ch = client.get_channel(envs["Ch"])
                    
                    if envs["Set"] == 0:
                        return

                    alpha = envs["alpha"]
                    num = envs["num"] + 1
                    envs["num"] = num
                    
                    with open("data.json","w") as f:
                        json.dump(envs,f)
                    
                    msg = await ch.send(f"!setchannel 1 {alpha+str(num)}")
                    grind.start()
                    
                elif a["title"] == "Multibattle Challenge Alert" and a["fields"][1]["value"] == "15 minutes left.":
                    
                    grind.cancel()
                    ch2 = client.get_channel(envs["Ch2"])
                    ch = client.get_channel(envs["Ch"])
                    
                    if envs["Set"] == 0:
                        await ch2.send(f"! <@!{envs['User']}>")
                        return

                    alpha = envs["alpha"]
                    num = envs["num"] + 1
                    envs["num"] = num
                    
                    with open("data.json","w") as f:
                        json.dump(envs,f)
                    
                    msg = await ch.send(f"!setchannel 1 {alpha+str(num)}")
                    grind.start()

def guildcheck():
    
    def predicate(ctx):
        
        gid = envs["Guild"]
        return ctx.guild.id == gid

    return commands.check(predicate)

@client.command(aliases=["b",])
@guildcheck()
async def start(ctx):
    grind.start()
    await ctx.message.delete()

@client.command(aliases=["s",])
@guildcheck()
async def stop(ctx):
    grind.stop()
    await ctx.message.delete()
    
@client.command(aliases=["cp",])
@guildcheck()
async def captcha(ctx,cp):
    ch = client.get_channel(envs["Ch"])
    await ch.send(f"!cp {cp}")
    await ctx.message.delete()
    await asyncio.sleep(5)
    grind.start()
    
@client.command(aliases=["d",])
@guildcheck()
async def do(ctx,*comds):
    cmd = " ".join(comds)
    await ctx.message.delete()
    ch = client.get_channel(envs["Ch"])
    await ch.send(f"!{cmd}")
    
@client.command(aliases=["st",])
@guildcheck()
async def setchannel(ctx,alpha : str,num :int):
    
    envs["alpha"] = alpha
    envs["num"] = num
    with open('data.json',"w") as f:
        json.dump(envs,f)
    await ctx.message.delete()
    ch = client.get_channel(envs["Ch"])
    msg = await ch.send(f"!setchannel 1 {alpha+str(num)}")
    
@client.command(aliases=["spd",])
@guildcheck()
async def speed(ctx,count:float):
    
    grind.change_interval(seconds=count)
    await asyncio.sleep(1)
    await ctx.message.delete()
    
@client.command()
async def stc(ctx,num:int):
    
    envs["Set"] = num
    await asyncio.sleep(2)
    await ctx.message.delete()
    
@tasks.loop(seconds=2.75)
async def grind():
    ch = client.get_channel(envs["Ch"])
    await ch.send("!s")
    await asyncio.sleep(1)
    await ch.send("!f 2")

client.run(envs["Token"],bot=False)