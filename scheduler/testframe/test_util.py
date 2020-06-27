from unittest import TestCase
from nose2.tools import params

import scheduler.util as sutil
import scheduler.json_backend as json_backend
from util import sort_by_name


class UtilTest(TestCase):
    """
    Tests for util functions
    """

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

    get_drivers_test_data = [
        (
            [
                {"name": "d1", "is_driver": True},
                {"name": "r1", "is_driver": False},
                {"name": "d2", "is_driver": True},
            ],
            2,
        )
    ]

    get_riders_test_data = [
        (
            [
                {"name": "d1", "is_driver": True},
                {"name": "r1", "is_driver": False},
                {"name": "d2", "is_driver": True},
            ],
            1,
        )
    ]

    filter_dues_payers_test_data = [
        (
            [
                {"name": "d1", "is_dues_paying": True},
                {"name": "r1", "is_dues_paying": False},
                {"name": "d2", "is_dues_paying": True},
            ],
            2,
            ["d1", "d2"],
        ),
        ([{"name": "r1", "is_dues_paying": False},], 0, []),
    ]

    @params(get_drivers_test_data[0])
    def test_get_drivers(self, members, driver_count):
        drivers = sutil.get_drivers(members)

        self.assertEqual(len(drivers), driver_count)

        for driver in drivers:
            self.assertTrue(driver["is_driver"])

    @params(get_riders_test_data[0])
    def test_get_riders(self, members, rider_count):
        riders = sutil.get_riders(members)

        self.assertEqual(len(riders), rider_count)

        for rider in riders:
            self.assertFalse(rider["is_driver"])

    @params(filter_dues_payers_test_data[0], filter_dues_payers_test_data[1])
    def test_dues_payers_filter(self, riders, payers_count, payers):
        filtered = sutil.filter_dues_payers(riders)

        self.assertEqual(len(filtered), payers_count)
        payers.sort()

        for filtered_payer, check in zip(sort_by_name(filtered), payers):
            self.assertEqual(filtered_payer["name"], check)

    @params(get_day_info_from_member_test_data[0])
    def test_get_day_info_from_member(self, member, day, key, check):
        result = sutil.get_day_info_from_member(member, day, key)
        self.assertListEqual(result, check)
