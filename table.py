from timetable import gen_timetable
from json import loads as json_loads
from json import dumps as json_dumps


class Table:
    @staticmethod
    def from_db(db, db_data: list):
        table = Table(db, db_data[1])
        table.id = db_data[0]
        table.occupied = json_loads(db_data[2])
        return table

    def __init__(self, db, capacity: int) -> None:
        self.db = db
        self.id = self.db.next_table_nr()
        self.capacity = capacity
        self.occupied = gen_timetable()

    def __str__(self) -> str:
        return f"Table {self.id}, capacity: {self.capacity}, occupied: {json_dumps(self.occupied, indent=2)}"

    def push_to_db(self):
        self.occupied = json_dumps(self.occupied)
        self.db.new_table(self)
