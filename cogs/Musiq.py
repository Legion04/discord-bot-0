import discord
from discord.ext import commands
import wavelink

class Musiq(commands.Cog):
    
    def __init__(self,bot : commands.Bot):
        self.bot=bot
        bot.loop.create_task(self.node.connect())
        
    async def node_connect(self):
        
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot,host='lavalinkinc.ml',port=443,password='incognito',https=True)
        
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self,node : wavelink.node):
        
        print(f'Node {node.identifier} is ready!')
        
    @commands.command()
    async def play(self,ctx : commands.Context, *,search : wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc : wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif getattr(ctx.author.voice,'channel',None):
            await ctx.send('Connect to a Vc Baka!')
        else:
            vc : wavelink.Player = ctx.voice_client
            
        await vc.play(search)
        
def setup(bot):
    bot.add_cog(Musiq(bot))
