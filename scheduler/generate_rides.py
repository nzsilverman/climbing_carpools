''' generate_rides.py. Generates rides based on a driver list and rider list '''
import random
from classes.Loc import Loc
from classes.Dept_Time import Dept_Time
from classes.Driver import Driver
from classes.Rider import Rider

def get_total_seats(drivers):
    """ Returns the number of available seats for passengers. """
    return sum([driver.num_riders for driver in drivers])

def seed_matched_dict(drivers):
    """ Returns a dict of drivers and information about
    how many seats they have remaining and who is in the car. """
    matched = dict()
    for driver in drivers:
        matched[driver] = {}
        matched[driver]["seats_left"] = driver.num_riders
        matched[driver]["riders"] = []

    return matched


def find_best_match(matched, rider):
    """ Find the best match for the rider. """
    compatible_drivers = []
    for driver in matched:
        # import pdb; pdb.set_trace()
        if matched[driver]["seats_left"]:
            # check depart time and location to see if driver is compatible
            if rider.dept_time == driver.dept_time or \
                (rider.dept_time == Dept_Time.BEFORE_730 and
                    driver.dept_time == Dept_Time.AT_730) and \
                    (driver.loc == rider.loc or \
                    (rider.loc == Loc.NORTH_AND_CENTRAL and
                        driver.loc == Loc.CENTRAL)):
                    # Compatbile with location
                    compatible_drivers.append(driver)
    # print("Comp drivers: ")
    # print(compatible_drivers)

    if not compatible_drivers:
        # No compatible drivers, so return
        return
    best_driver = compatible_drivers[0]

    # Seletcting the best match looks in compatible drivers,
    # and either returns a perfect match (same time and location)
    # or prioritizes a driver that leaves at the same location as the
    # rider. If none of the drivers leave at the same location as the rider,
    # the default best driver of the first in the list is used. This is not a
    # perfect algorithm but it is simple and does what is needed for this program
    for driver in compatible_drivers:
        if driver.loc == rider.loc:
            if driver.dept_time == rider.dept_time:
                # Perfect match, return this driver
                return driver

            # If no perfect match, prefer a driver that will leave from the
            # same location as the rider
            best_driver = driver

    return best_driver


def generate_rides(riders, drivers):
    ''' Generates rides. '''
    seats_remaining = get_total_seats(drivers)
    # print(seats_remaining)
    # print("num riders: " + str(num_riders))

    matched = seed_matched_dict(drivers)
    # print("Matched dict to start")
    # print(matched)

    # Randomize order of riders
    random.shuffle(riders)

    while seats_remaining and len(riders) > 0:
        # Match a rider with the best possible driver
        # Pick a random rider
        chosen_rider = riders.pop()
        # print("Chosen Rider " + str(chosen_rider.name))

        best_driver = find_best_match(matched, chosen_rider)
        if best_driver:
            # Add rider to that drivers car
            matched[best_driver]["riders"].append(chosen_rider)
            matched[best_driver]["seats_left"] = \
                matched[best_driver]["seats_left"] - 1
            seats_remaining -= 1
            # print(chosen_rider.name +" matched with " + best_driver.name)

    return matched
