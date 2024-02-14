from json import dumps as json_dumps


def gen_timetable() -> dict:
    weekdays = {"Monday": None, "Tuesday": None, "Wednesday": None,
                "Thursday": None, "Friday": None, "Saturday": None, "Sunday": None}
    time_slots = {}
    for i in range(17, 23):
        time_slots[i] = False

    for value in weekdays:
        weekdays[value] = time_slots

    return weekdays


def gen_timetable_string() -> str:
    return json_dumps(gen_timetable())
