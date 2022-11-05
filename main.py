from discord.ext import commands
import cfg
import commands.levels as lvl
from commands.customization import *
import time
from discord.utils import get

initial_extensions = ['commands.general', 'commands.lol']
bot = commands.Bot(command_prefix=cfg.BOT_PREFIX,
                   pm_help=True, case_insensitive=True)

if __name__ == '__main__':
    if cfg.BOT_TOKEN == "":
        print("Error: No bot token!")
        exit()
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print('Load extension -', extension)
        except Exception as e:
            print(e)


@bot.event
async def on_message(ctx):
    if ctx.author.id != 953947346704691241:
        new = lvl.add_point(ctx.author.id, len(ctx.content))
        if new[2]:
            role = get(ctx.guild.roles, name='1 стадия')
            role_b = get(ctx.guild.roles, name='Духовный Мир')
            await ctx.author.add_roles(role_b)
            await ctx.author.add_roles(role)
        if new[0] != 0:
            role_delete = get(ctx.guild.roles, name='пиковая стадия')
            role = get(ctx.guild.roles, name='1 стадия')
            role_b_d = get(ctx.guild.roles, name=cfg.CULT_RANKS_NAME[new[0]-2])
            role_b = get(ctx.guild.roles, name=cfg.CULT_RANKS_NAME[new[0]-1])
            await ctx.channel.send(ctx.author.mention + 'Поздравляем вы проравались на новую стадию!!!')
            await ctx.author.remove_roles(role_delete)
            await ctx.author.add_roles(role)
            await ctx.author.remove_roles(role_b_d)
            await ctx.author.add_roles(role_b)
        if new[1] != 0 and new[0] == 0:
            if new[1] == 9:
                role = get(ctx.guild.roles, name='пиковая стадия')
            else:
                role = get(ctx.guild.roles, name=str(new[1])+' стадия')
            role_delete = get(ctx.guild.roles, name=str(new[1]-1)+' стадия')
            await ctx.author.remove_roles(role_delete)
            await ctx.author.add_roles(role)

    await bot.process_commands(ctx)


@bot.event
async def on_voice_state_update(member, before, after):
    t = time.localtime()
    current_time = str(time.strftime("%H:%M:%S", t))
    if not (
            before.self_mute or after.self_mute or before.afk or after.afk or before.suppress
            or after.suppress or before.self_video or after.self_video or before.self_stream or after.self_stream
            or before.self_deaf or after.self_deaf or before.mute or after.mute or before.deaf or after.deaf):
        lvl.set_time(member.id, current_time)


bot.run(cfg.BOT_TOKEN, bot=True, reconnect=True)
