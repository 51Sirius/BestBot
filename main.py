from discord.ext import commands
import cfg
import commands.levels as lvl
from commands.customization import *

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
    await lvl.add_point(ctx.author.id, len(ctx.content))
    await bot.process_commands(ctx)


bot.run(cfg.BOT_TOKEN, bot=True, reconnect=True)
