"""
This module contains the `Article` class.
"""

from datetime import datetime

class Article:
    """Article Class
    
    With `Article` object, you can use the following properties and methods:

        - article._id
        - article.info
        - article.responses
        - article.fans_ids
        - article.fans
        - article.related_articles_ids
        - article.related_articles
        - article.is_self_published
        - article.content
        - article.markdown
        - article.html
        - article.json

        - article.save_info()
        - article.save_content()
        - article.save_markdown()
        - article.save_html()
        - article.fetch_responses()
        - article.fetch_fans()
        - article.fetch_related_articles()

    Note:
        `Article` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.article`.

    """
    def __init__(self, article_id, get_resp, fetch_articles, fetch_users, fetch_publications, fetch_lists, save_info=False):
        self.__get_resp = get_resp
        self.article_id = str(article_id)

        self.__fetch_articles = fetch_articles
        self.__fetch_users = fetch_users
        self.__fetch_publications = fetch_publications
        self.__fetch_lists = fetch_lists

        self.title = None
        self.subtitle = None
        self.claps = None
        self.author = None
        self.url = None
        self.published_at = None
        self.publication_id = None
        self.tags = None
        self.topics = None
        self.last_modified_at = None
        self.reading_time = None
        self.word_count = None
        self.responses_count = None
        self.voters = None
        self.lang = None
        self.image_url = None
        self.is_series = None
        self.is_locked = None

        self.publication = None

        self.__info = None
        self.__content = None
        self.__markdown = None
        self.__html = None
        self.__response_ids = None
        self.__responses = None
        self.__fans_ids = None
        self.__fans = None
        self.__related_articles_ids = None
        self.__related_articles = None

        if save_info:
            self.save_info()

    def save_info(self):
        """Saves the information related to the article
        
        Note:
            Only after running ``article.save_info()`` you can use the following
            variables:

                - ``article.title``
                - ``article.subtitle``
                - ``article.claps``
                - ``article.author``
                - ``article.url``
                - ``article.published_at``
                - ``article.publication_id``
                - ``article.tags``
                - ``article.topics``
                - ``article.last_modified_at``
                - ``article.reading_time``
                - ``article.word_count``
                - ``article.responses_count``
                - ``article.voters``
                - ``article.lang``
                - ``article.is_series``
                - ``article.is_locked``
                - ``article.image_url`` 
                - ``article.publication``
        """
        from medium_api._user import User
        from medium_api._publication import Publication

        article = self.info

        self.title = article.get('title')
        self.subtitle = article.get('subtitle')
        self.claps = article.get('claps')
        self.author = User(user_id=article['author'], 
                           get_resp=self.__get_resp, 
                           fetch_articles=self.__fetch_articles,
                           fetch_users=self.__fetch_users,
                           fetch_publications=self.__fetch_publications,
                           fetch_lists=self.__fetch_lists,
                           save_info=False) if article.get('author') else None
        self.url = article.get('url')
        self.published_at = datetime.strptime(article['published_at'], '%Y-%m-%d %H:%M:%S') if article.get('published_at') else None
        self.publication_id = article.get('publication_id')
        self.tags = article.get('tags')
        self.topics = article.get('topics')
        self.last_modified_at = datetime.strptime(article['last_modified_at'], '%Y-%m-%d %H:%M:%S') if article.get('last_modified_at') else None
        self.reading_time = article.get('reading_time')
        self.word_count = article.get('word_count')
        self.responses_count = article.get('responses_count')
        self.voters = article.get('voters')
        self.lang = article.get('lang')
        self.is_series = article.get('is_series')
        self.is_locked = article.get('is_locked')
        self.image_url = article.get('image_url')

        if not self.is_self_published:
            self.publication = Publication(publication_id=self.publication_id, 
                                           get_resp=self.__get_resp,
                                           fetch_articles=self.__fetch_articles,
                                           fetch_users=self.__fetch_users,
                                           fetch_publications=self.__fetch_publications,
                                           fetch_lists=self.__fetch_lists,
                                           save_info=False)
        
        if self.title is None:
            print(f"[ERROR]: Could not retrieve article for the given article_id ({self.article_id}). Please check if this article exists.")
            print(f"[ERROR]: Link to unknown article: https://medium.com/p/{self.article_id}")


    def save_content(self):
        """Saves the textual content of the article

        Can be accessed later using ``article.content``
        
        Returns:
            None

        """
        self.__content = self.content

    def save_markdown(self):
        """Saves the markdown of the article

        Can be accessed later using ``article.markdown``
        
        Returns:
            None

        """
        self.__markdown = self.markdown

    @property
    def _id(self):
        """To get the article_id

        Returns:
            str: Returns article_id of the object.
        
        """
        return self.article_id

    @property
    def info(self):
        """To get the articles information
        
        Returns:
            dict: Returns a dictionary object containing `title, subtitle, claps,
            voters, author, publication_id, word_count, etc ...` (excluding `content`)
        
        """
        if self.__info is None:
            resp, _ = self.__get_resp(f'/article/{self.article_id}')
            self.__info = dict(resp)
        
        return self.__info

    @property
    def response_ids(self):
        """To get the list of ids of responses (comments) on the article
        
        Returns:
            list: Returns a list of `response_ids`.
        """
        if self.__response_ids is None:
            resp, _ = self.__get_resp(f'/article/{self.article_id}/responses')
            self.__response_ids = list(resp['responses'])
        
        return self.__response_ids

    @property
    def responses(self):
        """To get the list of responses (Article Objects)

        Returns:
            list[Article]: Returns a list of `Article` Objects.
        """
        if self.__responses is None:
            self.__responses = [Article(
                                    article_id=response_id, 
                                    get_resp=self.__get_resp, 
                                    fetch_articles=self.__fetch_articles,
                                    fetch_users=self.__fetch_users,
                                    fetch_publications=self.__fetch_publications,
                                    fetch_lists=self.__fetch_lists,
                                    save_info=False
                                )
                                for response_id in self.response_ids]

        return self.__responses

    def fetch_responses(self, content=False):
        """To fetch all the responses/comments information and textual content.

        Args:
            content (bool, optional): Set it to `True` if you want to fetch the 
                textual content of the response as well. Otherwise, default is `False`.

        Returns:
            None: All the fetched information will be access via `article.responses`.

            ``article.responses[0].content``
            ``article.responses[1].claps``
        """
        self.__fetch_articles(self.responses, content=content)

    @property
    def fans_ids(self):
        """To get the list of `user_ids` of the people who clapped on the article (voters or fans)
        
        Returns:
            list: Returns a list of `user_ids`.
        """
        if self.__fans_ids is None:
            resp, _ = self.__get_resp(f'/article/{self.article_id}/fans')
            self.__fans_ids = list(resp['voters'])
        
        return self.__fans_ids

    @property
    def fans(self):
        """To get the list of Users who clapped on the article (voters/fans).

        Returns:
            list[User]: Returns a list of `User` Objects.
        """
        from medium_api._user import User

        if self.__fans is None:
            self.__fans = [User(
                                user_id=fan_id, 
                                get_resp=self.__get_resp, 
                                fetch_articles=self.__fetch_articles,
                                fetch_users=self.__fetch_users,
                                fetch_publications=self.__fetch_publications,
                                fetch_lists=self.__fetch_lists,
                                save_info=False
                            )
                            for fan_id in self.fans_ids]

        return self.__fans

    @property
    def related_articles_ids(self):
        """To get the list of `article_ids` of the related posts.
        
        Returns:
            list: Returns a list of `article_ids`.
        """
        if self.__related_articles_ids is None:
            resp, _ = self.__get_resp(f'/article/{self.article_id}/related')
            self.__related_articles_ids = list(resp['related_articles'])
        
        return self.__related_articles_ids

    @property
    def related_articles(self):
        """To get the list of related articles (Article Objects)

        Returns:
            list[Article]: Returns a list of `Article` Objects.
        """
        if self.__related_articles is None:
            self.__related_articles = [Article(
                                                article_id=related_article_id, 
                                                get_resp=self.__get_resp, 
                                                fetch_articles=self.__fetch_articles,
                                                fetch_users=self.__fetch_users,
                                                fetch_publications=self.__fetch_publications,
                                                fetch_lists=self.__fetch_lists,
                                                save_info=False,
                                              )
                                for related_article_id in self.related_articles_ids]

        return self.__related_articles

    @property
    def is_self_published(self):
        """To check if the article is self-published or not
        
        Returns:
            bool: Returns `True` if article is self-published, else `False` if article 
            is published under a Medium Publication.
        """
        article = self.info
        if article['publication_id'] != '*Self-Published*':
            return False
        else:
            return True

    @property
    def content(self):
        """To get the textual content of the article

        Returns:
            str: A single string containing `kicker, title, subtitle, paragraphs,
            image captions, listicles, etc ...` within an article 
        """
        if self.__content is None:
            resp, _ = self.__get_resp(f'/article/{self.article_id}/content')
            self.__content = str(resp['content'])

        return self.__content

    @property
    def markdown(self):
        """To get the Markdown of the Medium Article

        Returns:
            str: A single string containing `kicker, title, subtitle, paragraphs,
            images, listicles, etc ...` within an article, in the markdown format 
        """
        if self.__markdown is None:
            resp, _ = self.__get_resp(f'/article/{self.article_id}/markdown')
            self.__markdown = str(resp['markdown'])

        return self.__markdown
    
    @property
    def html(self):
        """To get the Medium Article in plain HTML format

        Returns:
            str: A single string containing the entire article in HTML format 
        """
        if self.__html is None:
            self.save_html(fullpage=False)

        return self.__html
    
    def save_html(self, fullpage:bool=False):
        """Saves the article in plain HTML format

        Args:

            fullpage (bool, optional): If 'True', saves full HTML page with head, body, title and meta tags. 
                Else, saves HTML inside body only.
        
        Returns:
            None

        """
        fullpage = 'true' if fullpage else 'false'
        resp, _ = self.__get_resp(f'/article/{self.article_id}/html?fullpage={fullpage}')
        self.__html = str(resp['html'])

    @property
    def json(self):
        """To get the articles information in JSON format
        
        Returns:
            dict: Returns a JSON object containing article `info`, `content`, `markdown` and `html` if 
            already fetched. Else, returns an empty object.
        
        """
        ret = {}
        if self.__info:
            ret.update(self.info)
        if self.__content:
            ret['content'] = self.content
        if self.__markdown:
            ret['markdown'] = self.markdown
        if self.__html:
            ret['html'] = self.html

        return ret
    
    def fetch_fans(self):
        """To fetch user-related information of the people who clapped on the article (voters/fans), using multi-threading

        Returns:
            None: All the fetched information will be access via `article.fans`.

            ``article.fans[0].name``
            ``article.fans[2].twitter_username``
            ``article.fans[1].bio``
        """
        self.__fetch_users(self.fans)

    def fetch_related_articles(self, content=False):
        """To fetch all the related articles information and textual content, using multi-threading

        Args:
            content (bool, optional): Set it to `True` if you want to fetch the 
                textual content of the related articles as well. Otherwise, default is `False`.

        Returns:
            None: All the fetched information will be access via `article.related_articles`.

            ``article.related_articles[0].content``
            ``article.related_articles[2].title``
            ``article.related_articles[1].claps``
        """
        self.__fetch_articles(self.related_articles, content=content)