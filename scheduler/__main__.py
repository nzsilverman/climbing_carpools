#!/usr/bin/env python3
""" Climbing Carpool generator. """

import logging
import os
import sys

from gform_backend import (
    members_from_sheet,
    write_to_sheet,
    delete_spreadsheet,
    list_spreadsheets,
)
from json_backend import members_from_json
from generate_rides import generate_rides

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
logger = logging.getLogger(__name__)

"""
Spreadsheet and output configuration
"""
DUES_SHEET = "dues-testing-v20.0.0"
SPREADSHEET = "Carpool Form v20.0.0 (Responses)"
OUTPUT_SPREADSHEET = "Carpool test output 1"
DAYS_ENABLED = ["TUESDAY", "THURSDAY", "SUNDAY"]
OUTPUT_FOLDER_ID = "1j1w_0k5bIgqxJfmQmxbZZoGr66fJT4Y4"


def get_members():
    """
    Gets members. Abstraction for any backends (JSON, google forms).
    Currently JSON only used in tests
    """

    return members_from_sheet(DUES_SHEET, SPREADSHEET, DAYS_ENABLED)


def main():
    riders, drivers = get_members()

    # convert generator to list for debugging
    schedule = list(generate_rides(riders, drivers, DAYS_ENABLED))

    write_to_sheet(schedule, OUTPUT_SPREADSHEET, OUTPUT_FOLDER_ID)

    print("Summary:")
    for day in schedule:
        for car in day[1]:
            print("day:", day[0])
            print("driver:", car.driver["name"])
            for r in car.riders:
                print(r["name"])
            print()


def clean_drive(sheets):
    """
    Deletes spreadsheets matching the provided names
    """
    delete_spreadsheet(sheets)
    logger.info("Done deleteing sheets")


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    if len(sys.argv) > 1:
        if sys.argv[1] == "clean" or sys.argv[1] == "c":
            clean_drive(sys.argv[2:])
        elif sys.argv[1] == "list" or sys.argv[1] == "l":
            list_spreadsheets()
    else:
        main()
