import disnake
import cfg

from disnake.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(General(bot))