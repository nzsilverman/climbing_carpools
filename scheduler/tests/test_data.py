class JsonBackendTestData:
    """
    Data for the JsonBackendTest
    """

    test_path_prefix = "scheduler/tests/json/"

    get_drivers_test_data = [(
        [
            {
                "name": "d1",
                "is_driver": True
            },
            {
                "name": "r1",
                "is_driver": False
            },
            {
                "name": "d2",
                "is_driver": True
            },
        ],
        2,
    )]

    get_riders_test_data = [(
        [
            {
                "name": "d1",
                "is_driver": True
            },
            {
                "name": "r1",
                "is_driver": False
            },
            {
                "name": "d2",
                "is_driver": True
            },
        ],
        1,
    )]

    backend_test_data = [
        (test_path_prefix + "simple_test.json", 2, 0, ["Roberts", "Suzy"], []),
        (test_path_prefix + "test.json", 3, 1, ["Roberts", "Bob",
                                                "Jon"], ["Suzy"]),
    ]


class GenerateRidesTestData:
    """
    Data for the GenerateRidesTest
    """

    get_total_seats_test_data = [
        (
            [
                {
                    "seats": 4,
                    "days": [{
                        "day": "FRIDAY"
                    }]
                },
                {
                    "seats": 3,
                    "days": [{
                        "day": "TUESDAY"
                    }]
                },
                {
                    "seats": 2,
                    "days": [{
                        "day": "MONDAY"
                    }]
                },
                {
                    "seats": 1,
                    "days": [{
                        "day": "TUESDAY"
                    }]
                },
            ],
            "TUESDAY",
            4,
        ),
        ([{
            "seats": 0,
            "days": [{
                "day": "MONDAY"
            }]
        }], "MONDAY", 0),
    ]

    check_in_days_test_data = [
        ({
            "days": [{
                "day": "MONDAY"
            }]
        }, "MONDAY", True),
        ({
            "days": [{
                "day": "MONDAY"
            }]
        }, "TUESDAY", False),
    ]

    are_location_compatible_test_data = [
        (
            {
                "name": "a",
                "days": [{
                    "day": "MONDAY",
                    "locations": ["NORTH"]
                }]
            },
            {
                "name": "b",
                "days": [{
                    "day": "MONDAY",
                    "locations": ["NORTH", "CENTRAL"]
                }],
            },
            "MONDAY",
            True,
        ),
        (
            {
                "name": "a",
                "days": [{
                    "day": "MONDAY",
                    "locations": ["NORTH"]
                }]
            },
            {
                "name": "b",
                "days": [{
                    "day": "MONDAY",
                    "locations": ["CENTRAL"]
                }]
            },
            "MONDAY",
            False,
        ),
        (
            {
                "name": "a",
                "days": [{
                    "day": "MONDAY",
                    "locations": ["NORTH"]
                }]
            },
            {
                "name": "b",
                "days": [{
                    "day": "TUESDAY",
                    "locations": ["NORTH"]
                }]
            },
            "TUESDAY",
            False,
        ),
    ]

    time_compatibility_test_data = [
        (
            {
                "days": [{
                    "day": "MONDAY",
                    "departure_times": [1, 2, 3, 4]
                }]
            },
            {
                "days": [{
                    "day": "MONDAY",
                    "departure_times": [4]
                }]
            },
            "MONDAY",
            4,
        ),
        (
            {
                "days": [{
                    "day": "TUESDAY",
                    "departure_times": [1, 2, 3, 4]
                }]
            },
            {
                "days": [{
                    "day": "TUESDAY",
                    "departure_times": [8]
                }]
            },
            "TUESDAY",
            -1,
        ),
        (
            {
                "days": [{
                    "day": "MONDAY",
                    "departure_times": [1.5, 2, 3, 4]
                }]
            },
            {
                "days": [{
                    "day": "MONDAY",
                    "departure_times": [0]
                }]
            },
            "MONDAY",
            -1,
        ),
    ]

    find_best_match_test_data = [
        (
            {
                "name":
                    "r",
                "days": [{
                    "day": "TUESDAY",
                    "locations": ["NORTH"],
                    "departure_times": [1, 2, 3],
                }],
            },
            [
                {
                    "name":
                        "a",
                    "seats":
                        3,
                    "seats_remaining":
                        3,
                    "days": [{
                        "day": "MONDAY",
                        "locations": ["CENTRAL", "NORTH"],
                        "departure_times": [0],
                    }],
                },
                {
                    "name":
                        "b",
                    "seats":
                        0,
                    "seats_remaining":
                        0,
                    "days": [{
                        "day": "MONDAY",
                        "locations": ["CENTRAL", "NORTH"],
                        "departure_times": [0],
                    }],
                },
                {
                    "name":
                        "c",
                    "seats":
                        4,
                    "seats_remaining":
                        4,
                    "days": [{
                        "day": "MONDAY",
                        "locations": ["NORTH"],
                        "departure_times": [8],
                    }],
                },
                {
                    "name":
                        "d",
                    "seats":
                        4,
                    "seats_remaining":
                        4,
                    "days": [{
                        "day": "TUESDAY",
                        "locations": ["NORTH"],
                        "departure_times": [2],
                    }],
                },
            ],
            "TUESDAY",
            "d",
        ),
    ]


class UtilTestData:
    """
    Test data for UtilTest
    """
    pass


class WSRangeTestData:
    """
    Test data for WSRangeTest
    """

    ws_range_basic = [
        (4, 4, 4, 6, "D4:F4"),
        (1, 1, 1, 1, "A1:A1"),
        (5, 6, 7, 7, "E6:G7"),
    ]


class WSCellTestData:
    """
    Test data for WSCellTest
    """

    ws_basic_test = [(2, 3, 2, 3), (1, 2, 1, 2)]

    column_increment_test_data = [(4, 5, 5, 10), (1, 2, -1, 1)]

    row_increment_test_data = [(4, 5, 5, 9), (1, 2, -1, 0)]

    get_a1_test_data = [(4, 5, "E4")]
