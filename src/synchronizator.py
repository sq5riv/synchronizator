import hashlib
import os
import shutil
from pathlib import Path

from src.utils import logger, Utils


class Synchronizator:
    """
    Class Synchronizator
    """

    def __init__(self, source_dir: str, replica_dir: str) -> None:
        """
        :param source_dir: source directory, source of truths for replica directory.
        :param replica_dir: replica directory always synchronized to source of true.
        """
        self.source_dir = os.path.abspath(source_dir)
        self.replica_dir = os.path.abspath(replica_dir)
        self.__post_init_()

    def __call__(self) -> None:
        """
        Run directories synchronization.
        """
        logger.info(f'start synchronization round {self.replica_dir} is synchronized to {self.source_dir}')
        self.source_empty, source_files = self.swipe(self.source_dir)
        self.replica_empty, replica_files = self.swipe(self.replica_dir)
        self.source_hash = self._hash_loop(source_files, self.source_dir)
        self.replica_hash = self._hash_loop(replica_files, self.replica_dir)
        logger.info(f'catalog file finished')
        self._delete()
        self._copy()
        logger.info(f'synchronization round finished')

    def __post_init_(self):
        """
        Checks arguments correctness
        """
        if self.source_dir == self.replica_dir:
            raise ValueError("source_dir and replica_dir cannot be the same")
        if not Path(self.source_dir).exists():
            raise FileNotFoundError(f'{self.source_dir} does not exist')
        if not Path(self.replica_dir).exists():
            Path(self.replica_dir).mkdir(parents=True)

    def _hash_loop(self, paths: list[str], path_base: str) -> dict[str, str]:
        """
        Hash given files list.
        :param paths: List of file paths to hash.
        :param path_base: path to directory where relative path starts.
        :return: dictionary of filepath and file hash.
        """
        return {file: self.hash_file(file, path_base) for file in paths}


    def _delete(self) -> None:
        """
        Delete all not existing in source of true files  and empty directories.
        """
        logger.info(f'delete files and folders from {self.replica_dir}')
        for file_path, file_hash in self.replica_hash.items():
            if file_hash not in self.source_hash.values():
                logger.info(f'delete file {file_path}')
                os.remove(file_path)
        empty_dirs, _ = self.swipe(self.replica_dir)
        del_dirs = 1
        while empty_dirs and del_dirs > 0:
            del_dirs = 0
            empty_dirs.reverse()
            for empty_dir in empty_dirs:
                if empty_dir not in self.source_empty:
                    logger.info(f'delete folder {empty_dir}')
                    os.rmdir(empty_dir)
                    del_dirs += 1
            empty_dirs, _ = self.swipe(self.replica_dir)
        logger.info(f'delete finished')

    def _copy(self) -> None:
        """
        Copies all files which exists in source of true directory and does not exist in replica directory.
        :return:
        """
        logger.info(f'copy files from {self.source_dir} to {self.replica_dir}')
        for file_path, file_hash in self.source_hash.items():
            if file_hash not in self.replica_hash.values():
                copy_path = os.path.join(self.replica_dir, os.path.relpath(file_path, self.source_dir))
                logger.info(f'copy file {file_path} to {copy_path}')
                Path(copy_path).parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path,  copy_path)
        for empty_dir in self.source_empty:
            if empty_dir not in self.replica_empty:
                logger.info(f'copy folder {empty_dir} to {empty_dir}')
                copy_path = os.path.relpath(empty_dir, self.source_dir)
                os.makedirs(os.path.join(self.replica_dir, copy_path), exist_ok=True)

    @staticmethod
    def hash_file(path: str, path_base: str, algorithm: str ="md5") -> str:
        """
        Hash file with given path and add relative path to hash result.
        :param path: file path.
        :param path_base: path to directory where relative path starts.
        :param algorithm: hash algorithm.
        :return: File checksum, with relative path added to file.
        """
        logger.info(f'hashing {path}')
        h = hashlib.new(algorithm)
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
            h.update(bytes(os.path.relpath(path, path_base),'utf-8'))
        return h.hexdigest()

    @staticmethod
    def swipe(base_dir: str) -> tuple[list[str], list[str]]:
        """
        Swipe method catalog all files and all empty directories.
        :param base_dir: path to directory to catalog files.
        :return: list of path to empty directories and list of paths to files.
        """
        empty_dirs = []
        filepaths = []
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                rel_path = os.path.abspath(os.path.join(root, file))
                filepaths.append(rel_path)
            if not dirs and not files:
                empty_dirs.append(os.path.abspath(root))
        return empty_dirs, filepaths


def main():
    pass

if __name__ == '__main__':
    main()
