from os import system, name


def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")

def remove_reservation():
    pass

def update_reservation():
    pass

def display_reservations():
    pass

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
                print("\nYou must only select either 1, 2, 3 or 4")
                input("Press enter to try again.")

if __name__=="__main__":
    menu()