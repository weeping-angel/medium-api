import os
import pytest

from medium_api import Medium
from medium_api import _publication
from medium_api._publication import Publication, Newsletter
from medium_api._article import Article
from medium_api._user import User

medium = Medium(os.getenv('RAPIDAPI_KEY'))

publication_id = '98111c9905da'
publication_slug = 'towards-artificial-intelligence'

_publication = medium.publication(publication_slug=publication_slug)

def test_publication_instance():
    assert isinstance(_publication, Publication)
    assert isinstance(_publication._id, str)
    assert _publication._id == publication_id

def test_publication_articles():
    from datetime import datetime, timedelta
    
    # Correct input
    _from = datetime.now()
    _to = _from - timedelta(days=5)

    articles = _publication.get_articles_between(_from=_from, _to=_to)

    assert isinstance(articles, list)
    assert isinstance(articles[0], Article)

    # No input
    articles = _publication.get_articles_between()

    assert isinstance(articles, list)
    assert isinstance(articles[0], Article)

    # Incorrect Input
    articles = _publication.get_articles_between(_from=_to, _to=_from)

    assert isinstance(articles, list)
    assert len(articles)==0

def test_publication_info():
    _publication.save_info()

    assert isinstance(_publication.name, str)
    assert isinstance(_publication.description, str)
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

    _publication.newsletter.save_info()

    assert isinstance(_publication.newsletter, Newsletter)
    assert isinstance(_publication.newsletter.id, str)
    assert isinstance(_publication.newsletter.name, str)
    assert isinstance(_publication.newsletter.slug, str)
    assert isinstance(_publication.newsletter.description, str)
    assert isinstance(_publication.newsletter.image_url, str)
    assert isinstance(_publication.newsletter.subscribers, int)
    assert isinstance(_publication.newsletter.creator, User)

    assert isinstance(_publication.info, dict)

