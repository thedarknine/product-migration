"""
Logging utilitiy tools
"""
import logging
import os
import sys
from datetime import datetime
from utilities import display

def init_file():
    """Initialize log file for current date"""
    try:
        cwd = os.path.dirname(os.path.abspath(__file__))
        current_date = datetime.now()

        # If directory does not exist, let's create it
        logs_dir = os.path.join(cwd, '../' + os.getenv("LOGS_DIR"))
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # Initialize log file
        log_file = os.path.join(os.getenv("LOGS_DIR"), current_date.strftime('%Y-%m-%d') + '.log')
        log_format = '%(asctime)s [%(levelname)s] %(message)s - %(filename)s / %(funcName)s() \
              (L.%(lineno)d)'
        logging.basicConfig(filename=log_file, level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
                            format=log_format)
    except FileNotFoundError:
        sys.exit(display.alert("Logs could not be initialized (" + repr(Exception) + ")"))
