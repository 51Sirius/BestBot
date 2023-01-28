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
