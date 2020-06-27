"""
Generates rides based on a driver list and rider list 
"""
import random
import logging
import sys

from scheduler.classes.Car import Car
from scheduler.classes.MeetingLocation import MeetingLocation

logger = logging.getLogger(__name__)


def check_in_days(member, day):
    """
    Checks if member is signed up for the given day
    """
    for d in member["days"]:
        if d["day"] == day:
            return True

    return False


def get_total_seats(drivers, day):
    """
    Returns the number of available seats for passengers.
    """
    return sum([driver["seats"] for driver in drivers if check_in_days(driver, day)])


def get_day_info_from_member(member, day, key):
    """
    Gets info associated with the key on the given day from the provided member
    """
    for d in member["days"]:
        if d["day"] == day:
            return d[key]

    logger.error("%s not found for %s in %s", key, day, member)
    return []


def are_location_compatible(rider, driver, day):
    """
    Checks if rider and driver have compatible location settings.
    """

    for location in get_day_info_from_member(rider, day, "locations"):
        if location in get_day_info_from_member(driver, day, "locations"):
            logger.debug("location match %s and %s", rider["name"], driver["name"])
            return True

    return False


def time_compatibility(rider, driver, day):
    """
    Checks time compatibility. Finds driver and rider with closest departure time
    """

    rider_times = get_day_info_from_member(rider, day, "departure_times")
    driver_times = get_day_info_from_member(driver, day, "departure_times")

    rider_times.sort()

    # there should only be one time here
    driver_times.sort()
    if len(driver_times) != 1:
        logger.error("driver has multiple departure times for %s", day)
        exit(2)

    driver_time = driver_times[0]

    result = sys.maxsize

    # finds minimum difference between rider departure times and driver time
    for time in rider_times:
        if abs(time - driver_time) < result:
            result = abs(time - driver_time)

    logger.debug("min time difference: %i", result)
    return result


def find_best_match(rider, drivers, day):
    """
    Find the best match for the rider.

    Input: rider, drivers, day
    Output: most compatible driver
    """

    # this probably needs to be rewritten with some kind of proper algorithm.
    # right now, we're choosing the driver that is leaving closest to the requested time
    # given day and location compatibility.
    #
    # this algorithm is a good choice if we truly want to give everyone an ~equal~ chance
    # in getting a car but we disregard how well they fit in it relative to others.

    compatible_drivers = []

    # finds all compatible drivers
    for driver in drivers:
        if driver["seats"] and are_location_compatible(rider, driver, day):
            compatible_drivers.append([driver, time_compatibility(rider, driver, day)])

    if not compatible_drivers:
        logger.warn("no compatible drivers for %s", rider["name"])
        return

    # return driver that best matches the time
    return sorted(compatible_drivers, key=lambda lst: lst[1])[0][0]


def generate_rides(riders, drivers, days_enabled):
    """
    Matches riders with drivers.
    """

    for day in days_enabled:
        # cars for the given day
        cars = []

        # shuffle the riders for every day
        random.shuffle(riders)

        seats_remaining = get_total_seats(drivers, day)
        logger.info("%i seats available", seats_remaining)

        days_riders = riders

        while seats_remaining > 0 and len(days_riders) > 0:

            chosen_rider = days_riders.pop()
            # don't match rider if not riding current day
            if not check_in_days(chosen_rider, day):
                print(chosen_rider["name"], "not riding", day)
                continue

            best_driver = find_best_match(chosen_rider, drivers, day)

            driver_has_car = False

            if best_driver:

                # add rider to selected driver's car
                for car in cars:
                    if car.driver == best_driver:
                        car.riders.append(chosen_rider)
                        driver_has_car = True

                # give driver a car if they don't already have one
                if not driver_has_car:
                    new_car = Car(best_driver)
                    new_car.riders.append(chosen_rider)
                    cars.append(new_car)

        yield (day, cars)
