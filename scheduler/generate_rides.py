"""
Generates rides based on a driver list and rider list 
"""
import random
import logging
import sys

from scheduler.classes.Car import Car
from scheduler.classes.MeetingLocation import MeetingLocation

logger = logging.getLogger(__name__)


def get_total_seats(drivers):
    """
    Returns the number of available seats for passengers.
    """
    return sum([driver["seats"] for driver in drivers])


def are_location_compatible(rider, driver):
    """
    Checks if rider and driver have compatible location settings.
    """

    for location in rider["locations"]:
        if location in driver["locations"]:
            logger.debug("location match %s and %s", rider["name"], driver["name"])
            return True

    return False


def time_compatibility(rider, driver):
    """
    Checks time compatibility. Finds driver and rider with closest departure time
    """
    rider_times = rider["departure_times"]
    driver_times = driver["departure_times"]

    rider_times.sort()
    driver_times.sort()

    result = sys.maxsize
    r = 0
    d = 0

    while r < len(rider_times) and d < len(driver_times):
        diff = abs(rider_times[r] - driver_times[d])
        if diff < result:
            result = diff

        if rider_times[r] < driver_times[d]:
            r += 1
        else:
            d += 1

    logger.debug("min time difference: %i", result)
    return result


def find_best_match(drivers, rider):
    """
    Find the best match for the rider. Criterion for best match is
    defined as 1) a matching location and 2) the closest available time.
    """
    compatible_drivers = []
    for driver in drivers:
        if driver["seats"] and are_location_compatible(rider, driver):
            compatible_drivers.append([driver, time_compatibility(rider, driver)])

    if not compatible_drivers:
        logger.warn("no compatible drivers for %s", rider["name"])
        return

    return sorted(compatible_drivers, key=lambda lst: lst[1])[0][0]


def generate_rides(riders, drivers):
    """
    Matches riders with drivers.
    """

    seats_remaining = get_total_seats(drivers)
    logger.info("%i seats available", seats_remaining)

    random.shuffle(riders)

    cars = []

    while seats_remaining > 0 and len(riders) > 0:
        chosen_rider = riders.pop()

        best_driver = find_best_match(drivers, chosen_rider)
        driver_has_car = False

        if best_driver:
            for car in cars:
                if car.driver == best_driver:
                    car.riders.append(chosen_rider)
                    driver_has_car = True

            if not driver_has_car:
                new_car = Car(best_driver)
                new_car.riders.append(chosen_rider)
                cars.append(new_car)

    return cars
