import sqlite3

with sqlite3.connect("animal.db") as db:
    db.row_factory =sqlite3.Row
    res = db.execute("select * from animals").fetchall()

    for i in res:
        print(dict(i))


