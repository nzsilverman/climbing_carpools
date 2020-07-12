from unittest import TestCase
from nose2.tools import params

from util import members_to_class
from test_data import GenerateRidesTestData as test_data

import scheduler.generate_rides as generate_rides

from scheduler.classes.Driver import Driver
from scheduler.classes.Member import Member
from scheduler.classes.Rider import Rider
import scheduler.classes.Day as Day


class GenerateRidesTest(TestCase):
    """
    Tests Ride Generation
    """

    get_total_seats_test_data = test_data.get_total_seats_test_data
    check_in_days_test_data = test_data.check_in_days_test_data
    are_location_compatible_test_data = test_data.are_location_compatible_test_data
    time_compatibility_test_data = test_data.time_compatibility_test_data
    find_best_match_test_data = test_data.find_best_match_test_data

    @params(check_in_days_test_data[0], check_in_days_test_data[1])
    def test_check_in_days(self, member, day, check):
        result = generate_rides.check_in_days(members_to_class(member),
                                              Day.from_str(day))
        self.assertEqual(result, check)

    @params(get_total_seats_test_data[0], get_total_seats_test_data[1])
    def test_get_total_seats(self, drivers, day, seats):
        seat_count = generate_rides.get_total_seats(members_to_class(drivers),
                                                    Day.from_str(day))
        self.assertEqual(seat_count, seats)

    @params(
        are_location_compatible_test_data[0],
        are_location_compatible_test_data[1],
        are_location_compatible_test_data[2],
    )
    def test_are_location_compatible(self, rider, driver, day, check):
        result = generate_rides.are_location_compatible(
            members_to_class(rider), members_to_class(driver),
            Day.from_str(day))
        self.assertEqual(result, check)

    @params(
        time_compatibility_test_data[0],
        time_compatibility_test_data[1],
        time_compatibility_test_data[2],
    )
    def test_time_compatibility(self, rider, driver, day, check):
        result = generate_rides.time_compatibility(members_to_class(rider),
                                                   members_to_class(driver),
                                                   Day.from_str(day))
        self.assertEqual(result, check)

    @params(find_best_match_test_data[0])
    def test_find_best_match(self, rider, drivers, day, check):
        result, _ = generate_rides.find_best_match(members_to_class(rider),
                                                   members_to_class(drivers),
                                                   Day.from_str(day))
        self.assertEqual(result.name, check)
