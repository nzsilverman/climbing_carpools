"""
Test utilities
"""
from scheduler.classes.Member import Member
from scheduler.classes.Driver import Driver
from scheduler.classes.Rider import Rider
import scheduler.classes.Day as Day


def convert_days(days: list) -> list:
    dayInfos = list()

    for d in days:
        day = Day.DayInfo(
            day=(Day.from_str(d["day"]) if d["day"] else None),
            times=(d["times"] if d["times"] else None),
            locations=(d["locations"] if d["locations"] else None))

        dayInfos.append(day)

    return dayInfos


def members_to_class(members: list) -> list:
    member_objects = list()
    for m in members:
        print(members)
        if m["is_driver"]:
            driver = Driver(
                name=(m["name"] if m["name"] else None),
                email=(m["email"] if m["email"] else None),
                phone=(m["phone"] if m["phone"] else None),
                days=(convert_days(m["days"]) if m["days"] else None),
                is_dues_paying=(m["is_dues_paying"]
                                if m["is_dues_paying"] else None),
                car_type=(m["car_type"] if m["car_type"] else None),
                seats=(m["seats"] if m["seats"] else None))
        else:
            rider = Rider(
                name=(m["name"] if m["name"] else None),
                email=(m["email"] if m["email"] else None),
                phone=(m["phone"] if m["phone"] else None),
                days=(convert_days(m["days"]) if m["days"] else None),
                is_dues_paying=(m["is_dues_paying"]
                                if m["is_dues_paying"] else None),
            )


def sort_by_name(members):
    """
    Sort the dictionary of members by name
    """
    return sorted(members, key=lambda m: m.name)
