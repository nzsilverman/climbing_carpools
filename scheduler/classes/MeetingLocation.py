from enum import Enum as enum


class MeetingLocation(enum):
    """Meeting Location.

    Either "NORTH" or "CENTRAL"
    """

    NORTH = 1
    CENTRAL = 2

def to_str(loc: MeetingLocation) -> str:
    if loc == MeetingLocation.NORTH:
        return "NORTH"
    elif loc == MeetingLocation.CENTRAL:
        return "CENTRAL"
    else:
        return "UNDEF"