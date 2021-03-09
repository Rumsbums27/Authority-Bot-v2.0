from discord.ext import commands
from discord import Embed
import os
from dotenv import load_dotenv


bot = commands.Bot(command_prefix='.', help_command=None)


@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    embed = Embed(
        title='Bot',
        description=f'Successfully reloaded {extension}',
        color=0x2f9c3f
    )
    await ctx.send(embed=embed)


#@bot.event
#async def on_command_error(ctx, error):
#    embed = Embed(
#        title='Error',
#        description=f'{error}',
#        color=0xff0000
#    )
#    await ctx.send(embed=embed)

disabled = [
]

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if filename[:-3] not in disabled:
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Successfully loaded {filename[:-3]}')

load_dotenv()
bot.run(os.getenv('TOKEN'))
