"""Date parsing and formatting utilities."""

from datetime import UTC, datetime

from dateutil import parser


def parse_date(date_string: str) -> datetime:
    """Parse a date string in the format 'EEE MMM d - HH:mm'.

    Args:
        date_string: Date string to parse

    Returns:
        Parsed datetime object with UTC timezone

    Note:
        Source website doesn't provide timezone info, so we assume UTC for consistency.
        This allows comparison with datetime.now(UTC).
    """
    try:
        # Try to parse with dateutil which is more flexible
        parsed = parser.parse(date_string, fuzzy=True)
        # Make timezone-aware by assuming UTC
        return parsed.replace(tzinfo=UTC)
    except (ValueError, parser.ParserError):
        # Fallback to current year if parsing fails
        now = datetime.now(UTC)
        parsed = datetime.strptime(f"{date_string} {now.year}", "%a %b %d - %H:%M %Y")
        return parsed.replace(tzinfo=UTC)


def format_date(date: datetime) -> str:
    """Format a date as 'EEE MMM d - HH:mm'.

    Args:
        date: Datetime object to format

    Returns:
        Formatted date string
    """
    return date.strftime("%a %b %-d - %H:%M")


def format_date_with_year(date: datetime) -> str:
    """Format a date as 'EEE MMM d - HH:mm (yyyy)'.

    Args:
        date: Datetime object to format

    Returns:
        Formatted date string with year
    """
    return date.strftime("%a %b %-d - %H:%M (%Y)")


def is_today(date: datetime, today: datetime) -> bool:
    """Check if a date is today.

    Args:
        date: Date to check
        today: Reference date to compare against

    Returns:
        True if the date is today, False otherwise
    """
    return date.day == today.day and date.month == today.month and date.year == today.year
