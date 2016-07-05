#!usr/bin/env python
import sys
import logging


# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace(
            "$RESET", RESET_SEQ)
    else:
        message = message.replace("$RESET", "")
    return message

COLORS = {
    'WARNING': 3,
    'INFO': 2,
    'DEBUG': 4,
    'CRITICAL': 1,
    'ERROR': 1
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) \
                + levelname + RESET_SEQ
            msg = COLOR_SEQ % (30 + COLORS[levelname]) \
                + record.msg + RESET_SEQ
            record.levelname = levelname_color
            record.msg = msg
        return logging.Formatter.format(self, record)


def set_logger(loglevel, use_color=True, handler=None):
    logger = logging.getLogger()
    if not handler:
        handler = logging.StreamHandler(sys.stdout)
        FORMAT = "[%(name)s$RESET:%(lineno)d] [%(levelname)s] [%(asctime)s]"\
                 " $RESET>> %(message)s "
    else:
        FORMAT = "[%(name)s$RESET] [%(levelname)s] >> %(message)s "
    if use_color:
        COLOR_FORMAT = formatter_message(FORMAT, True)
        color_formatter = ColoredFormatter(COLOR_FORMAT)
        handler.setFormatter(color_formatter)
    else:
        handler.setFormatter(logging.Formatter(
            formatter_message(FORMAT, False)))
    # ignore requests lib
    logging.getLogger("requests").setLevel(logging.WARNING)
    logger.setLevel(loglevel)
    logger.addHandler(handler)
