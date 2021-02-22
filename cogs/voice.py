from discord.ext import commands
from discord import PermissionOverwrite,Member,Embed

class VoiceCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
#        if member.bot:
#            return

        if after.channel:
            if after.channel.name == 'New Talk':
                category = after.channel.category
                channel = await after.channel.guild.create_voice_channel(name=f"{member.name}'s Talk",
                                                                         category=category)
                if channel:
                    await member.move_to(channel)

            if after.channel.name == 'New Private Talk':
                overwrites = {
                    after.channel.guild.default_role: PermissionOverwrite(connect=False),
                    member: PermissionOverwrite(connect=True,
                                                speak=True)
                }
                category2 = after.channel.category
                channel2 = await after.channel.guild.create_voice_channel(name=f"{member.name}'s Talk",
                                                                          category=category2,
                                                                          overwrites=overwrites)
                if channel2:
                    await member.move_to(channel2)

        if before.channel:
            if before.channel.category.name == 'Voice':
                if len(before.channel.members) == 0:
                    if before.channel.name == 'New Talk' or before.channel.name == 'New Private Talk':
                        pass
                    else:
                        await before.channel.delete()

def setup(bot):
    bot.add_cog(VoiceCog(bot))