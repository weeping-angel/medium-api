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
        - article.is_self_published
        - article.content
        - article.markdown
        - article.json

        - article.save_info()
        - article.save_content()
        - article.save_markdown()
        - article.fetch_responses()

    Note:
        `Article` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.article`.

    """
    def __init__(self, article_id, get_resp, fetch_articles, save_info=False):
        self.__get_resp = get_resp
        self.article_id = str(article_id)
        self.__fetch_articles = fetch_articles

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
        self.voters = None
        self.lang = None
        self.image_url = None

        self.publication = None

        self.__info = None
        self.__content = None
        self.__markdown = None
        self.__response_ids = None
        self.__responses = None

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
                - ``article.voters``
                - ``article.lang``
                - ``article.image_url`` 
                - ``article.publication``
        """
        from medium_api._user import User
        from medium_api._publication import Publication

        article = self.info

        self.title = article['title']
        self.subtitle = article['subtitle']
        self.claps = article['claps']
        self.author = User(user_id=article['author'], 
                           get_resp=self.__get_resp, 
                           fetch_articles=self.__fetch_articles, 
                           save_info=False)
        self.url = article['url']
        self.published_at = datetime.strptime(article['published_at'], '%Y-%m-%d %H:%M:%S')
        self.publication_id = article['publication_id']
        self.tags = article['tags']
        self.topics = article['topics']
        self.last_modified_at = datetime.strptime(article['last_modified_at'], '%Y-%m-%d %H:%M:%S')
        self.reading_time = article['reading_time']
        self.word_count = article['word_count']
        self.voters = article['voters']
        self.lang = article['lang']
        self.image_url = article['image_url']

        if not self.is_self_published:
            self.publication = Publication(publication_id=self.publication_id, 
                                           get_resp=self.__get_resp,
                                           fetch_articles=self.__fetch_articles,
                                           save_info=False)


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
                                    fetch_articles=self.__fetch_articles
                                )
                                for response_id in self.response_ids]

        return self.__responses

    def fetch_responses(self, content=True):
        """To fetch all the responses information and content on an article.

        Args:
            content (bool, optional): Set it to `True` if you want to fetch the 
                textual content of the article as well. Otherwise, default is `False`.

        Returns:
            None: All the fetched information will be access via `user.articles`.

            ``article.responses[0].content``
            ``article.responses[1].claps``
        """
        self.__fetch_articles(self.responses, content=content)


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
    def json(self):
        """To get the articles information in JSON format
        
        Returns:
            dict: Returns a JSON object containing article `info`, `content`, and `markdown` if 
            already fetched. Else, returns an empty object.
        
        """
        ret = {}
        if self.__info:
            ret.update(self.info)
        if self.__content:
            ret['content'] = self.content
        if self.__markdown:
            ret['markdown'] = self.markdown

        return ret