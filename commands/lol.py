import discord
import cfg
from commands.customization import *
from commands.levels import set_nick
from discord.ext import commands
from discord.ext.commands import has_permissions


class Lol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setlolnick', aliases=['setnick'])
    async def _setlolnick(self, ctx, nick):
        await set_nick(ctx.author.id, nick)


def setup(bot):
    bot.add_cog(Lol(bot))
