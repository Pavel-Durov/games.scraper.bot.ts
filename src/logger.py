"""Logger configuration module."""

import logging
import sys

from config import LOG_LEVEL


def init_log(label: str) -> logging.Logger:
    """Initialize and configure a logger with the given label.

    Args:
        label: Label to use for the logger

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(label)
    logger.setLevel(getattr(logging, LOG_LEVEL))

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, LOG_LEVEL))

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger
