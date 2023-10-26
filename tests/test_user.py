import os
import pytest
from datetime import datetime

from medium_api import Medium
from medium_api._user import User
from medium_api._article import Article
from medium_api._publication import Publication
from medium_api._medium_list import MediumList

medium = Medium(os.getenv('RAPIDAPI_KEY'))

username = 'nishu-jain'
user_id = '1985b61817c3'

user = medium.user(username = username, save_info=False)

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
    assert isinstance(user.bio, str)
    assert isinstance(user.image_url, str)

    assert isinstance(user.followers_count, int)
    assert isinstance(user.following_count, int)
    
    assert isinstance(user.medium_member_at, datetime) or user.medium_member_at is None
    assert isinstance(user.top_writer_in, list)

    assert isinstance(user.is_writer_program_enrolled, bool)
    assert isinstance(user.is_suspended, bool)
    assert isinstance(user.allow_notes, bool)
    assert isinstance(user.has_list, bool)
    assert isinstance(user.is_book_author, bool)

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

def test_user_following():
    following_ids = user.following_ids
    following = user.following

    # user.fetch_following()

    assert isinstance(following_ids, list)
    if len(following_ids) != 0:
        assert isinstance(following_ids[0], str)

    assert isinstance(following, list)
    if len(following) != 0:
        assert isinstance(following[0], User)
        # assert isinstance(following[0].fullname, str)

def test_user_followers():
    followers_ids = user.followers_ids
    followers = user.followers

    # user.fetch_followers()

    assert isinstance(followers_ids, list)
    if len(followers_ids) != 0:
        assert isinstance(followers_ids[0], str)

    assert isinstance(followers, list)
    if len(followers) != 0:
        assert isinstance(followers[0], User)
        # assert isinstance(followers[0].fullname, str)

    all_followers_ids = user.all_followers_ids
    all_followers = user.all_followers

    assert isinstance(all_followers_ids, list)
    if len(all_followers_ids) != 0:
        assert isinstance(all_followers_ids[0], str)

    assert isinstance(all_followers, list)
    if len(all_followers) != 0:
        assert isinstance(all_followers[0], User)

def test_user_publications():
    publication_ids = user.publication_ids
    publications = user.publications

    # user.fetch_publications()

    assert isinstance(publication_ids, list)
    if len(publication_ids) != 0:
        assert isinstance(publication_ids[0], str)

    assert isinstance(publications, list)
    if len(publications) != 0:
        assert isinstance(publications[0], Publication)
        # assert isinstance(publications[0].name, str)

def test_user_lists():
    list_ids = user.list_ids
    lists = user.lists

    # user.fetch_lists()

    assert isinstance(list_ids, list)
    if len(list_ids) != 0:
        assert isinstance(list_ids[0], str)

    assert isinstance(lists, list)
    if len(lists) != 0:
        assert isinstance(lists[0], MediumList)
        # assert isinstance(lists[0].name, str)

def test_user_interests():
    interests = user.interests

    assert isinstance(interests, list)
    if interests:
        assert isinstance(interests[0], str)


