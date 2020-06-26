from unittest import TestCase
from nose2.tools import params

from util import sort_by_name

import scheduler.generate_rides as generate_rides


class GenerateRidesTest(TestCase):
    """
    Tests Ride Generation
    """

    get_total_seats_test_data = [
        (
            [
                {"seats": 4, "days": [{"day": "FRIDAY"}]},
                {"seats": 3, "days": [{"day": "TUESDAY"}]},
                {"seats": 2, "days": [{"day": "MONDAY"}]},
                {"seats": 1, "days": [{"day": "TUESDAY"}]},
            ],
            "TUESDAY",
            4,
        ),
        ([{"seats": 0, "days": [{"day": "MONDAY"}]},], 0),
    ]

    @params(get_total_seats_test_data[0])
    def test_get_total_seats(self, drivers, day, seats):
        seat_count = generate_rides.get_total_seats(drivers, day)
        self.assertEqual(seat_count, seats)
