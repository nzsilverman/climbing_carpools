""" Generates rides based on a driver list and rider list 

Typical Usage:
    import generate_rides
    <call one of the functions in this file>
"""
import random
import logging
import sys
from copy import deepcopy

from scheduler.classes.Car import Car
from scheduler.classes.MeetingLocation import MeetingLocation
from scheduler.classes.Configuration import Configuration
from scheduler.classes.Driver import Driver
from scheduler.classes.Member import Member
from scheduler.classes.Rider import Rider
import scheduler.classes.Day as Day

logger = logging.getLogger(__name__)


def check_in_days(member: Member, day: Day.DayName) -> bool:
    """ Checks if member is signed up for the given day

    Args:
        member:
            Member object
        day:
            Day.DayName enum, day to check if member is signed up for

    Returns:
        True -> member is signed up for the given day
        False -> member is not signed up for the given day
    """

    for d in member.days:
        if d.day == day:
            logger.debug("%s is in %s", member.name, day)
            return True

    logger.debug("%s is not in %s", member.name, day)

    return False


def get_total_seats(drivers: list, day: Day.DayName) -> int:
    """ Returns the number of available seats for passengers across all drivers for a certain day.

    Args:
        drivers:
            list of Driver objects
        day:
            Day.DayName enum specifying the day for which to calculate seats
    
    Returns:
        Integer of total number of seats avaialble for a certain day across all drivers for that day
    """

    return sum([
        driver.seats_remaining
        for driver in drivers
        if check_in_days(driver, day)
    ])


def are_location_compatible(rider: Rider, driver: Driver,
                            day: Day.DayName) -> bool:
    """ Checks if rider and driver have compatible location settings.
    
    Compatible locations are defined as listing the same location as an option to
    leave from for both the driver and the rider. Drivers and Riders may list multiple 
    locations they are ok with leaving from

    Returns:
        True -> Locations are compatible
        False -> Locations are not compatible

    """

    for location in rider.get_locations(day):
        if location in driver.get_locations(day):
            logger.debug("location match %s and %s", rider.name, driver.name)
            return True

    return False


def time_compatibility(rider: Rider, driver: Driver, day: Day.DayName) -> float:
    """ Checks time compatibility. Finds driver and rider with closest departure time.

    For a specific driver and rider, returns the smallest time difference between when
    that driver wants to leave and the times the rider listed they would be able to leave
    
    Args:
        rider:
            Rider object
        driver:
            Driver object
        day:
            Day.DayName enum of day for which to check time compatability

    Returns:
        Float that is the minimum time difference between when a specific driver and rider would
        like to leave
    """

    rider_times = rider.get_times(day)
    driver_times = driver.get_times(day)

    rider_times.sort()

    # there should only be one time here, so maybe remove
    # maybe keep this in case there are more than 1 to keep things deterministic
    driver_times.sort()

    if len(driver_times) != 1:
        logger.error("driver has multiple departure times for %s", day)
        exit(2)

    driver_time = driver_times[0]

    #
    result = sys.maxsize

    # finds earliest matching time, rider times are sorted
    for time in rider_times:
        if time == driver_time:
            logger.debug("rider %s time compatible with %s", rider.name,
                         driver.name)
            result = time
            break

    return result


def find_best_match(rider: Rider, drivers: list,
                    day: Day.DayName) -> (Driver, list):
    """Find the best match for the rider.

    Finds all compatible drivers for the rider and gives priority to the driver
    that has available seats and minimizes the time between when the rider and driver
    would like to leave. 

    Args:
        rider:
            Rider object
        drivers:
            list of Driver objects
        day:
            Day.DayName enum of day for which a match is being found
        
    Returns:
        (Driver, list)
        Driver: This was the riders best match driver

        The list is the updated drivers list. The seats remaining count has been updated for that
        list, so it is important the returned list is used as the new drivers list

    """

    # this probably needs to be rewritten with some kind of proper algorithm.
    # right now, we're choosing the driver that matches the earliest of the
    # rider's desired times
    #
    # this algorithm is a good choice if we truly want to give everyone an ~equal~ chance
    # in getting a car but we disregard how well they fit in it relative to others.

    compatible_drivers = list()

    # finds all compatible drivers
    for driver in drivers:
        if driver.seats_remaining and are_location_compatible(
                rider, driver, day):
            compatible_drivers.append(
                [driver, time_compatibility(rider, driver, day)])

    if not compatible_drivers:
        logger.warn("no compatible drivers for %s", rider.name)
        return None, drivers

    # compatible_drivers is a list where each entry is a list with two elements
    # inner list strucutre:
    # [0] -> Driver object
    # [1] -> float that is the timne delta between when this specific driver and a rider want to leave

    # Sort the compatible drivers list to find the compatible driver leaving earliest
    # Store the smallest driver dictionary value into the best match variable
    best_match = sorted(compatible_drivers, key=lambda lst: lst[1])[0][0]

    # Decrement the seats remaining for the driver that was the best match
    for d in drivers:
        if best_match == d:
            d.seats_remaining -= 1

    # return driver that best matches the time and the updated driver list
    return best_match, drivers


def generate_rides(riders: list, drivers: list) -> list:
    """Matches riders with drivers.

    Args:
        riders:
            A list of Rider objects. 
        drivers:
            A list of Driver objects.

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

    # copy only once
    days_drivers = deepcopy(drivers)

    # Collect which days the club wishes to run a carpool
    days_enabled = Configuration.config("mcc.days_enabled")

    for day in days_enabled:

        # we're only copying the entire list of drivers once now.
        # now copying only the seats remaining every day instead
        # of the whole list.
        for (days_d, d) in zip(days_drivers, drivers):
            days_d.seats_remaining = d.seats_remaining

        day = Day.from_str(day)

        # cars for the given day
        cars = list()

        # shuffle the riders for every day to ensure they are chosen fairly
        random.shuffle(riders)

        seats_remaining = get_total_seats(days_drivers, day)
        logger.info("%i seats available for %s", seats_remaining,
                    Day.to_str(day))

        # Copy the riders to maintain the original list of riders so that
        # each iteration of the loop has an unaffected rider list
        # TODO: find a more efficient way to do this
        days_riders = deepcopy(riders)

        # keep picking riders until no more seats remain or no more riders remain
        while seats_remaining > 0 and len(days_riders) > 0:
            chosen_rider = days_riders.pop()
            # don't match rider if not riding current day
            if not check_in_days(chosen_rider, day):
                logger.debug("%s not riding %s", chosen_rider.name, day)
                continue

            best_driver, days_drivers = find_best_match(chosen_rider,
                                                        days_drivers, day)

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
                logger.debug("%s not matched", chosen_rider.name)

        schedule.append((day, cars))

    return schedule
