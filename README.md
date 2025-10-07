# Arsenal FC Fixtures Scraper Bot

A Python Telegram bot that scrapes Arsenal FC fixtures from their official website and sends updates via Telegram.

## Features

- 🔍 Scrapes Arsenal FC fixtures from the official website
- 📱 Sends formatted updates via Telegram
- ⚽ Filters fixtures by venue (Emirates Stadium)
- 📅 Highlights today's matches
- 🔔 Interactive bot commands

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) for fast dependency management

> **Note:** This project uses only `pyproject.toml` with `uv` - no separate requirements.txt files needed!

## Getting Started

### Installation

1. Install `uv` if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone the repository and navigate to it:
```bash
cd games.scraper.bot.ts
```

3. Create a virtual environment and install dependencies:
```bash
uv sync --all-extras
```

This will automatically create a virtual environment and install all dependencies from `pyproject.toml`.

### Configuration

Set up the following environment variables (you can use a `.envrc` file or export them):

```bash
export ARSENAL_GAMES_TELEGRAM_BOT_TOKEN="your_bot_token_here"
export ARSENAL_GAMES_TELEGRAM_BOT_CHAT_ID="your_chat_id_here"
```

To get a bot token:
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the token provided

## Usage

### Run the scraper once

```bash
python src/main.py
```

### Run the interactive bot

```bash
python -m src.bot
```

The bot supports the following commands:
- `/start` - Triggers a fixtures scrape and sends results

## Development

### Run tests

```bash
pytest tests/ -v
```

### Run tests with coverage

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Linting

```bash
# Check for issues
ruff check src tests

# Auto-fix issues
ruff check --fix src tests
```

### Formatting

```bash
# Check formatting
ruff format --check src tests

# Format code
ruff format src tests
```

## Project Structure

```
.
├── src/
│   ├── __init__.py
│   ├── bot.py             # Telegram bot integration
│   ├── config.py          # Configuration and environment variables
│   ├── date_utils.py      # Date parsing and formatting utilities
│   ├── domain.py          # Data models
│   ├── format.py          # Telegram message formatting
│   ├── logger.py          # Logging configuration
│   ├── main.py            # Main entry point
│   └── scrape.py          # Web scraping logic
├── tests/
│   ├── test_date.py       # Date utilities tests
│   └── test_format.py     # Formatting tests
├── pyproject.toml         # Project dependencies and configuration
└── README.md
```

## CI/CD

The project uses GitHub Actions for continuous integration:
- Runs tests on Python 3.11 and 3.12
- Checks code formatting with `ruff`
- Runs linting checks
- Generates coverage reports

## License

ISC

## Author

Pavel (pavel@p3ld3v.dev)
