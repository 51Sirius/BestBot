import disnake
import cfg
import src.card.card as card
from src.main import *

from disnake.ext import commands


class Ranks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='card', aliases=['cardme'], description="Вернет карточку с рангом")
    async def card(self, inter, member: disnake.Member = None):
        if member is not None:
            rank = get_info_rank(member.id)
            card.create_card(member, rank, get_rank_name(member.id))
            await inter.send(file=disnake.File('src/card/w.png'))
        else:
            rank = get_info_rank(inter.author.id)
            card.create_card(inter.author, rank, get_rank_name(inter.author.id))
            await inter.send(file=disnake.File('src/card/w.png'))



def setup(bot):
    bot.add_cog(Ranks(bot))
