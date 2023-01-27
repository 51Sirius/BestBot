import disnake
import cfg
from disnake.ext import commands
from main import *
from disnake.utils import get

intents = disnake.Intents.default()
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
                    if check not in roles:
                        try:
                            role = get(guild.roles, name=check)
                            await member.add_roles(role)
                            print(f"User - {member.name} was update with main roles")
                        except Exception as error:
                            print(error)
                #cult_from_db = get_cult_from_db()


bot.run(cfg.BOT_TOKEN_TEST)
