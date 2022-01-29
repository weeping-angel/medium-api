import os
import pytest

from medium_apis import Medium
from medium_apis import publication
from medium_apis.publication import Publication

medium = Medium(os.getenv('RAPIDAPI_KEY'))

publication_id = '98111c9905da'

publication = medium.publication(publication_id=publication_id)

def test_publication_instance():
    assert isinstance(publication, Publication)

def test_publication_id():
    assert isinstance(publication._id, str)
    assert publication._id == publication_id

def test_publication_info():
    publication.set_info()

    assert isinstance(publication.name, str)
    assert isinstance(publication.description, str)
    assert isinstance(publication.url, str)
    assert isinstance(publication.tagline, str)
    assert isinstance(publication.followers, int)
    assert isinstance(publication.slug, str)
    assert isinstance(publication.tags, list)
    assert isinstance(publication.twitter_username, str)
    assert isinstance(publication.instagram_username, str)
    assert isinstance(publication.facebook_pagename, str)

    assert isinstance(publication.info, dict)

