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
        ([{"seats": 0, "days": [{"day": "MONDAY"}]}], "MONDAY", 0),
    ]

    check_in_days_test_data = [
        ({"days": [{"day": "MONDAY"}]}, "MONDAY", True),
        ({"days": [{"day": "MONDAY"}]}, "TUESDAY", False),
    ]

    get_day_info_from_member_test_data = [
        (
            {
                "days": [
                    {"day": "MONDAY", "departure_times": [0, 1, 2, 3]},
                    {"day": "TUESDAY", "departure_times": [2, 3]},
                ]
            },
            "TUESDAY",
            "departure_times",
            [2, 3],
        )
    ]

    are_location_compatible_test_data = [
        (
            {"name": "a", "days": [{"day": "MONDAY", "locations": ["NORTH"]}]},
            {
                "name": "b",
                "days": [{"day": "MONDAY", "locations": ["NORTH", "CENTRAL"]}],
            },
            "MONDAY",
            True,
        ),
        (
            {"name": "a", "days": [{"day": "MONDAY", "locations": ["NORTH"]}]},
            {"name": "b", "days": [{"day": "MONDAY", "locations": ["CENTRAL"]}]},
            "MONDAY",
            False,
        ),
        (
            {"name": "a", "days": [{"day": "MONDAY", "locations": ["NORTH"]}]},
            {"name": "b", "days": [{"day": "TUESDAY", "locations": ["NORTH"]}]},
            "TUESDAY",
            False,
        ),
    ]

    time_compatibility_test_data = [
        (
            {"days": [{"day": "MONDAY", "departure_times": [1, 2, 3, 4]}]},
            {"days": [{"day": "MONDAY", "departure_times": [4]}]},
            "MONDAY",
            0,
        ),
        (
            {"days": [{"day": "TUESDAY", "departure_times": [1, 2, 3, 4]}]},
            {"days": [{"day": "TUESDAY", "departure_times": [8]}]},
            "TUESDAY",
            4,
        ),
        (
            {"days": [{"day": "MONDAY", "departure_times": [1.5, 2, 3, 4]}]},
            {"days": [{"day": "MONDAY", "departure_times": [0]}]},
            "MONDAY",
            1.5,
        ),
    ]

    find_best_match_test_data = [
        (
            {
                "name": "r",
                "days": [
                    {
                        "day": "MONDAY",
                        "locations": ["NORTH"],
                        "departure_times": [1, 2, 3],
                    }
                ],
            },
            [
                {
                    "name": "a",
                    "seats": 3,
                    "days": [
                        {
                            "day": "MONDAY",
                            "locations": ["CENTRAL", "NORTH"],
                            "departure_times": [0],
                        }
                    ],
                },
                {
                    "name": "b",
                    "seats": 0,
                    "days": [
                        {
                            "day": "MONDAY",
                            "locations": ["CENTRAL", "NORTH"],
                            "departure_times": [0],
                        }
                    ],
                },
                {
                    "name": "c",
                    "seats": 4,
                    "days": [
                        {
                            "day": "MONDAY",
                            "locations": ["NORTH"],
                            "departure_times": [8],
                        }
                    ],
                },
                {
                    "name": "d",
                    "seats": 4,
                    "days": [
                        {
                            "day": "TUESDAY",
                            "locations": ["CENTRAL"],
                            "departure_times": [2],
                        }
                    ],
                },
            ],
            "MONDAY",
            "a",
        ),
    ]

    @params(check_in_days_test_data[0], check_in_days_test_data[1])
    def test_check_in_days(self, member, day, check):
        result = generate_rides.check_in_days(member, day)
        self.assertEqual(result, check)

    @params(get_total_seats_test_data[0], get_total_seats_test_data[1])
    def test_get_total_seats(self, drivers, day, seats):
        seat_count = generate_rides.get_total_seats(drivers, day)
        self.assertEqual(seat_count, seats)

    @params(get_day_info_from_member_test_data[0])
    def test_get_day_info_from_member(self, member, day, key, check):
        result = generate_rides.get_day_info_from_member(member, day, key)
        self.assertListEqual(result, check)

    @params(
        are_location_compatible_test_data[0],
        are_location_compatible_test_data[1],
        are_location_compatible_test_data[2],
    )
    def test_are_location_compatible(self, rider, driver, day, check):
        result = generate_rides.are_location_compatible(rider, driver, day)
        self.assertEqual(result, check)

    @params(
        time_compatibility_test_data[0],
        time_compatibility_test_data[1],
        time_compatibility_test_data[2],
    )
    def test_time_compatibility(self, rider, driver, day, check):
        result = generate_rides.time_compatibility(rider, driver, day)
        self.assertEqual(result, check)

    @params(find_best_match_test_data[0])
    def test_find_best_match(self, rider, drivers, day, check):
        result = generate_rides.find_best_match(rider, drivers, day)
        self.assertEqual(result["name"], check)
