from discord.ext import commands
import cfg
import commands.levels as lvl
from commands.customization import *
import time

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
        if new:
            await ctx.channel.send(ctx.author.mention + 'Поздравляем вы проравались на новую стадию!!!')
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
