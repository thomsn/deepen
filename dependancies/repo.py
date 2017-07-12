import os
import shutil
import git


class Repo():
    dir_name = 'temp_repo'
    def __init__(self, url):
        os.makedirs(self.dir_name)
        git.Git().clone(url, self.dir_name, depth=1)

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.dir_name)
