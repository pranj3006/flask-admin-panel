""" Logger config"""

import logging
import os
from logging.handlers import RotatingFileHandler

def configure_logging():
    """
    Add logging configurations
    """

    log_file = "./logs/"+os.getenv("LOG_FILE","app.log")

    formatter = logging.Formatter('%s(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(log_file,maxBytes=1024000,backupCount=10)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(stdout_handler)
    