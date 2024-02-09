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
        
    def next_reservation_id(self):
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
    
    def insert_reservation(self, data):
        """
    Inserts reservation data into the 'reservation' table of the connected database.

    Parameters:
    - self: The instance of the class representing the database connection.
    - data (tuple): A tuple containing reservation data in the order (id, name, amt_guests, date, table_nr).

    Returns:
    - None: Returns None if an exception occurs during the database interaction.

    Raises:
    - sqlite3.ProgrammingError: Raised if there's an issue with the SQL execution.

    Description:
    This method attempts to insert reservation data into the 'reservation' table of the connected database. The provided
    data tuple is used to populate the corresponding columns (id, name, amt_guests, date, table_nr). If an exception,
    specifically sqlite3.ProgrammingError, occurs during the SQL execution, it is caught, printed, and the function
    returns None. Otherwise, the changes are committed to the database.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    reservation_data = (1, 'John Doe', 4, '2024-02-02', 3)
    db_connection.insert_reservation(reservation_data)
    ```
    """
        with self as db:
            cursor = db.cursor()
            if data[0] > 0 and data[2] > 0 and data[4] > 0:
                try:
                    cursor.execute("INSERT INTO reservation (id, name, amt_guests, date, table_nr) \
                                    VALUES (?, ?, ?, ?, ?)", data)
                except sqlite3.ProgrammingError as p:
                    print(p)
                    return None
            else:
                print("None digit value was entered.")
            db.commit()
            
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
            
            if not id == "*": cursor.execute("SELECT * FROM reservation WHERE id=?", (id,))
            else: cursor.execute("SELECT * FROM reservation")
            
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
    
    def new_table(self, data):
        """
    Adds a new table to the 'tables' table of the connected database.

    Parameters:
    - self: The instance of the class representing the database connection.
    - data (tuple): A tuple containing table information in the order (table_nr, capacity, occupied).

    Returns:
    - None: Returns None if an exception occurs during the database interaction.

    Raises:
    - sqlite3.ProgrammingError: Raised if there's an issue with the SQL execution.
    - Any exceptions that may occur during database interaction.

    Description:
    This method adds a new table to the 'tables' table in the connected database. The provided data tuple is used to
    populate the corresponding columns (table_nr, capacity, occupied). The function checks if the table number and
    capacity are positive values before attempting to insert the data. If a non-digit value is entered for either the
    table number or capacity, an error message is printed. If an exception, specifically sqlite3.ProgrammingError,
    occurs during the SQL execution, it is caught, printed, and the function returns None. The changes are committed to
    the database.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    new_table_data = (1, 4, False)
    db_connection.new_table(new_table_data)
    ```
    """
        with self as db:
            cursor = db.cursor()
            if data[0] > 0 and data[1] > 0:
                try:
                    cursor.execute("INSERT INTO tables (table_nr, capacity, occupied) VALUES (?, ?, ?)", data)
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
                cursor.execute("DELETE FROM tables WHERE table_nr=?", (table_nr,))
            except sqlite3.InterfaceError as i:
                print(i)
                return None
            if old_length == len(self.get_tables()):
                print("Error: Id not found.")
                
            db.commit()
    
    def set_occupied(self, table_nr, bool):
        """
    Updates the 'occupied' status of a table in the 'tables' table of the connected database.

    Parameters:
    - self: The instance of the class representing the database connection.
    - table_nr (int): The table number to identify the record to be updated.
    - bool (bool or int): The new 'occupied' status to be set for the table.
      Should be either True/False, or 1/0.

    Returns:
    - None: Returns None if an exception occurs during the database interaction.

    Raises:
    - IndexError: Raised if there's an issue with the index while accessing elements in the 'data' tuple.
    - Any exceptions that may occur during database interaction.

    Description:
    This method updates the 'occupied' status of a table in the 'tables' table of the connected database. It first
    checks if the provided table number exists in the table. If the table is not found, an error message is printed.
    If the 'occupied' value provided is not a valid boolean or integer, another error message is printed. Otherwise,
    the function attempts to update the 'occupied' column for the specified table number. If an exception, specifically
    IndexError, occurs during the SQL execution, it is caught, printed, and the function returns None. The changes are
    committed to the database.

    Example:
    ```
    db_connection = YourDatabaseConnection()
    
    # Set the 'occupied' status of table number 3 to True
    db_connection.set_occupied(3, True)

    # Set the 'occupied' status of table number 5 to False
    db_connection.set_occupied(5, False)
    ```
    """
        with self as db:
            cursor = db.cursor()
            if self.get_tables(table_nr) == []:
                print("Error: table not found.")
            elif bool not in [1, 0, True, False]:
                print("Entered occupied value is invalid.")
            else:
                try:
                    cursor.execute("UPDATE tables SET occupied=? WHERE table_nr=?", (bool, table_nr))
                except IndexError as i:
                    print(i)
                    return None
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
            
            cursor.execute("SELECT * FROM tables WHERE capacity=? AND occupied=False", (capacity,))
            
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
            
            if not table_nr == "*": cursor.execute("SELECT * FROM tables WHERE table_nr=?", (table_nr,))
            else: cursor.execute("SELECT * FROM tables")
            
            return cursor.fetchall()
    