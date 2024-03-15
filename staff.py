from os import system, name
from database import Database
from reservations import Reservation
import datetime
from json import loads as json_loads
from table import Table


database = Database("./db.db")


def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")


def remove_reservation():
    """
    Function to remove a reservation from the database.

    This function displays a list of reservations and prompts the user to select one by entering its ID.
    After selecting a reservation, it presents the details of the reservation and asks for confirmation
    to remove it. If confirmed, it removes the reservation from the database.

    Note: This function relies on a global variable `database` which should be an instance of the class
    representing the database connection.

    Parameters:
    - None

    Returns:
    - None

    Raises:
    - None

    Description:
    This function displays a list of reservations from the database and prompts the user to select one
    by entering its ID. It then presents the details of the selected reservation and asks for confirmation
    to remove it. If confirmed, it removes the reservation from the database using the `remove_reservation`
    method of the `database` instance.

    Example:
    ```
    remove_reservation()
    ```
    """
    clear()
    print("\nRemove reservation\nSelect id\n")
    for i in database.get_reservation():
        print(f"{i[0]}. {i[1]}")
    choice = input("\n")
    try:
        if choice != "":
            for i in database.get_reservation():
                if int(choice) == i[0]:
                    clear()
                    print(f"""
Reservation info

Id: {i[0]}
Name: {i[1]}
Amount of guessts: {i[2]}
Date: {i[3]}
Table number: {i[4]}
                        """)
                    confirmation = input(
                        "Are you sure you want to remove this reservation, y or n?\n")
                    if confirmation == "y" or confirmation == "Y":
                        db_data = database.get_reservation(choice)
                        reservation = Reservation.from_db(database, db_data)
                        database.set_occupied(reservation)
                        database.remove_reservation(choice)
                    elif confirmation == "n" or confirmation == "N":
                        break
                    else:
                        print("Non accepted value entered, interpreted as n.")
                        input()

    except ValueError:
        print("\nEntered id was of invalid value.")
        input("Press enter to try again.")


def select_date(weekdays_dict) -> str:
    """
    Function to select a date for a reservation.

    This function displays a list of weekdays and prompts the user to select one by entering its index.
    It then returns the selected date as a string.

    Parameters:
    - weekdays_dict (dict): A dictionary mapping weekday indices to their corresponding dates.

    Returns:
    - str: The selected date.

    Raises:
    - None

    Description:
    This function displays a list of weekdays along with their indices and prompts the user to select one
    by entering its index. It validates the input and returns the selected date as a string. If the input
    is invalid, it prompts the user to input a valid selection.

    Example:
    ```
    weekdays_dict = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
    selected_date = select_date(weekdays_dict)
    ```
    """
    clear()
    for i, date in enumerate(weekdays_dict.keys()):
        print(f"{i+1}. {date}")

    date = input("Please input the date of your reservation:")
    # try:
    date = int(date) - 1
    if date < 0 or date > 6:
        print("Please input a valid selection.")
        select_date(weekdays_dict)
    else:
        date = list(weekdays_dict.values())[date]
    # except:
    #     print("Please input a valid number.")
    #     select_date(weekdays_dict)

    return date


def gen_dates() -> dict:
    """
    Function to generate a dictionary of weekday names and corresponding dates for the next 7 days.

    This function generates a dictionary where the keys are weekday names ("Today", "Tomorrow", and the next 5 weekdays)
    and the values are the corresponding dates in the format YYYY-MM-DD.

    Parameters:
    - None

    Returns:
    - dict: A dictionary mapping weekday names to their corresponding dates.

    Raises:
    - None

    Description:
    This function generates a dictionary containing the current weekday followed by the next 6 weekdays along with their
    corresponding dates. It calculates the dates for each weekday using the current date as a reference and the
    datetime module. The dictionary is returned with weekday names as keys and dates in the format YYYY-MM-DD as values.

    Example:
    ```
    weekdays_dict = gen_dates()
    print(weekdays_dict)
    # Output:
    # {
    #   'Today': '2024-02-01',
    #   'Tomorrow': '2024-02-02',
    #   'Wednesday': '2024-02-02',
    #   'Thursday': '2024-02-03',
    #   'Friday': '2024-02-04',
    #   'Saturday': '2024-02-05',
    #   'Sunday': '2024-02-06'
    # }
    ```
    """
    now = datetime.datetime.now()

    # Create a dictionary to hold the current weekday followed by the next 6 weekdays as keys
    weekdays_dict = {}

    # Loop to fill in the dictionary
    for i in range(7):
        # Calculate the date for the current iteration
        date = now + datetime.timedelta(days=i)
        # Get the weekday name and format the date
        date_str = date.strftime('%Y-%m-%d')
        if i == 0:
            weekdays_dict["Today"] = date.strftime('%A')
        elif i == 1:
            weekdays_dict["Tomorrow"] = date.strftime('%A')
        else:
            weekdays_dict[date.strftime('%A')] = date.strftime('%A')

    return weekdays_dict


def select_time(times: dict) -> str:
    """
    Function to select a time for a reservation.

    This function displays a list of available times for reservation based on the provided dictionary `times`,
    where keys are time slots and values indicate whether the slot is occupied or not. The user is prompted
    to select a time by entering its index. If the selected time is occupied or the input is invalid, the
    user is prompted to input a valid selection.

    Parameters:
    - times (dict): A dictionary mapping time slots to their occupancy status.

    Returns:
    - str: The selected time slot.

    Raises:
    - None

    Description:
    This function displays a list of available time slots along with their occupancy status and prompts the user
    to select one by entering its index. It validates the input and returns the selected time slot as a string.
    If the input is invalid or the selected time slot is occupied, it prompts the user to input a valid selection.

    Example:
    ```
    times = {"09:00": False, "10:00": True, "11:00": False}
    selected_time = select_time(times)
    ```
    """
    for i, time in enumerate(times.keys()):
        if times[time] == False:
            print(f"{i+1}. {time}.00")
        else:
            print(f"{i+1}. {time}.00 (Occupied)")

    time = input("Please select the new time for the reservation: ")

    try:
        time = int(time) - 1
        if list(times.values())[time] == True:
            print("Please select a non-occupied time.")
            select_time(times)

        if time < 0 or time > len(times) - 1:
            print("Please input a valid selection.")
            select_time(times)

        time = list(times.keys())[time]

    except:
        print("Please input a valid number.")
        select_time(times)

    return time


def select_new_reservation_date(amount, table_number):
    """
    Function to select a date and time for a new reservation.

    This function prompts the user to select a date and time for a new reservation based on the given table's
    available capacities and timeslots. It first prompts the user to select a date using the `select_date` function
    with available dates generated by `gen_dates`. Then, it retrieves the available timeslots for the given table
    and date from the database. Finally, it prompts the user to select a time from the available timeslots using
    the `select_time` function, and returns the concatenated string of the selected date and time.

    Parameters:
    - amount (int): The capacity required for the reservation.
    - table_number (int): The number of the table for which the reservation is being made.

    Returns:
    - str: The concatenated string representing the selected date and time in the format "YYYY-MM-DD_HH:00".

    Raises:
    - None

    Description:
    This function guides the user to select a date and time for a new reservation based on the given capacity
    requirement and table number. It ensures that the selected date and time are valid and available for reservation.

    Example:
    ```
    selected_date_time = select_new_reservation_date(4, 1)
    print(selected_date_time)
    # Output: "2024-02-05_15:00"
    ```
    """
    date = select_date(gen_dates())

    available_tables = database.get_tables_by_capacity(amount)
    for i in available_tables:
        if i[0] == table_number:
            available_times = json_loads(i[2])[date]

    time = select_time(available_times)

    return f"{date}_{time}"


def select_new_reservation_table(amount, date, old_table_id):
    """
    Function to select a new table for a reservation.

    This function prompts the user to select a new table for a reservation, based on the required capacity,
    the provided date, and the current table ID. It first displays available tables with the required capacity
    retrieved from the database. The user is prompted to select a new table by entering its index. The function
    then validates the selection and ensures that the selected table is available at the booked time. If the
    selection is invalid or the table is not available, the user is prompted to input a valid selection.

    Parameters:
    - amount (int): The capacity required for the reservation.
    - date (str): The date and time of the reservation in the format "YYYY-MM-DD_HH:00".
    - old_table_id (int): The ID of the current table for the reservation.

    Returns:
    - int: The ID of the selected new table for the reservation.

    Raises:
    - None

    Description:
    This function guides the user to select a new table for a reservation based on the provided capacity, date,
    and the current table ID. It ensures that the selected table is available at the booked time and validates
    the user input to ensure a valid selection.

    Example:
    ```
    new_table_id = select_new_reservation_table(4, "2024-02-05_15:00", 1)
    print(new_table_id)
    # Output: 3
    ```
    """
    avalible_tables = database.get_tables_by_capacity(amount)
    print(f"Avalible tables with capasity {amount}")
    for i in range(len(avalible_tables)):
        if avalible_tables[i][0] == old_table_id:
            print(f"{i+1}. Id: {avalible_tables[i][0]} (Current)")
        else:
            print(f"{i+1}. Id: {avalible_tables[i][0]}")

    new_table = input("Please select the new table for the reservation: ")

    try:
        new_table = int(new_table) - 1
        table = Table.from_db(database, avalible_tables[new_table])
        date_list = date.split("_")
        if table.occupied[date_list[0]][date_list[1]] == True:
            print(
                "The selected table is not avalible at the booked time, please select another table.")
            select_new_reservation_table(amount, date, old_table_id)

        if new_table < 0 or new_table > len(avalible_tables) - 1:
            print("Please input a valid selection.")
            select_new_reservation_table(amount, date, old_table_id)

    except:
        print("Please input a valid number.")
        select_new_reservation_table(amount, date, old_table_id)

    return table.id


def update_reservation():
    """
    Function to update a reservation in the database.

    This function guides the user through the process of updating a reservation. It displays a list of reservations 
    with their IDs and prompts the user to select a reservation by entering its ID. Once a reservation is selected, 
    the function presents the details of the chosen reservation and asks the user to choose the information to update.
    The user can update the name, amount of guests, date, or table number of the reservation. The function then updates
    the reservation in the database according to the user's input.

    Parameters:
    - None

    Returns:
    - None

    Raises:
    - None

    Description:
    This function provides an interactive interface for updating reservation information. It handles user input 
    gracefully and ensures that the entered reservation ID is valid.

    Example:
    ```
    update_reservation()
    ```
    """
    clear()
    print("\nUpdate reservation\nSelect id\n")
    for i in database.get_reservation():
        print(f"{i[0]}. {i[1]}")
    choice = input("\n")
    try:
        if choice != "":
            for i in database.get_reservation():
                if int(choice) == i[0]:
                    clear()
                    print(f"""
Reservation info

Id: {i[0]}
1. Name: {i[1]}
2. Amount of guessts: {i[2]}
3. Date: {f"{i[3].split('_')[0]}, {i[3].split('_')[1]}:00"}
4. Table number: {i[4]}
                        """)
                    info_choice = input(
                        "Enter the info you wish to update.\nId's cannot be updated.\n").lower()
                    match info_choice:
                        case "1":
                            new_name = input(
                                "Enter the new name: ").capitalize()
                            database.update_reservation(
                                (i[0], new_name, i[2], i[3], i[4]))
                        case "2":
                            while True:
                                try:
                                    new_amount_of_guests = int(input("Enter the new amount of guests:"))
                                    if new_amount_of_guests > i[2]:
                                        print("New number of guests cannot exceed current value. Try again.")
                                        input("Press ENTER to continue.")
                                        continue
                                    
                                    if new_amount_of_guests <= 0:
                                        print("New number of guests be zero or less than zero. Try again.")
                                        input("Press ENTER to continue.")
                                        continue
                                    break
                                except KeyboardInterrupt:
                                    exit()
                                except:
                                    print("Invalid input. Try again.")
                            database.update_reservation(
                                (i[0], i[1], new_amount_of_guests, i[3], i[4])) 
                        case "3":
                            new_date = select_new_reservation_date(i[2], i[4])
                            database.update_reservation(
                                (i[0], i[1], i[2], new_date, i[4]))
                            updated_reservation = Reservation(
                                db=database, user_amount=i[2], user_name=i[1], user_date=new_date, table_id=i[4])
                            updated_reservation.id = i[0]
                            database.set_occupied(updated_reservation)
                            old_reservation = Reservation(
                                db=database, user_amount=i[2], user_name=i[1], user_date=i[3], table_id=i[4])
                            old_reservation.id = i[0]
                            database.set_occupied(old_reservation)
                        case "4":
                            new_table_nr = select_new_reservation_table(
                                i[2], i[3], i[4])
                            database.update_reservation(
                                (i[0], i[1], i[2], i[3], new_table_nr))
                            updated_reservation = Reservation(
                                db=database, user_amount=i[2], user_name=i[1], user_date=i[3], table_id=new_table_nr)
                            updated_reservation.id = i[0]
                            database.set_occupied(updated_reservation)
                            old_reservation = Reservation(
                                db=database, user_amount=i[2], user_name=i[1], user_date=i[3], table_id=i[4])
                            old_reservation.id = i[0]
                            database.set_occupied(old_reservation)
                        case other:
                            pass

    except ValueError:
        print("\nEntered id was of invalid value.")
        input("Press enter to try again.")


def display_reservations():
    """
    Function to display reservations and their details.

    This function continuously displays a list of reservations along with their details, such as ID, name, 
    number of guests, date, and table number. The user is prompted to select a reservation by entering its ID.
    Upon selection, the details of the chosen reservation are displayed. The loop continues until the user 
    chooses to exit by entering an empty input.

    Parameters:
    - None

    Returns:
    - None

    Raises:
    - None

    Description:
    This function continuously displays reservation information and handles user input to view details 
    of specific reservations. It ensures that the entered reservation ID is valid and handles any 
    invalid input gracefully.

    Example:
    ```
    display_reservations()
    ```
    """
    while True:
        clear()
        print("\nReservations\nSelect id\n")
        for i in database.get_reservation():
            print(f"{i[0]}. {i[1]}")
        choice = input("\n")
        try:
            if choice != "":
                for i in database.get_reservation():
                    if int(choice) == i[0]:
                        clear()
                        print(f"""
Reservation info

Id: {i[0]}
Name: {i[1]}
Amount of guessts: {i[2]}
Date: {f"{i[3].split('_')[0]}, {i[3].split('_')[1]}:00"}
Table number: {i[4]}
                            """)
                        input()
                        break
            else:
                break
        except ValueError:
            print("\nEntered id was of invalid value.")
            input("Press enter to try again.")


def menu():
    """
    Function to display and navigate the staff terminal menu.

    This function continuously displays a menu for staff terminal options and prompts the user to select 
    an action by entering a corresponding number. The user can choose to remove a reservation, update a 
    reservation, display reservations, or exit the terminal. The function then directs the user to the 
    respective action based on their input.

    Parameters:
    - None

    Returns:
    - None

    Raises:
    - None

    Description:
    This function serves as the main menu for the staff terminal, allowing staff members to perform various 
    actions related to reservations. It ensures that the user input is valid and handles any invalid choices 
    gracefully.

    Example:
    ```
    menu()
    ```
    """
    while True:
        clear()
        print("""
Staff terminal

1. Remove reservation
2. Update reservation
3. Display reservations
4. Exit
            """)
        match input("Enter your choice: "):
            case "1": remove_reservation()
            case "2": update_reservation()
            case "3": display_reservations()
            case "4": break
            case other:
                print("\nYou must only select either 1, 2, 3, or 4.")
                input("Press enter to try again.")


if __name__ == "__main__":
    menu()
