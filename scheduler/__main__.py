""" Climbing Carpool generator.

This carpool scheduling software is designed to fairly match riders with drivers that
best meet their date, location, and time preferences. It is designed to give priority 
to due paying club members who are seeking a ride. The software pulls google form response
data from a google sheet that is specified in the user-config.toml file. It then fairly
selects due paying riders to be matched to available drivers. This matching is then 
written to a google sheet.

    Typical Usage Example:

        scheduler -m
 """

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
from scheduler.generate_rides import generate_rides
from scheduler.util import get_version

from scheduler.classes.Rider import Rider
from scheduler.classes.Driver import Driver
import scheduler.classes.Day as Day

logging.basicConfig(
    filename="climbing_carpools.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def get_members() -> (list, list):
    """ Gets all club members who are looking to ride or drive.
    
    This function is an abstraction that allows this function to be agnostic of the backend that
    the member data is stored in / collected from (JSON, google forms/ sheets, etc).

    Returns:
        (riders list, drivers list)
        Returns a tuple of lists- the first containing Rider objects, and the second containing driver objects.
    """

    return members_from_sheet()


def match() -> None:
    """ Matches riders to a car, writes the result to the google sheet.

    """
    riders, drivers = get_members()

    schedule = generate_rides(riders, drivers)

    write_to_sheet(schedule)

    print("Summary of rides generated:")
    for day in schedule:
        print("Rides for:\t{}".format(Day.to_str(day[0])))
        for car in day[1]:
            print("Driver:\t{}".format(car.driver.name))
            for r in car.riders:
                print("Rider:\t{}".format(r.name))
            print()


def print_tab(message: str) -> None:
    """ Print a tab followed by the message string passed in. 
    """
    print("\t{}".format(message))


def usage() -> None:
    """ Print program usage.
    """

    print("scheduler\tversion: {}\n".format(get_version()))
    print("NAME:")
    print_tab("scheduler - a command line utility for scheduling carpools")
    print("SYNOPSIS")
    print_tab("-m\t--match\tMatch drivers and riders, publish google sheet")
    print_tab("-c\t--config <filename>\t Provide a path to a config file")
    print_tab("-l\t--list\tList all files the service account has access to")
    print_tab(
        "-d\t--delete <sheet name> Delete the specified sheet from google drive"
    )
    print_tab("-h\t--help\t Print help menu")
    print_tab("-v\t--version\tPrint version number")

    print("DESCRIPTION")
    print_tab(
        "This software matches riders to the best carpool driver for them.")
    print_tab(
        "It is designed to do this task fairly, and take into account whether ")
    print_tab(
        "riders have paid dues. Please see the github repository for more information."
    )
    print_tab(
        "The repository can be found here: https://github.com/nzsilverman/climbing_carpools"
    )


def main():
    """ Orchestrate the running of the scheduler program.

    Parses arguments, decides how the program should be run.
    """

    # Extract command line arguments
    try:
        opts, _ = getopt.getopt(
            sys.argv[1:], "mlcvh:d:t",
            ["match", "list", "config=", "delete=", "test", "version", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    matching: bool = False
    config_file: str = None
    config_provided: bool = False
    is_test: bool = False

    if len(opts) == 0:
        usage()
        sys.exit(0)

    # Decide how to treat arguments that were passed in
    for opt, arg in opts:
        if opt == "-l" or opt == "--list":
            list_spreadsheets()
            sys.exit(0)
        elif opt == "-d" or opt == "--delete":
            delete_spreadsheet(arg)
            sys.exit(0)
        elif opt == "-m" or opt == "--match":
            matching = True
        elif opt == "-c" or opt == "--config":
            config_file = arg
            config_provided = True
        elif opt == "-t" or opt == "--test":
            # do whatever with this, just set up the infrastructure
            is_test = True
        elif opt == "-h" or opt == "--help":
            usage()
            sys.exit(0)
        elif opt == "-v" or opt == "--version":
            print("Version: {}".format(get_version()))
            sys.exit(0)

    # initialize configuration instance
    if config_provided is False:
        Configuration.config(filename=config_file)

    if matching:
        match()


if __name__ == "__main__":
    main()
