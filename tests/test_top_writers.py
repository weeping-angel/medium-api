import os
import pytest

from medium_api import Medium
from medium_api._top_writers import TopWriters
from medium_api._user import User

medium = Medium(os.getenv('RAPIDAPI_KEY'))

topic_slug = 'technology'

top_writers = medium.top_writers(topic_slug=topic_slug)

def test_top_writers_instance():
    assert isinstance(top_writers, TopWriters)

def test_top_writers_ids():
    ids = top_writers.ids

    assert isinstance(ids, list)
    assert isinstance(ids[0], str)

def test_top_writers_users():
    users = top_writers.users

    assert isinstance(users, list)
    assert isinstance(users[0], User)

def test_top_writers_fetch_users():
    top_writers.fetch_users()

    assert 'fullname' in top_writers.users[0].info.keys()
    assert top_writers.users[0].fullname is not None

