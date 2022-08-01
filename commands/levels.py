from sqlite3 import *
import cfg


con = connect('db.sqlite')
cur = con.cursor()


def add_point(user_id, points):
    user = cur.execute('select * from users where id = ?', (user_id,))
    if user.fetchone() is None:
        user = add_user(user_id)
    old_point = int(cur.execute('select exp from users where id = ?', (user_id,)).fetchone()[0])
    cur.execute(f'update users set exp={old_point+points*cfg.BUST_XP} where id=?', (user_id,))
    con.commit()


def add_user(user_id):
    cur.execute("INSERT INTO users(id) VALUES (?)", (user_id,))
    con.commit()
    print(f'Add new user with id - {user_id}')
    return cur.execute('select * from users where id = ?', (user_id,))
