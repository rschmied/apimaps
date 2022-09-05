"fixtures for testing"

import os
import json

import pytest


@pytest.fixture
def test_data():
    "fixture to load test data"

    def _method(filename: str):
        folder_path = os.path.abspath(os.path.dirname(__file__))
        folder = os.path.join(folder_path, "test_data")
        jsonfile = os.path.join(folder, filename)
        with open(jsonfile, encoding="utf-8") as file:
            return json.load(file)

    return _method
