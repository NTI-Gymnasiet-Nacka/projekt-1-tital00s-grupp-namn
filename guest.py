from reservations import Reservation
import datetime


def main():
    name = input("Please input your name:")

    # Amount input
    while True:
        amount = input("Please input the amount of people you are bringing:")
        try:
            amount = int(amount)
            if amount > 8:
                Reservation.imposible()
                continue
            else:
                break
        except:
            print("Please input a valid number.")

    # Date input
    print()
    # Get the current date and time
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
            weekdays_dict["Today"] = date_str
        elif i == 1:
            weekdays_dict["Tomorrow"] = date_str
        else:
            weekdays_dict[date.strftime('%A')] = date_str

    for i, date in enumerate(weekdays_dict.keys()):
        print(f"{i+1}. {date}")

    while True:
        date = input("Please input the date of your reservation:")
        try:
            date = int(date)
            if date < 1 or date > 7:
                print("Please input a valid selection.")
                continue
            else:
                date = list(weekdays_dict.values())[date-1]
                break
        except:
            print("Please input a valid number.")


if __name__ == "__main__":
    main()
