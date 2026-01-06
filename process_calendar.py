from icalendar import Calendar

with open("original.ics", "rb") as file:
    raw_data = file.read()

cal = Calendar.from_ical(raw_data)

for event in cal.walk("VEVENT"):
    summary = event.get("SUMMARY")
    if "Emnekode" not in summary:
        continue

    summary_text = str(summary)
    new_summary = summary_text.replace(
        "Emnekode: ", ""
    ).replace(
        "Emnenavn: ", ""
    ).replace(". ", " - ")
    event["SUMMARY"] = new_summary

raw_output = cal.to_ical()

with open("processed.ics", "wb") as file:
    file.write(raw_output)
    print("file written")

