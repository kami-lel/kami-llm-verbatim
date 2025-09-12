"""kamilog: Customized Logging Output Module

This script provides a simple interface to obtain Python loggers with a
customized logging output format. The format includes timestamps and padded
log level names for cleaner, more uniform log display.





Installation as Script:
Copy the single script `./kamilog/kamilog.py` into your project folder.

Example directory structure::

    your_project/
    ├── kamilog.py
    └── main.py

In `main.py`, import the module as follows::

    import kamilog





Installation as Module:
Copy the entire `kamilog` folder into your project's source folder.

Example directory structure::

    your_project/
    ├── project_abc/
    │   ├── kamilog/
    │   │   ├── __init__.py
    │   │   └── kamilog.py
    │   ├── module_a/
    │   │   └── some_code.py
    │   └── module_b/
    │       └── other_code.py
    └── setup.py

Then you can import `kamilog` anywhere within the project like this::

    from project_abc import kamilog





Usage:
Use ``kamilog.getLogger()` (in places of `logging.getLogger()`)
to get a configured logger instance::

    import logging
    import kamilog

    my_logger = kamilog.getLogger("myLogger")
    my_logger.setLevel(logging.DEBUG)

    my_logger.debug("Debugging details here")
    my_logger.info("Informational message")
    my_logger.warning("Warning message")
    my_logger.error("Error occurred!")
    my_logger.critical("Critical issue!")

    try:
        1 / 0
    except ZeroDivisionError as err:
        my_logger.exception(err)

Output::

    [2024-06-15 14:30:00,000] DEBUG: Debugging details here
    [2024-06-15 14:30:00,000] INFO : Informational message
    [2024-06-15 14:30:00,000] WARN : Warning message
    [2024-06-15 14:30:00,001] ERROR: Error occurred!
    [2024-06-15 14:30:00,001] CRIT : Critical issue!
    [2024-06-15 14:30:00,001] ERROR: division by zero
    Traceback (most recent call last):
      File "/home/kami/repos/kami-log-py/example.py", line 18, in <module>
        1 / 0
        ~~^~~
    ZeroDivisionError: division by zero
"""

# todo option to use relative time
# todo option to omit date in time
# todo include logger name in the message

import logging
from logging import Formatter, StreamHandler

__version__ = "1.1.1-alpha"
__author__ = "kamiLeL"
__all__ = ("getLogger",)


MESSAGE_FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"


_PADDED_LEVELNAMES = ("DEBUG", "INFO ", "WARN ", "ERROR", "CRIT ")


def _levelno2padded_levelname(levelno):
    """
    :param levelno:
    :type levelno: int
    :return: padded level name, always 5 letter width
    :rtype: str
    """
    return _PADDED_LEVELNAMES[levelno // 10 - 1]


class _LogFormatter(Formatter):

    def __init__(
        self,
        fmt=MESSAGE_FORMAT,
        datefmt=None,
        style="%",
        validate=True,
        *,
        defaults=None
    ):
        super().__init__(fmt, datefmt, style, validate, defaults=defaults)

    def format(self, record):
        record.levelname = _levelno2padded_levelname(record.levelno)
        return super().format(record)


_INITIALIZED_LOGGERS = []


def getLogger(name=None):
    """
    :param name: logger name
    :type name: str
    :return: a logger with the `name`, create if non-existence;
            root logger if `name` is `None`
    :rtype: logging.Logger
    """
    global _INITIALIZED_LOGGERS

    logger = logging.getLogger(name)

    # no repeated configure/initialize for any loggers
    if name in _INITIALIZED_LOGGERS:
        return logger

    # init loggers  ============================================================
    # console stream handler  --------------------------------------------------
    console_handler = StreamHandler()
    console_formatter = _LogFormatter()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # todo add file handler option

    _INITIALIZED_LOGGERS.append(name)

    return logger
