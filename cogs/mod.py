from discord.ext import commands
from discord import Embed, Member, utils


class ModCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mute(self, ctx, member: Member):
        muted = utils.get(ctx.guild.roles, name='muted')

        if not muted:
            await ctx.guild.create_role(name='muted')

        for channel in ctx.guild.channels:
            await channel.set_permissions(muted,
                                          speak=False,
                                          send_messages=False,
                                          read_message_history=True,
                                          read_messages=True)

        await member.add_roles(muted)
        embed = Embed(
            title='Moderator',
            description=f'{member.mention} was muted by an moderator',
            color=0x3273a8
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def unmute(self, ctx, member: Member):
        muted = utils.get(ctx.guild.roles, name='muted')
        await member.remove_roles(muted)
        embed = Embed(
            title='Moderator',
            description=f'{member.mention} was unmuted by an moderator',
            color=0x3273a8
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ModCog(bot))
