from discord.ext import commands
from discord import Embed
from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()
cluster = MongoClient(os.getenv("MONGODB"))
db = cluster['authority']
inventory = db['inventory']


class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def insert_new_user(self, ctx):
        inventory.insert_one({'_id': ctx.author.id, 'money': 1000})
        get_money_embed = Embed(title='You got sucessfully 1000 $')
        await ctx.channel.send(embed=get_money_embed)

    @commands.command(aliases=['sm'])
    async def start_money(self, ctx):
        if inventory.find_one({'_id': ctx.author.id}):
            for i in inventory.find({'_id': ctx.author.id}):
                current_money = i['money']
                if current_money > 0:
                    has_used_command = Embed(
                        title='You alredy have used this Command, or already own Money', color=0xff0000)
                    await ctx.channel.send(embed=has_used_command)
        else:
            await self.insert_new_user(ctx=ctx)

    @commands.command(aliases=['ls', 'list-shop', 'listShop', 'Listshop'])
    async def list_shop(self, ctx):
        pass


def setup(bot):
    bot.add_cog(ShopCog(bot))

