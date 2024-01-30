from pandas import read_html
from datetime import datetime
from re import search
from ics import Calendar, Event
from typing import List


URL = "https://mzb.biu.ac.il/node/5733"
TABLE_HEADER = 'לוח זמנים לשנת הלימודים תשפ"ד - ניצבים כ"א'
OUTPUT_FILE = 'Schedule.ics'


def iterate_schedule_events(dates, times, class_names) -> List[Event]:
    for event in zip(dates, times, class_names):
        date = search(r'\d{2}\.\d{2}\.\d{2}', str(event[0]))
        time = search(r'\d{2}:\d{2}-\d{2}:\d{2}', str(event[1]))
        if not date or not time or any(map(lambda a: type(a) == float, event)):
            continue
        else:
            date = date.group(0)
            time = time.group(0)
            events.append(Event(
                name=event[2],
                begin=datetime.strptime(
                    f'{date}-{time.split("-")[0]}',
                    r'%d.%m.%y-%H:%M',
                ),
                end=datetime.strptime(
                    f'{date}-{time.split("-")[1]}',
                    r'%d.%m.%y-%H:%M'
                )
            ))
    return events


if __name__ == '__main__':
    tables = read_html(URL)
    events = list()
    for table in tables:
        if table[0][0] == TABLE_HEADER:
            break
    first_day = iterate_schedule_events(table[0], table[1], table[2])
    second_day = iterate_schedule_events(table[3], table[4], table[5])
    cal = Calendar(events=set(first_day + second_day))
    with open(OUTPUT_FILE, "wb") as f:
        f.write(cal.serialize().encode('utf-8'))



