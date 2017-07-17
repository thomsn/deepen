from urllib.parse import urlparse
from django.core.validators import URLValidator
from dependencies import EntryException


def clean_url(url):
    if '@' in url:
        raise EntryException('Deepn does not work with private repositories')
    validator = URLValidator()
    validator(url)
    parsed_url = urlparse(url)
    return "{}{}".format(parsed_url.netloc, parsed_url.path)