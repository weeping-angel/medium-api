import os
import pytest
import random

from medium_api import Medium
from medium_api._article import Article
from medium_api._topfeeds import TopFeeds

medium = Medium(os.getenv('RAPIDAPI_KEY'))

tag = 'startup'

def test_topfeeds_modes():
    modes = [
        'new',
        'hot',
        'top_year',
        'top_month',
        'top_all_time',
        'top_week',
    ]
    print('\n')
    for mode in modes:
        count = random.choice(range(10, 35))
        topfeeds = medium.topfeeds(tag=tag, mode=mode, count=count)

        print("Mode: ", mode, "\t Count: ", count)

        assert isinstance(topfeeds, TopFeeds)

        assert isinstance(topfeeds.ids, list)
        assert len(topfeeds.ids) == count
        assert isinstance(topfeeds.ids[0], str)

        assert isinstance(topfeeds.articles, list)
        assert isinstance(topfeeds.articles[0], Article)

