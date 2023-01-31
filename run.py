import disnake
import cfg
from disnake.ext import commands
from src.main import *
from disnake.utils import get
import time

intents = disnake.Intents.all()
intents.members = True

initial_extensions = ['src.general']
bot = commands.InteractionBot(intents=intents)

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
async def on_ready():
    print("Init bot, start synchronization")
    for guild in bot.guilds:
        for member in guild.members:
            roles = [role.name for role in member.roles]
            if "Bots" not in roles and member.id != bot.user.id:
                for check in cfg.MAIN_ROLES:
                    if check not in roles and member.id != cfg.ADMIN_ID:
                        try:
                            role = get(guild.roles, name=check)
                            await member.add_roles(role)
                            print(f"User - {member.name} was update with main roles")
                        except Exception as error:
                            print(error)
                cultivation, antisync, new = sync(member.id, roles)
                if new:
                    await give_role_with_cult(member, [1, 1])
                if not antisync:
                    await give_role_with_cult(member, cultivation)
    print("Bot was started!!!")


@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None or after.channel is None:
        t = int(time.time())
        if before.channel is None:
            await set_time(member.id, t)
        else:
            await update_status(member, t, before.channel.guild)


@bot.event
async def on_member_join(member):
    for check in cfg.MAIN_ROLES:
        try:
            role = get(member.guild.roles, name=check)
            await member.add_roles(role)
            print(f"User - {member.name} was update with main roles")
        except Exception as error:
            print(error)
    cult = [1, 1]
    if exist_user(member.id):
        cult = get_cult_from_db(member.id)
    else:
        add_user(member.id)
    await give_role_with_cult(member, cult)


@bot.event
async def on_message(ctx):
    if ctx.author.id != bot.user.id:
        points = len(ctx.content)
        cult, update = add_point(ctx.author.id, points)
        if update:
            await give_role_with_cult(ctx.author, cult)


bot.run(cfg.BOT_TOKEN_TEST)
