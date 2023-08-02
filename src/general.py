import disnake

import cfg
import src.image.conv as conv

from disnake.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name='convert_to_multi', description="Вернет мультяшный вариант")
    async def convert_to_multi(self, inter, image: str):

        conv.convert_to_multi(image, 'src/image/1.jpg')
        await inter.send(file=disnake.File('src/image/1.jpg'))


def setup(bot):
    bot.add_cog(General(bot))
