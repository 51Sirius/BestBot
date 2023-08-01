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
    if not exist_user(member_id):
        add_user(member_id)
        return 0, True, True
    cult_from_db = get_cult_from_db(member_id)
    cult_from_ds = get_cult_from_ds(roles)
    if cult_from_db[0] != cult_from_ds[0] or cult_from_db[1] != cult_from_ds[1]:
        if cult_from_db[0] * 9 + cult_from_db[1] > cult_from_ds[0] * 9 + cult_from_ds[1]:
            return [cult_from_db[0], cult_from_db[1]], False, False
        else:
            set_cultivation(member_id, cult_from_ds)
            return [cult_from_ds[0], cult_from_ds[1]], True, False

    else:
        return cult_from_db, True, False


async def clear_role_cultivation(member, guild):
    cult_rank, stage = get_cult_from_ds([role.name for role in member.roles])
    role_1 = get(guild.roles, name=cfg.CULT_RANKS_NAME[cult_rank - 1])
    role_2 = get(guild.roles, name=give_name_stage(stage))
    try:
        await member.remove_roles(role_1)
        await member.remove_roles(role_2)
    except AttributeError:
        pass


def add_point(member_id, value):
    cult = get_cult(member_id)
    stage = get_stage(member_id)
    flag = False
    while get_score(member_id) + value >= cfg.CULT_POINTS_WALL[cult - 1]:
        flag = True
        stage += 1
        value -= cfg.CULT_POINTS_WALL[cult - 1] - get_score(member_id)
        if stage == 10:
            cult += 1
            stage = 1
        set_score(member_id, 0)
    set_score(member_id, value+get_score(member_id))
    print(f'User - {member_id} was update score')
    return [cult, stage], flag


async def update_member(member, guild):
    cultivation = get_cult_from_db(member.id)
    await clear_role_cultivation(member, guild)
    role_cult = get(guild.roles, name=cfg.CULT_RANKS_NAME[cultivation[0] - 1])
    role_stage = get(guild.roles, name=give_name_stage(cultivation[1]))
    try:
        await member.add_roles(role_cult)
        await member.add_roles(role_stage)
    except AttributeError:
        pass
    print(f'User - {member.name} was update with cultivation roles')


async def add_voice_count(member_id, count):
    pass


async def update_status(member, t, guild):
    last = int(get_time(member.id))
    points = (t - last) // 30
    cult, status = add_point(member.id, points * cfg.BUST_XP * get_bust_exp(member.id))
    await set_time(member.id, 0)
    if status:
        await update_member(member, guild)


async def give_role_with_cult(member, cult):
    await clear_role_cultivation(member, member.guild)
    role_cult = get(member.guild.roles, name=cfg.CULT_RANKS_NAME[cult[0] - 1])
    role_stage = get(member.guild.roles, name=give_name_stage(cult[1]))
    try:
        await member.add_roles(role_cult)
        await member.add_roles(role_stage)
    except AttributeError:
        pass
    print(f'User - {member.name} was add role with cult')


def get_rank_name(user_id):
    rank_cult = cur.execute('select cult_rank from users where id=?', (user_id,)).fetchone()[0]
    stage = cur.execute('select stadia_cult from users where id=?', (user_id,)).fetchone()[0]
    return str(cfg.CULT_RANKS_NAME[rank_cult - 1] + ' ' + str(stage))