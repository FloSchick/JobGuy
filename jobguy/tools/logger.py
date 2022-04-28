import logging
import sys
from typing import Optional


def get_logger(
    logger_name: str, level: int, message_format: str, file_path: Optional[str] = None
) -> logging.Logger:
    """Initialize and return a logger
    NOTE: you can use this as a method to add logging to any function, but if
        you want to use this within a class, just inherit Logger class.
    TODO: make more easily configurable w/ defaults
    TODO: streamline
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    formatter = logging.Formatter(message_format)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    if file_path:
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


class Logger:
    """Class that adds a self.logger attribute for stdio and fileio"""

    def __init__(
        self,
        level: int,
        file_path: Optional[str] = None,
        logger_name: Optional[str] = None,
        message_format: Optional[str] = None,
    ) -> None:
        """Add a logger to any class
        Args:
            level (int): logging level, which ought to be an Enum but isn't
            file_path (Optional[str], optional): file path to log messages to.
                NOTE: this logs at the specified log level.
            logger_name (Optional[str], optional): base name for the logger,
                should be unique. Defaults to inherited class name.
            message_format (Optional[str], optional): the formatting of the
                message to log. Defaults to a complete message with all info.
        """
        logger_name = logger_name or self.__class__.__name__
        message_format = message_format or (
            f"[%(asctime)s] [%(levelname)s] {logger_name}: %(message)s"
        )
        self.logger = get_logger(
            logger_name=logger_name,
            level=level,
            file_path=file_path,
            message_format=message_format,
        )
