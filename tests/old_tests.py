import pytest
from medium_apis import Medium
import os

medium = Medium(os.getenv('RAPIDAPI_KEY'))

username = 'nishu-jain'
user_id = '1985b61817c3'
article_id = '562c5821b5f0'

publication_id = '98111c9905da'
publication_slug = 'towards-artificial-intelligence'

topic_slug = 'relationships'

def test_get_userid():
    uid = medium.get_user_id(username=username)
    assert isinstance(uid, str)
    assert uid == user_id

def test_user():
    user = medium.get_user(user_id=user_id)
    assert isinstance(user, dict)
    assert user['id'] == user_id

def test_user_articles_ids():
    article_ids = medium.get_user_articles_ids(user_id=user_id)
    assert isinstance(article_ids, list)
    assert article_id in article_ids

def test_user_following():
    user_following = medium.get_user_following(user_id=user_id)
    assert isinstance(user_following, list)

def test_article_info():
    article_info = medium.get_article_info(article_id=article_id)
    assert isinstance(article_info, dict)
    assert article_info['id'] == article_id

def test_article_content():
    article_content = medium.get_article_content(article_id=article_id)
    assert isinstance(article_content, str)

def test_publication_info():
    publication_info = medium.get_publication_info(publication_id=publication_id)
    assert isinstance(publication_info, dict)
    assert publication_slug == publication_info['slug']

def test_top_writers_ids():
    top_writers_ids = medium.get_top_writers_ids(topic_slug)
    assert isinstance(top_writers_ids, list)
    assert len(top_writers_ids) > 0

def test_latestposts_ids():
    latestposts_ids = medium.get_latestposts_ids(topic_slug)
    assert isinstance(latestposts_ids, list)
    assert len(latestposts_ids) > 0