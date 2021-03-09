from discord.ext import commands
from random import randint
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from discord import Embed, Member


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
        if ctx.author.bot:
            return
        generated_xp = self.xpgen(a=5, b=10)
        check = xp.find_one({'_id': f'{ctx.author.id}'})
        if check:
            for i in xp.find({'_id': f'{ctx.author.id}'}):
                current_xp = i['how_much_xp']
                current_xp += generated_xp
                xp.update_one({'_id': f'{ctx.author.id}'}, {
                    '$set': {'how_much_xp': current_xp}
                })
                if current_xp % 100 <= 10:
                    level_up = Embed(
                        title='Level Up',
                        color=0x946523
                    )
                    level_up.add_field(name='Level', value=f'{current_xp // 100}')
                    level_up.add_field(name='XP', value=f'{current_xp}')
                    await ctx.channel.send(embed=level_up)

        else:
            xp.insert_one({'_id': f'{ctx.author.id}', 'how_much_xp': generated_xp})

    @commands.command()
    async def lvl(self, ctx, member: Member = None):
        if member is None:
            member = ctx.author
        check = xp.find_one({'_id': f'{member.id}'})
        if check:
            for i in xp.find({'_id': f'{member.id}'}):
                current_xp = i['how_much_xp']
                rank = Embed(
                    title='Level',
                    color=0x5864a6
                )
                rank.add_field(name='Level', value=f'{current_xp // 100}')
                rank.add_field(name='XP', value=f'{current_xp}')
                await ctx.send(embed=rank)

        else:
            not_in_database = Embed(
                title='Not in Database',
                description="You or the User you mentioned is not in the database yet.",
                color=0x93b349
            )
            await ctx.send(embed=not_in_database)


def setup(bot):
    bot.add_cog(LvlCog(bot))
