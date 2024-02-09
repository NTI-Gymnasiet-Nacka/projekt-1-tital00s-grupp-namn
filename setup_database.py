import sqlite3

conn = sqlite3.connect("./db.db")

cur = conn.cursor()

cur.execute(''' CREATE TABLE IF NOT EXISTS reservation 
            (id INTEGER,
            name TEXT,
            amt_guests INTEGER,
            date TEXT,
            table_nr INTEGER)
''')

cur.execute(''' CREATE TABLE IF NOT EXISTS tables 
            (table_nr INTEGER,
            capacity INTEGER,
            occupied BOOL)
''')

cur.close()
conn.close()

# Det här är ett schema för vår databas där all information 
# sparas i ordningen ovan där id i int osv. frågor mejla niklas