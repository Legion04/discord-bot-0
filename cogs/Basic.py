import discord,json,os,asyncio,supabase_py
from discord.ext.commands import *
from discord_components import Button

supabase = supabase_py.create_client(os.environ.get("Url"),os.environ.get("Key"))
print(supabase)

class BASICCMD(Cog):

    def __init__(self,client):

        self.client = client

    @command()
    async def ping(self,ctx):

        embed = discord.Embed(title = "Ping",description = f"{round((self.client.latency)*1000)}ms", color = discord.Color.blue() )
        embed.set_author(name = ctx.message.author)
        embed.set_thumbnail(url = ctx.message.author.avatar_url)
        await ctx.send(embed = embed)
        
    @command(aliases=["xo",])
    async def tictactoe(self,ctx,player2 : discord.User = None):
        if player2 is None:
            await ctx.send("Solo?")
            return
        components = []
        for i in range(3):
            m = list()
            for j in range(3):
                m.append(Button(label="---",style=1,id=str(i)+str(j)))
            components.append(m)
        player1 = ctx.author
        embed = discord.Embed(title="Tic-Tac-Toe",color = discord.Color.blue())
        embed.add_field(name=f"{player1.mention}\'s Turn.",value=" X ")
        msg = await ctx.send(embed=embed,components=components)
        turns = 1
        sign = " X "
        moves = {"00":None,"01":None,"02":None,"10":None,"11":None,"12":None,"20":None,"21":None,"22":None}
        def wincheck(moves):
            if (moves["00"] == 0 and moves["01"] == 0 and moves ["02"] == 0) or (moves["10"] == 0 and moves["11"] == 0 and moves ["12"] == 0) or (moves["20"] == 0 and moves["21"] == 0 and moves ["22"] == 0) or (moves["00"] == 0 and moves["10"] == 0 and moves ["20"] == 0) or (moves["01"] == 0 and moves["11"] == 0 and moves ["21"] == 0) or (moves["02"] == 0 and moves["12"] == 0 and moves ["22"] == 0) or (moves["00"] == 0 and moves["11"] == 0 and moves ["22"] == 0) or (moves["02"] == 0 and moves["11"] == 0 and moves ["20"] == 0):
                return True
            elif (moves["00"] == 1 and moves["01"] == 1 and moves ["02"] == 1) or (moves["10"] == 1 and moves["11"] == 1 and moves ["12"] == 1) or (moves["20"] == 1 and moves["21"] == 1 and moves ["22"] == 1) or (moves["00"] == 1 and moves["10"] == 1 and moves ["20"] == 1) or (moves["01"] == 1 and moves["11"] == 1 and moves ["21"] == 1) or (moves["02"] == 1 and moves["12"] == 1 and moves ["22"] == 1) or (moves["00"] == 1 and moves["11"] == 1 and moves ["22"] == 1) or (moves["02"] == 1 and moves["11"] == 1 and moves ["20"] == 1):
                return False
            else:
                return None

        while turns<10:
            embed.clear_fields()
            if turns %2 == 1:
                def check(res):
                    return player1 == res.user and res.channel == ctx.channel
                try:
                    res = await self.client.wait_for("button_click",check=check,timeout=15)
                except asyncio.TimeoutError:
                    await msg.delete()
                    await ctx.send("Timed Out.")
                    return
                sign = " X "
                col = 3
                embed.add_field(name=f"{player2.mention}\'s Turn",value=" O ")
            elif turns%2 == 0:
                def check(res):
                    return player2 == res.user and res.channel == ctx.channel
                try:
                    res = await self.client.wait_for("button_click",check=check,timeout=15)
                except asyncio.TimeoutError:
                    await msg.delete()
                    await ctx.send("Timed Out.")
                    return
                sign = " O "
                col = 4
                embed.add_field(name=f"{player1.mention}\'s Turn",value=" X ")
            if moves[res.component.custom_id] == None:
                pass
            else:
                continue
            x = int(res.component.custom_id[0])
            y = int(res.component.custom_id[1])
            components[x][y] = Button(style=col,label=sign,id=res.component.custom_id)
            moves[res.component.custom_id] = col - 3
            turns += 1
            await msg.edit(components=components)
            if wincheck(moves) is not None:
                break
            await msg.edit(embed=embed)
            
        else:
            await msg.delete()
            await asyncio.sleep(1)
            embed.clear_fields()
            embed.add_field(name="No winner.",value="**While you were distracted a monkey took the trophy and ran.**")
            await ctx.send(embed=embed)
            return

        embed.clear_fields()
        await asyncio.sleep(2)
        
        if wincheck(moves):
            embed.add_field(name=f"{player1.mention} Won.",value="Well Played ! Ggs.")
            
        else:
            embed.add_field(name=f"{player2.mention} Won.",value="Well Played ! Ggs.")
        await msg.edit(embed=embed,components=[])
            
def setup(client):
    client.add_cog(BASICCMD(client))