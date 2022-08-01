from sqlite3 import *
import cfg

con = connect('db.sqlite')
cur = con.cursor()


async def add_point(user_id, points):
    user = cur.execute('select * from users where id = ?', (user_id,))
    if user.fetchone() is None:
        user = await add_user(user_id)
    old_point = int(cur.execute('select exp from users where id = ?', (user_id,)).fetchone()[0])
    points = old_point + points * cfg.BUST_XP
    points, new = check_rank(user_id, points)
    cur.execute(f'update users set exp={points} where id=?', (user_id,))
    con.commit()
    return new


async def add_user(user_id):
    cur.execute("INSERT INTO users(id,exp,cult_rank,stadia_cult) VALUES (?,?,?,?)", (user_id, 0, 1, 1))
    con.commit()
    print(f'Add new user with id - {user_id}')
    return cur.execute('select * from users where id = ?', (user_id,))


async def set_nick(user_id, nick):
    cur.execute(f'update users set lol=? where id={user_id}', (nick,))
    con.commit()
    print('Set nick lol to user -', user_id)


async def add_hero(name):
    cur.execute(f'insert into lol_heroes(name) values (?)', (name,))
    con.commit()
    print('Create new hero -', name)


def get_score(user_id):
    return cur.execute('select exp from users where id=?', (user_id,)).fetchone()[0]


def get_rank(user_id):
    count = 1
    ls_users = cur.execute('select id from users order by exp desc').fetchall()
    for i in ls_users:
        if i[0] == user_id:
            return count
        count += 1


def check_rank(user_id, points):
    rank_cult = cur.execute('select cult_rank from users where id=?', (user_id,)).fetchone()[0]
    wall = cfg.CULT_POINTS_WALL[rank_cult - 1]
    point = points
    new = False
    if points >= wall:
        point = points - wall
        stage = cur.execute('select stadia_cult from users where id=?', (user_id,)).fetchone()[0]
        if stage == 9:
            cur.execute(f'update users set cult_rank=? where id={user_id}', (rank_cult + 1,))
            cur.execute(f'update users set stadia_cult=1 where id={user_id}')
            new = True
        else:
            cur.execute(f'update users set stadia_cult=? where id={user_id}', (stage + 1,))
        con.commit()
    return point, new


def get_rank_name(user_id):
    rank_cult = cur.execute('select cult_rank from users where id=?', (user_id,)).fetchone()[0]
    stage = cur.execute('select stadia_cult from users where id=?', (user_id,)).fetchone()[0]
    return str(cfg.CULT_RANKS_NAME[rank_cult - 1] + ' ' + str(stage))


def get_info_rank(user_id):
    rank_cult = cur.execute('select cult_rank from users where id=?', (user_id,)).fetchone()[0]
    return [rank_cult, [get_score(user_id), cfg.CULT_POINTS_WALL[rank_cult - 1]]]
