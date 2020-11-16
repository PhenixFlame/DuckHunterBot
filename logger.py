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
    _loop = None

    def __init__(self, name):
        logger = logging.getLogger('AsyncLogger')
        with fs.log_errors(logger):
            if isinstance(name, str):
                self.logger = logging.getLogger(name)
            elif isinstance(name, logging.Logger):
                self.logger = name
            elif isinstance(name, AsyncLogger):
                self.logger = name.logger
            else:
                raise TypeError('name must be Logger or str')

    @property
    def loop(self):
        if self._loop is None:
            self._loop = asyncio.get_running_loop()
        return self._loop

    def threadrun(self, msg, type_):
        self.loop.run_in_executor(self.Executor, getattr(self.logger, type_), msg)

    def debug(self, msg):
        self.threadrun(msg, 'debug')

    def info(self, msg):
        self.threadrun(msg, 'info')

    def error(self, msg):
        self.threadrun(msg, 'error')

    def critical(self, msg):
        self.threadrun(msg, 'critical')

    def getChild(self, name):
        return AsyncLogger(self.logger.getChild(name))

    def __repr__(self):
        return str(self.logger).replace('Logger', type(self).__name__)



