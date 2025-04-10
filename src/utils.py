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
        parser.add_argument('--synchronization-interval', type=str, default='00:00:01',
                            help='Synchronization interval in HH:MM:SS format')
        parser.add_argument('--source-folder', type=str, default='None',
                            help='Source folder path for one-way synchronization')
        parser.add_argument('--replica-folder', type=str, default='None',
                            help='Replica folder path for one-way synchronization')
        parser.add_argument('--log-file', type=str, default='None', help='Log file path')

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
        h, m, s = map(int, time.split(":"))
        return int(timedelta(hours=h, minutes=m, seconds=s).total_seconds())
