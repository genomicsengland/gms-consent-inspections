# creates the loggers and handlers
# console and file handlers
# file handler is a timed rotating handler (currently rotating each day) and keeping backups
import logging
import logging.config
import logging.handlers

def setupLogger():
    """set up logging handlers and formatters"""
    d = {
        'version': 1,
        'formatters': {
            'fFormatter': {
                'class': 'logging.Formatter',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'cFormatter': {
                'class': 'logging.Formatter',
                'format': '%(name)s - %(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'consoleHandler': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'cFormatter'
            },
            'fileHandler': {
                'class': 'logging.handlers.TimedRotatingFileHandler',
                'filename': 'log/ngis-mq.log',
                'formatter': 'fFormatter',
                'when': 'd',
                'interval': 1,
                'backupCount': 7
            }
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['consoleHandler', 'fileHandler']
        }
    }
    logging.config.dictConfig(d)

setupLogger()
