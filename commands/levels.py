from sqlite3 import *
import cfg

con = connect('db.sqlite')
cur = con.cursor()


async def add_point(user_id, points):
    user = cur.execute('select * from users where id = ?', (user_id,))
    if user.fetchone() is None:
        user = await add_user(user_id)
    old_point = int(cur.execute('select exp from users where id = ?', (user_id,)).fetchone()[0])
    cur.execute(f'update users set exp={old_point + points * cfg.BUST_XP} where id=?', (user_id,))
    con.commit()


async def add_user(user_id):
    cur.execute("INSERT INTO users(id,exp) VALUES (?,?)", (user_id, 0))
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