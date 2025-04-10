import pytest

@pytest.fixture
def test_dirs(tmp_path):
    source = tmp_path / "source"
    replica = tmp_path / "replica"
    source.mkdir()
    replica.mkdir()
    return source, replica

@pytest.fixture
def test_dirs2(tmp_path):
    source = tmp_path / "source"
    replica = tmp_path / "replica"
    source.mkdir()
    return source, replica, tmp_path

@pytest.fixture
def test_dirs3(tmp_path):
    source = tmp_path / "source"
    replica = tmp_path / "replica"
    source.mkdir()
    replica.mkdir()
    (source / "file1.txt").write_text("content of file 1")
    (source / "file2.txt").write_text("content of file 2")
    subfolder = source / "subfolder"
    subfolder.mkdir()
    (subfolder / "file3.txt").write_text("content of file 3")
    subfolder2 = source / "subfolder2"
    subfolder2.mkdir()
    (replica / "empty_folder").mkdir()
    #(replica / "empty_folder2" / "empty_folder3").mkdir()
    (replica / "file3.txt").write_text("content of file 3")
    return source, replica, tmp_path

