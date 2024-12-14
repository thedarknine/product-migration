"""
Logging utilitiy tools
"""

import logging
import os
import sys
import arrow
from sources.utilities import display


def init_logger(logs_path: str = os.getenv("LOGS_DIR", "logs")) -> logging.Logger:
    """
    Initialize log file for current date

    Args:
        logs_path (str): Path to logs directory

    Returns:
        logging.Logger: Logger object
    """
    try:
        current_date = arrow.now(os.getenv("TIMEZONE", "Europe/Paris"))

        # If directory does not exist, let's create it
        logs_dir = os.path.join(os.getcwd(), logs_path)
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # Create a logger
        logger = get_logger()
        logger.setLevel(logging.DEBUG)

        # Create a handler and initialize log file
        handler = logging.FileHandler(
            os.path.join(logs_dir, current_date.strftime("%Y-%m-%d") + ".log")
        )
        handler.setLevel(logging.DEBUG)

        # Create a formatter and set it for the handler
        formatter = logging.Formatter(
            os.getenv("LOGS_FORMAT", "%(asctime)s - %(levelname)s - %(message)s")
        )
        handler.setFormatter(formatter)

        # Add the handler to the logger and set its level
        logger.addHandler(handler)
        logger.debug("Logs initialized")

        return get_logger()
    except FileNotFoundError:
        sys.exit(
            display.alert("Logs could not be initialized (" + repr(Exception) + ")")
        )


def get_logger():
    """
    Get logger with defined name

    Returns:
        logging.Logger: Logger object
    """
    return logging.getLogger(os.getenv("LOGS_NAME", "logs"))
