import os

from medium_api import Medium
from medium_api._article import Article
from medium_api._user import User
from medium_api._medium_list import MediumList
from medium_api._recommended_feed import RecommendedFeed
from medium_api._recommended_lists import RecommendedLists
from medium_api._recommended_users import RecommendedUsers

medium = Medium(os.getenv('RAPIDAPI_KEY'))

tag = 'startup'
count = 30

def test_recommended_feed():
    recommended_feed = medium.recommended_feed(tag=tag, count=count)

    assert isinstance(recommended_feed, RecommendedFeed)

    assert isinstance(recommended_feed.ids, list)
    assert isinstance(recommended_feed.ids[0], str)

    assert isinstance(recommended_feed.articles, list)
    assert isinstance(recommended_feed.articles[0], Article)

    assert len(recommended_feed.articles) == count == len(recommended_feed.ids)

def test_recommended_lists():
    recommended_lists = medium.recommended_lists(tag=tag)

    assert isinstance(recommended_lists, RecommendedLists)

    assert isinstance(recommended_lists.ids, list)
    assert isinstance(recommended_lists.ids[0], str)

    assert isinstance(recommended_lists.objs, list)
    assert isinstance(recommended_lists.objs[0], MediumList)

def test_recommended_users():
    recommended_users = medium.recommended_users(tag=tag)

    assert isinstance(recommended_users, RecommendedUsers)

    assert isinstance(recommended_users.ids, list)
    assert isinstance(recommended_users.ids[0], str)

    assert isinstance(recommended_users.users, list)
    assert isinstance(recommended_users.users[0], User)