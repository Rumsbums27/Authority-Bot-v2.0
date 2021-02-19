from discord.ext import commands
import json
from discord import Embed
import os

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

def get_configs(config):
    with open('configs.json','r') as data:
        configs = json.load(data)
    return configs[config]

@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(get_configs('token'))