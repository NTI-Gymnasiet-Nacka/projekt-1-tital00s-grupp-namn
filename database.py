import sqlite3
from table import Table
from reservations import Reservation
from json import dumps as json_dumps


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
    
    def next_reservation_id(self):
        """
    Generate the next unique ID for a new reservation based on existing entries in the database.

    This method queries the database to determine the next available reservation ID. It fetches all existing 
    reservations from the 'reservation' table, calculates the maximum ID, and returns the next available ID 
    by incrementing the maximum ID by one. If no reservations exist in the database, it returns 1 as the 
    starting ID.

    Parameters:
    - self: The instance of the class representing the database connection.

    Returns:
    - new_id (int): The next available unique ID for a new reservation.

    Raises:
    - Any exceptions that may occur during database interaction.

    Description:
    This method retrieves the next available reservation ID to ensure the uniqueness of reservation IDs 
    within the database. It is typically used when adding a new reservation to the database to assign a 
    unique ID to the reservation.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    next_id = db_connection.next_reservation_id()
    print("Next available reservation ID:", next_id)
    ```

    Note: This method assumes that reservation IDs are integers and are stored in the first column of the 
    'reservation' table in the database.
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

    def insert_reservation(self, reservation: Reservation):
        """
    Inserts reservation data into the 'reservation' table of the connected database.

    Parameters:
    - self: The instance of the class representing the database connection.
    - reservation (Reservation): An instance of the Reservation class representing the reservation to be inserted.

    Returns:
    - None: Returns None if an exception occurs during the database interaction.

    Raises:
    - sqlite3.ProgrammingError: Raised if there's an issue with the SQL execution.

    Description:
    This method attempts to insert reservation data into the 'reservation' table of the connected database. The provided
    reservation object is used to populate the corresponding columns (id, name, amt_guests, date, table_nr). If an 
    exception, specifically sqlite3.ProgrammingError, occurs during the SQL execution, it is caught, printed, and the 
    function returns None. Otherwise, the changes are committed to the database, and the occupancy status of the 
    associated table is updated accordingly.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    new_reservation = Reservation(id=1, user_name='John Doe', user_amount=4, user_date='2024-02-02', table_id=3)
    db_connection.insert_reservation(new_reservation)
    ```
    """
        with self as db:
            cursor = db.cursor()
            if reservation.id > 0 and reservation.user_amount > 0 and reservation.table_id > 0:
                try:
                    cursor.execute("INSERT INTO reservation (id, name, amt_guests, date, table_nr) \
                                    VALUES (?, ?, ?, ?, ?)", reservation.to_db_format())
                except sqlite3.ProgrammingError as p:
                    print(p)
                    return None
            else:
                print("None digit value was entered.")

            db.commit()
            self.set_occupied(reservation)

    def remove_reservation(self, id):
        """
    Removes a reservation record from the 'reservation' table based on the provided reservation ID.

    Parameters:
    - self: The instance of the class representing the database connection.
    - id (int or str): The reservation ID to identify the record to be deleted.

    Raises:
    - Any exceptions that may occur during database interaction.

    Description:
    This method removes a reservation record from the 'reservation' table in the connected database. The provided
    reservation ID is used to identify the specific record to be deleted. If the ID is not found in the table, an error
    message is printed. The changes are committed to the database after the execution of the SQL DELETE statement.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    reservation_id_to_remove = 1
    db_connection.remove_reservation(reservation_id_to_remove)
    ```
    """
        old_length = len(self.get_reservation())
        with self as db:
            cursor = db.cursor()
            cursor.execute("DELETE FROM reservation WHERE id=?", (id,))
            if old_length == len(self.get_reservation()):
                print("Error: Id not found.")
            db.commit()

    def update_reservation(self, data):
        """
    Updates reservation data in the 'reservation' table of the connected database based on the provided reservation ID.

    Parameters:
    - self: The instance of the class representing the database connection.
    - data (tuple): A tuple containing reservation data in the order (id, name, amt_guests, date, table_nr).

    Returns:
    - None: Returns None if an exception occurs during the database interaction.

    Raises:
    - IndexError: Raised if there's an issue with the index while accessing elements in the 'data' tuple.
    - Any exceptions that may occur during database interaction.

    Description:
    This method updates a reservation record in the 'reservation' table of the connected database. It first checks if
    the provided reservation ID exists in the table. If the ID is not found, an error message is printed. Otherwise,
    the function attempts to update the corresponding columns (name, amt_guests, date, table_nr) for the specified
    reservation ID. If an exception, specifically IndexError, occurs during the SQL execution, it is caught, printed,
    and the function returns None. The changes are committed to the database.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    updated_reservation_data = (1, 'New Name', 5, '2024-02-03', 4)
    db_connection.update_reservation(updated_reservation_data)
    ```
    """
        with self as db:
            cursor = db.cursor()
            if self.get_reservation(data[0]) == []:
                print("Error: Id not found.")
            else:
                try:
                    cursor.execute("UPDATE reservation SET name=?, amt_guests=?, date=?, table_nr=? WHERE id=?",
                                   (data[1], data[2], data[3], data[4], data[0]))
                except IndexError as i:
                    print(i)
                    return None
            db.commit()

    def get_reservation(self, id="*"):
        """
    Retrieves reservation data from the 'reservation' table of the connected database based on the provided reservation ID.

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
    all_reservations = db_connection.get_reservation()

    # Retrieve reservation data for a specific ID
    reservation_id_to_retrieve = 1
    specific_reservation = db_connection.get_reservation(reservation_id_to_retrieve)
    ```
    """
        with self as db:
            cursor = db.cursor()

            if not id == "*":
                cursor.execute("SELECT * FROM reservation WHERE id=?", (id,))
            else:
                cursor.execute("SELECT * FROM reservation")

            return cursor.fetchall()

    def next_table_nr(self):
        """
    Retrieves the next available table number for a new table in the 'tables' table of the connected database.

    Parameters:
    - self: The instance of the class representing the database connection.

    Returns:
    - int: The next available table number.

    Raises:
    - Any exceptions that may occur during database interaction.

    Description:
    This method determines the next available table number for a new table in the 'tables' table of the connected
    database. It queries the existing table numbers and calculates the maximum value, then increments it to find the next
    available table number. If no tables exist in the database, the function returns 1 as the starting table number.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    next_available_table_number = db_connection.next_table_nr()
    ```
    """
        with self as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM tables")
            tables = cursor.fetchall()

            if len(tables) == 0:
                new_id = 1
                return new_id

            new_id = max([int(data[0]) for data in tables]) + 1
            return new_id

    def update_table(self, table: Table):
        """
    Updates table information in the 'tables' table of the connected database based on the provided table object.

    Parameters:
    - self: The instance of the class representing the database connection.
    - table (Table): An instance of the Table class representing the table to be updated.

    Returns:
    - None: Returns None if an exception occurs during the database interaction.

    Raises:
    - IndexError: Raised if there's an issue with the index while accessing elements in the provided table object.
    - Any exceptions that may occur during database interaction.

    Description:
    This method updates table information in the 'tables' table of the connected database. It first checks if the provided
    table ID exists in the table. If the ID is not found, an error message is printed, and the function returns.
    Otherwise, the function attempts to update the corresponding columns (capacity, occupied) for the specified table
    ID. If an exception, specifically IndexError, occurs during the SQL execution, it is caught, printed, and the
    function returns None. The changes are committed to the database.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    table_to_update = Table(id=1, capacity=6, occupied={})
    db_connection.update_table(table_to_update)
    ```
    """
        with self as db:
            cursor = db.cursor()
            if self.get_tables(table.id) == []:
                print("Error: Table not found.")
                return
            try:
                cursor.execute("UPDATE tables SET capacity=?, occupied=? WHERE table_nr=?",
                               (table.capacity, json_dumps(table.occupied), table.id))
            except IndexError as i:
                print(i)
                return None
            db.commit()

    def new_table(self, data: Table):
        """
    Adds a new table to the 'tables' table of the connected database.

    Parameters:
    - self: The instance of the class representing the database connection.
    - data (Table): An instance of the Table class representing the table to be added.

    Returns:
    - None: Returns None if an exception occurs during the database interaction.

    Raises:
    - sqlite3.ProgrammingError: Raised if there's an issue with the SQL execution.
    - Any exceptions that may occur during database interaction.

    Description:
    This method adds a new table to the 'tables' table in the connected database. The provided data object represents
    the table to be added, including attributes such as table number, capacity, and occupancy status. The function
    checks if the provided capacity is a positive value before attempting to insert the data. If a non-digit value is
    entered for the capacity, an error message is printed. If an exception, specifically sqlite3.ProgrammingError,
    occurs during the SQL execution, it is caught, printed, and the function returns None. The changes are committed to
    the database.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    new_table_data = Table(id=1, capacity=4, occupied=False)
    db_connection.new_table(new_table_data)
    ```
    """
        with self as db:
            cursor = db.cursor()
            if data.capacity > 0:
                try:
                    cursor.execute(
                        "INSERT INTO tables (table_nr, capacity, occupied) VALUES (?, ?, ?)", (data.id, data.capacity, data.occupied))
                except sqlite3.ProgrammingError as p:
                    print(p)
                    return None
            else:
                print("Non digit value was entered.")
            db.commit()

    def remove_table(self, table_nr):
        """
    Removes a table record from the 'tables' table of the connected database based on the provided table number.

    Parameters:
    - self: The instance of the class representing the database connection.
    - table_nr (int): The table number to identify the record to be deleted.

    Returns:
    - None: Returns None if an exception occurs during the database interaction.

    Raises:
    - sqlite3.InterfaceError: Raised if there's an issue with the SQLite interface.
    - Any exceptions that may occur during database interaction.

    Description:
    This method removes a table record from the 'tables' table in the connected database. The provided table number is
    used to identify the specific record to be deleted. If the table number is not found, an error message is printed.
    If an exception, specifically sqlite3.InterfaceError, occurs during the SQL execution, it is caught, printed, and
    the function returns None. The changes are committed to the database.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    table_number_to_remove = 1
    db_connection.remove_table(table_number_to_remove)
    ```
    """
        old_length = len(self.get_tables())
        with self as db:
            cursor = db.cursor()
            try:
                cursor.execute(
                    "DELETE FROM tables WHERE table_nr=?", (table_nr,))
            except sqlite3.InterfaceError as i:
                print(i)
                return None
            if old_length == len(self.get_tables()):
                print("Error: Id not found.")

            db.commit()

    def set_occupied(self, reservation: Reservation):
        """
    Updates the 'occupied' status of a table in the 'tables' table of the connected database.

    Parameters:
    - self: The instance of the class representing the database connection.
    - reservation (Reservation): The reservation object containing the information of the reservation.

    Returns:
    - None: Returns None if an exception occurs during the database interaction.

    Raises:
    - Any exceptions that may occur during database interaction.

    Description:
    This method updates the 'occupied' status of a table in the 'tables' table of the connected database based on the
    provided reservation information. It first checks if the provided table number exists in the table. If the table is
    not found, an error message is printed. The 'occupied' status of the corresponding table and time slot is toggled
    between True and False. The function then updates the 'occupied' column for the specified table number in the
    database. If an exception occurs during the database interaction, it is caught and handled accordingly. The changes
    are committed to the database.

    Example:
    ```
    db_connection = YourDatabaseConnection()

    # Set the 'occupied' status of a table based on a reservation
    reservation = YourReservationObject()
    db_connection.set_occupied(reservation)
    ```
    """
        with self as db:
            cursor = db.cursor()
            table = self.get_tables(reservation.table_id)

            # Check if table exists
            if len(table) == 0:
                print("Error: table not found.")
                return

            day, time = reservation.user_date.split("_")
            table = Table.from_db(self, table[0])

            if table.occupied[day][time] == False:
                table.occupied[day][time] = True
            else:
                table.occupied[day][time] = False

            self.update_table(table)
            db.commit()

    def get_tables_by_capacity(self, capacity):
        """
    Retrieves unoccupied tables from the 'tables' table of the connected database based on the provided capacity.

    Parameters:
    - self: The instance of the class representing the database connection.
    - capacity (int): The capacity of the tables to filter the results.

    Returns:
    - list of tuples: A list containing tuples representing unoccupied tables with the specified capacity.
      Each tuple corresponds to a row in the 'tables' table.

    Raises:
    - Any exceptions that may occur during database interaction.

    Description:
    This method retrieves unoccupied tables from the 'tables' table in the connected database based on the provided
    capacity. The function only returns tables with the specified capacity that are not marked as occupied. The result
    is a list of tuples, where each tuple contains the values of a row in the 'tables' table.

    Example:
    ```
    db_connection = YourDatabaseConnection()

    # Retrieve unoccupied tables with a specific capacity
    tables_with_capacity_4 = db_connection.get_tables_by_capacity(4)

    # Retrieve unoccupied tables with a different capacity
    tables_with_capacity_6 = db_connection.get_tables_by_capacity(6)
    ```
    """
        with self as db:
            cursor = db.cursor()

            cursor.execute(
                "SELECT * FROM tables WHERE capacity=?", (capacity,))

            return cursor.fetchall()

    def get_tables(self, table_nr="*"):
        """
    Retrieves table information from the 'tables' table of the connected database based on the provided table number.

    Parameters:
    - self: The instance of the class representing the database connection.
    - table_nr (int or str, optional): The table number to identify the record to be retrieved.
      Defaults to "*" (wildcard), meaning all table records will be retrieved.

    Returns:
    - list of tuples: A list containing tuples representing table information matching the provided table number.
      Each tuple corresponds to a row in the 'tables' table.

    Raises:
    - Any exceptions that may occur during database interaction.

    Description:
    This method retrieves table information from the 'tables' table in the connected database. If a specific
    table number is provided, only the record with that table number is retrieved. If the table number is set to "*",
    all table records are retrieved. The function returns a list of tuples, where each tuple contains the values of a
    row in the 'tables' table.

    Example:
    ```
    db_connection = YourDatabaseConnection()

    # Retrieve all table information
    all_tables = db_connection.get_tables()

    # Retrieve table information for a specific table number
    table_number_to_retrieve = 1
    specific_table = db_connection.get_tables(table_number_to_retrieve)
    ```
    """
        with self as db:
            cursor = db.cursor()

            if not table_nr == "*":
                cursor.execute(
                    "SELECT * FROM tables WHERE table_nr=?", (table_nr,))
            else:
                cursor.execute("SELECT * FROM tables")

            return cursor.fetchall()
