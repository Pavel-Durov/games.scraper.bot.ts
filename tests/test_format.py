"""Tests for fixture formatting."""

import sys
from datetime import datetime

sys.path.insert(0, "src")

from domain import Fixture, FixturesUpdate
from format import fixtures_to_rich_text


def test_no_games():
    """Test formatting with no games."""
    update = FixturesUpdate(
        fixtures=[],
        date=datetime(2023, 11, 16, 15, 40, 0, 980000),
        venue="Emirates Stadium",
        source="test.com",
    )
    today = datetime(2022, 11, 12, 15, 40, 0, 980000)
    result = fixtures_to_rich_text(update, today)

    expected = """📟 *Update for Thu Nov 16 - 15:40 (2023)*
*No upcoming games for the year*
"""
    assert result == expected


def test_single_game():
    """Test formatting with a single game."""
    update = FixturesUpdate(
        date=datetime(2023, 11, 16, 15, 40, 0, 980000),
        venue="Emirates Stadium",
        fixtures=[
            Fixture(
                date=datetime(2023, 12, 16, 15, 40, 0, 980000),
                venue="Emirates Stadium",
                league="Premier League",
                home_team="Arsenal",
                away_team="Chelsea",
            )
        ],
        source="test.com",
    )
    today = datetime(2022, 11, 12, 15, 40, 0, 980000)
    result = fixtures_to_rich_text(update, today)

    expected = """📟 *Update for Thu Nov 16 - 15:40 (2023)*
⚽ *2023 games at Emirates Stadium*

*Sat Dec 16 - 15:40* - Arsenal VS Chelsea (Premier League)

📡 [Source](test.com)
"""
    assert result == expected


def test_today_annotation():
    """Test formatting with today annotation."""
    update = FixturesUpdate(
        date=datetime(2022, 11, 12, 15, 40, 0, 980000),
        venue="Emirates Stadium",
        fixtures=[
            Fixture(
                date=datetime(2022, 11, 12, 15, 40, 0, 980000),
                venue="Emirates Stadium",
                league="Premier League",
                home_team="Arsenal",
                away_team="Chelsea",
            ),
            Fixture(
                date=datetime(2022, 11, 16, 15, 40, 0, 980000),
                venue="Emirates Stadium",
                league="Premier League",
                home_team="Arsenal",
                away_team="Tel Aviv",
            ),
        ],
        source="test.com",
    )
    today = datetime(2022, 11, 12, 15, 40, 0, 980000)
    result = fixtures_to_rich_text(update, today)

    expected = """📟 *Update for Sat Nov 12 - 15:40 (2022)*
⚽ *2022 games at Emirates Stadium*

Today 👉 **Sat Nov 12 - 15:40* - Arsenal VS Chelsea (Premier League)
*Wed Nov 16 - 15:40* - Arsenal VS Tel Aviv (Premier League)

📡 [Source](test.com)
"""
    assert result == expected
