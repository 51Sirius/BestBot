from sqlite3 import *
import cfg

con = connect('db.sqlite')
cur = con.cursor()


def add_point(user_id, points):
    user = cur.execute('select * from users where id = ?', (user_id,))
    if user.fetchone() is None:
        user = add_user(user_id)
    old_point = int(cur.execute('select exp from users where id = ?', (user_id,)).fetchone()[0])
    points = old_point + points * cfg.BUST_XP
    points, new = check_rank(user_id, points)
    cur.execute(f'update users set exp={points} where id=?', (user_id,))
    con.commit()
    return new


def add_user(user_id):
    cur.execute("INSERT INTO users(id,exp,cult_rank,stadia_cult) VALUES (?,?,?,?)", (user_id, 0, 1, 1))
    con.commit()
    print(f'Add new user with id - {user_id}')
    return cur.execute('select * from users where id = ?', (user_id,))


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
    new = [0, 0, False]
    stage = cur.execute('select stadia_cult from users where id=?', (user_id,)).fetchone()[0]
    if stage == 1 and rank_cult == 1:
        new[2] = True
    if points >= wall:
        point = points - wall
        if stage == 9:
            cur.execute(f'update users set cult_rank=? where id={user_id}', (rank_cult + 1,))
            cur.execute(f'update users set stadia_cult=1 where id={user_id}')
            new = [rank_cult+1, 1]
        else:
            cur.execute(f'update users set stadia_cult=? where id={user_id}', (stage + 1,))
            new[0], new[1] = [0, stage+1]
            print(new)
        con.commit()
    return point, new


def get_rank_name(user_id):
    rank_cult = cur.execute('select cult_rank from users where id=?', (user_id,)).fetchone()[0]
    stage = cur.execute('select stadia_cult from users where id=?', (user_id,)).fetchone()[0]
    return str(cfg.CULT_RANKS_NAME[rank_cult - 1] + ' ' + str(stage))


def get_info_rank(user_id):
    rank_cult = cur.execute('select cult_rank from users where id=?', (user_id,)).fetchone()[0]
    return [rank_cult, [get_score(user_id), cfg.CULT_POINTS_WALL[rank_cult - 1]]]


def set_time(user_id, current_time):
    time = cur.execute('select time_start from users where id=?', (user_id,)).fetchone()[0]
    if time == '0':
        cur.execute('update users set time_start=? where id=?', (current_time, user_id))
        con.commit()

    else:
        cur.execute('update users set time_start=? where id=?', ('0', user_id))
        con.commit()
        points = 0
        hours_first = int(time[:2])
        hours_second = int(current_time[:2])
        tmp_hours = hours_second - hours_first
        minutes_first = int(time[3:5])
        minutes_second = int(current_time[3:5])
        tmp_minutes = minutes_second - minutes_first
        if tmp_hours < 0:
            tmp_hours += 24
        if tmp_minutes <= 0:
            points = (tmp_hours*60 + minutes_second - minutes_first)*2*cfg.BUST_XP
        else:
            points = (tmp_hours*60 + tmp_minutes)*2*cfg.BUST_XP
        add_point(user_id, points)
