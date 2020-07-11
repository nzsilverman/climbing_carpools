from unittest import TestCase
from nose2.tools import params

from util import sort_by_name
from test_data import JsonBackendTestData as test_data

import scheduler.json_backend as json_backend


class JsonBackendTest(TestCase):
    """
    Test JSON backend
    """

    backend_test_data = test_data.backend_test_data

    @params(backend_test_data[0], backend_test_data[1])
    def test_backend(self, filename, rider_count, driver_count, rider_names,
                     driver_names):
        riders, drivers = json_backend.members_from_json(filename)

        self.assertEqual(len(riders), rider_count)
        self.assertEqual(len(drivers), driver_count)

        rider_names.sort()
        driver_names.sort()

        for rider, check in zip(sort_by_name(riders), rider_names):
            self.assertEqual(rider["name"], check)

        for driver, check in zip(sort_by_name(drivers), driver_names):
            self.assertEqual(driver["name"], check)
