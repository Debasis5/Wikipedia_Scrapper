import os
import logging

class log:
    def __init__(self, log_name):
        # Create logger
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.DEBUG)
        self.log_format = '[%(levelname)s] [%(name)s] %(asctime)s | %(message)s'
        self.formatter = logging.Formatter(self.log_format)
        # Add console handler
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)
        # Add File handler
        self.log_file_name = log_name + '.log'
        self.fh = logging.FileHandler(self.log_file_name)
        self.fh.setLevel(logging.DEBUG)
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    def close_log(self):
        print('Removing all log handlers...')
        # get all loggers
        loggers = [logging.getLogger(name) if 'wikipedia' in name else None for name in logging.root.manager.loggerDict]
        # for each valid logger remove all handlers
        for log in loggers:
            if log != None:
                while bool(len(log.handlers)):
                    for handler in log.handlers:
                        log.removeHandler(handler)

