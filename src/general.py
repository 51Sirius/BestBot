import disnake
import cfg

from disnake.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='commands', aliases=['cmd'], description="Responds with 'World'")
    async def _cmd(self, ctx):
        pass


def setup(bot):
    bot.add_cog(General(bot))