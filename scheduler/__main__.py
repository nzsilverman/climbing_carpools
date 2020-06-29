#!/usr/bin/env python3
""" Climbing Carpool generator. """

import logging
import os
import sys, getopt

from scheduler.classes.Configuration import Configuration
from scheduler.gform_backend import (
    members_from_sheet,
    write_to_sheet,
    delete_spreadsheet,
    list_spreadsheets,
)
from scheduler.json_backend import members_from_json
from scheduler.generate_rides import generate_rides, test

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
logger = logging.getLogger(__name__)

"""
Spreadsheet and output configuration
"""
DUES_SHEET = "dues-testing-v20.0.0"
SPREADSHEET = "Carpool Form v20.0.0 (Responses)"
OUTPUT_SPREADSHEET = "Carpool test output 3"
DAYS_ENABLED = ["TUESDAY", "THURSDAY", "SUNDAY"]
OUTPUT_FOLDER_ID = "1j1w_0k5bIgqxJfmQmxbZZoGr66fJT4Y4"


def get_members():
    """
    Gets members. Abstraction for any backends (JSON, google forms).
    Currently JSON only used in tests
    """

    return members_from_sheet(DUES_SHEET, SPREADSHEET, DAYS_ENABLED)


def match():
    riders, drivers = get_members()

    # convert generator to list for debugging
    schedule = generate_rides(riders, drivers, DAYS_ENABLED)

    write_to_sheet(schedule, OUTPUT_SPREADSHEET, OUTPUT_FOLDER_ID)

    print("Summary:")
    for day in schedule:
        for car in day[1]:
            print("day:", day[0])
            print("driver:", car.driver["name"])
            for r in car.riders:
                print(r["name"])
            print()


def usage():
    print("Usage: scheduler [-m|--match] [-c|--config <filename>] [-l|--list]")


def main():
    try:
        opts, _ = getopt.getopt(
            sys.argv[1:], "mlc:d:t", ["match", "list", "config=", "delete=", "--test"]
        )
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    matching = False
    config_file = None
    test = False

    if len(opts) == 0:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-l" or opt == "--list":
            list_spreadsheets()
        elif opt == "-d" or opt == "--delete":
            delete_spreadsheet(arg)
        elif opt == "-m" or opt == "--match":
            matching = True
        elif opt == "-c" or opt == "--config":
            config_file = arg

    Configuration(config_file)

    if test:
        return

    if matching:
        match()


if __name__ == "__main__":
    main()
