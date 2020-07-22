import enum


class DayName(enum.Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def from_str(day_name_str: str) -> DayName:
    """Returns corresponding DayName enum to a day name provided by string
    """

    #TODO: this can be better, maybe use a dict to pair these up instead?
    if day_name_str == "MONDAY":
        return DayName.MONDAY
    if day_name_str == "TUESDAY":
        return DayName.TUESDAY
    if day_name_str == "WEDNESDAY":
        return DayName.WEDNESDAY
    if day_name_str == "THURSDAY":
        return DayName.THURSDAY
    if day_name_str == "FRIDAY":
        return DayName.FRIDAY
    if day_name_str == "SATURDAY":
        return DayName.SATURDAY
    if day_name_str == "SUNDAY":
        return DayName.SUNDAY


def to_str(day_name: DayName) -> str:
    """Returns corresponding DayName enum to a day name provided by string
    """

    #TODO: this can be better, maybe use a dict to pair these up instead?
    if day_name == DayName.MONDAY:
        return "MONDAY"
    if day_name == DayName.TUESDAY:
        return "TUESDAY"
    if day_name == DayName.WEDNESDAY:
        return "WEDNESDAY"
    if day_name == DayName.THURSDAY:
        return "THURSDAY"
    if day_name == DayName.FRIDAY:
        return "FRIDAY"
    if day_name == DayName.SATURDAY:
        return "SATURDAY"
    if day_name == DayName.SUNDAY:
        return "SUNDAY"


class DayInfo:
    """DayInfo class representing member departure times and locations
    for a given day

    Attributes:
        day:
            DayName corresponding the day for which the information is true
        times:
            list of times the member is willing to leave campus
        locations:
            list of locations from which the member is willing to depart

    Typical Usage:
        day = DayInfo(DayName.MONDAY, [6], ["NORTH", "CENTRAL"])
    """

    def __init__(self, day: DayName, times: list, locations: list):
        self.day: DayName = day
        self.times: list = times
        self.locations: list = locations

    def __repr__(self):
        """ Return the representation of the object. """
        return 'DayInfo(%r, %r, %r)' % (self.day, self.times, self.locations)
