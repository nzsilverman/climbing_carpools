"""
A collection of utilties needed by several modules
"""

import logging
import json

logger = logging.getLogger(__name__)


def filter_dues_payers(riders: list) -> list:
    """
    Returns list of riders that are dues paying.
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
    """
    Gets drivers from the list of members
    """

    drivers = list()

    for member in members:
        if member["is_driver"]:
            drivers.append(member)

    return drivers


def get_riders(members: list) -> list:
    """
    Gets riders from the list of members
    """

    riders = list()

    for member in members:
        if not member["is_driver"]:
            riders.append(member)

    return riders


def get_day_info_from_member(member: dict, day: str, key: str):
    """
    Gets info associated with the key on the given day from the provided member
    """

    for d in member["days"]:
        if d["day"] == day:
            return d[key]

    logger.error("%s not found for %s in %s", key, day, member)
    return list()


def get_version() -> str:
    """ Return the version number of the program.
    
    Reads from the VERSION file for this information
    """
    with open('VERSION') as version_file:
        version = version_file.read().strip()
    return version