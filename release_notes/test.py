import unittest

from release_notes.scrape import extract_version


class TestVersionScrape(unittest.TestCase):

    test_strings = [
        ('Version 1.2.3', '1.2.3'),
        ('Version 2.3', '2.3'),
        ('Version 3.a', '3.a'),
        ('Nice Daty today. Version 3.67765', '3.67765')
    ]

    def test_version_scrape(self):
        for version in self.test_strings:
            self.assertEqual(extract_version(version[0]), version[1])

if __name__ == '__main__':
    unittest.main()