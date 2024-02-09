def remove_reservation():
    pass

def update_reservation():
    pass

def display_reservations():
    pass

while True:
    print("""
          1. remove reservation
          2. update reservation
          3. display reservations
          4. exit
          """)
    choice = input("Enter your choice: ")
    if choice == "1":
        remove_reservation()
    elif choice == "2":
        update_reservation()
    elif choice == "3":
        display_reservations()
    elif choice == "4":
        break
    else:
        print("You must only select either 1,2,3, or 4")
        print("Please try again")
        continue
      