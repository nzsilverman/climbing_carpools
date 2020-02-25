#!/usr/bin/env python3
""" Climbing Carpool generator. """
from read_responses import *
from generate_rides import *
from print_responses import *
from write_to_sheet import *

def main():
    # Sheet name: Carpool Scheduling Template (Responses)
    # Dues sheet name: Due Paying Members
    sheet_name = "Responses 2-23-20"
    output_sheet_name =  "MCC Carpools 2-23-20"
    dues_sheet_name = "MCC Dues Paying Members 2019-2020"

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

    print("Tuesday Generation happening... :")
    tues_rides = generate_rides(tues_riders, tues_drivers)
    # print("\n\nTuesday Rides: \n")
    # print_matched_debug(tues_rides)

    print("Thursday Generation happening... :")
    thurs_rides = generate_rides(thurs_riders, thurs_drivers)
    # print("\n\nThursday Rides: \n")
    # print_matched_debug(thurs_rides)

    print("Sunday Generation happening... :")
    sun_rides = generate_rides(sun_riders, sun_drivers)
    # print("\n\nSunday Rides: \n")
    # print_matched_debug(sun_rides)

    print("Writing to google sheet... ")
    write_to_gsheet(tues_rides, thurs_rides, sun_rides, output_sheet_name)

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    main()
