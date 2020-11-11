import logging
import asyncio
from logging.config import dictConfig

loggerDictConfig = {
  "formatters": {
    "detailed": {
      "class": "logging.Formatter",
      "datefmt": "%m/%d/%Y %I:%M:%S",
      "format": "[%(asctime)s] %(relativeCreated)dms : %(name)s : %(levelname)s : %(message)s"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "formatter": "detailed",
      "level": "DEBUG"
    }
  },
  "root": {
    "handlers": [
      "console"
    ],
    "level": "DEBUG"
  },
  "version": 1
}

dictConfig(loggerDictConfig)


class AsyncLogger:
    """
    because default logger is blocked I/O
    """
    Executor = None

    def __init__(self, name):
        self.logger = logging.getLogger(name)

    async def run(self, msg, type_):
        loop = asyncio.get_running_loop()
        loop.run_in_executor(self.Executor, getattr(self.logger, type_), msg)

    async def debug(self, msg):
        await self.run(msg, 'debug')

    async def info(self, msg):
        await self.run(msg, 'info')

    async def error(self, msg):
        await self.run(msg, 'error')

    async def critical(self, msg):
        await self.run(msg, 'critical')
