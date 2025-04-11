import argparse
import logging
from datetime import timedelta
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Utils:

    @staticmethod
    def argument_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(description="Folder synchronization")
        parser.add_argument('-si', '--synchronization-interval', type=str, required=True,
                            help='Synchronization interval in HH:MM:SS format')
        parser.add_argument('-sf', '--source-folder', type=str, required=True,
                            help='Source folder path for one-way synchronization')
        parser.add_argument('-rf', '--replica-folder', type=str, required=True,
                            help='Replica folder path for one-way synchronization')
        parser.add_argument('-lf', '--log-file', type=str, default='None', help='Log file path')

        return parser

    @staticmethod
    def set_logger(path:str) -> None:

        formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # Console gets INFO and above
        console_handler.setFormatter(formatter)

        # File handler
        Utils.check_path(path)
        file_handler = logging.FileHandler(path)  # Logs to app.log
        file_handler.setLevel(logging.DEBUG)  # File gets everything
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)


    @staticmethod
    def check_path(path:str, is_folder: bool = False) -> Path:
        p = Path(path)
        if is_folder:
            if not p.is_dir():
                raise NotADirectoryError
        return p

    @staticmethod
    def time_parser(time: str) -> int:
        try:
            h, m, s = map(int, time.split(":"))
        except ValueError:
            raise argparse.ArgumentTypeError("Invalid time format, --synchronization-interval should be HH:MM:SS format")
        return int(timedelta(hours=h, minutes=m, seconds=s).total_seconds())
