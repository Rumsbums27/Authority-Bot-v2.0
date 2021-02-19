from discord.ext import commands
from discord import Embed

class HelpCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def help(self,ctx):
        embed = Embed(
            title='Help'
        )

def setup(bot):
    bot.add_cog(HelpCog(bot))