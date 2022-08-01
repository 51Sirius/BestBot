import discord
import cfg
from commands.customization import *

from discord.ext import commands
import commands.images as img
from commands.levels import *
from discord.ext.commands import has_permissions


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='commands', aliases=['cmd'])
    async def _connect(self, ctx):
        await ctx.send(frm_ls_to_block(cfg.COMMAND_LIST))

    @commands.command(name='rank', aliases=['r'])
    async def _rank(self, ctx):
        img.create_lvl_card(ctx)
        #await ctx.channel.send(file=discord.File('images/tmp.png'))


def setup(bot):
    bot.add_cog(General(bot))
