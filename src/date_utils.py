"""Date parsing and formatting utilities."""

from datetime import datetime

from dateutil import parser


def parse_date(date_string: str) -> datetime:
    """Parse a date string in the format 'EEE MMM d - HH:mm'.

    Args:
        date_string: Date string to parse

    Returns:
        Parsed datetime object
    """
    try:
        # Try to parse with dateutil which is more flexible
        return parser.parse(date_string, fuzzy=True)
    except (ValueError, parser.ParserError):
        # Fallback to current year if parsing fails
        now = datetime.now()
        return datetime.strptime(f"{date_string} {now.year}", "%a %b %d - %H:%M %Y")


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
