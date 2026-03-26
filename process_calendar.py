from icalendar import Calendar


def read_ics(filename):
    with open(filename, "rb") as f:
        raw_data = f.read()

    if not raw_data:
        return None

    return Calendar.from_ical(raw_data)


def process_calendar(cal):
    if cal is None:
        return None

    events_to_remove = []

    for event in cal.walk("VEVENT"):
        summary = event.get("SUMMARY")
        if not summary:
            continue

        summary_text = str(summary)

        if "Emnekode" not in summary_text:
            if "Tittel" in summary_text:  # remove public holidays
                events_to_remove.append(event)
            continue

        parts = summary_text.split(". ")
        code = parts[0].replace("Emnekode:", "").strip()
        name = parts[1].replace("Emnenavn:", "").strip()

        new_summary = f"{name} ({code})"

        event["SUMMARY"] = new_summary

    for event in events_to_remove:
        cal.subcomponents.remove(event)

    return cal


def combine_calendars(old, new):
    if old is None and new is None:
        return None

    combined = Calendar()

    source = new if new is not None else old
    if source is not None:
        for key, value in source.items():
            combined.add(key, value)

    events_from_uid = {}

    if old is not None:
        for event in old.walk("VEVENT"):
            uid = str(event.get("UID")) if event.get("UID") else None
            if uid is not None:
                events_from_uid[uid] = event

    if new is not None:
        for event in new.walk("VEVENT"):
            uid = str(event.get("UID")) if event.get("UID") else None
            if uid is not None:
                # prioritize events from new
                events_from_uid[uid] = event

    for event in events_from_uid.values():
        combined.add_component(event)

    return combined


new_cal = read_ics("original.ics")
new_cal = process_calendar(new_cal)

old_cal = read_ics("processed.ics")

combined_cal = combine_calendars(old_cal, new_cal)

if combined_cal is not None:
    with open("processed.ics", "wb") as f:
        f.write(combined_cal.to_ical())


















