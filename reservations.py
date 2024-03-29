import sqlite3
from json import loads as json_loads


class Reservation:
    """Denhär klassen är för att boka bord och spara bokningar i databasen och för att göra förändringar i bokningar"""

    @staticmethod
    def from_db(db, db_data: list):
        db_data = db_data[0]
        reservation = Reservation(
            db, db_data[2], db_data[1], db_data[3], db_data[4], db_data[0])
        return reservation

    def __init__(self, db, user_amount, user_name, user_date, table_id, id=None):
        self.db = db
        self.id = db.next_reservation_id() if id == None else id
        self.user_amount = user_amount
        self.user_name = user_name
        self.user_date = user_date
        self.table_id = table_id

    def __str__(self):
        # Visar vad användares bokning innehåller
        return f"Reservation '{self.user_name}':\nID: {self.id}\nAmount: {self.user_amount}\nDate: {self.user_date}\nTable #: {self.table_id}"

    def imposible(self):
        # Ifall användaren försöker boka för mer än 8 personer
        return "This is not possible.\n Cant make reservation for more than 8 people.\nThis is a restaurant not a circus."

    def push_to_db(self):
        self.db.insert_reservation(self)

    def to_db_format(self):
        # Metod för att spara bokningar i databasen
        # (id, name, amt_guests, date, table_nr)
        return (self.id, self.user_name, self.user_amount, self.user_date, self.table_id)
