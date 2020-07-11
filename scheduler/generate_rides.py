""" Generates rides based on a driver list and rider list 

Typical Usage:
    import generate_rides
    <call one of the functions in this file>
"""
import random
import logging
import sys

from scheduler.classes.Car import Car
from scheduler.classes.MeetingLocation import MeetingLocation
from scheduler.classes.Configuration import Configuration
from scheduler.util import get_day_info_from_member

logger = logging.getLogger(__name__)


def check_in_days(member: dict, day: str) -> bool:
    """ Checks if member is signed up for the given day

    Args:
        member:
            member dictionary
        day:
            day to check if member is signed up for

    Returns:
        True -> member is signed up for the given day
        False -> member is not signed up for the given day
    """

    for d in member["days"]:
        if d["day"] == day:
            return True

    return False


def get_total_seats(drivers: list, day: str) -> int:
    """ Returns the number of available seats for passengers across all drivers for a certain day.

    Args:
        drivers:
            list of drivers, each driver is a dictionary entry of a driver
        day:
            string specifying which day the query is for
    
    Returns:
        Integer of total number of seats avaialble for a certain day across all drivers for that day
    """

    return sum(
        [driver["seats"] for driver in drivers if check_in_days(driver, day)])


def are_location_compatible(rider: dict, driver: dict, day: str) -> bool:
    """ Checks if rider and driver have compatible location settings.
    
    Compatible locations are defined as listing the same location as an option to
    leave from for both the driver and the rider. Drivers and Riders may list multiple 
    locations they are ok with leaving from

    Returns:
        True -> Locations are compatible
        False -> Locations are not compatible

    """

    for location in get_day_info_from_member(rider, day, "locations"):
        if location in get_day_info_from_member(driver, day, "locations"):
            logger.debug("location match %s and %s", rider["name"],
                         driver["name"])
            return True

    return False


# TODO- this function does not ensure that a rider is ok at leaving when the driver
# wants to leave. This could results in riders being assigned times that are invalid for
# when they want to leave, which is an error
def time_compatibility(rider: dict, driver: dict, day: str) -> float:
    """ Checks time compatibility. Finds driver and rider with closest departure time.

    For a specific driver and rider, returns the smallest time difference between when
    that driver wants to leave and the times the rider listed they would be able to leave
    
    Args:
        rider:
            dictionary of a rider
        driver:
            dictionary of a driver
        day:
            string of day to check time compatability for

    Returns:
        Float that is the minimum time difference between when a specific driver and rider would
        like to leave
    """

    rider_times = get_day_info_from_member(rider, day, "departure_times")
    driver_times = get_day_info_from_member(driver, day, "departure_times")

    rider_times.sort()

    # there should only be one time here
    driver_times.sort()
    if len(driver_times) != 1:
        logger.error("driver has multiple departure times for %s", day)
        # Todo- this probably does not need to kill the program, we could prob
        # catch this kind of error more gracefully and ignore that driver and
        # output that
        exit(2)

    driver_time = driver_times[0]

    result = sys.maxsize

    # finds minimum difference between rider departure times and driver time
    for time in rider_times:
        if abs(time - driver_time) < result:
            result = abs(time - driver_time)

    logger.debug("min time difference: %i", result)
    return result


def find_best_match(rider: dict, drivers: list, day: str) -> (dict, list):
    """Find the best match for the rider.

    Finds all compatible drivers for the rider and gives priority to the driver
    that has available seats and minimizes the time between when the rider and driver
    would like to leave. 

    Args:
        rider:
            dictionary entry that represents a rider
        drivers:
            list of drivers, each driver is a dictionary entry
        day:
            day that a match is being found for
        
    Returns:
        (dict, list)
        The dict is the dictionary for the driver that should drive the inputed rider. This was
        the riders best match driver

        The list is the updated drivers list. The seats remaining count has been updated for that
        list, so it is important the returned list is used as the new drivers list

    """

    # this probably needs to be rewritten with some kind of proper algorithm.
    # right now, we're choosing the driver that is leaving closest to the requested time
    # given day and location compatibility.
    #
    # this algorithm is a good choice if we truly want to give everyone an ~equal~ chance
    # in getting a car but we disregard how well they fit in it relative to others.

    compatible_drivers = list()

    # finds all compatible drivers
    for driver in drivers:
        if driver["seats_remaining"] and are_location_compatible(
                rider, driver, day):
            compatible_drivers.append(
                [driver, time_compatibility(rider, driver, day)])

    if not compatible_drivers:
        logger.warn("no compatible drivers for %s", rider["name"])
        return None, drivers

    # compatible_drivers is a list where each entry is a list with two elements
    # inner list strucutre:
    # [0] -> driver dictionary entry
    # [1] -> float that is the timne delta between when this specific driver and a rider want to leave

    # Sort the compatible drivers list based on the time delta between drivers and riders
    # Store the smallest driver dictionary value into the best match variable
    best_match = sorted(compatible_drivers, key=lambda lst: lst[1])[0][0]

    # Decrement the seats remaining for the driver that was the best match
    for d in drivers:
        if best_match == d:
            d["seats_remaining"] -= 1

    # return driver that best matches the time and the updated driver list
    return best_match, drivers


def generate_rides(riders: list, drivers: list) -> list:
    """Matches riders with drivers.

    Args:
        riders:
            A list of riders, where each rider is a dictionary entry. 
        drivers:
            A list of drivers, where each driver is a dictionary entry.

    Returns:
        A list of departure days and corresponding cars. The list has the following format:
        [(DAY 1, [CAR 1, CAR2, CAR 3]), (DAY 2, [CAR 1]), (etc, etc)]
        
        Each entry in the list is a tuple. The tuple holds a string in index 0 that 
        corresponds to the day that group of cars will be departing. Index 1 holds a list of the car 
        objects that are departing on that day.
    
    Typical Usage:
        schedule = generate_rides(riders, drivers)
    """

    schedule = list()

    # Collect which days the club wishes to run a carpool
    days_enabled = Configuration.config("mcc.days_enabled")

    for day in days_enabled:
        # cars for the given day
        cars = list()

        for driver in drivers:
            driver["seats_remaining"] = driver["seats"]

        # shuffle the riders for every day to ensure they are chosen fairly
        random.shuffle(riders)

        seats_remaining = get_total_seats(drivers, day)
        logger.info("%i seats available", seats_remaining)

        # Copy the riders to maintain the original list of riders so that
        # each iteration of the loop has an unaffected rider list
        days_riders = riders.copy()

        # keep picking riders until no more seats remain or no more riders remain
        while seats_remaining > 0 and len(days_riders) > 0:
            chosen_rider = days_riders.pop()
            # don't match rider if not riding current day
            if not check_in_days(chosen_rider, day):
                logger.debug("%s not riding %s", chosen_rider["name"], day)
                continue

            best_driver, drivers = find_best_match(chosen_rider, drivers, day)

            # Used to check if a Car object has been created for this rider, for this day yet
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

                seats_remaining -= 1
            else:
                logger.debug("%s not matched", chosen_rider["name"])

        schedule.append((day, cars))

    return schedule
