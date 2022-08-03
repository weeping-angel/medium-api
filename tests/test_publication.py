import os
import pytest

from medium_api import Medium
from medium_api import _publication
from medium_api._publication import Publication, Newsletter
from medium_api._article import Article
from medium_api._user import User

medium = Medium(os.getenv('RAPIDAPI_KEY'))

publication_id = '98111c9905da'

_publication = medium.publication(publication_id=publication_id)

def test_publication_instance():
    assert isinstance(_publication, Publication)

def test_publication_id():
    assert isinstance(_publication._id, str)
    assert _publication._id == publication_id

def test_publication_article_ids():
    assert isinstance(_publication.article_ids, list)
    assert isinstance(_publication.article_ids[0], str)

def test_publication_articles():
    assert isinstance(_publication.articles, list)
    assert isinstance(_publication.articles[0], Article)

def test_publication_info():
    _publication.save_info()

    assert isinstance(_publication.name, str)
    assert isinstance(_publication.description, str)
    assert isinstance(_publication.url, str)
    assert isinstance(_publication.tagline, str)
    assert isinstance(_publication.followers, int)
    assert isinstance(_publication.slug, str)
    assert isinstance(_publication.tags, list)
    assert isinstance(_publication.domain, str)
    assert isinstance(_publication.twitter_username, str)
    assert isinstance(_publication.instagram_username, str)
    assert isinstance(_publication.facebook_pagename, str)
    assert isinstance(_publication.creator, User)
    assert isinstance(_publication.editors, list)
    if _publication.editors:
        assert isinstance(_publication.editors[0], User)

    assert isinstance(_publication.newsletter, Newsletter)
    assert isinstance(_publication.newsletter.id, str)
    assert isinstance(_publication.newsletter.name, str)
    assert isinstance(_publication.newsletter.slug, str)
    assert isinstance(_publication.newsletter.description, str)
    assert isinstance(_publication.newsletter.image_url, str)
    assert isinstance(_publication.newsletter.subscribers, int)
    assert isinstance(_publication.newsletter.creator, User)

    assert isinstance(_publication.info, dict)

