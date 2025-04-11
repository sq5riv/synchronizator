import sys
import pytest

from src.utils import Utils


def test_custom_args(monkeypatch):
    parser = Utils.argument_parser()
    monkeypatch.setattr('sys.argv', ['program',
                                     '--synchronization-interval', '01:00:10',
                                     '--source-folder', '/path/to/folder',
                                     '--replica-folder', '/path/to/folder',
                                     '--log-file', '/path/to/file'],)
    args = parser.parse_args()
    assert args.synchronization_interval == '01:00:10'
    assert args.source_folder is '/path/to/folder'
    assert args.replica_folder is '/path/to/folder'
    assert args.log_file is '/path/to/file'

def test_set_logger():
    Utils.set_logger('test')

def test_check_path():
    Utils.check_path('./tests/test_utils.py', False)

def test_check_path_incorect():
    with pytest.raises(NotADirectoryError):
        Utils.check_path('./tests/test_utils.py', True)

