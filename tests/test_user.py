import os
import pytest

from medium_api import Medium
from medium_api._user import User
from medium_api._article import Article

medium = Medium(os.getenv('RAPIDAPI_KEY'))

username = 'nishu-jain'
user_id = '1985b61817c3'

user = medium.user(username = username)

def test_user_instance():
    assert isinstance(user, User)
    assert isinstance(user._id, str)
    assert user._id == user_id

def test_user_info():
    assert isinstance(user.info, dict)

    user.save_info()

    assert isinstance(user.fullname, str)
    assert isinstance(user.username, str)
    assert isinstance(user.twitter_username, str)
    assert isinstance(user.is_writer_program_enrolled, bool)
    assert isinstance(user.followers, int)
    assert isinstance(user.following, list)
    assert isinstance(user.bio, str)
    assert isinstance(user.image_url, str)

def test_user_article_ids():
    user_articles_ids = user.article_ids

    assert isinstance(user_articles_ids, list)
    assert isinstance(user_articles_ids[0], str)

def test_user_top_article_ids():
    top_articles_ids = user.top_article_ids

    assert isinstance(top_articles_ids, list)
    assert isinstance(top_articles_ids[0], str)

def test_user_articles_instances():
    user_articles = user.articles

    assert isinstance(user_articles, list)
    assert isinstance(user_articles[0], Article)

def test_user_top_articles_instances():
    top_articles = user.top_articles

    assert isinstance(top_articles, list)
    assert isinstance(top_articles[0], Article)

def test_user_articles_as_json():
    user.fetch_articles(content=True)

    user_articles_as_json = user.articles_as_json

    assert isinstance(user_articles_as_json, list)
    assert isinstance(user_articles_as_json[0], dict)
    
    articles_keys = user_articles_as_json[0].keys()

    assert 'title' in articles_keys
    assert 'content' in articles_keys



