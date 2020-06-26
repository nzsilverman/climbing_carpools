#!/usr/bin/env python3
""" Climbing Carpool generator. """

import logging
import os

from gform_backend import members_from_sheet
from generate_rides import generate_rides

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
logger = logging.getLogger(__name__)

DUES_PAYERS_SHEET_NAME = ""
RESPONSES_SHEET_NAME = ""

def get_members():
    """
    Gets members. Abstraction for any backends (JSON, google forms).
    Currently JSON only used in tests
    """

    logger.info("getting members from google sheet")
    return members_from_sheet(DUES_PAYERS_SHEET_NAME, RESPONSES_SHEET_NAME)

def main():
    riders, drivers = get_members()
    cars = generate_rides(riders, drivers)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
