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
from scheduler.generate_rides import generate_rides

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
logger = logging.getLogger(__name__)


def get_members() -> (list, list):
    """
    Gets members. Abstraction for any backends (JSON, google forms).
    Currently JSON only used in tests. 
    """

    return members_from_sheet()


def match() -> None:
    riders, drivers = get_members()

    # convert generator to list for debugging
    schedule = generate_rides(riders, drivers)

    write_to_sheet(schedule)

    print("Summary:")
    for day in schedule:
        for car in day[1]:
            print("day:", day[0])
            print("driver:", car.driver["name"])
            for r in car.riders:
                print(r["name"])
            print()


def usage() -> None:
    print(
        "Usage: scheduler [-m|--match] [-c|--config <filename>] [-l|--list] [-d|--delete <sheet name>"
    )


def main():
    try:
        opts, _ = getopt.getopt(sys.argv[1:], "mlc:d:t",
                                ["match", "list", "config=", "delete=", "test"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    matching: bool = False
    config_file: str = None
    is_test: bool = False

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
        elif opt == "-t" or opt == "--test":
            # do whatever with this, just set up the infrastructure
            is_test = True

    # initializes configuration instance
    Configuration(config_file=config_file)

    if matching:
        match()


if __name__ == "__main__":
    main()
