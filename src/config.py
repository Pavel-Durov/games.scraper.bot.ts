"""Configuration module for environment variables."""

import os

TELEGRAM_BOT_TOKEN = os.environ.get("ARSENAL_GAMES_TELEGRAM_BOT_TOKEN", "")
TELEGRAM_BOT_CHAT_ID = os.environ.get("ARSENAL_GAMES_TELEGRAM_BOT_CHAT_ID", "")

LOG_LEVEL = "DEBUG"
