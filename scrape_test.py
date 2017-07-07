import unittest
from scrape import scrape

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

    def test_eve(self):
        deps = scrape('https://github.com/pyeve/eve.git')
        for dep in self.expected_deps:
            self.assertIn(dep, deps)


if __name__ == '__main__':
    unittest.main()