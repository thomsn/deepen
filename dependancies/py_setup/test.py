import unittest

from dependancies.py_setup.scrape import ScrapePySetupDeps
from dependancies.repo import Repo


class TestScrape(unittest.TestCase):
    expected_deps1 = [
        'pytz',
        'bcrypt',
        'argon2-cffi'
    ]

    def test_PySetup(self):
        with Repo('https://github.com/twilio/twilio-python.git') as repo:
            scraper = ScrapePySetupDeps()
            deps = scraper.scrape(repo.dir_name)

        dep_names = []
        for dep in deps:
            dep_names.append(dep['name'])

        for dep in self.expected_deps1:
            self.assertIn(dep, dep_names)

    expected_deps2 = [
        'Werkzeug',
        'Jinja2',
        'itsdangerous',
        'click',
        'blinker',
        'greenlet',
        'pytest',
        'coverage',
        'tox',
        'sphinx',
        'sphinxcontrib-log-cabinet'
    ]

    def test_PySetup2(self):
        with Repo('https://github.com/pallets/flask.git') as repo:
            scraper = ScrapePySetupDeps()
            deps = scraper.scrape(repo.dir_name)

        dep_names = []
        for dep in deps:
            dep_names.append(dep['name'])

        for dep in self.expected_deps2:
            self.assertIn(dep, dep_names)


if __name__ == '__main__':
    unittest.main()