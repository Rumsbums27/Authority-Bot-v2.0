from discord.ext import commands
import json
from discord import Embed,Intents
import os

bot = commands.Bot(command_prefix='.',intents=Intents.all(),help_command=None)

def get_configs(config):
    with open('configs.json','r') as data:
        configs = json.load(data)
    return configs[config]

@bot.command()
@commands.is_owner()
async def reload(ctx,extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    embed = Embed(
        title='Bot',
        description=f'Successfully reloaded {extension}',
        color=0xa35c3e
    )
    await ctx.send(embed=embed)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Successfully loaded {filename[:-3]}')

bot.run(get_configs('token'))