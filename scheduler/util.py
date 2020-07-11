""" A collection of utilties needed by several modules.

    Typical Usage Example:

    from util import get_version
    get_version()
"""

import logging
import json

logger = logging.getLogger(__name__)


def filter_dues_payers(riders: list) -> list:
    """ Returns list of riders that are dues paying.

        Args:
            riders:
                A list of riders, each rider is a dictionary entry
        Returns:
            A list of riders (each entry being a dictionary entry) that paid dues
    """

    dues_payers = list()

    for rider in riders:
        if rider["is_dues_paying"]:
            logger.debug("%s is dues paying", rider["name"])
            dues_payers.append(rider)
        else:
            logger.debug("%s is not dues paying", rider["name"])

    return dues_payers


def get_drivers(members: list) -> list:
    """ Gets drivers from the list of members.
    
    Returns:
        A list of members that are drivers
    """

    drivers = list()

    for member in members:
        if member["is_driver"]:
            drivers.append(member)

    return drivers


def get_riders(members: list) -> list:
    """ Gets riders from the list of members.

    Returns:
         A list of members that are riders
    """

    riders = list()

    for member in members:
        if not member["is_driver"]:
            riders.append(member)

    return riders


# TODO- very confusing about what is a member vs rider vs driver and what info
# this is actually fetching. Need classes 

def get_day_info_from_member(member: dict, day: str, key: str):
    """ Gets info associated with the key on the given day from the provided member.

    Reads the member dict for a specific day to return the information stored under a specific
    key for that day. For example, if you wanted to know about the locations a member wants to leave
    from on a specific day, you could pass in "member", "THURSDAY", "locations", and it would return
    what information the member entered for that combination

    Args:
        member:
            Dictionary entry containing information for a specific member
        day:
            Day the requested information is pertaining to
        key:
            Key into the member dict that information is wanted about.
    
    Returns:   
        Variable return type based on the query parameter
    """

    for d in member["days"]:
        if d["day"] == day:
            return d[key]

    logger.error("%s not found for %s in %s", key, day, member)
    return list()


def get_version() -> str:
    """ Return the version number of the program.
    
    Reads from the VERSION file for this information

    Returns:
        Returns a string of the version number or an error message
    """
    try:
        with open('VERSION') as version_file:
            version = version_file.read().strip()
    except:
        return "Error Getting Version Number"
    return version