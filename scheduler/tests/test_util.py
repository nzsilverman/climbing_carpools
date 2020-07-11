from unittest import TestCase
from nose2.tools import params

import scheduler.util as sutil
import scheduler.json_backend as json_backend

from util import sort_by_name
from test_data import UtilTestData as test_data


class UtilTest(TestCase):
    """
    Tests for util functions
    """

    get_day_info_from_member_test_data = test_data.get_day_info_from_member_test_data
    get_drivers_test_data = test_data.get_drivers_test_data
    get_riders_test_data = test_data.get_riders_test_data
    filter_dues_payers_test_data = test_data.filter_dues_payers_test_data

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
