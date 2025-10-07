"""Fixture formatting utilities for Telegram messages."""

from datetime import datetime

from date_utils import format_date, format_date_with_year, is_today
from domain import Fixture, FixturesUpdate


def get_fixture_line(fixture: Fixture, today: datetime) -> str:
    """Format a single fixture as a line of text.

    Args:
        fixture: Fixture to format
        today: Current date for comparison

    Returns:
        Formatted fixture line
    """
    fdate = format_date(fixture.date)
    result = ""

    if fixture.home_team is None or fixture.away_team is None:
        result = f"*{fdate}* - ({fixture.league})\n"
    elif fixture.away_team is None:
        result = f"*{fdate}* - {fixture.home_team} ({fixture.league})\n"
    else:
        result = f"*{fdate}* - {fixture.home_team} VS {fixture.away_team} ({fixture.league})\n"

    if is_today(fixture.date, today):
        result = f"Today 👉 *{result}"

    return result


def fixtures_to_rich_text(update: FixturesUpdate, today: datetime) -> str:
    """Convert fixtures update object to telegram rich text message.

    Args:
        update: Fixture update object
        today: Current date for comparison

    Returns:
        Formatted telegram rich text message
    """
    result = f"📟 *Update for {format_date_with_year(update.date)}*\n"

    if not update.fixtures or len(update.fixtures) == 0:
        return f"{result}*No upcoming games for the year*\n"

    result += f"⚽ *{update.date.year} games at {update.venue}*\n\n"

    for fixture in update.fixtures:
        result += get_fixture_line(fixture, today)

    result += f"\n📡 [Source]({update.source})\n"

    return result
