"""Tests for date utilities."""

import sys
from datetime import datetime

sys.path.insert(0, "src")

from date_utils import format_date, is_today


def test_format_date():
    """Test date formatting."""
    date = datetime(2023, 11, 16, 15, 40, 0, 980000)
    result = format_date(date)
    assert result == "Thu Nov 16 - 15:40"


def test_is_today_same_date():
    """Test is_today with same date."""
    date1 = datetime(2023, 11, 16, 15, 40, 0, 980000)
    date2 = datetime(2023, 11, 16, 15, 40, 0, 980000)
    assert is_today(date1, date2) is True


def test_is_today_different_date():
    """Test is_today with different dates."""
    date1 = datetime(2023, 11, 16, 15, 40, 0, 980000)
    date2 = datetime(2023, 11, 17, 15, 40, 0, 980000)
    assert is_today(date1, date2) is False
