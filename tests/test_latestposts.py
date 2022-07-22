import os
import pytest

from medium_api import Medium
from medium_api._article import Article
from medium_api._latestposts import LatestPosts

medium = Medium(os.getenv('RAPIDAPI_KEY'))

topic_slug = 'artificial-intelligence'
wrong_topic_slug = 'xyz123'

latestposts = medium.latestposts(topic_slug=topic_slug)
wrong_latestposts = medium.latestposts(topic_slug=wrong_topic_slug)

def test_latestposts_instance():
    assert isinstance(latestposts, LatestPosts)

def test_latestposts_ids():
    ids = latestposts.ids
    wrong_ids = wrong_latestposts.ids

    assert isinstance(ids, list)
    assert isinstance(ids[0], str)
    assert isinstance(wrong_ids, list)
    assert len(wrong_ids) == 0

def test_latestposts_articles():
    articles = latestposts.articles
    wrong_articles = wrong_latestposts.articles

    assert isinstance(articles, list)
    assert isinstance(articles[0], Article)
    assert isinstance(wrong_articles, list)
    assert len(wrong_articles) == 0

def test_latestposts_fetch_articles():
    latestposts.fetch_articles()

    assert 'title' in latestposts.articles[0].info.keys()
    assert latestposts.articles[0].title is not None

