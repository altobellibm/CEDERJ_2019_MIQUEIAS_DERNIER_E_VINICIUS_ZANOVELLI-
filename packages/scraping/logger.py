import os
import logging

__all__ = ['VerboseLogger', 'LOG_FILE_EXTENSION']

LOG_FILE_EXTENSION = '.log'


class ContextualLogger(object):
    # logs formatting
    __LOG_FORMAT = '%(asctime)s;%(levelname)s;%(message)s'
    __LOG_DT_FORMAT = "%Y-%m-%d %H:%M:%S"

    # overwriting constructor to return a logging instance
    def __new__(cls, context, path, charset, level=logging.INFO):
        log_file = os.path.abspath(os.path.join(path, context + LOG_FILE_EXTENSION))
        log_format = logging.Formatter(cls.__LOG_FORMAT, cls.__LOG_DT_FORMAT)

        # get logging handler and set logs format
        handler = logging.FileHandler(log_file, 'a', charset)
        handler.setFormatter(log_format)

        # get, configure and return context logger
        logger = logging.getLogger(context)
        logger.addHandler(handler)
        logger.setLevel(level)
        return logger


class VerboseLogger(object):

    def __init__(self, context, path, charset, verbose, debug):
        level = logging.DEBUG if debug else logging.INFO
        self.__logger = ContextualLogger(context, path, charset, level)
        self.__verbose = verbose
        self.__debug = debug
        pass

    def log(self, message, level='info'):
        level = level.lower()

        # encode semicolons (used in format to make logs filterable)
        message = message.replace(';', '%3B')

        # expose only logging methods of interest
        if level in ['debug', 'info', 'warning', 'error', 'critical']:
            if level != 'debug' or (level == 'debug' and self.__debug):

                # forward the call to the actual logging instance
                if hasattr(self.__logger, level):
                    logger = getattr(self.__logger, level)
                    logger(message)

                # produce the verbose
                if self.__verbose:
                    print('[' + level.upper() + '] ' + message)
