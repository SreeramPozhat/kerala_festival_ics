import os
from datetime import datetime, timedelta

class CalendarEvent:
    def __init__(self, line, year):
        parts = line.strip().split(" : ")
        if len(parts) != 2:
            raise ValueError(f"Invalid line format: {line}")
        date_part, name = parts
        month, day = map(int, date_part.strip().split("-"))
        self.name = name.strip()
        self.start_date = datetime(int(year), month, day)
        self.end_date = self.start_date + timedelta(days=1)
        self.uid = f"{self.start_date.strftime('%Y%m%d')}-{abs(hash(name))%100000}@malayalam"

    def to_ics(self, dtstamp):
        return (
            "BEGIN:VEVENT\n"
            f"DTSTART;VALUE=DATE:{self.start_date.strftime('%Y%m%d')}\n"
            f"DTEND;VALUE=DATE:{self.end_date.strftime('%Y%m%d')}\n"
            f"DTSTAMP:{dtstamp}\n"
            f"UID:{self.uid}\n"
            f"SUMMARY:{self.name}\n"
            "END:VEVENT\n"
        )

def read_events(filepath, year):
    events = []
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    event = CalendarEvent(line, year)
                    events.append(event)
                except Exception as e:
                    print(f"Skipped line: {line} ({e})")
    return events

def generate_ics_file(events, output_file):
    now = datetime.utcnow()
    dtstamp = now.strftime('%Y%m%dT%H%M%SZ')

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("BEGIN:VCALENDAR\n")
        f.write("VERSION:2.0\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\n")
        f.write("PRODID:-//Malayalam Holidays//Calendar//ML\n")
        f.write("X-WR-CALNAME:സനാതനി ആഘോഷങ്ങൾ\n")
        f.write("X-WR-TIMEZONE:Asia/Kolkata\n")
        f.write("BEGIN:VTIMEZONE\n")
        f.write("TZID:Asia/Kolkata\n")
        f.write("X-LIC-LOCATION:Asia/Kolkata\n")
        f.write("BEGIN:STANDARD\n")
        f.write("TZOFFSETFROM:+0530\n")
        f.write("TZOFFSETTO:+0530\n")
        f.write("TZNAME:IST\n")
        f.write("DTSTART:19700101T000000\n")
        f.write("END:STANDARD\n")
        f.write("END:VTIMEZONE\n")

        for event in events:
            f.write(event.to_ics(dtstamp))

        f.write("END:VCALENDAR\n")

def main():
    year = 2025
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(script_dir, "data")
    filenames = ["ചന്ദ്ര 2025.txt", "സൗര 2025.txt", "നക്ഷത്ര 2025.txt", "Julian.txt"]

    all_events = []
    for filename in filenames:
        path = os.path.join(folder, filename)
        if os.path.exists(path):
            events = read_events(path, year)
            all_events.extend(events)
        else:
            print(f"⚠️ File not found: {path}")

    output_path = os.path.join(script_dir, f"കേരളാഘോഷങ്ങൾ_{year}.ics")
    generate_ics_file(all_events, output_path)
    print(f"✅ Created: {output_path}")


if __name__ == "__main__":
    main()
