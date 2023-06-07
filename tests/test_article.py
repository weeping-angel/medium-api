import os
import pytest
from datetime import datetime

from medium_api import Medium
from medium_api._publication import Publication
from medium_api._user import User
from medium_api._article import Article

medium = Medium(os.getenv('RAPIDAPI_KEY'))

article_id = '67fa62fc1971'

article = medium.article(article_id=article_id)

def test_article_instance():
    assert isinstance(article, Article)
    assert isinstance(article._id, str)
    assert article._id == article_id

def test_article_info():
    article.save_info()

    assert isinstance(article.title, str)
    assert isinstance(article.subtitle, str)
    assert isinstance(article.url, str)
    assert isinstance(article.publication_id, str)
    assert isinstance(article.lang, str)
    assert isinstance(article.image_url, str)
    
    assert isinstance(article.claps, int)
    assert isinstance(article.word_count, int)
    assert isinstance(article.responses_count, int)
    assert isinstance(article.voters, int)

    assert isinstance(article.is_series, bool)
    assert isinstance(article.is_locked, bool)

    assert isinstance(article.reading_time, float)

    assert isinstance(article.tags, list)
    assert isinstance(article.topics, list)

    assert isinstance(article.published_at, datetime)
    assert isinstance(article.last_modified_at, datetime)

    assert isinstance(article.author, User)

    assert isinstance(article.info, dict)

def test_article_responses():
    assert isinstance(article.response_ids, list)
    assert isinstance(article.response_ids[0], str)

    assert isinstance(article.responses, list)
    assert isinstance(article.responses[0], Article)

    assert article.responses[0].title is None

    # article.fetch_responses()

    # assert article.responses[0].title is not None

def test_article_fans():
    assert isinstance(article.fans_ids, list)
    assert isinstance(article.fans_ids[0], str)

    assert isinstance(article.fans, list)
    assert isinstance(article.fans[0], User)

    assert article.fans[0].fullname is None

    # article.fetch_fans()

    # assert article.fans[0].fullname is not None

def test_related_articles():
    assert isinstance(article.related_articles_ids, list)
    assert isinstance(article.related_articles_ids[0], str)

    assert isinstance(article.related_articles, list)
    assert isinstance(article.related_articles[0], Article)

    assert article.related_articles[0].title is None

    # article.fetch_related_articles()

    # assert article.related_articles[0].title is not None

def test_article_content():
    article.save_content()

    assert isinstance(article.content, str)
    assert len(article.content) > 0

def test_article_markdown():
    article.save_markdown()

    assert isinstance(article.markdown, str)
    assert len(article.markdown) > 0

def test_article_html():
    article.save_html(fullpage=True)

    assert isinstance(article.html, str)
    assert len(article.html) > 0
    assert article.html[:len('<html')] == '<html'

def test_article_json():
    article.save_info()
    article.save_content()
    article.save_markdown()
    article.save_html(fullpage=True)
    
    article_json = article.json

    assert isinstance(article_json, dict)
    assert 'content' in article_json.keys()
    assert 'markdown' in article_json.keys()
    assert 'html' in article_json.keys()
    assert 'title' in article_json.keys()

def test_article_publication():
    is_self_published = article.is_self_published

    assert isinstance(is_self_published, bool)

    if not is_self_published:
        assert isinstance(article.publication, Publication)
    else:
        assert article.publication is None

