from sqlite3 import *

con = connect('db.sqlite')
cur = con.cursor()


def get_stage(member_id):
    return cur.execute('select stadia_cult from users where id=?', (member_id,)).fetchone()[0]


def get_cult(member_id):
    return cur.execute('select cult_rank from users where id=?', (member_id,)).fetchone()[0]


def set_cult(member_id, value):
    try:
        cur.execute('update users set cult_rank=? where id=?', (value, member_id))
        con.commit()
        return True
    except Exception as error:
        print(error)
        return False


def set_stage(member_id, value):
    try:
        cur.execute('update users set stadia_cult=? where id=?', (value, member_id))
        con.commit()
        return True
    except Exception as error:
        print(error)
        return False


def set_cultivation(member_id, values):
    set_cult(member_id, values[0])
    set_stage(member_id, values[1])


async def set_time(member_id, value):
    try:
        cur.execute('update users set time_start=? where id=?', (value, member_id))
        con.commit()
        return True
    except Exception as error:
        print(error)
        return False


def get_time(member_id):
    return cur.execute('select time_start from users where id=?', (member_id,)).fetchone()[0]


def get_score(member_id):
    return cur.execute('select exp from users where id=?', (member_id,)).fetchone()[0]


def set_score(member_id, value):
    try:
        cur.execute('update users set exp=? where id=?', (value, member_id))
        con.commit()
        return True
    except Exception as error:
        print(error)
        return False


def get_bust_exp(member_id):
    return cur.execute('select bust_exp from users where id=?', (member_id,)).fetchone()[0]


def exist_user(member_id):
    return cur.execute('select * from users where id=?', (member_id,)).fetchone() is not None


def add_user(user_id, points=0):
    cur.execute("INSERT INTO users(id,exp,cult_rank,stadia_cult) VALUES (?,?,?,?)", (user_id, points, 1, 1))
    con.commit()
    print(f'Add new user with id - {user_id}')
    return cur.execute('select * from users where id = ?', (user_id,))

