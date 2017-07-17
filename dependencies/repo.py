import os
import shutil
from git import Repo as gitRepo
import logging
from django.core.validators import URLValidator
from urllib.parse import urlparse

from dependencies import EntryException


class Repo():
    dir_name = 'temp_repo'
    def __init__(self, url):
        self.url = url

    def __enter__(self):
        os.makedirs(self.dir_name)
        try:
            gitRepo.clone_from('https://open:source@{}'.format(self.url), self.dir_name, depth=1, branch='master')
        except Exception as e:
            shutil.rmtree(self.dir_name)
            logging.info(str(e))
            raise EntryException('Unable to access repository')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.dir_name)
