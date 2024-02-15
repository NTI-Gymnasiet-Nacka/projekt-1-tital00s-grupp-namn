import sqlite3


class Reservation:
    """Denhär klassen är för att boka bord och spara bokningar i databasen och för att göra förändringar i bokningar"""

    def __init__(self, db, user_amount, user_name, user_date, table_id):
        self.db = db
        self.id = db.next_reservation_id()
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

    def new_reservation(self):
        # Metod för att göra reservationer
        pass

    def push_to_db(self):
        self.db.insert_reservation(self)

    def to_db_format(self):
        # Metod för att spara bokningar i databasen
        # (id, name, amt_guests, date, table_nr)
        return (self.id, self.user_name, self.user_amount, self.user_date, self.table_id)
