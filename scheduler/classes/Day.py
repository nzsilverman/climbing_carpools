import enum

class DayNames(enum.Enum):
    MONDAY = 0,
    TUESDAY = 1,
    WEDNESDAY = 2,
    THURSDAY = 3,
    FRIDAY = 4,
    SATURDAY = 5,
    SUNDAY = 6


class Day:

    def __init__(self, day, times, locations):
        self.day = day
        self.times = times
        self.locations = locations
