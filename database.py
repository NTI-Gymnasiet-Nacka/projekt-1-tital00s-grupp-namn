import sqlite3



class Database:

    def __init__(self, path="./db.db", **kwargs):
        self.path = "./db.db"
        self.schemas = {}
        for schema_name, schema in kwargs.items():
            self.schemas[schema_name] = schema 
        print(self.schemas)

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        return self.conn
    
    def __exit__(self):
        self.conn.close()
        
    def insert_data(self, data):
        """
    Inserts reservation data into the database.

    Parameters:
    - self: The instance of the class representing the database connection.
    - data (tuple): A tuple containing reservation data in the order (id, name, amt_guests, date, table_nr).

    Raises:
    - Any exceptions that may occur during database interaction.

    Description:
    This method inserts reservation data into the 'reservation' table of the connected database. It uses the provided data
    tuple to populate the corresponding columns (id, name, amt_guests, date, table_nr). The changes are committed to the
    database after the execution of the SQL INSERT statement.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    reservation_data = (1, 'John Doe', 4, '2024-02-02', 3)
    db_connection.insert_data(reservation_data)
    ```
    """
        with self as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO reservation (id, name, amt_guests, date, table_nr) VALUE (?, ?, ?, ?, ?)", data)
            db.commit()
            

    def remove_data(self, data):
        """
    Removes reservation data from the database based on the provided reservation ID.

    Parameters:
    - self: The instance of the class representing the database connection.
    - data (tuple): A tuple containing the reservation ID to identify the record to be deleted.

    Raises:
    - Any exceptions that may occur during database interaction.

    Description:
    This method removes a reservation record from the 'reservation' table in the connected database. It uses the provided
    reservation ID to identify the specific record to be deleted. The changes are committed to the database after the
    execution of the SQL DELETE statement.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    reservation_id_to_remove = ("example", "data")
    db_connection.remove_data(reservation_id_to_remove)
    ```
    Note: The reservation ID should be provided as a single-element tuple.

    """
        with self as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM reservation WHERE id=?", data[0])
            db.commit()

    def update_data():
        pass

    def get_data():
        pass

db = Database(reservation=["first_name", "last_name"])
    