import sqlite3
import pandas as pd

def create_conn():
    con = sqlite3.connect('../data/database.db')
    cur = con.cursor()
    return cur

def query_execute(cur, query):
    res = cur.execute(query)
    data = res.fetchall()
    df = pd.DataFrame(data, columns= [i[0] for i in res.description])
    return df

def close_conn(cur):
    cur.close()

