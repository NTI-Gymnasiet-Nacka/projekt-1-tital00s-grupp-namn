from reservations import Reservation
import datetime
import database
from json import loads as json_loads


def get_party_amount():
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


def select_time(times) -> str:
    for i, time in enumerate(times.keys()):
        if times[time] == False:
            print(f"{i+1}. {time}.00")
        else:
            print(f"{i+1}. {time}.00 (Occupied)")

    time = input("Please select the time of your reservation:")
    # TODO
    if TODO == True:
        print("Please select a non-occupied time.")
        select_time(times)

    try:
        time = int(time) - 1
        if time < 0 or time > len(times) - 1:
            print("Please input a valid selection.")
            select_date(times)
        else:
            time = list(times.keys())[time]
    except:
        print("Please input a valid number.")
        select_date(times)

    return time


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


def main():
    name = input("Please input your name:")
    amount = get_party_amount()
    print()
    date = select_date(gen_dates())

    db = database.Database("./test.db")
    available_tables = db.get_tables_by_capacity(amount)
    available_times = json_loads(available_tables[0][2])[date]

    time = select_time(available_times)
    reservation = Reservation(
        amount, name, f"{date}_{time}", available_tables[0])
    print(
        f"Thank you {name}, your reservation for {amount} people on {date}, {time}:00 has been made.")

    print()
    # print()


if __name__ == "__main__":
    main()
