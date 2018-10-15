import logging
from os import path
from os import remove
import lib.config as config
import json

fh_logger = logging.getLogger("FileHandler")


class FileHandler:

    def __init__(self, filename=config.filename):
        self.filename = filename

    def clean_up_file(self):
        try:
            remove(self.filename)
            fh_logger.info('Removed file {}'.format(self.filename))
            return True
        except Exception:
            fh_logger.warn('Couldn\'t remove file {}'.format(self.filename))
            return False

    def file_exists(self):
        return path.exists(self.filename)

    def write_json_to_file(self, j):
        json_as_str = json.dumps(j)
        with open(self.filename, mode='w') as a_file:
            a_file.write(json_as_str)
            a_file.close()
            fh_logger.info("Successfully written json:{} to file".format(
                json_as_str))
            return True
        return False

    def read_json_from_file(self):
        try:
            with open(self.filename) as a_file:
                content = a_file.read()
                a_file.close()
        except FileNotFoundError:
            fh_logger.error(
                'File {} does not exist.\n Exiting...'.format(self.filename))
            raise
        return json.loads(content)
