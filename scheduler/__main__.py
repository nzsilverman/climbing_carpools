#!/usr/bin/env python3
""" Climbing Carpool generator. """
from read_responses import *
from generate_rides import *
from print_responses import *

def main():
    # Sheet name: Carpool Scheduling Template (Responses)
    # Dues sheet name: Due Paying Members
    sheet_name = "Carpool Scheduling Template (Responses)"
    dues_sheet_name = "Due Paying Members"

    form_responses = create_lists(sheet_name, dues_sheet_name)
    tues_drivers = form_responses[0]
    tues_riders = form_responses[1]
    thurs_drivers = form_responses[2]
    thurs_riders = form_responses[3]
    sun_drivers = form_responses[4]
    sun_riders = form_responses[5]

    # print("tues_drivers")
    # print(tues_drivers)

    # print("tues_riders")
    # print(tues_riders)

    # print("thurs_drivers")
    # print(thurs_drivers)

    # print("thurs_riders")
    # print(thurs_riders)

    # print("sun_drivers")
    # print(sun_drivers)

    # print("sun_riders")
    # print(sun_riders)

    tues_rides = generate_rides(tues_riders, tues_drivers)
    thurs_rides = generate_rides(thurs_riders, thurs_drivers)
    sun_rides = generate_rides(sun_riders, sun_drivers)

    print("Tuesday Rides: \n")
    print_matched_debug(tues_rides)

    print("Thursday Rides: \n")
    print_matched_debug(thurs_rides)

    print("Sunday Rides: \n")
    print_matched_debug(sun_rides)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
