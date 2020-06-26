#!/usr/bin/env python3
"""
Testing
"""

import logging
from unittest import TestCase
from nose2.tools import params

import scheduler.json_backend as json_backend

logger = logging.getLogger(__name__)

test_path_prefix = "scheduler/testframe/json/"

class JsonInputTests(TestCase):

    @params((test_path_prefix + "simple_test.json", 2, ["Roberts", "Suzy"]))
    def test_backend(self, filename, member_count, names):
        members = json_backend.members_from_json(filename)[0]
        self.assertTrue(len(members) == member_count)
        for member in members:
            self.assertTrue(member["name"] in names)
    