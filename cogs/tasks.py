from discord.ext import commands
from discord import Member, Embed, Colour
import sqlite3

# Ready
print("Database Succesfully created")


class TasksCog(commands.Cog):
    def __init__(self, bot):
        # DB Variables
        self.bot = bot
        self.db = sqlite3.connect("tasks.sqlite")
        self.db.execute("CREATE TABLE IF NOT EXISTS main (task TEXT, user INT, author INT)")
        self.cursor = self.db.cursor()

    # async def board(self, ctx, member: Member, *, mess):
    #     verbindung = sqlite3.connect('messages.db')
    #     verbindung.execute('CREATE TABLE IF NOT EXISTS board (name TEXT, messages TEXT)')
    #     name = str(member)
    #     cursor = verbindung.cursor()
    #     cursor.execute('INSERT INTO board (name, messages) VALUES (?,?)', (name, mess))
    #     verbindung.commit()
    #     verbindung.close()
    #     await ctx.message.delete()
    #     embed = Embed(title='Nachrichtenbrett',
    #                   description=f'Die Nachricht wurde erfolgreich an das Nachrichtenbrett von {member.mention} angeheftet.',
    #                   color=0x00ffff)
    #     await ctx.send(embed=embed)

    @commands.command()
    async def addtask(self, ctx, user: Member, *, task_param):
        print("000")
        # ErrorEmbed
        error = Embed(title="Error!",
                      description="You got not enough or wrong arguments",
                      colour=0xff0000)
        error.set_footer(text="Please check the correct use and try it again!")
        print("1")
        self.cursor.execute(
            f"INSERT INTO main (task, user, author) VALUES ({task_param}, {user.id}, {ctx.author.id})")
        print("2")
        embed = Embed(title="New Task addet!",
                      description=f"You´ve addet the task `{task_param}` to the user {user.mention}",
                      colour=Colour.from_rgb(0, 255, 56))
        embed.set_footer(text="The task would be displayed on him/her taskboard.")

    @commands.command()
    async def showtasks(self, ctx):
        task = self.cursor.execute(f"SELECT main (task) WHERE user = {ctx.author.id}")
        if task:
            embed = Embed(title="New Task",
                          description="You´ve got following new Task:\n"
                                      "\n"
                                      f"`{task}`",
                          colour=Colour.from_rgb(0, 35, 255))
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(TasksCog(bot))
