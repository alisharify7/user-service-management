import logging
import sys
from typing import Optional

from aiologger import Logger
from aiologger.formatters.base import Formatter
from aiologger.handlers.files import AsyncTimedRotatingFileHandler, RolloverInterval
from aiologger.handlers.streams import AsyncStreamHandler


async def get_async_logger(
    log_level: int,
    logger_name: str = "user-service",
    log_file: Optional[str] = None,
    rotation: RolloverInterval = RolloverInterval.MIDNIGHT,
    backup_count: int = 7,
    encoding: str = "utf-8",
) -> Logger:
    """
    Create an advanced asynchronous logger with optional file rotation.

    Args:
        log_level: Logging level (e.g., logging.INFO, logging.DEBUG)
        logger_name: Name for the logger (default: "user-service")
        log_file: Path to log file (optional)
        rotation: When to rotate logs ('S', 'M', 'H', 'D', 'midnight', or W0-W6)
        backup_count: Number of backup files to keep
        encoding: File encoding (default: utf-8)

    Returns:
        Configured async Logger instance
    """
    log_level = log_level or logging.DEBUG
    log_format = f"[{logger_name}" + "- %(levelname)s] [%(asctime)s] - %(message)s"
    formatter = Formatter(log_format)

    handlers = [
        AsyncStreamHandler(stream=sys.stdout, level=log_level, formatter=formatter)
    ]

    if log_file:
        rotation_handler = AsyncTimedRotatingFileHandler(
            filename=log_file,
            when=rotation,
            interval=1,
            backup_count=backup_count,
            encoding=encoding,
        )
        rotation_handler.formatter = formatter
        handlers.append(rotation_handler)

    logger = Logger(
        name=logger_name,
        level=log_level,
    )

    for handler in handlers:
        logger.add_handler(handler)

    return logger
