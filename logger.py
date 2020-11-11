import logging
import asyncio
from logging.config import dictConfig
import funcsource as fs
import os

DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
loggerDictConfig = fs.read_file(DIR + 'logger_config.yaml')

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
