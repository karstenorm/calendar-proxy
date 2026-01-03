from icalendar import Calendar

with open("original.ics", "rb") as file:
    raw_data = file.read()

cal = Calendar.from_ical(raw_data)
print(cal)


