from reservations import Reservation
import datetime
import database
from json import loads as json_loads


def get_party_amount():
    """
    Prompts the user to input the number of people they are bringing for a reservation.

    Returns:
    - int: The number of people for the reservation.

    Description:
    This function requests the user to input the number of people they intend to bring for a reservation. It validates
    the input to ensure it is a valid integer. If the input is not a valid integer or exceeds the maximum capacity of 8
    people, it prompts the user again until a valid number is provided. Once a valid input is received, the function
    returns the amount entered as an integer.

    Example:
    ```
    party_size = get_party_amount()
    ```
    """
    amount = input("Please input the amount of people you are bringing:")
    try:
        amount = int(amount)
        if amount > 8:
            Reservation.imposible()
            get_party_amount()
    except:
        print("Please input a valid number.")
        get_party_amount()

    return amount


def select_date(weekdays_dict) -> str:
    """
    Prompts the user to select a date for their reservation from a dictionary of weekdays.

    Parameters:
    - weekdays_dict (dict): A dictionary containing weekdays as keys and their corresponding dates as values.

    Returns:
    - str: The selected date for the reservation.

    Description:
    This function displays a list of weekdays along with their corresponding dates for the user to choose from.
    It prompts the user to input the index number of their desired date. If the input is not a valid index or is
    out of range, an error message is displayed, and the user is prompted again until a valid selection is made.
    Once a valid selection is made, the function returns the chosen date as a string.

    Example:
    ```
    weekdays = {"Monday": "2024-02-05", "Tuesday": "2024-02-06", "Wednesday": "2024-02-07", 
                "Thursday": "2024-02-08", "Friday": "2024-02-09", "Saturday": "2024-02-10", 
                "Sunday": "2024-02-11"}
    selected_date = select_date(weekdays)
    ```
    """
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


def select_time(times: dict) -> str:
    """
    Prompts the user to select a time for their reservation from a dictionary of available times.

    Parameters:
    - times (dict): A dictionary containing available times as keys and their occupancy status as values.

    Returns:
    - str: The selected time for the reservation.

    Description:
    This function displays a list of available times along with their occupancy status for the user to choose from.
    It prompts the user to input the index number of their desired time. If the input is not a valid index or is
    out of range, an error message is displayed, and the user is prompted again until a valid selection is made.
    Additionally, it checks if the selected time is already occupied. If so, the user is prompted to select another
    time until a non-occupied time is chosen. Once a valid and non-occupied selection is made, the function returns
    the chosen time as a string.

    Example:
    ```
    available_times = {"09:00": False, "10:00": True, "11:00": False, "12:00": False}
    selected_time = select_time(available_times)
    ```
    """
    for i, time in enumerate(times.keys()):
        if times[time] == False:
            print(f"{i+1}. {time}.00")
        else:
            print(f"{i+1}. {time}.00 (Occupied)")

    time = input("Please select the time of your reservation:")

    try:
        time = int(time) - 1
        if list(times.values())[time] == True:
            print("Please select a non-occupied time.")
            select_time(times)

        if time < 0 or time > len(times) - 1:
            print("Please input a valid selection.")
            select_date(times)

        time = list(times.keys())[time]

    except:
        print("Please input a valid number.")
        select_date(times)

    return time


def gen_dates() -> dict:
    """
    Generates a dictionary of weekdays for the current week, including today and the next six days.

    Returns:
    - dict: A dictionary where each key represents a day of the week and its corresponding value is the full
            name of the weekday (e.g., "Monday", "Tuesday").

    Description:
    This function generates a dictionary containing the weekdays for the current week, starting from today and
    including the next six days. It uses the datetime module to calculate the dates and weekdays. The keys in the
    dictionary represent the days of the week (e.g., "Today", "Tomorrow", and the names of the weekdays), while
    the values are the full names of the corresponding weekdays. The function then returns the generated dictionary.

    Example:
    ```
    weekdays = gen_dates()
    print(weekdays)
    # Output: {'Today': 'Monday', 'Tomorrow': 'Tuesday', 'Wednesday': 'Wednesday', ...}
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


def main():
    """
    Executes the main functionality of the reservation system, allowing users to make a new reservation.

    Description:
    This function represents the main functionality of the reservation system. It prompts the user to input their name
    and the number of people in their party. Then, it retrieves the available dates for reservation using the
    'gen_dates()' function and prompts the user to select a date. Next, it creates a new database instance, retrieves
    available tables based on the party size using 'get_tables_by_capacity()' method, and gets the available times for
    the selected date. The user is then prompted to select a time slot using 'select_time()' function. Afterward, a new
    Reservation object is created with the provided details, and it is pushed to the database using 'push_to_db()'
    method. Finally, a confirmation message is printed to acknowledge the successful reservation.

    Example:
    ```
    main()
    # Output:
    # Please input your name: John
    # Please input the amount of people you are bringing: 4
    #
    # 1. Today
    # 2. Tomorrow
    # 3. Wednesday
    # ...
    # Please input the date of your reservation: 2
    #
    # 1. 12.00
    # 2. 14.00 (Occupied)
    # 3. 16.00
    # ...
    # Please select the time of your reservation: 1
    #
    # Thank you John, your reservation for 4 people on Tomorrow, 12:00 has been made.
    ```
    """
    name = input("Please input your name:")
    amount = get_party_amount()

    print()
    date = select_date(gen_dates())

    db = database.Database()
    available_tables = db.get_tables_by_capacity(amount)
    available_times = json_loads(available_tables[0][2])[date]

    print()
    time = select_time(available_times)

    reservation = Reservation(db,
                              amount, name, f"{date}_{time}", available_tables[0][0])
    reservation.push_to_db()

    print(
        f"Thank you {name}, your reservation for {amount} people on {date}, {time}:00 has been made.")


if __name__ == "__main__":
    main()
