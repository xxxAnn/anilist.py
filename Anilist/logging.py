import logging

class AnilistFormatter(logging.Formatter):

    black = "\x1b[30;20m"
    blue = "\x1b[34;20m"
    green = "\x1b[32;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(asctime)s]: %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: green + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
    
# Singleton
class AnilistLogger:
    _instance = None
    _done = False

    def __init__(self, level = logging.INFO):
        if not AnilistLogger._done:
            logger = logging.getLogger("AnilistLogger")
            logger.setLevel(level)

            ch = logging.StreamHandler()
            ch.setLevel(level)

            ch.setFormatter(AnilistFormatter())

            logger.addHandler(ch)

            self._logger = logger
            AnilistLogger._done = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AnilistLogger, cls).__new__(cls)
        
        return cls._instance

    def __getattr__(self, k):
        return self._logger.__getattribute__(k)