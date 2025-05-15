import logging
import sys
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)

    # Create logger
    logger = logging.getLogger('jeopardyze')
    logger.setLevel(logging.INFO)

    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = RotatingFileHandler(
        'logs/jeopardyze.log',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )

    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

logger = setup_logging() 