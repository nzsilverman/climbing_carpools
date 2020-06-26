"""
Backend tests
"""

from unittest import TestCase
from nose2.tools import params

from util import sort_by_name

import scheduler.json_backend as json_backend

test_path_prefix = "scheduler/testframe/json/"


class JsonBackendTest(TestCase):

    backend_test_data = [
        (test_path_prefix + "simple_test.json", 2, 0, ["Roberts", "Suzy"], []),
        (test_path_prefix + "test.json", 3, 1, ["Roberts", "Bob", "Jon"], ["Suzy"]),
    ]

    @params(backend_test_data[0], backend_test_data[1])
    def test_backend(
        self, filename, rider_count, driver_count, rider_names, driver_names
    ):
        riders, drivers = json_backend.members_from_json(filename)

        self.assertEqual(len(riders), rider_count)
        self.assertEqual(len(drivers), driver_count)

        rider_names.sort()
        driver_names.sort()

        for rider, check in zip(sort_by_name(riders), rider_names):
            self.assertEqual(rider["name"], check)

        for driver, check in zip(sort_by_name(drivers), driver_names):
            self.assertEqual(driver["name"], check)
