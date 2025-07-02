import pytest
from test import time_format

# Check if the time_format function works correctly

@pytest.mark.parametrize("input_duration, expected_output", [
    ("PT1H4M3S", "1 hours, 4 minutes, 3 seconds"),
]) 
def test_time_format(input_duration, expected_output):
    assert time_format(input_duration) == expected_output