from os import system, name
from database import Database
from reservations import Reservation
import datetime
from json import loads as json_loads


database = Database("./db copy.db")


def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")

def remove_reservation():
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
                    confirmation = input("Are you sure you want to remove this reservation, y or n?\n")
                    if confirmation == "y" or confirmation == "Y":
                        pass
                    elif confirmation == "n" or confirmation == "N":
                        break
                    else:
                        print("Non accepted value entered, interpreted as n.")
                        input()
                        
    except ValueError:
        print("\nEntered id was of invalid value.")
        input("Press enter to try again.")

def select_date(weekdays_dict) -> str:
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
    date = select_date(gen_dates())
    
    available_tables = database.get_tables_by_capacity(amount)
    for i in available_tables:
        if i[0] == table_number:
            available_times = json_loads(i[2])[date]
    
    time = select_time(available_times)
    
    return f"{date}_{time}"

def select_new_reservation_table(amount, date):
    avalible_tables = database.get_tables_by_capacity(amount)
    print(f"Avalible tables with capasity {amount}")
    for i in range(len(avalible_tables)):
        print(f"{i+1}. Id: {avalible_tables[i][0]}")
        
    new_table = input("Please select the new table for the reservation: ")
    
    try:
        new_table = int(new_table) - 1
        date_list = date.split("_")
        if avalible_tables[new_table][3][date_list[0]][date_list[1]] == True:
            print("The selected table is not avalible at the booked time, please select another table.")
            select_new_reservation_table(amount, date)
        
        if new_table < 0 or new_table > len(avalible_tables) - 1:
            print("Please input a valid selection.")
            select_new_reservation_table(amount, date)
        
    except:
        # Hoppar hit av någon anledning
        print("Please input a valid number.")
        select_new_reservation_table(amount, date)
    
    return new_table

def update_reservation():
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
                    info_choice = input("Enter the info you wish to update or enter 'all' to update all info.\nId's cannot be updated.\n").lower()
                    match info_choice:
                        case "1":
                            new_name = input("Enter the new name: ").capitalize()
                            database.update_reservation((i[0], new_name, i[2], i[3], i[4]))
                        case "2":
                            pass
                        case "3":
                            new_date = select_new_reservation_date(i[2], i[4])
                            database.update_reservation((i[0], i[1], i[2], new_date, i[4]))
                            updated_reservation = Reservation(db=database, user_amount=i[2], user_name=i[1], user_date=new_date, table_id=i[4])
                            updated_reservation.id = i[0]
                            database.set_occupied(updated_reservation)
                            old_reservation = Reservation(db=database, user_amount=i[2], user_name=i[1], user_date=i[3], table_id=i[4])
                            old_reservation.id = i[0]
                            database.set_occupied(old_reservation)
                        case "4":
                            new_table_nr = select_new_reservation_table(i[2], i[3])
                            database.update_reservation((i[0], i[1], i[2], i[3], new_table_nr))
                            updated_reservation = Reservation(db=database, user_amount=i[2], user_name=i[1], user_date=i[3], table_id=new_table_nr)
                            updated_reservation.id = i[0]
                            database.set_occupied(updated_reservation)
                            old_reservation = Reservation(db=database, user_amount=i[2], user_name=i[1], user_date=i[3], table_id=i[4])
                            old_reservation.id = i[0]
                            database.set_occupied(old_reservation)
                        case "all":
                            new_name = input("New name: ")
                            new_amount_of_guests = input("New amount of guests: ")
                            select_new_reservation_date()
                        case other:
                            pass
                        
    except ValueError:
        print("\nEntered id was of invalid value.")
        input("Press enter to try again.")

def display_reservations():
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

def display_avalible_tables():
    pass

def edit_table_occupancy():
    pass

def menu():
    while True:
        clear()
        print("""
Staff terminal

1. Remove reservation
2. Update reservation
3. Display reservations
4. Display avalible tables
5. Edit table occupancy
6. Exit
            """)
        match input("Enter your choice: "): 
            case "1": remove_reservation()
            case "2": update_reservation()
            case "3": display_reservations()
            case "4": display_avalible_tables()
            case "5": edit_table_occupancy()
            case "6": break
            case other:
                print("\nYou must only select either 1, 2, 3, 4, 5 or 6.")
                input("Press enter to try again.")

if __name__=="__main__":
    menu()
    