import sqlite3


class Database:
    def __init__(self, path="./db.db", **kwargs):
        self.path = path
        self.schemas = {}
        for schema_name, schema in kwargs.items():
            self.schemas[schema_name] = schema 
        print(self.schemas)

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        return self.conn
    
    def __exit__(self, *args):
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
            cursor.execute("INSERT INTO reservation (id, name, amt_guests, date, table_nr) \
                            VALUES (?, ?, ?, ?, ?)", data)
            db.commit()
            

    def remove_data(self, id):
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
            cursor.execute("DELETE FROM reservation WHERE id=?", (id,))
            db.commit()

    def update_data(self, data):
        """
    Updates reservation data in the database based on the provided reservation ID.

    Parameters:
    - self: The instance of the class representing the database connection.
    - data (tuple): A tuple containing reservation data in the order (id, name, amt_guests, date, table_nr).

    Raises:
    - Any exceptions that may occur during database interaction.

    Description:
    This method updates a reservation record in the 'reservation' table of the connected database. It uses the provided
    data tuple to update the corresponding columns (name, amt_guests, date, table_nr) for the specified reservation ID.
    The changes are committed to the database after the execution of the SQL UPDATE statement.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    updated_reservation_data = (1, 'New Name', 5, '2024-02-03', 4)
    db_connection.update_data(updated_reservation_data)
    ```
    """
        with self as db:
            cursor = db.cursor()
            cursor.execute("UPDATE reservation SET name=?, amt_guests=?, date=?, table_nr=? WHERE id=?", 
                           (data[1], data[2], data[3], data[4], data[0]))
            db.commit()

    def get_data(self, id="*"):
        
        with self as db:
            cursor = db.cursor()
            
            if not id == "*": cursor.execute("SELECT * FROM reservation WHERE id=?", id)
            else: cursor.execute("SELECT * FROM reservation")
            
            return cursor.fetchall()
