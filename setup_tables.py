from table import Table
from database import Database

db = Database("./test.db")
for i in range(4):
    table = Table(db, 2)
    table.push_to_db()

for i in range(6):
    table = Table(db, 4)
    table.push_to_db()

for i in range(6):
    table = Table(db, 6)
    table.push_to_db()

for i in range(6):
    table = Table(db, 6)
    table.push_to_db()
