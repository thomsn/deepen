import requests
from bs4 import BeautifulSoup


def extract_version(text):
    tokens = text.split()
    for token in tokens:
        if '.' in token and 0 < token.index('.') < len(token) - 1 and len(token) >= 3:
            return token.replace('¶', '').strip()


def scrape(url):
    versions = []
    tree = BeautifulSoup(requests.get(url).content, 'lxml')
    # find a heading with a version inside its text.  #.#.#
    for level in range(1,6):
        headings = tree.find_all('h{}'.format(level))
        for heading in headings:
            version = extract_version(heading.text)
            if version:
                notes = []
                for sibling in heading.find_next_siblings():
                    if sibling.name == 'ul':
                        for note in sibling.find_all('li'):
                            note = note.text
                            if note and len(note):
                                lower_note = note.lower()
                                bug = False
                                if 'bug' in lower_note or 'fix' in lower_note:
                                    bug = True
                                notes.append({'text': note, 'bug': bug})
                    # parse each list item as a note.
                versions.append({'name': version, 'notes': notes})
    return versions

