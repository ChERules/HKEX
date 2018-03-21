import os
import sqlite3

def csv2db(inp, tbl):
    sqlcom = 'INSERT INTO ' + tbl +' VALUES ('
    t = tuple()
    co = open(inp, 'r')
    l = co.readline()
    t = l.split(',')
    sqlcom = sqlcom + ('?,'*len(t))[:-1] + ')'

    for l in co:
        l = l.strip()
        t = l.split(',')
        c.execute(sqlcom, t)
    co.close()
    conn.commit()

ddir = os.getcwd() + '/Data/'
# os.chdir(ddir)
if os.path.isfile('quotes.db'): os.remove('quotes.db')

conn = sqlite3.connect('quotes.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS company (
    code integer,
    name text,
    cur  text,
    outstanding integer,
    added integer)''')

csv2db((ddir+'company.csv'), 'company')

c.execute('''CREATE TABLE IF NOT EXISTS quotations (
    code integer,
    date integer,
    tdn integer,
    high real,
    low real,
    close real,
    ask real,
    bid real,
    turnover integer,
    volumename integer)''')

csv2db((ddir+'quotations.csv'), 'quotations')

conn.close()
