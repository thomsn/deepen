from bs4 import BeautifulSoup
import re

def extract_version(text):
    tokens = text.split()
    for token in tokens:
        if '.' in token and 0 < token.index('.') < len(token) - 1 and len(token) >= 3:
            return token.replace('¶', '').strip()


def scrape(html_txt):
    versions = []
    tree = BeautifulSoup(html_txt)
    # find a heading with a version inside its text.  #.#.#
    for level in range(1,6):
        headings = tree.find_all('h{}'.format(level))
        for heading in headings:
            version = extract_version(heading.text)
            if version:
                notes = []
                # search the heading's siblings for a list.
                print(heading)
                for sibling in heading.find_next_siblings():
                    if sibling.name == 'ul':
                        for note in sibling.find_all('li'):
                            notes.append(note.text)
                    # parse each list item as a note.
                versions.append({'name': version, 'notes': notes})
    return versions



if __name__ == '__main__':
    import requests
    resp = requests.get('http://flask.pocoo.org/docs/0.12/changelog/')
    print(scrape(resp.content))