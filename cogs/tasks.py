from discord.ext import commands
from discord import Member, Embed, Colour
import sqlite3


class TasksCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addtask(self, ctx, user: Member, *, task_param):
        connection = sqlite3.connect('tasks.db')
        connection.execute("CREATE TABLE IF NOT EXISTS main (task TEXT, user TEXT)")
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO main (task, user) VALUES (?, ?)", (task_param, user))
        connection.commit()
        connection.close()
        embed = Embed(title="New Task addet!",
                      description=f"Successfully addet the task `{task_param}` to the user {user.mention}",
                      colour=Colour.from_rgb(0, 255, 56))
        await ctx.send(embed=embed)

    @commands.command(aliases=['showtask'])
    async def showtasks(self, ctx):
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute("SELECT task FROM main WHERE user=?", ctx.author)
        rows = cursor.fetchall()
        for i in rows:
            embed = Embed(title='Your Tasks', color=0x00ffff)
            embed.add_field(name='Task', value=f'{str(i)[:-3][2:]}')
            await ctx.send(embed=embed)
        cursor.execute('DELETE FROM main WHERE user=?', ctx.author)
        connection.commit()
        connection.close()


def setup(bot):
    bot.add_cog(TasksCog(bot))
