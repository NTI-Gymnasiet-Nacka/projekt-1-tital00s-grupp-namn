from os import system, name
from database import Database
from reservations import Reservation


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
Date: {i[3]}
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
    