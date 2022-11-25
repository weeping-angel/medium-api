import os
import pytest

from medium_api import Medium

medium = Medium(os.getenv('RAPIDAPI_KEY'))

tag = 'blockchain'

def test_related_tags():
    related_tags = medium.related_tags(given_tag="blockchain")

    assert isinstance(related_tags, list)
    assert isinstance(related_tags[0], str)

