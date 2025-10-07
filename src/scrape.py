"""Web scraping module for Arsenal fixtures."""

import sys
from datetime import UTC, datetime
from http import HTTPStatus

import requests
from bs4 import BeautifulSoup

from bot import send_rich_text
from date_utils import parse_date
from domain import Fixture, FixturesUpdate
from format import fixtures_to_rich_text
from logger import init_log

logger = init_log("main")

URL = (
    "https://www.arsenal.com/fixtures"
    "?field_arsenal_team_target_id=All"
    "&field_competition_target_id=All"
    "&field_home_away_or_neutral_value=All"
    "&field_tv_channel_target_id=All"
    "&revision_information="
)

VENUE = "Emirates Stadium"


def parse_fixtures(content: str) -> list[Fixture]:
    """Parse HTML content to extract fixtures.

    Args:
        content: HTML content from Arsenal website

    Returns:
        List of parsed fixtures
    """
    result: list[Fixture] = []
    soup = BeautifulSoup(content, "html.parser")

    cards = soup.find_all(class_="fixture-card")
    for card in cards:
        headers = card.find_all(class_="card__header")
        fixture = None

        for header in headers:
            date_elem = header.find(class_="event-info__date")
            venue_elem = header.find(class_="event-info__venue")
            extra_elem = header.find(class_="event-info__extra")

            date_text = date_elem.get_text(strip=True) if date_elem else ""
            venue_text = venue_elem.get_text(strip=True) if venue_elem else ""
            extra_text = extra_elem.get_text(strip=True) if extra_elem else ""

            fixture = {
                "date": parse_date(date_text) if date_text else datetime.now(UTC),
                "venue": venue_text,
                "league": extra_text,
                "home_team": None,
                "away_team": None,
            }

        # If no headers found, create a default fixture
        if fixture is None:
            fixture = {
                "date": datetime.now(UTC),
                "venue": "",
                "league": "",
                "home_team": None,
                "away_team": None,
            }

        contents = card.find_all(class_="team-crest__name-value")

        if len(contents) > 0:
            fixture["home_team"] = contents[0].get_text(strip=True)
        if len(contents) > 1:
            fixture["away_team"] = contents[1].get_text(strip=True)

        if fixture:
            result.append(
                Fixture(
                    date=fixture["date"],
                    venue=fixture["venue"],
                    league=fixture["league"],
                    home_team=fixture["home_team"],
                    away_team=fixture["away_team"],
                )
            )

    return result


async def scrape_arsenal_fixtures(chat_id: str | None = None):
    """Scrape Arsenal fixtures and send to Telegram.

    Args:
        chat_id: Optional Telegram chat ID to send message to

    Note:
        Uses synchronous requests in an async function due to httpx SSL/TLS issues.
        This is acceptable for this use case as the function is short-lived.
    """
    now = datetime.now(UTC)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        logger.info("Fetching fixtures from %s", URL)
        response = requests.get(URL, headers=headers, timeout=30.0)

        if response.status_code == HTTPStatus.OK:
            fixtures = parse_fixtures(response.text)
            update = FixturesUpdate(
                date=now,
                venue=VENUE,
                fixtures=[f for f in fixtures if f.venue == VENUE and f.date > now],
                source=URL,
            )
            message = fixtures_to_rich_text(update, now)
            logger.info(message)
            await send_rich_text(message, chat_id)
        else:
            logger.error("Unable to fetch the page. Status Code: %s", response.status_code)
    except requests.exceptions.ConnectionError as error:
        logger.error(
            "Network connection error: Unable to connect to %s. "
            "Check your internet connection or the website may be down. Error: %s",
            URL,
            error,
        )
    except requests.exceptions.Timeout as error:
        logger.error("Request timed out while fetching %s. Error: %s", URL, error)
    except Exception as error:
        logger.exception("Unexpected error: %s", error)

    logger.info("Process is about to exit.")
    sys.exit(0)
