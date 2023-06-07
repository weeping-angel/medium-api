import os
import pytest
import random

from medium_api import Medium
from medium_api._top_writers import TopWriters
from medium_api._user import User

medium = Medium(os.getenv('RAPIDAPI_KEY'))

topic_slug = 'technology'
count = random.choice(range(10, 25))

top_writers = medium.top_writers(topic_slug=topic_slug, count=count)

def test_top_writers_instance():
    assert isinstance(top_writers, TopWriters)

def test_top_writers_ids():
    ids = top_writers.ids

    assert isinstance(ids, list)
    assert len(ids) == count
    assert isinstance(ids[0], str)

def test_top_writers_users():
    users = top_writers.users

    assert isinstance(users, list)
    assert isinstance(users[0], User)

