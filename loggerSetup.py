import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import os


class Logger:
    def __init__(self, name: str, log_dir: str = "logs/", max_bytes: int = 5 * 1024 * 1024, backup_count: int = 3):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Generate a log file name with the current date and time
        current_time = datetime.now().strftime("%Y-%m-%d_%H")
        log_file = f"{log_dir}/{current_time}.log"

        self.logger = logging.getLogger(current_time)
        self.logger.setLevel(logging.DEBUG)  # Set the minimum log level

        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Log level for the console

        # Create a file handler with rotation
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count
        )
        file_handler.setLevel(logging.DEBUG)  # Log level for the file

        # Define the log message format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """
        Returns the configured logger instance.

        :return: A logging.Logger instance.
        """
        return self.logger

logger = Logger("MyAppLogger").get_logger()
