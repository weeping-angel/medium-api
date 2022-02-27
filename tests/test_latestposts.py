import os
import pytest

from medium_api import Medium
from medium_api._article import Article
from medium_api._latestposts import LatestPosts

medium = Medium(os.getenv('RAPIDAPI_KEY'))

topic_slug = 'artificial-intelligence'

latestposts = medium.latestposts(topic_slug=topic_slug)

def test_latestposts_instance():
    assert isinstance(latestposts, LatestPosts)

def test_latestposts_ids():
    ids = latestposts.ids

    assert isinstance(ids, list)
    assert isinstance(ids[0], str)

def test_latestposts_articles():
    articles = latestposts.articles

    assert isinstance(articles, list)
    assert isinstance(articles[0], Article)

def test_latestposts_fetch_articles():
    latestposts.fetch_articles()

    assert 'title' in latestposts.articles[0].info.keys()
    assert latestposts.articles[0].title is not None

