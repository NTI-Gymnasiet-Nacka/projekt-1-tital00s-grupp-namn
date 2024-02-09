from json import dumps as json_dumps
from json import loads as json_loads


def gen_timetable() -> str:
    weekdays = {"Monday": None, "Tuesday": None, "Wednesday": None,
                "Thursday": None, "Friday": None, "Saturday": None, "Sunday": None}
    time_slots = {}
    for i in range(17, 23):
        time_slots[i] = False

    for value in weekdays:
        weekdays[value] = time_slots

    return json_dumps(weekdays, indent=2)


timetable = gen_timetable()
print(timetable)
print(type(json_loads(timetable)["Monday"]["17"]))
