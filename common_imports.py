import logging
import sys
import config as cfg
from logging.handlers import TimedRotatingFileHandler

try:
    from colorlog import ColoredFormatter

    FORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | " \
             "%(blue)s%(message)s%(reset)s " \
             "--- %(filename) -2s%(lineno)d"
    CONSOLE_FORMATTER = ColoredFormatter(
        FORMAT,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }
    )
except ImportError:
    # No color available, use default config
    CONSOLE_FORMATTER = logging.Formatter("%(levelname)s: %(message)s")
    color_disabled = True
else:
    color_disabled = False

LOG_FILE = cfg.PATHS["LOGS"]
FILE_FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %("
                                   "levelname)s — %(message)s")


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CONSOLE_FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FILE_FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(
        logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger


def main():
    pass


if __name__ == "__main__":
    main()
