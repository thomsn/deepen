from dependencies.repo import Repo
from dependencies.py_txt.scrape import ScrapePyTxtDeps
from dependencies.py_setup.scrape import ScrapePySetupDeps


def get_deps(url):
    with Repo(url) as repo:
        scrapers = [ScrapePyTxtDeps(), ScrapePySetupDeps()]
        for scraper in scrapers:
            if scraper.check(repo.dir_name):   # only handles one type at a time atm.
                return scraper.scrape(repo.dir_name)
    return []