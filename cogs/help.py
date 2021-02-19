from discord.ext import commands
from discord import Embed

class HelpCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def help(self,ctx):
        embed = Embed(
            title='Help',
            color=0x00ffff
        )
        embed.add_field(name='Prefix',value='`.`')
        embed.add_field(name='Commands',value='`help` - Zeigt diese Nachricht')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCog(bot))