# pylint: disable=missing-docstring
import logging
from logging.config import dictConfig

LOGGING_CONFIG = dict(
    version=1,
    formatters={
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
        },
    loggers={
        '': {'handlers': ['h'],
             'level': logging.DEBUG}
        }
    )

dictConfig(LOGGING_CONFIG)
