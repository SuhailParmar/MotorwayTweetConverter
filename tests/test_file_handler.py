from pytest import raises
from lib.file_handler import FileHandler


class TestFileHandler:

    fh = FileHandler(filename="tests/test.json")

    def test_read_json_file_not_found(self):
        with raises(FileNotFoundError):
            assert self.fh.read_json_from_file()

    def test_write_json_to_file(self):
        j = {"test": 0}
        assert self.fh.write_json_to_file(j)

    def test_read_json_from_file(self):
        assert self.fh.read_json_from_file() == {"test": 0}

    def test_cleanup(self):
        assert self.fh.clean_up_file()
