import sqlite3

def Init(db):
    connection = None
    try:
        connection = sqlite3.connect(db)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return connection

connection = Init("gradingDB")
connection.close()