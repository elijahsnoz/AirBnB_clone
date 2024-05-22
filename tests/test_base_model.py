#!/usr/bin/python3
"""
A module that contains the test suite for the BaseModel class
"""
import unittest
import json  # Import the json module
from time import sleep
from datetime import datetime, timezone, timedelta
from uuid import uuid4

import models
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """
    The test suite for models.base_model.BaseModel
    """

    # Your test cases...

    def test_to_dict_to_json(self):
        """
        Checks that to_dict() returns a JSON-serializable dictionary
        """
        b = BaseModel()
        self.assertEqual(type(b.to_dict()), dict)
        try:
            json.dumps(b.to_dict())
        except Exception as e:
            self.fail("to_dict() method failed to produce JSON-serializable dictionary")

    # Your other test cases...

if __name__ == "__main__":
    unittest.main()
