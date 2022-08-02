from sqlite3 import *
import cfg

con = connect('db.sqlite')
cur = con.cursor()


def set_nick(user_id, nick):
    cur.execute(f'update users set lol=? where id={user_id}', (nick,))
    con.commit()
    print('Set nick lol to user -', user_id)


def add_hero(name):
    url = 'https://www.leagueofgraphs.com/champions/builds/'+name
    cur.execute(f'insert into lol_heroes(name, url_graph) values (?, ?)', (name, url))
    con.commit()
    print('Create new hero -', name)


def add_achievement(name):
    rslt = ''
    for i in name:
        rslt += i + ' '
    cur.execute(f'insert into lol_achievements(name) values (?)', (rslt,))
    con.commit()
    print('Create new achievement lol -', rslt)
