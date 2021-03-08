from discord.ext import commands
from random import randint
from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()
cluster = MongoClient(os.getenv("MONGODB"))
db = cluster['authority']
xp = db['xp']


class LvlCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def xpgen(self, a: int, b: int) -> int:
        return randint(a, b)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == commands.bot:
            return
        generated_xp = self.xpgen(a=5, b=10)
        if check := xp.find_one({'_id': f'{ctx.author.id}'}):
            for _ in check:
                pass


def setup(bot):
    bot.add_cog(LvlCog(bot))
