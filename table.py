from database import next_table_id
from database import new_table


class Table:
    @staticmethod
    def from_db(db_data: list):
        table = Table(db_data[1])
        table.id = db_data[0]
        table.occupied = db_data[2]
        return table

    def __init__(self, capacity: int) -> None:
        self.id = next_table_id()
        self.capacity = capacity
        self.occupied = False

    def push_to_db(self):
        new_table(self.id, self.capacity, self.occupied)
