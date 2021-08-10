import discord,asyncio,DiscordUtils
from discord.ext import commands, tasks
from discord.ext.commands import *
from discord_components import *

music = DiscordUtils.Music()

class Music(Cog):
    
    def __init__(self,bot):
        self.bot = bot

    @command(aliases=["j",])
    async def join(self,ctx):
        
        if not ctx.voice_client:
            
            if ctx.author.voice is None:
            
                await ctx.send("You are not in a Voice Channel yet.")
                return
        
            elif ctx.guild.me.voice == ctx.author.voice:
            
                pass

            await ctx.author.voice.channel.connect()
        
        else:
            try:
                await ctx.author.voice.channel.connect()
            except Exception as e:
                print(e)

    @command(aliases=["l",])
    async def leave(self,ctx):
        
        if not ctx.voice_client:
        
            await ctx.send("I\'m not in a Voice Channel yet.")
        
        else:
            
            await ctx.voice_client.disconnect()
            """
    @command()
    async def play(self,ctx,*urls):
        
        url = str(" ".join(urls))
            
        await ctx.invoke(self.bot.get_command("join"))
        
        if not ctx.voice_client:
            return

        player = music.get_player(guild_id = ctx.guild.id)

        if not player:
            player = music.create_player(ctx,ffmpeg_error_betterfix = True)

        if not ctx.voice_client.is_playing():
            await player.queue(url,search=True)

            song = await player.play()
            await ctx.send(f"Started Playing {song.name}.")
            
        else:
            song = await player.queue(url,search=True)
            await ctx.send(f"Added {song.name} to queue.")"""
            
    @command(aliases=["pl","play"])
    async def playlist(self,ctx,*uri):
        
        urls = str(" ".join(uri))
        
        try:
            url = urls.split(",")
        except:
            url = uri

        await ctx.invoke(self.bot.get_command("join"))
        player = music.get_player(guild_id = ctx.guild.id)

        if not ctx.voice_client is None:
            if not player:
                player = music.create_player(ctx,ffmpeg_error_betterfix = True)

            if not ctx.voice_client.is_playing():
                
                await player.queue(url[0],search=True)
                song = await player.play()
                await ctx.send(f"Started Playing {song.name}.")
                url.pop(0)
            
            if len(url) > 0:
                
                for i in url:
                    
                    await player.queue(i,search=True)
                    
            await ctx.send("Added Playlist!")
            await ctx.invoke(self.bot.get_command("queue"))
        
    @command()
    async def queue(self,ctx):
        
        if not ctx.voice_client:
            return
        player = music.get_player(guild_id = ctx.guild.id)
        embed = discord.Embed(title="Queue", description="Songs in Queue :" , color = discord.Color.random())
        msg = ""
        num = 1
        time = 0
        for i in player.current_queue():
            dur = i.duration
            minutes = dur//60
            seconds = dur%60
            time += dur
            msg += f"{num}. {i.name} {minutes}:{seconds}"
            msg += "\n"
            num += 1
        if len(player.current_queue()) == 0:
            msg = "None"
        minutes = time//60
        seconds = time%60
        embed.add_field(name=msg,value="\u200b")
        embed.set_footer(icon_url=ctx.author.avatar_url,text=f"Total time - {minutes}:{seconds}")
        await ctx.send(embed=embed)
        
    @command()
    async def resume(self,ctx):
        
        if not ctx.voice_client:
            return
        player = music.get_player(guild_id = ctx.guild.id)
        song = await player.resume()
        await ctx.send(f"Resumed Playing {song.name}")

    @command()
    async def pause(self,ctx):
        
        if not ctx.voice_client:
            return
        player = music.get_player(guild_id = ctx.guild.id)
        song = await player.pause()
        await ctx.send(f"Paused Playing {song.name}")
        
    @command(aliases=["r",])
    async def remove(self,ctx,num : int):
        
        if not ctx.voice_client:
            return
        player = music.get_player(guild_id = ctx.guild.id)
        num -= 1
        if num == 0:
            return await ctx.invoke(self.bot.get_command("skip"))
        elif num > 0:
            try:
                song = await player.remove_from_queue(num)
                if len(player.current_queue()) == 1:
                    name = song.name
                else:
                    name = song[0].name
                await ctx.send(f"Removed {name} from queue.")
            except IndexError:
                await ctx.send("Invalid number provided. Check the number from queue command.")

    @command(aliases=["s",])
    async def skip(self,ctx):
        
        if not ctx.voice_client:
            return
        player = music.get_player(guild_id = ctx.guild.id)
        song = await player.skip(force=True)
        await ctx.send(f"Skipped {song[0].name}")
    
    @command()
    async def loop(self,ctx):
        
        if not ctx.voice_client:
            return
        player = music.get_player(guild_id = ctx.guild.id)
        song = await player.toggle_song_loop()
        
        if song.is_looping:
            await ctx.send(f"{song.name} is now looping.")
            
        else:
            await ctx.send(f"Stopped looping {song.name}.")
            
    @command(aliases=["vol",])
    async def volume(self,ctx,num : int = None):
        
        if not ctx.voice_client:
            return
        player = music.get_player(guild_id = ctx.guild.id)
        if num:
            vol = num/100
            await player.change_volume(vol)
            await ctx.send(f"Volume changed to {num}%")
        else:
            msg = await ctx.send("> Volume :",components=[[Button(style=1,custom_id="0",label="0"),Button(style=1,custom_id="25",label="25"),Button(style=1,custom_id="50",label="50"),Button(style=1,custom_id="75",label="75"),Button(style=1,custom_id="100",label="100"),]])
            def check(res):
                return res.user == ctx.author and res.message.id == msg.id
            self.bot.flag = True
            while self.bot.flag:
                res = await self.bot.wait_for("button_click",check = check)
                vol = int(res.component.custom_id)
                await player.change_volume(vol)
                await res.respond(content="https://cdn.discordapp.com/emojis/803643669323972638.gif?v=1")
        
    @volume.before_invoke
    async def kk(self,ctx):
        
        self.bot.flag = False
            
    @command()
    async def stop(self,ctx):
        
        if ctx.voice_client is not None:
            
            try:
                player = music.get_player(guild_id = ctx.guild.id)
                await player.stop()
                await ctx.send("Stopped!")
            except Exception as e:
                print(e)
                
    @command(aliases=["p",])
    async def player(self,ctx):
        
        if not ctx.voice_client:
            
            return
            
        player = music.get_player(guild_id=ctx.guild.id)
        msg = await ctx.send("> Player :", components=[[Button(style=1,emoji="🔁",custom_id="loop"),Button(style=1,emoji="⏸️",custom_id="pause"),Button(style=3,emoji="▶️",custom_id="resume"),Button(style=4,emoji="⏹️",custom_id="stop"),Button(style=4,emoji="⏭️",custom_id="skip")]])
            
        self.bot.flag = True
        while self.bot.flag:
            def check(res):
                    
                return res.user == ctx.author and res.message.id == msg.id
                
            res = await self.bot.wait_for("button_click",check=check)
            m1 = await ctx.send("Done.")
            await asyncio.sleep(1)
            await m1.delete()
            await ctx.invoke(self.bot.get_command(res.component.custom_id))
    
    @player.before_invoke
    async def playe(self,ctx):
        
        self.bot.flag = False
            
    @Cog.listener()
    async def on_voice_state_update(self,user,bfr,aftr):
        
        try:
            if aftr.channel is None:
                voice = discord.utils.get(self.bot.voice_clients,guild = bfr.channel.guild)
                if bfr.channel == voice.channel and len(bfr.channel.members) == 1 and self.bot.user in bfr.channel.members:
                    if not voice.is_connected():
                        return
                    try:
                        player = music.get_player(guild_id=bfr.channel.guild.id)
                        await player.stop()
                    except Exception as e:
                        print(e)
                    await voice.disconnect()

        except AttributeError as e:
            
            print(e)

    @Cog.listener()
    async def on_command_error(self,ctx,error):
        
        if isinstance(error,CommandNotFound):
            pass
        else:
            raise(error)

def setup(bot):
    bot.add_cog(Music(bot))
