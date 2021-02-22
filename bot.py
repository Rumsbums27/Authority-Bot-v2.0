from discord.ext import commands
import json
from discord import Embed
import os

def get_configs(config):
    with open('configs.json','r') as data:
        configs = json.load(data)
    return configs[config]

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'cogs.{extension}')
    embed = Embed(
        title='Bot',
        description=f'Successfully loaded {extension}',
        color=0x2f9c3f
    )
    await ctx.send(embed=embed)

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'cogs.{extension}')
    embed = Embed(
        title='Bot',
        description=f'Successfully unloaded {extension}',
        color=0x2f9c3f
    )
    await ctx.send(embed=embed)

@bot.command()
async def reload(ctx,extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    embed = Embed(
        title='Bot',
        description=f'Successfully reloaded {extension}',
        color=0x2f9c3f
    )
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.CommandNotFound):
        embed = Embed(
            title='Error',
            description='Fatal error: Command not found',
            color=0xff0000
        )
        await ctx.send(embed=embed)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(get_configs('token'))