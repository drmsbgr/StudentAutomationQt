import sqlite3

DBNAME = "main.db"


def connectDB():
    con = sqlite3.connect(DBNAME)
    return con


def loadTable(tableName):
    cur = connectDB().cursor()
    res = cur.execute(f"SELECT * FROM {tableName}")
    return res.fetchall()


def executeSql(sql, params=""):
    conn = connectDB()
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    conn.close()
    return cur.lastrowid


def createTable(sql):
    con = connectDB()
    cur = con.cursor()
    cur.execute(sql)
    con.close()


def insertToTable(tableName: str, schema: str, data: tuple):
    con = connectDB()
    cur = con.cursor()
    cur.executemany(f"INSERT INTO {tableName} VALUES ({schema})", data)
    con.commit()
    con.close()
