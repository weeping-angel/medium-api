import os
import pytest

from medium_apis import Medium
from medium_apis._article import Article
from medium_apis._topfeeds import TopFeeds

medium = Medium(os.getenv('RAPIDAPI_KEY'))

tag = 'blockchain'

def test_topfeeds_modes():
    modes = [
        'new',
        'hot',
        'top_year',
        'top_week',
        'top_month',
        'top_all_time'
    ]

    for mode in modes:
        topfeeds = medium.topfeeds(tag=tag, mode=mode)
        assert isinstance(topfeeds, TopFeeds)

        assert isinstance(topfeeds.ids, list)
        assert isinstance(topfeeds.ids[0], str)

        assert isinstance(topfeeds.articles, list)
        assert isinstance(topfeeds.articles[0], Article)

    topfeeds.fetch_articles()

    assert 'title' in topfeeds.articles[0].info.keys()
    assert topfeeds.articles[0].title is not None

