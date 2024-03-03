import os

from medium_api import Medium
from medium_api._article import Article
from medium_api._recommended_feed import RecommendedFeed

medium = Medium(os.getenv('RAPIDAPI_KEY'))

tag = 'startup'
count = 30

def test_recommended_feed():
    print('\n')

    recommended_feed = medium.recommended_feed(tag=tag, count=count)

    assert isinstance(recommended_feed, RecommendedFeed)

    assert isinstance(recommended_feed.ids, list)
    assert isinstance(recommended_feed.ids[0], str)

    assert isinstance(recommended_feed.articles, list)
    assert isinstance(recommended_feed.articles[0], Article)

    assert len(recommended_feed.articles) == count == len(recommended_feed.ids)