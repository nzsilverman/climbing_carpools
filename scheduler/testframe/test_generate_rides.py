"""
Generate Rides tests
"""

from unittest import TestCase
from nose2.tools import params

from util import sort_by_name

import scheduler.generate_rides as generate_rides


class GenerateRidesTest(TestCase):

    get_total_seats_test_data = [
        ([{"seats": 4}, {"seats": 3}, {"seats": 2}, {"seats": 1}], 10),
        ([{"seats": 0},], 0),
    ]

    @params(get_total_seats_test_data[0])
    def test_get_total_seats(self, drivers, seats):
        seat_count = generate_rides.get_total_seats(drivers)
        self.assertEqual(seat_count, seats)
