import os
import pytest

from src.synchronizator import Synchronizator
from src.utils import logger


def test_synchronizator(test_dirs):
    source, replica = test_dirs
    Synchronizator(source, replica)

def test_synchronizator_replica_not_exist(test_dirs2):
    source, replica, tmp_path = test_dirs2
    Synchronizator(source, replica)
    assert tmp_path.is_dir()

@pytest.mark.parametrize('source, replica',[('same_dir','same_dir'),
                                            ('not_exist','holder')])
def test_synchronizator_improper(source, replica):
    with pytest.raises( (ValueError, FileNotFoundError), match=r"source_dir and replica_dir cannot be the same|"
                                                               r"(\w|\W)+ does not exist\Z"):
        Synchronizator(source, replica)

def test_synchronizator_work(test_dirs3):
    source, replica, tmp_path = test_dirs3
    Synchronizator(source, replica)()
    source_files = []
    source_folders = []
    for root, dirs, files in os.walk(source):
        for f in files:
            source_files.append(os.path.relpath(os.path.join(root, f), source))
        for d in dirs:
            source_folders.append(os.path.relpath(os.path.join(root, d), source))

    for root, dirs, files in os.walk(replica):
        for f in files:
            tr = os.path.relpath(os.path.join(root, f), replica)
            try:
                source_files.remove(tr)
            except ValueError:
                logger.error(f"Can't remove {tr} from file list")
        for d in dirs:
            tr = os.path.relpath(os.path.join(root, d), replica)
            try:
                source_folders.remove(tr)
            except ValueError:
                logger.error(f"Can't remove {tr} from empty catalog list")

    assert len(source_files) == 0
    assert len(source_folders) == 0
