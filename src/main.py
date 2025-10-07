"""Main entry point for the application."""

import asyncio

from config import TELEGRAM_BOT_CHAT_ID
from scrape import scrape_arsenal_fixtures


async def start(chat_id: str | None = None):
    """Start the scraper.

    Args:
        chat_id: Optional Telegram chat ID to send message to
    """
    await scrape_arsenal_fixtures(chat_id)


if __name__ == "__main__":
    asyncio.run(start(TELEGRAM_BOT_CHAT_ID))
