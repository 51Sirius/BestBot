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

    @commands.has_role('Глава секты')
    @commands.slash_command(name='transport', aliases=['trans'],
                            description="Перенесет культивацию с одного человека другому")
    async def transport(self, inter, from_member: disnake.Member, to_member: disnake.Member):
        score = give_point_from_user(from_member.id)
        cult, update = add_point(to_member.id, score)
        clear_cult(from_member)
        if update:
            await give_role_with_cult(to_member, cult)
        await inter.send('Transfer is successfully')

    @commands.has_role('Глава секты')
    @commands.slash_command(name='add_point',
                            description="Добавляет очки")
    async def add_point(self, inter, to_member: disnake.Member = None, value=0):
        if to_member is not None:
            cult, update = add_point(to_member.id, value)
            if update:
                await give_role_with_cult(to_member, cult)
            await inter.send('Add points to member')
        else:
            cult, update = add_point(inter.author.id, int(value))
            if update:
                await give_role_with_cult(inter.author, cult)
            await inter.send('Add point')

    @commands.has_role('Глава секты')
    @commands.slash_command(name='how_many_dao',
                            description="Сколько духовной силы у человека")
    async def how_many_dao(self, inter, member: disnake.Member = None):
        if member is not None:
            score = give_point_from_user(member.id)
            await inter.send(f'User {member.name} has {score}')
        else:
            score = give_point_from_user(inter.author.id)
            await inter.send(f'You have {score}')


def setup(bot):
    bot.add_cog(Ranks(bot))
