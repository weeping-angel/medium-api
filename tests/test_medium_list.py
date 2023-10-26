import os
from datetime import datetime
import pytest

from medium_api import Medium
from medium_api._medium_list import MediumList
from medium_api._article import Article
from medium_api._user import User

medium = Medium(os.getenv('RAPIDAPI_KEY'))

list_id = '35ba15f348d7'

medium_list = medium.list(list_id=list_id, save_info=False)

def test_medium_list_instance():
    assert isinstance(medium_list, MediumList)
    assert isinstance(medium_list._id, str)
    assert medium_list._id == list_id

def test_medium_list_articles():
    article_ids = medium_list.article_ids
    assert isinstance(article_ids, list)
    assert isinstance(article_ids[0], str)

    # medium_list.fetch_articles()

    articles = medium_list.articles
    assert isinstance(articles, list)
    assert isinstance(articles[0], Article)

def test_medium_list_responses():
    response_ids = medium_list.response_ids
    assert isinstance(response_ids, list)
    assert isinstance(response_ids[0], str)

    # medium_list.fetch_responses()

    responses = medium_list.responses
    assert isinstance(responses, list)
    assert isinstance(responses[0], Article)

def test_medium_list_info():
    # Before save_info

    assert medium_list.name is None
    assert medium_list.description is None
    assert medium_list.thumbnail is None
    assert medium_list.count is None
    assert medium_list.responses_count is None
    assert medium_list.claps is None
    assert medium_list.voters is None
    assert medium_list.created_at is None
    assert medium_list.last_item_inserted_at is None
    assert medium_list.author is None

    # After save_info
    
    medium_list.save_info()

    assert isinstance(medium_list.info, dict)

    assert isinstance(medium_list.name, str)
    assert isinstance(medium_list.description, str)
    assert isinstance(medium_list.thumbnail, str)

    assert isinstance(medium_list.count, int)
    assert isinstance(medium_list.responses_count, int)
    assert isinstance(medium_list.claps, int)
    assert isinstance(medium_list.voters, int)

    assert isinstance(medium_list.created_at, datetime)
    assert isinstance(medium_list.last_item_inserted_at, datetime)

    assert isinstance(medium_list.author, User)