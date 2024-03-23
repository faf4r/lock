
from loguru import logger

logger.add(
    'log.log',
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}",
    level="INFO",
)


class Controller:
    NotImplemented
