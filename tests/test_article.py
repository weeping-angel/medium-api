import os
import pytest
from datetime import datetime

from medium_api import Medium
from medium_api._publication import Publication
from medium_api._user import User
from medium_api._article import Article

medium = Medium(os.getenv('RAPIDAPI_KEY'))

article_id = '562c5821b5f0'

article = medium.article(article_id=article_id)

def test_article_instance():
    assert isinstance(article, Article)
    assert isinstance(article._id, str)
    assert article._id == article_id

def test_article_info():
    article.save_info()

    assert isinstance(article.title, str)
    assert isinstance(article.subtitle, str)
    assert isinstance(article.claps, int)
    assert isinstance(article.author, User)
    assert isinstance(article.url, str)
    assert isinstance(article.published_at, datetime)
    assert isinstance(article.publication_id, str)
    assert isinstance(article.tags, list)
    assert isinstance(article.topics, list)
    assert isinstance(article.last_modified_at, datetime)
    assert isinstance(article.reading_time, float)
    assert isinstance(article.word_count, int)
    assert isinstance(article.voters, int)
    assert isinstance(article.image_url, str)

    assert isinstance(article.info, dict)

def test_article_content():
    article.save_content()

    assert isinstance(article.content, str)
    assert len(article.content) > 0

def test_article_json():
    article.save_info()
    article.save_content()
    
    article_json = article.json

    assert isinstance(article_json, dict)
    assert 'content' in article_json.keys()
    assert 'title' in article_json.keys()

def test_article_publication():
    is_self_published = article.is_self_published

    assert isinstance(is_self_published, bool)

    if not is_self_published:
        assert isinstance(article.publication, Publication)
    else:
        assert article.publication is None

