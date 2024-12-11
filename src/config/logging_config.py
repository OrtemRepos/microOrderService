import os
import sys

from loguru import logger
from rich.console import Console
from rich.logging import RichHandler

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

logger.remove()
if ENVIRONMENT == "production":
    logger.add(
        sys.stderr,
        level="INFO",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        serialize=True,
    )
    logger.add(
        "logs/app.log",
        level="INFO",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        rotation="10 MB",
        retention="10 days",
        serialize=True,
    )
else:
    console = Console()
    logger.add(
        RichHandler(console=console, markup=True),
        level="DEBUG",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    )
    logger.add(
        "logs/app.log",
        level="DEBUG",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
        rotation="10 MB",
        retention="10 days",
    )
