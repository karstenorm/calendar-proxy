from icalendar import Calendar

with open("original.ics", "rb") as file:
    raw_data = file.read()

cal = Calendar.from_ical(raw_data)

for event in cal.walk("VEVENT"):
    summary = event.get("SUMMARY")
    if not summary:
        continue

    summary_text = str(summary)
    if "Emnekode" not in summary_text:
        continue

    parts = summary_text.split(". ")
    code = parts[0].replace("Emnekode:", "").strip()
    name = parts[1].replace("Emnenavn:", "").strip()

    new_summary = f"{name} ({code})"

    event["SUMMARY"] = new_summary

raw_output = cal.to_ical()

with open("processed.ics", "wb") as file:
    file.write(raw_output)

