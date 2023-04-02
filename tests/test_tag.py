import os
import pytest

from medium_api import Medium

medium = Medium(os.getenv('RAPIDAPI_KEY'))

tag = 'blockchain'

def test_related_tags():
    related_tags = medium.related_tags(given_tag=tag)

    assert isinstance(related_tags, list)
    assert isinstance(related_tags[0], str)

def test_tag_info():
    tag_info = medium.tag_info(tag=tag)

    assert isinstance(tag_info, dict)

    assert isinstance(tag_info['tag'], str)
    assert isinstance(tag_info['name'], str)
    assert isinstance(tag_info['articles_count'], int)
    assert isinstance(tag_info['latest_articles_count'], int)
    assert isinstance(tag_info['latest_authors_count'], int)
    assert isinstance(tag_info['authors_count'], int)

