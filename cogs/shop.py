from discord.ext import commands
from discord.colour import Color
from discord import Embed
from pymongo import MongoClient
from dotenv import load_dotenv
import pytz
import datetime
import os

# ToDo: implement Harvest Command to harvest the Plants

load_dotenv()
cluster = MongoClient(os.getenv("MONGODB"))
db = cluster['authority']
inventory = db['inventory']
shop_inventory = db['shop-inv']
timezome = pytz.timezone('Europe/Berlin')


class ShopCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def current_time(self):
        time = datetime.datetime.now(tz=timezome)
        return int(time.strftime('%H.%M'))

    async def insert_new_user(self, ctx):
        """
        :param ctx:
        :return None:
        Insert a new User to the User DB
        business looks like:
        business: {
        drugs:{
        weed: {},
        opium: {}
        },
        weapons:{},
        machines: {},
        }
        """
        inventory.insert_one(
            {'_id': ctx.author.id, 'money': 1000, 'business': {}})
        get_money_embed = Embed(title='You got sucessfully 1000 $')
        await ctx.channel.send(embed=get_money_embed)

    @commands.command(aliases=['sb'])
    async def start_business(self, ctx):
        if inventory.find_one({'_id': ctx.author.id}):
            for i in inventory.find({'_id': ctx.author.id}):
                current_money = i['money']
                if current_money > 0:
                    has_used_command = Embed(
                        title='You already have used this Command, or already own Money', color=0xff0000)
                    await ctx.channel.send(embed=has_used_command)
        else:
            await self.insert_new_user(ctx=ctx)

    @commands.command(aliases=['ls', 'list-shop', 'listShop', 'Listshop'])
    async def list_shop(self, ctx):
        list_shop_embed = Embed(title='SHOP', color=Color.green)
        list_shop_embed.add_field(
            name='Grass', value='A little green Plant... look likes Tea...')
        await ctx.channel.send(embed=list_shop_embed)

    @commands.command()
    async def harvest(self, ctx, name):
        if shop_inventory.find_one({'_id': name}):
            for i in shop_inventory.find({'_id': name}):
                if i['has_cooldown']:
                    plant_cooldown = i['cooldown']
                    category = i['category']
                    give_amount = i['give']
                    give_name = i['give_name']
                    if inventory.find_one({'_id': ctx.author.id}):
                        for x in inventory.find({'_id': ctx.author.id}):
                            current_business = x['business']
                            plant_amount = current_business[category][name]['amount']
                            has_harvest = current_business[category][name]['cooldown']
                            if has_harvest - self.current_time() >= plant_cooldown:
                                for y in shop_inventory.find({'_id': give_name}):
                                    category = y['category']
                                    current_amount = current_business[category][give_name]['amount']
                                    current_business[category][give_name]['amount'] = current_amount + (
                                        give_amount * plant_amount)
                                    inventory.update_one({'_id': ctx.author.id},
                                                         {'$set': {'business': current_business}})
                                    sucess_harved = Embed(
                                        title=f"""Congrats Bro, you have harvest {current_amount + (
                                                give_amount * plant_amount)} {give_name}"""
                                    )
                            else:
                                has_haved = Embed(
                                    title='Yo, yo, yo bro you already harvest, try it later again',
                                    color=Color.red)
                                await ctx.channel.send(embed=has_haved)
                else:
                    not_harvestable = Embed(title='Yo dude you want to harvest somethinng that is not harvestable',
                                            color=Color.red)
                    await ctx.channel.send(embed=not_harvestable)

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx):
        farm_embed = Embed(title="You're Inventory:", color=Color.green)
        if inventory.find_one({'_id': ctx.author.id}):
            for i in inventory.find({'_id': ctx.author.id}):
                business: dict = i['business']
                drugs = business['drugs']
                for x in drugs:
                    farm_embed.add_field(
                        name=x, value=f"Amount: {drugs[x]['amount']}")
                await ctx.channel.send(embed=farm_embed)

    async def buy_with_cooldown(self, ctx, name, price, category, amount):
        if inventory.find_one({'_id': ctx.author.id}):
            for x in inventory.find({'_id': ctx.author.id}):
                money = x['money']
                current_business = x['business']
                if money - price * amount >= 0:
                    inventory.update_one({'_id': ctx.author.id}, {
                                         '$set': {'money': money - (price * amount)}})
                    if name in current_business[category]:
                        current_amount = current_business[category][name]['amount']
                        current_business[category][name]['amount'] = current_amount + amount
                        current_business[category][name]['cooldown'] = self.current_time(
                        )
                        inventory.update_one({'_id': ctx.author.id},
                                             {'$set': {'business': current_business}})
                        sucess_buy = Embed(
                            title=f'Sucessfully buyed {name}, {amount} times', color=Color.green)
                        await ctx.channel.send(embed=sucess_buy)
                    else:
                        current_business[category][name] = {
                            'amount': amount, 'cooldown': self.current_time()}
                        inventory.update_one({'_id': ctx.author.id},
                                             {'$set': {'business': current_business}})
                        sucess_buy = Embed(
                            title=f'Sucessfully buyed {name}, {amount} times', color=Color.green)
                        await ctx.channel.send(embed=sucess_buy)
        else:
            dont_start_business = Embed(
                title="You don't started you're business yet.. maybe you start it with `.sb`?", color=0xff0000)
            await ctx.channel.send(embed=dont_start_business)

    async def buy_without_cooldown(self, ctx, name, price, category, amount):
        if inventory.find_one({'_id': ctx.author.id}):
            for x in inventory.find({'_id': ctx.author.id}):
                money = x['money']
                current_business = x['business']
                if money - price * amount >= 0:
                    inventory.update_one({'_id': ctx.author.id}, {
                                         '$set': {'money': money - (price * amount)}})
                    if name in current_business[category]:
                        current_amount = current_business[category][name]['amount']
                        current_business[category][name]['amount'] = current_amount + amount
                        inventory.update_one({'_id': ctx.author.id},
                                             {'$set': {'category': current_business}})
                        sucess_buy = Embed(
                            title=f'Sucessfully buyed {name}, {amount} times', color=Color.green)
                        await ctx.channel.send(embed=sucess_buy)
                    else:
                        current_business[category][name] = {'amount': amount}
                        inventory.update_one({'_id': ctx.author.id},
                                             {'$set': {'category': current_business}})
                        sucess_buy = Embed(
                            title=f'Sucessfully buyed {name}, {amount} times', color=Color.green)
                        await ctx.channel.send(embed=sucess_buy)

    @commands.command()
    async def buy(self, ctx, name, amount=1):
        if shop_inventory.find_one({'_id': name}):
            for i in shop_inventory.find({'_id': name}):
                price = i['price']
                category = i['category']
                need_cooldown = i['cooldown']
                if need_cooldown:
                    self.buy_with_cooldown(
                        ctx=ctx, name=name, price=price, category=category, amount=amount)
                self.buy_without_cooldown(
                    ctx=ctx, name=name, price=price, category=category, amount=amount)


def setup(bot):
    bot.add_cog(ShopCog(bot))


# ToDo: Add first Element to shop_inventory db
"""
shop inv looks like
'_id': <str: drug/plant-name>,'has_cooldown': <bool: Need cooldown> ,'cooldown': <int: hours to wait, when needed(negative)>, 
'price': <int/float: to buy this>, 'resell_price': <int/float: to resell this>, 'category': <str: name of category>,
'give_amount': <int: amount of get when harvest>, 'give': <str: name of thing to get when harvest>

"""
