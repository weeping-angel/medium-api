import os

from medium_api import Medium

medium = Medium(os.getenv('RAPIDAPI_KEY'))

tag = 'self-improvement'

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
    assert isinstance(tag_info['children'], list)
    assert isinstance(tag_info['children'][0], str)

def test_root_tags():
    root_tags = medium.root_tags()

    assert isinstance(root_tags, list)
    assert isinstance(root_tags[0], str)