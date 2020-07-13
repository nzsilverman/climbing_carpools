"""
Test utilities
"""
from scheduler.classes.Member import Member
from scheduler.classes.Driver import Driver
from scheduler.classes.Rider import Rider
import scheduler.classes.Day as Day


def convert_days(days: list) -> list:
    """Converts a list of dictionary days to DayInfo objects

    This is a TODO item. This function works, but it was written to get tests working again.
    It might not be needed once a better testing framework gets worked out.


        Args:
            days:
                a list of dictionaries containing the required information to create a DayInfo object
        
        Returns:
            A DayInfo object
    """

    dayInfos = list()

    for d in days:
        day = Day.DayInfo(day=Day.from_str(get_with_check(d, "day")),
                          times=get_with_check(d, "departure_times"),
                          locations=get_with_check(d, "locations"))

        dayInfos.append(day)

    return dayInfos


def get_with_check(d: dict, key: str):
    """Returns value for key if key exists in the provided dictionary.

        Not all dictionaries used for tests contain all the data required
        to create a Rider, Driver, or Member object so we create 
        a Rider, Driver, or Member object with only the data present in 
        the provided dictionary a fill the empty Rider, Driver, or Member
        constructor parameters with None

        Args:
            d:
                dictionary
            key:
                key to retrieve from dictionary if it exists
            
        Returns:
            value for key if the key exists or None if the key doesn't exist

        Typical Usage:

    """
    if key in d:
        return d[key]
    else:
        return None


# FIXME: this a quick fix to get the tests working again. should be redone
# TODO: probably should split this up into a to riders and a to drivers function
# TODO: find a better way to handle single vs. multiple members
# TODO: add return type hint
def members_to_class(member: Member = None,
                     members: list = None,
                     is_driver: bool = False):
    """Converts a dictionary to a Rider or a Driver object

        Args:
            member:
                A single member to be converted
            members:
                A list of members to be converted
            is_driver:
                Flag to set if member is a driver

        Returns:
            Member objects, number of objects is equal to the number of members passed in the parameters

    """

    #TODO: this is hacky
    member_objects = list()

    # TODO: this is pretty hacky too I think
    if member is not None:
        members = [member]

    for m in members:
        if is_driver:

            # not all dictionaries used for tests contain all the data required
            # to create a Driver, we must check if the key exists first.
            # If the key doesn't exist we can substitute None instead
            driver = Driver(name=get_with_check(m, "name"),
                            email=get_with_check(m, "email"),
                            phone=get_with_check(m, "phone"),
                            days=convert_days(get_with_check(m, "days")),
                            is_dues_paying=get_with_check(m, "is_dues_paying"),
                            car_type=get_with_check(m, "car_type"),
                            seats=get_with_check(m, "seats"))

            member_objects.append(driver)

        else:

            # not all dictionaries used for tests contain all the data required
            # to create a Rider, we must check if the key exists first.
            # If the key doesn't exist we can substitute None instead
            rider = Rider(name=get_with_check(m, "name"),
                          email=get_with_check(m, "email"),
                          phone=get_with_check(m, "phone"),
                          days=convert_days(get_with_check(m, "days")),
                          is_dues_paying=get_with_check(m, "is_dues_paying"))

            member_objects.append(rider)

    if member is not None:
        return member_objects[0]
    else:
        return member_objects


def sort_by_name(members):
    """
    Sort the dictionary of members by name
    """
    return sorted(members, key=lambda m: m.name)
