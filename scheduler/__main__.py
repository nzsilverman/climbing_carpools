#!/usr/bin/env python3
""" Climbing Carpool generator. """

import logging
import os

from gform_backend import members_from_sheet
from json_backend import members_from_json
from generate_rides import generate_rides

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
logger = logging.getLogger(__name__)

DUES_SHEET = "dues-testing-v20.0.0"
SPREADSHEET = "Carpool Form v20.0.0 (Responses)"
DAYS_ENABLED = ["TUESDAY", "THURSDAY", "SUNDAY"]


def get_members():
    """
    Gets members. Abstraction for any backends (JSON, google forms).
    Currently JSON only used in tests
    """

    return members_from_sheet(DUES_SHEET, SPREADSHEET, DAYS_ENABLED)


def main():
    riders, drivers = get_members()

    print("riders:")
    for r in riders:
        print(r)

    print("drivers")
    for d in drivers:
        print(d)

    # convert generator to list for debugging
    schedule = list(generate_rides(riders, drivers, DAYS_ENABLED))

    for day in schedule:
        for car in day:
            print(car.driver)
            print(car.riders)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
