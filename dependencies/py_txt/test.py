import unittest
from dependencies.repo import Repo
from dependencies.py_txt.scrape import ScrapePyTxtDeps


class TestScrape(unittest.TestCase):

    expected_deps = [
        'Cerberus',
        'Events',
        'Flask',
        'itsdangerous',
        'Jinja2',
        'MarkupSafe',
        'pymongo',
        'simplejson',
        'Werkzeug',
        'backport_collections'
    ]

    def test_requirementstxt(self):
        with Repo('https://github.com/pyeve/eve.git') as repo:
            scraper = ScrapePyTxtDeps()
            deps = scraper.scrape(repo.dir_name)

        dep_names = []
        for dep in deps:
            dep_names.append(dep['name'])

        for dep in self.expected_deps:
            self.assertIn(dep, dep_names)

if __name__ == '__main__':
    unittest.main()