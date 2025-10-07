"""Telegram bot module."""

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from config import TELEGRAM_BOT_TOKEN
from logger import init_log

logger = init_log("telegram")


async def send_rich_text(rich_text: str, chat_id: str | None, bot_token: str | None = None):
    """Send a rich text message to a Telegram chat.

    Args:
        rich_text: Message text with Markdown formatting
        chat_id: Telegram chat ID to send message to
        bot_token: Optional bot token (defaults to config)
    """
    if not chat_id:
        logger.error("No chatId!")
        return

    token = bot_token or TELEGRAM_BOT_TOKEN
    if not token:
        logger.error("No bot token!")
        return

    try:
        # Create a temporary application just for sending
        app = Application.builder().token(token).build()
        await app.initialize()
        await app.bot.send_message(chat_id=chat_id, text=rich_text, parse_mode="Markdown")
        logger.info(f"[{chat_id}] Message sent")
        await app.shutdown()
    except Exception as e:
        logger.error(f"Error sending message: {e}")


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    chat_id = str(update.effective_chat.id)
    logger.info(f"[{chat_id}] Got start command!")

    # Import here to avoid circular imports
    from scrape import scrape_arsenal_fixtures

    await scrape_arsenal_fixtures(chat_id)


async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo received messages.

    Args:
        update: Telegram update object
        context: Telegram context object
    """
    chat_id = update.effective_chat.id
    message_text = update.message.text
    await context.bot.send_message(chat_id=chat_id, text=f"You said: {message_text}")


def run_bot():
    """Initialize and run the Telegram bot."""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return

    # Create application
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

    logger.info("Bot started polling...")
    # Run the bot
    app.run_polling()
