import sys

from src.utils import Utils

def test_default_args(monkeypatch):
    args = Utils.argument_parser().parse_args([])
    assert args.synchronization_interval == '00:00:01'
    assert args.source_folder is 'None'
    assert args.replica_folder is 'None'
    assert args.log_file is 'None'


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

