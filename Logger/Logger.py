__author__ = 'teddycool'
import time
import datetime
from config import roverconfig

import os
import logging
import sys

LOG_FILENAME = roverconfig["Logger"]["LogFile"]

class Singleton(object):
    """
    Singleton interface:
    http://www.python.org/download/releases/2.2.3/descrintro/#__new__
    """
    def __new__(cls, *args, **kwds):
        it = cls.__dict__.get("__it__")
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwds)
        return it

    def init(self, *args, **kwds):
        pass


class LoggerManager(Singleton):

    """
      Logger Manager.
      Handles all logging files.
      """
    def init(self):
        self.logger = logging.getLogger()
        handler = None
        try:
            handler = logging.FileHandler(LOG_FILENAME, "a")
        except:
            raise IOError("Couldn't create/open file \"" + \
                          LOG_FILENAME + "\". Check permissions.")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.debug(msg)

    def error(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.error(msg)

    def info(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.info(msg)

    def warning(self, loggername, msg):
        self.logger = logging.getLogger(loggername)
        self.logger.warning(msg)


class Logger(object):
    """
    Logger object.
    """
    def __init__(self, loggername="root"):
        self.lm = LoggerManager() # LoggerManager instance
        self.loggername = loggername # logger name

    def debug(self, msg):
        self.lm.debug(self.loggername, msg)

    def error(self, msg):
        self.lm.error(self.loggername, msg)

    def info(self, msg):
        self.lm.info(self.loggername, msg)

    def warning(self, msg):
        self.lm.warning(self.loggername, msg)
