import sqlite3

DBNAME = "main.db"


def connectDB():
    con = sqlite3.connect(DBNAME)
    return con


def loadTable(tableName):
    cur = connectDB().cursor()
    res = cur.execute(f"SELECT * FROM {tableName}")
    return res.fetchall()


def executeSql(sql):
    cur = connectDB().cursor()
    return cur.execute(sql)


def createTable(sql):
    con = connectDB()
    cur = con.cursor()
    cur.execute(sql)
    con.close()
