import os

from medium_api import Medium
from medium_api._publication import Publication
from medium_api._user import User
from medium_api._article import Article
from medium_api._medium_list import MediumList

medium = Medium(os.getenv('RAPIDAPI_KEY'))

def test_search_articles():
    results = medium.search_articles(query = "data science", save_info=False)

    assert isinstance(results, list)
    assert len(results) > 0
    assert isinstance(results[0], Article)

def test_search_publications():
    results = medium.search_publications(query = "mental health", save_info=False)

    assert isinstance(results, list)
    assert len(results) > 0
    assert isinstance(results[0], Publication)

def test_search_users():
    results = medium.search_users(query = "data engineer", save_info=False)

    assert isinstance(results, list)
    assert len(results) > 0
    assert isinstance(results[0], User)

def test_search_lists():
    results = medium.search_lists(query = "medium", save_info=False)

    assert isinstance(results, list)
    assert len(results) > 0
    assert isinstance(results[0], MediumList)

def test_search_tags():
    results = medium.search_tags(query = "blockchain")

    assert isinstance(results, list)
    assert len(results) > 0
    assert isinstance(results[0], str)