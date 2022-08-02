import discord
import cfg
from commands.customization import *
from commands.lol_db import *
from discord.ext import commands
from discord.ext.commands import has_permissions


class Lol(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setlolnick', aliases=['setnick'])
    async def _setlolnick(self, ctx, nick):
        set_nick(ctx.author.id, nick)

    @commands.command(name='addhero', aliases=['addherolol'])
    async def _addhero(self, ctx, nick):
        add_hero(nick)

    @commands.command(name='addachievemnt', aliases=['addach'])
    async def _addach(self, ctx, *args):
        add_achievement(args)


def setup(bot):
    bot.add_cog(Lol(bot))
