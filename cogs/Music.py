import discord,asyncio,DiscordUtils
from discord.ext import commands, tasks
from discord.ext.commands import *

music = DiscordUtils.Music()

class Music(Cog):
    
    def __init__(self,bot):
        self.bot = bot

    @command()
    async def join(self,ctx):
        
        if not ctx.voice_client is None:
            
            if ctx.author.voice is None:
            
                await ctx.send("You are not in a Voice Channel yet.")
                return
        
            elif ctx.guild.me.voice == ctx.author.voice:
            
                pass

            elif not ctx.voice_client.is_connected():
            
                await ctx.author.voice.channel.connect()
        
        else:
            try:
                await ctx.author.voice.chann.connect()
            except:
                pass

    @command()
    async def leave(self,ctx):
        
        if not ctx.voice_client is None:
        
            if not ctx.voice_client.is_connected():
            
                await ctx.voice_client.disconnect()
                
            else:
                
                await ctx.send("I\'m not in a Voice Channel yet.")
        
        else:
            
            await ctx.send("I\'m not in a Voice Channel yet.")
            
    @command()
    async def play(self,ctx,url = None):
        
        await ctx.invoke(self.bot.get_command("join"))
        await asyncio.sleep(3)
        
        player = music.get_player(guild_id = ctx.guild.id)
        print(not player)
        if not ctx.voice_client is None:
            if not player:
                player = music.create_player(ctx,ffmpeg_error_betterfix = True)
                print("Yep")
            if not ctx.voice_client.is_playing():
                await player.queue(url,search=True)
                print("Ok")
                song = await player.play()
                await ctx.send(f"Started Playing {song.name}.")
            elif url == None:
                await ctx.invoke(self.bot.get_command("resume"))
            else:
                song = await player.queue(url,search=True)
                await ctx.send(f"Added {song.name} to queue.")
                
        else:
            print("Not connected to voice error again ffs.")
        
    @command()
    async def queue(self,ctx):
        
        player = music.get_player(guild_id = ctx.guild.id)
        embed = discord.Embed(title="Queue", description="Songs in Queue :" , color = discord.Color.random())
        msg = ""
        num = 1
        for i in player.current_queue():
            dur = i.duration
            minutes = dur//60
            seconds = dur%60
            msg += f"{num}. {i.name} {minutes}:{seconds}"
            msg += "\n"
            num += 1
        if len(player.current_queue()) == 0:
            msg = "None"
        embed.add_field(name=msg,value="\u200b")
        embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Requested by {ctx.message.author}")
        await ctx.send(embed=embed)
        
    @command()
    async def resume(self,ctx):
        
        player = music.get_player(guild_id = ctx.guild.id)
        song = await player.resume()
        await ctx.send(f"Resumed Playing {song.name}")

    @command()
    async def pause(self,ctx):
        
        player = music.get_player(guild_id = ctx.guild.id)
        song = await player.pause()
        await ctx.send(f"Paused Playing {song.name}")
        
    @command()
    async def remove(self,ctx,num : int):
        
        player = music.get_player(guild_id = ctx.guild.id)
        num += 1
        if num == 1:
            return await ctx.invoke(self.bot.get_command("skip"))
        elif num > 1:
            try:
                song = await player.remove_from_queue(num)
                await ctx.send(f"Removed {song.name} from queue.")
            except:
                await ctx.send("Invalid number provided. Check the number from queue command.")

    @command()
    async def skip(self,ctx):
        player = music.get_player(guild_id = ctx.guild.id)
        song = await player.skip(force=True)
        await ctx.send(f"Skipped {song.name}")
    
    @command()
    async def loop(self,ctx):
        
        player = music.get_player(guild_id = ctx.guild.id)
        song = await player.toggle_song_loop()
        
        if song.is_looping:
            await ctx.send(f"{song.name} is now looping.")
            
        else:
            await ctx.send(f"Stopped looping {song.name}.")
            
    @command()
    async def volume(self,ctx,num : int):
        
        player = music.get_player(guild_id = ctx.guild.id)
        vol = num/100
        await player.change_volume(vol)
        await ctx.send(f"Volume changed to {num}%")
    '''
    @Cog.listener()
    async def on_voice_state_update(self,user,bfr,aftr):
        
        if not (user.id == self.bot.user.id):
            return

        elif bfr.channel is None:
            voice = aftr.channel.guild.voice_client
            time = 0
            while True:
                await asyncio.sleep(1)
                time = time + 1
                if voice.is_playing() and not voice.is_paused():
                    time = 0
                if time >= 120:
                    await voice.disconnect()
                    time = 0
                    break
                if not voice.is_connected():
                    break

        for i in self.bot.voice_clients:
            if len(i.channel.members) == 1 and self.bot.user.id == i.channel.members[0].id:
                await asyncio.sleep(5)
                await i.disconnect()'''

def setup(bot):
    bot.add_cog(Music(bot))
