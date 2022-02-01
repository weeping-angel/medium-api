import os
import pytest

from medium_apis import Medium
from medium_apis._article import Article
from medium_apis._latestposts import LatestPosts

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

