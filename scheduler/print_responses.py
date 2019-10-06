""" print_responses.py
    This file helps print the dictionaries created for pairing drivers and riders
    It is useful for debugging and as a stand in until the data gets published
    to a google sheet. """

from classes.Loc import Loc
from classes.Dept_Time import Dept_Time
from classes.Driver import Driver
from classes.Rider import Rider

def print_matched_debug(matched):
    """ print the matched dict with all info, for the debug. It has the format:
    {Driver: {'seats_left': #, 'riders': [Rider, ..., Rider]}, ...} """

    driver_email_list = []
    rider_email_list = []

    for driver in matched:
        driver_email_list.append(driver.email)
        print("Driver: {}\tPhone: {}\tDept. Time: {}\tAlt Time: {}\t Dept. Location: {}\t Open Spots: {}"\
                .format(driver.name, driver.phone, driver.dept_time, driver.alt_time, driver.loc, matched[driver]["seats_left"]))
        rider_num = 1
        for rider in matched[driver]["riders"]:
            rider_email_list.append(rider.email)
            # print("Rider {} Name: {}\t Email: {}".format(rider.name, rider.email))
            print("Rider {} Name: {}\tPhone: {}\t Email: {}\t Loc: {}\tDept. Time:{}".format(rider_num, rider.name, rider.phone, rider.email, rider.loc, rider.dept_time))
            rider_num = rider_num + 1

        print("\n\n")

    print("\nDriver Email List:")
    print(driver_email_list)

    print("\nRider Email List:")
    print(rider_email_list)

