from disnake.utils import get
import disnake
import cfg
from src.db import *


def get_cult_from_ds(member_roles):
    cult, tmp_cult, stage = 0, 0, 0
    for role_cult in cfg.CULT_RANKS_NAME:
        if role_cult in member_roles:
            tmp_cult += 1
            cult = tmp_cult
            break
        else:
            tmp_cult += 1
    for i in range(1, 9):
        name_stage = str(i) + ' стадия'
        if name_stage in member_roles:
            stage = i
    if stage == 0 and 'пиковая стадия' in member_roles:
        stage = 9
    return cult, stage


def give_name_stage(stage):
    if stage == 9:
        name_stage = 'пиковая стадия'
    else:
        name_stage = str(stage) + ' стадия'
    return name_stage


def get_cult_from_db(member_id):
    return get_cult(member_id), get_stage(member_id)


def sync(member_id, roles):
    cult_from_db = get_cult_from_db(member_id)
    cult_from_ds = get_cult_from_ds(roles)
    if cult_from_db[0] != cult_from_ds[0] or cult_from_db[1] != cult_from_ds[1]:
        if cult_from_db[0] * cult_from_db[1] > cult_from_ds[0] * cult_from_ds[1]:
            return [cult_from_db[0], cult_from_db[1]], False
            print()
        else:
            set_cultivation(member_id, cult_from_ds)
            return [cult_from_ds[0], cult_from_ds[1]], True

    else:
        return cult_from_db, True


async def clear_role_cultivation(member, guild):
    cult_rank, stage = get_cult_from_ds([role.name for role in member.roles])
    role_1 = get(guild.roles, name=cfg.CULT_RANKS_NAME[cult_rank - 1])
    role_2 = get(guild.roles, name=give_name_stage(stage))
    try:
        await member.remove_roles(role_1)
        await member.remove_roles(role_2)
    except AttributeError:
        pass
