import logging
import os
import coloredlogs

from os.path import exists
from logging.handlers import TimedRotatingFileHandler

def baseLogger(log_level: str) -> None:
    """
    Configure logging throughout the application
    
    Arguments:
        log_level: str
    
    Returns:
        None
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError("Invalid log level: %s" % log_level)

    if not exists("logs/"):
        os.makedirs("logs/")

    logging.basicConfig(level=numeric_level)
    logger = logging.getLogger()
    rotatory_handler = TimedRotatingFileHandler(
        "logs/combined.log", when="D", interval=1, backupCount=30
    )
    rotatory_handler.setLevel(logging.INFO)
    coloredlogs.install(level=log_level.upper())
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s", "%m-%d-%Y %H:%M:%S"
    )
    rotatory_handler.setFormatter(formatter)
    logger.addHandler(rotatory_handler)
    logger.info("Log Level: %s" % log_level.upper())