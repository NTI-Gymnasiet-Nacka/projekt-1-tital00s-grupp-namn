import sqlite3


class Database:
    def __init__(self, path="./db.db", **kwargs):
        self.path = path
        self.schemas = {}
        for schema_name, schema in kwargs.items():
            self.schemas[schema_name] = schema

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        return self.conn
    
    def __exit__(self, *args):
        self.conn.close()
        
    def next_id(self):
        """
    Generate the next unique ID for a new reservation based on existing entries in the database.

    This method accesses the 'reservation' table in the database, retrieves all existing reservations,
    and calculates the next available unique ID. If there are no existing reservations, it starts the
    IDs from 1. Otherwise, it finds the maximum ID in use and increments it by 1 to ensure uniqueness.

    Returns:
        new_id (int): The next available unique ID for a new reservation.
    """
        with self as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM reservation")
            reservations = cursor.fetchall()
            
            if len(reservations) == 0:
                new_id = 1
                return new_id
            
            new_id = max([int(data[0]) for data in reservations]) + 1
            return new_id
    
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
        """
    Retrieves reservation data from the database based on the provided reservation ID.

    Parameters:
    - self: The instance of the class representing the database connection.
    - id (int or str, optional): The reservation ID to identify the record to be retrieved.
      Defaults to "*" (wildcard), meaning all records will be retrieved.

    Returns:
    - list of tuples: A list containing tuples representing reservation data matching the provided ID.
      Each tuple corresponds to a row in the 'reservation' table.

    Raises:
    - Any exceptions that may occur during database interaction.

    Description:
    This method retrieves reservation data from the 'reservation' table in the connected database. If a specific
    reservation ID is provided, only the record with that ID is retrieved. If the ID is set to "*", all records are
    retrieved. The function returns a list of tuples, where each tuple contains the values of a row in the 'reservation'
    table.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    
    # Retrieve all reservation data
    all_reservations = db_connection.get_data()

    # Retrieve reservation data for a specific ID
    reservation_id_to_retrieve = 1
    specific_reservation = db_connection.get_data(reservation_id_to_retrieve)
    ```
    """
        with self as db:
            cursor = db.cursor()
            
            if not id == "*": cursor.execute("SELECT * FROM reservation WHERE id=?", (id,))
            else: cursor.execute("SELECT * FROM reservation")
            
            return cursor.fetchall()
