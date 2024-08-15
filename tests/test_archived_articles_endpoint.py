import os

from medium_api import Medium
from medium_api._article import Article
from medium_api._archived_articles import ArchivedArticles

medium = Medium(os.getenv('RAPIDAPI_KEY'))

tag = 'startup'

def test_archived_articles():
    archived_articles = medium.archived_articles(tag=tag, count=30, year='2021', month='10')

    assert isinstance(archived_articles, ArchivedArticles)

    assert isinstance(archived_articles.ids, list)
    assert isinstance(archived_articles.ids[0], str)

    assert isinstance(archived_articles.articles, list)
    assert isinstance(archived_articles.articles[0], Article)

    assert len(archived_articles.articles) == 30 == len(archived_articles.ids)
    # assert medium.calls == 2

    archived_articles_2 = medium.archived_articles(tag=tag)

    assert isinstance(archived_articles_2, ArchivedArticles)

    assert isinstance(archived_articles_2.ids, list)
    assert isinstance(archived_articles_2.ids[0], str)

    assert isinstance(archived_articles_2.articles, list)
    assert isinstance(archived_articles_2.articles[0], Article)

    assert len(archived_articles_2.articles) == 20 == len(archived_articles_2.ids)
    # assert medium.calls == 3