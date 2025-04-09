import hashlib
import os

from pathlib import Path

from utils import logger, Utils




class Synchronizator:

    def __init__(self, source_dir: str, replica_dir: str) -> None:
        self.source_dir = source_dir
        self.replica_dir = replica_dir
        self.__post_init_()

    def __call__(self) -> None:
        source_empty, source_files = self.swipe(self.source_dir)
        replica_empty, replica_files = self.swipe(self.replica_dir)
        self.source_hash = self.hash_file(source_files)
        self.replica_hash = self.hash_file(replica_files)
        self.delete()
        self.copy()

    def __post_init_(self):
        if not Path(self.source_dir).exists():
            raise FileNotFoundError(f'{self.source_dir} does not exist')
        if not Path(self.replica_dir).exists():
            Path(self.replica_dir).mkdir(parents=True)

    def hash_loop(self, paths: list[str]) -> dict[str, str]:
        return {file: self.hash_file(file) for file in paths}


    @staticmethod
    def hash_file(path: str, algorithm: str ="md5") -> str:
        h = hashlib.new(algorithm)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
            h.update(bytes(path, 'utf-8'))
        return h.hexdigest()

    @staticmethod
    def swipe(base_dir: str) -> tuple[list[str], list[str]]:
        empty_dirs = []
        filepaths = []
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                full_path = os.path.join(root, file)
                filepaths.append(os.path.abspath(full_path))
            if not dirs and not files:
                empty_dirs.append(os.path.abspath(root))
        return empty_dirs, filepaths

    def delete(self) -> None:
        pass

    def copy(self) -> None:
        pass



def main():
    args = Utils.argument_parser().parse_args()
    Utils.get_logger(args.log_file)
    logger.info(f"Synchronization interval: {args.synchronization_interval}")



if __name__ == '__main__':
    main()
