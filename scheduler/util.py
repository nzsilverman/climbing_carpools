import logging
import json

logger = logging.getLogger(__name__)


def filter_dues_payers(riders):
    """
    Returns list of riders that are dues paying.
    """
    dues_payers = []

    for rider in riders:
        if rider["is_dues_paying"]:
            logger.debug("%s is dues paying", rider["name"])
            dues_payers.append(rider)
        else:
            logger.debug("%s is not dues paying", rider["name"])

    return dues_payers


def get_drivers(members):
    """
    Gets drivers from the list of members
    """
    drivers = []

    for member in members:
        if member["is_driver"]:
            drivers.append(member)

    return drivers


def get_riders(members):
    """
    Gets riders from the list of members
    """
    riders = []

    for member in members:
        if not member["is_driver"]:
            riders.append(member)

    return riders


def get_day_info_from_member(member, day, key):
    """
    Gets info associated with the key on the given day from the provided member
    """
    for d in member["days"]:
        if d["day"] == day:
            return d[key]

    logger.error("%s not found for %s in %s", key, day, member)
    return []
