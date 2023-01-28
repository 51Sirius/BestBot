import disnake
import cfg

from disnake.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='echo', aliases=['echo'], description="Responds with 'World'")
    async def echo(self, ctx):
        pass


def setup(bot):
    bot.add_cog(General(bot))