from database import next_table_nr
from database import new_table
from timetable import gen_timetable
from json import loads as json_loads
from json import dumps as json_dumps


class Table:
    @staticmethod
    def from_db(db_data: list):
        table = Table(db_data[1])
        table.id = db_data[0]
        table.occupied = json_loads(db_data[2])
        return table

    def __init__(self, capacity: int) -> None:
        self.id = next_table_nr()
        self.capacity = capacity
        self.occupied = gen_timetable()

    def push_to_db(self):
        new_table(self.id, self.capacity, json_dumps(self.occupied))
