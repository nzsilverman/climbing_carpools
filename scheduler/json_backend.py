"""Backend for reading data from JSON.

Primarily for debugging and testing

"""

import json
import logging

from scheduler.util import *

logger = logging.getLogger(__name__)


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


def members_from_json(filename: str) -> (list, list):
    """
    Gets members from a JSON file.
    """

    with open(filename) as f:
        members = json.load(f)

    riders = util.filter_dues_payers(get_riders(members))
    drivers = get_drivers(members)

    return riders, drivers
