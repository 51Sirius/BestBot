from discord.ext import commands
import cfg
import commands.database as db
from commands.customization import *
import time
from discord.utils import get
import discord

intents = discord.Intents.default()
intents.members = True

initial_extensions = ['commands.general', 'commands.lol']
bot = commands.Bot(command_prefix=cfg.BOT_PREFIX,
                   pm_help=True, case_insensitive=True, intents=intents)

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
        points = len(ctx.content)
        new_1, new_2 = db.add_point(ctx.author.id, points)
        if new_1:
            role = get(ctx.guild.roles, name="Духовный Мир")
            role_b = get(ctx.guild.roles, name="1 стадия")
            await ctx.author.add_roles(role)
            await ctx.author.add_roles(role_b)
        else:
            if not (new_2[0] == 0 and new_2[1] == 0):
                await clear_rank_role(ctx.author, ctx.guild)
                await ctx.author.add_roles(get(ctx.guild.roles, name=cfg.CULT_RANKS_NAME[new_2[0] - 1]))
                await ctx.author.add_roles(get(ctx.guild.roles, name=f"{new_2[1]} стадия"))

    await bot.process_commands(ctx)


@bot.event
async def on_voice_state_update(member, before, after):
    t = time.localtime()
    current_time = str(time.strftime("%H:%M:%S", t))
    if not (
            before.self_mute or after.self_mute or before.afk or after.afk or before.suppress
            or after.suppress or before.self_video or after.self_video or before.self_stream or after.self_stream
            or before.self_deaf or after.self_deaf or before.mute or after.mute or before.deaf or after.deaf):
        db.set_time(member.id, current_time)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        for member in guild.members:
            roles = [x.name for x in member.roles]
            for check in cfg.MAIN_ROLES:
                if check not in roles:
                    role = get(guild.roles, name=check)
                    await member.add_roles(role)
                    print(f"User - {member.name} was update")
            flag = False
            rank_cult = 1
            for check in cfg.CULT_RANKS_NAME:
                if check in roles:
                    flag = True
                    break
                rank_cult += 1
            if not flag:
                db.add_user(member.id)
                role = get(guild.roles, name="Духовный Мир")
                role_b = get(guild.roles, name="1 стадия")
                await member.add_roles(role)
                await member.add_roles(role_b)
            else:
                db.check_user(member.id)
                stadia = 9
                for i in range(1, 9):
                    if str(i) + ' стадия' in roles:
                        stadia = i
                if not db.check_sync(member.id, rank_cult, stadia):
                    print(f"User - {member.name} was sync to {rank_cult, stadia}")
    print("BOT has start working")


async def clear_rank_role(user, guild, rank_cult=None, stadia=None):
    roles = user.roles
    roles = [x.name for x in roles]
    if stadia is None:
        stadia = 9
        for i in range(1, 9):
            if str(i) + ' стадия' in roles:
                stadia = i
        if stadia == 9:
            stadia = "пиковая"
    if rank_cult is None:
        rank_cult = 1
        for check in cfg.CULT_RANKS_NAME:
            if check in roles:
                break
            rank_cult += 1
            print(check, roles)
    role_1 = get(guild.roles, name=cfg.CULT_RANKS_NAME[rank_cult - 1])
    role_2 = get(guild.roles, name=str(stadia) + ' стадия')
    await user.remove_roles(role_1)
    await user.remove_roles(role_2)


bot.run(cfg.BOT_TOKEN_TEST, bot=True, reconnect=True)
